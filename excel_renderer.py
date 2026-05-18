"""
excel_renderer.py
Render file Excel thành HTML table tối ưu mobile.

Nguyên tắc: style quan trọng (nowrap, min-width) nhúng TRỰC TIẾP vào
attribute style="" của từng ô — không phụ thuộc CSS class bên ngoài
vì Streamlit có thể override chúng.
"""

import os
import streamlit as st
import openpyxl

# ═══════════════════════════════════════════════════════════
#  MÀU SẮC EXCEL
# ═══════════════════════════════════════════════════════════

_OFFICE_THEME_COLORS: dict[int, tuple[int, int, int]] = {
    0: (0,   0,   0),    1: (255, 255, 255),
    2: (68,  84,  106),  3: (231, 230, 230),
    4: (68,  114, 196),  5: (237, 125, 49),
    6: (165, 165, 165),  7: (255, 192, 0),
    8: (68,  114, 196),  9: (112, 173, 71),
}

_TRANSPARENT = {"00000000", "FFFFFFFF", "00FFFFFF"}


def _hex_to_rgb(hex_str: str) -> tuple[int, int, int] | None:
    if not hex_str or hex_str in _TRANSPARENT:
        return None
    try:
        h = hex_str[-6:]
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except Exception:
        return None


def _apply_tint(base: tuple[int, int, int], tint: float) -> tuple[int, int, int]:
    """Áp dụng tint lên màu base (tint > 0: sáng, < 0: tối)."""
    r, g, b = base
    if tint > 0:
        r, g, b = int(r + (255 - r) * tint), int(g + (255 - g) * tint), int(b + (255 - b) * tint)
    else:
        r, g, b = int(r * (1 + tint)), int(g * (1 + tint)), int(b * (1 + tint))
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def _resolve_font_color(font) -> tuple[int, int, int] | None:
    if not font or not font.color:
        return None
    fc = font.color
    try:
        if fc.type == "rgb":
            return _hex_to_rgb(fc.rgb)
        if fc.type == "theme":
            base = _OFFICE_THEME_COLORS.get(int(fc.theme))
            if base is None:
                return None
            tint = getattr(fc, "tint", 0) or 0
            return base if tint == 0 else _apply_tint(base, tint)
    except Exception:
        pass
    return None


def _luminance(rgb: tuple[int, int, int]) -> float:
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def _cell_styles(cell) -> dict[str, str]:
    """Trả về dict CSS style từ định dạng ô Excel."""
    styles: dict[str, str] = {}

    # Màu nền
    bg_rgb = None
    try:
        fg = cell.fill.fgColor.rgb if cell.fill and cell.fill.fgColor else None
        bg_rgb = _hex_to_rgb(fg) if fg else None
    except Exception:
        pass
    if bg_rgb:
        styles["background-color"] = f"rgb{bg_rgb}"

    # In đậm
    try:
        if cell.font and cell.font.bold:
            styles["font-weight"] = "700"
    except Exception:
        pass

    # Căn lề ngang
    try:
        h = cell.alignment.horizontal if cell.alignment else None
        if h in ("center", "centerContinuous"):
            styles["text-align"] = "center"
        elif h == "right":
            styles["text-align"] = "right"
    except Exception:
        pass

    # Màu chữ — ưu tiên tương phản với nền, fallback màu font gốc
    if bg_rgb:
        styles["color"] = "#ffffff" if _luminance(bg_rgb) < 140 else "#1a2a3a"
    else:
        font_rgb = _resolve_font_color(getattr(cell, "font", None))
        if font_rgb and _luminance(font_rgb) < 230:
            styles["color"] = f"rgb{font_rgb}"

    return styles


# ═══════════════════════════════════════════════════════════
#  INLINE STYLES (không phụ thuộc class bên ngoài)
# ═══════════════════════════════════════════════════════════

_BASE_CELL = (
    "white-space:nowrap;min-width:72px;padding:9px 14px;"
    "border:1px solid #E4E9F0;vertical-align:middle;"
    "font-size:0.9rem;font-family:'Sora',sans-serif;line-height:1.5;"
)
_BASE_HEADER = (
    "white-space:nowrap;min-width:72px;padding:10px 14px;"
    "border:1px solid #D0D8E8;border-bottom:2px solid #B0BEEF;"
    "vertical-align:middle;font-size:0.88rem;font-family:'Sora',sans-serif;"
    "font-weight:700;text-align:center;background-color:#EAF0FB;color:#1a2a3a;"
)
_WRAPPER = (
    "overflow-x:auto;-webkit-overflow-scrolling:touch;"
    "border-radius:12px;border:1px solid #E4E9F0;"
    "box-shadow:0 2px 12px rgba(0,0,0,0.06);margin-top:8px;"
)
_TABLE = "border-collapse:collapse;width:max-content;min-width:100%;font-family:'Sora',sans-serif;"

_MONEY_STYLE = "color:#c04800;font-weight:700;"
_MONEY_UNITS = ("K", "đ", "VND", "%")


def _is_money(text: str) -> bool:
    return any(u in text for u in _MONEY_UNITS) and any(ch.isdigit() for ch in text)


def _render_ws_html(ws) -> str:
    """Render một worksheet → HTML string."""
    max_row, max_col = ws.max_row, ws.max_column

    # Merged cells
    skip_map: dict[tuple, bool] = {}
    span_map: dict[tuple, tuple] = {}
    for rng in ws.merged_cells.ranges:
        r0, r1, c0, c1 = rng.min_row, rng.max_row, rng.min_col, rng.max_col
        span_map[(r0, c0)] = (r1 - r0 + 1, c1 - c0 + 1)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if (r, c) != (r0, c0):
                    skip_map[(r, c)] = True

    # Tìm hàng đầu có dữ liệu
    actual_start = next(
        (r for r in range(1, max_row + 1)
         if any(ws.cell(r, c).value is not None for c in range(1, max_col + 1))),
        1,
    )

    # Lọc hàng có nội dung
    content_rows = [
        r for r in range(actual_start, max_row + 1)
        if any(
            not skip_map.get((r, c))
            and (ws.cell(r, c).value is not None or (r, c) in span_map)
            for c in range(1, max_col + 1)
        )
    ]

    if not content_rows:
        return f'<div style="{_WRAPPER}"><p style="padding:1rem;color:#888">Không có dữ liệu.</p></div>'

    def _cell_tag(r: int, c: int, is_header: bool) -> str:
        cell = ws.cell(r, c)
        text = "" if cell.value is None else str(cell.value).strip().replace("\n", "<br>")
        rs, cs = span_map.get((r, c), (1, 1))
        spans = (f' rowspan="{rs}"' if rs > 1 else "") + (f' colspan="{cs}"' if cs > 1 else "")
        excel_css = _cell_styles(cell)

        if is_header:
            extra = ""
            if "background-color" in excel_css:
                extra += f"background-color:{excel_css['background-color']};"
            if "color" in excel_css:
                extra += f"color:{excel_css['color']};"
            style = _BASE_HEADER + extra
            return f"<th{spans} style=\"{style}\">{text}</th>"
        else:
            extra = "".join(f"{k}:{v};" for k, v in excel_css.items())
            money = _MONEY_STYLE if text and "background-color" not in excel_css and _is_money(text) else ""
            return f"<td{spans} style=\"{_BASE_CELL}{extra}{money}\">{text}</td>"

    def _row_html(r: int, is_header: bool) -> str:
        cells = "".join(
            _cell_tag(r, c, is_header)
            for c in range(1, max_col + 1)
            if not skip_map.get((r, c))
        )
        return f"<tr>{cells}</tr>"

    header = _row_html(content_rows[0], is_header=True)
    body   = "".join(_row_html(r, is_header=False) for r in content_rows[1:])

    return (
        f'<div style="{_WRAPPER}">'
        f'<table style="{_TABLE}">'
        f"<thead>{header}</thead>"
        f"<tbody>{body}</tbody>"
        f"</table></div>"
    )


# ═══════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════

@st.cache_data(ttl=60)
def render_excel_file(file_path: str) -> list[tuple[str, str]]:
    """
    Đọc file Excel, render từng sheet thành HTML.
    Trả về list[(sheet_name, html_string)]. Cache 60 giây.
    """
    if not os.path.isfile(file_path):
        return [("Lỗi", f"<p style='color:red'>❌ Không tìm thấy: <code>{file_path}</code></p>")]
    try:
        wb = openpyxl.load_workbook(file_path)
        result = [(name, _render_ws_html(wb[name])) for name in wb.sheetnames]
        wb.close()
        return result
    except Exception as e:
        return [("Lỗi", f"<p style='color:red'>❌ Lỗi đọc file: {e}</p>")]