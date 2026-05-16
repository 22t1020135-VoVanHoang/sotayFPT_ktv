"""
excel_renderer.py
Render file Excel thành HTML table tối ưu mobile.

Nguyên tắc chống lỗi bị-bẻ-dọc trên mobile:
  - white-space:nowrap và min-width nhúng TRỰC TIẾP vào style="" của mỗi ô
    (không phụ thuộc CSS class bên ngoài bị Streamlit override)
  - Wrapper div dùng overflow-x:auto inline style để đảm bảo scroll ngang
  - width:max-content trên <table> để bảng không bị ép nhỏ
"""

import os
import streamlit as st
import openpyxl


# ═══════════════════════════════════════════════════════════
#  HELPERS — MÀU SẮC EXCEL
# ═══════════════════════════════════════════════════════════

_OFFICE_THEME_COLORS = {
    0: (0,   0,   0),
    1: (255, 255, 255),
    2: (68,  84,  106),
    3: (231, 230, 230),
    4: (68,  114, 196),
    5: (237, 125, 49),
    6: (165, 165, 165),
    7: (255, 192, 0),
    8: (68,  114, 196),
    9: (112, 173, 71),
}


def _hex_to_rgb(hex_str):
    if not hex_str or hex_str in ("00000000", "FFFFFFFF", "00FFFFFF"):
        return None
    try:
        h = hex_str[-6:]
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except Exception:
        return None


def _resolve_font_color(font):
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
            if tint == 0:
                return base
            r, g, b = base
            if tint > 0:
                r = int(r + (255 - r) * tint)
                g = int(g + (255 - g) * tint)
                b = int(b + (255 - b) * tint)
            else:
                r = int(r * (1 + tint))
                g = int(g * (1 + tint))
                b = int(b * (1 + tint))
            return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    except Exception:
        pass
    return None


def _get_cell_bg_and_font(cell) -> dict:
    """Trả về dict style từ màu nền và font của ô Excel."""
    styles = {}
    has_bg = False
    bg_rgb = None

    # Màu nền
    try:
        fg = cell.fill.fgColor.rgb if cell.fill and cell.fill.fgColor else None
        bg_rgb = _hex_to_rgb(fg) if fg else None
        if bg_rgb:
            has_bg = True
            styles["background-color"] = f"rgb({bg_rgb[0]},{bg_rgb[1]},{bg_rgb[2]})"
    except Exception:
        pass

    # In đậm
    try:
        if cell.font and cell.font.bold:
            styles["font-weight"] = "700"
    except Exception:
        pass

    # Căn lề ngang
    try:
        align = cell.alignment
        if align:
            if align.horizontal in ("center", "centerContinuous"):
                styles["text-align"] = "center"
            elif align.horizontal == "right":
                styles["text-align"] = "right"
    except Exception:
        pass

    # Màu chữ
    font_rgb = _resolve_font_color(getattr(cell, "font", None))
    if has_bg and bg_rgb:
        lum = 0.299 * bg_rgb[0] + 0.587 * bg_rgb[1] + 0.114 * bg_rgb[2]
        styles["color"] = "#ffffff" if lum < 140 else "#1a2a3a"
    elif font_rgb:
        r, g, b = font_rgb
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        styles["color"] = "#1a2a3a" if lum >= 230 else f"rgb({r},{g},{b})"

    return styles


# ═══════════════════════════════════════════════════════════
#  RENDER EXCEL → HTML
# ═══════════════════════════════════════════════════════════

# Style cố định nhúng thẳng vào mỗi ô — không bị Streamlit override
_BASE_TD_STYLE = (
    "white-space:nowrap;"          # KHÔNG bẻ dọc chữ
    "min-width:72px;"              # chiều rộng tối thiểu mỗi ô
    "padding:9px 14px;"
    "border:1px solid #E4E9F0;"
    "vertical-align:middle;"
    "font-size:0.9rem;"
    "font-family:'Sora',sans-serif;"
    "line-height:1.5;"
)

_BASE_TH_STYLE = (
    "white-space:nowrap;"
    "min-width:72px;"
    "padding:10px 14px;"
    "border:1px solid #D0D8E8;"
    "border-bottom:2px solid #B0BEEF;"
    "vertical-align:middle;"
    "font-size:0.88rem;"
    "font-family:'Sora',sans-serif;"
    "font-weight:700;"
    "text-align:center;"
    "background-color:#EAF0FB;"
    "color:#1a2a3a;"
)

# Wrapper div — inline style đảm bảo scroll ngang bất kể CSS class
_WRAPPER_STYLE = (
    "overflow-x:auto;"
    "-webkit-overflow-scrolling:touch;"
    "border-radius:12px;"
    "border:1px solid #E4E9F0;"
    "box-shadow:0 2px 12px rgba(0,0,0,0.06);"
    "margin-top:8px;"
)

# <table> — width:max-content là chìa khóa: bảng không bị ép nhỏ
_TABLE_STYLE = (
    "border-collapse:collapse;"
    "width:max-content;"           # QUAN TRỌNG: không ép thu nhỏ
    "min-width:100%;"
    "font-family:'Sora',sans-serif;"
)


def _render_ws_html(ws, css_class: str = "xl-wrap") -> str:
    """
    Render một worksheet → HTML string.
    Mọi style quan trọng (nowrap, min-width, padding) đều
    được nhúng trực tiếp vào attribute style="" của từng ô.
    """
    max_row = ws.max_row
    max_col = ws.max_column

    # ── Merged cells ──
    skip_map: dict = {}
    span_map: dict = {}
    for rng in ws.merged_cells.ranges:
        r0, r1 = rng.min_row, rng.max_row
        c0, c1 = rng.min_col, rng.max_col
        span_map[(r0, c0)] = (r1 - r0 + 1, c1 - c0 + 1)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if (r, c) != (r0, c0):
                    skip_map.setdefault(r, {})[c] = True

    # ── Tìm hàng đầu có dữ liệu ──
    actual_start = 1
    for r in range(1, max_row + 1):
        if any(ws.cell(r, c).value is not None for c in range(1, max_col + 1)):
            actual_start = r
            break

    # ── Lọc hàng có nội dung ──
    content_rows = [
        r for r in range(actual_start, max_row + 1)
        if any(
            not skip_map.get(r, {}).get(c)
            and (ws.cell(r, c).value is not None or (r, c) in span_map)
            for c in range(1, max_col + 1)
        )
    ]

    if not content_rows:
        return f'<div style="{_WRAPPER_STYLE}"><p style="padding:1rem;color:#888">Không có dữ liệu.</p></div>'

    def _cell_html(r: int, c: int, tag: str) -> str:
        """Render một ô thành <td> hoặc <th> với full inline style."""
        cell = ws.cell(r, c)
        text = "" if cell.value is None else str(cell.value).strip().replace("\n", "<br>")

        rs, cs_ = span_map.get((r, c), (1, 1))
        span_attrs = ""
        if rs > 1:
            span_attrs += f' rowspan="{rs}"'
        if cs_ > 1:
            span_attrs += f' colspan="{cs_}"'

        # Style gốc từ Excel
        excel_styles = _get_cell_bg_and_font(cell)

        if tag == "th":
            # Header: bắt đầu từ base TH style, đè lên màu Excel nếu có
            style = _BASE_TH_STYLE
            if "background-color" in excel_styles:
                style += f"background-color:{excel_styles['background-color']};"
            if "color" in excel_styles:
                style += f"color:{excel_styles['color']};"
        else:
            # Data cell: bắt đầu từ base TD style
            style = _BASE_TD_STYLE
            for k, v in excel_styles.items():
                style += f"{k}:{v};"
            # Tô màu số tiền nếu không có màu nền từ Excel
            if text and "background-color" not in excel_styles:
                if (
                    any(k in text for k in ["K", "đ", "VND", "%"])
                    and any(ch.isdigit() for ch in text)
                ):
                    style += "color:#c04800;font-weight:700;"

        return f"<{tag}{span_attrs} style=\"{style}\">{text}</{tag}>"

    def _render_row(r: int, tag: str) -> str:
        cells = "".join(
            _cell_html(r, c, tag)
            for c in range(1, max_col + 1)
            if not skip_map.get(r, {}).get(c)
        )
        return f"<tr>{cells}</tr>"

    # ── Ghép HTML ──
    parts = [
        f'<div style="{_WRAPPER_STYLE}">',
        f'<table style="{_TABLE_STYLE}">',
        "<thead>",
        _render_row(content_rows[0], tag="th"),
        "</thead>",
        "<tbody>",
    ]
    for r in content_rows[1:]:
        parts.append(_render_row(r, tag="td"))
    parts.append("</tbody></table></div>")

    return "".join(parts)


# ═══════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════

@st.cache_data(ttl=30)
def render_excel_file(file_path: str, css_class: str = "xl-wrap") -> list:
    """
    Đọc file Excel và render từng sheet thành HTML.
    Trả về list of (sheet_name, html_string). Cache 30 giây.
    """
    if not os.path.exists(file_path):
        return [("Lỗi", f"<p style='color:red'>❌ Không tìm thấy file: <code>{file_path}</code></p>")]
    try:
        wb = openpyxl.load_workbook(file_path)
        return [(name, _render_ws_html(wb[name], css_class)) for name in wb.sheetnames]
    except Exception as e:
        return [("Lỗi", f"<p style='color:red'>❌ Lỗi đọc file: {e}</p>")]


def show_excel_inline(file_path: str, css_class: str = "xl-wrap"):
    """Hiển thị file Excel inline trong Streamlit, kèm nút tải về."""
    sheets = render_excel_file(file_path, css_class)
    multi  = len(sheets) > 1
    for name, html in sheets:
        if multi:
            st.markdown(
                f"<p style='color:#F26F21;font-weight:700;margin:12px 0 6px 0;"
                f"font-family:Sora,sans-serif;font-size:0.88rem;'>📋 {name}</p>",
                unsafe_allow_html=True,
            )
        st.markdown(html, unsafe_allow_html=True)

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            st.download_button(
                label="📥  Tải file Excel",
                data=f,
                file_name=os.path.basename(file_path),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"dl_{file_path}",
            )