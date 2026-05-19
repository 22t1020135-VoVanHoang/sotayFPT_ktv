"""
error_code_renderer.py
Render file Quy_hoach_ma_loi_FPT_Play.xlsx thành Accordion Cards
tối ưu cho Mobile — thay thế bảng HTML bị tràn ngang.

Mỗi sheet được render thành danh sách cards.
Card đóng: Badge nền tảng + Mã lỗi + Mô tả ngắn + arrow icon.
Card mở: Nguyên nhân (bullet list) + Cách xử lý (step list).
"""

import os
import re
import html as _html

import streamlit as st
import openpyxl

# ═══════════════════════════════════════════════════════════════
#  MÀU SẮC BADGE THEO NỀN TẢNG / SHEET
# ═══════════════════════════════════════════════════════════════

_SHEET_CONFIG: dict[str, dict] = {
    "SmartTV LG,Sony HTML,SamSung": {
        "icon": "📺",
        "badge_bg": "#EFF6FF",
        "badge_color": "#005DA3",
        "badge_border": "#BDD7F5",
        "accent": "#005DA3",
        "label": "SmartTV LG,Sony HTML,SamSung",
    },
    "Android(all Platform)": {
        "icon": "🤖",
        "badge_bg": "#EFFAF4",
        "badge_color": "#1A7A42",
        "badge_border": "#A3DDB8",
        "accent": "#1A7A42",
        "label": "Android(all Platform)",
    },
    "iOS": {
        "icon": "🍎",
        "badge_bg": "#F3F0FF",
        "badge_color": "#6D28D9",
        "badge_border": "#C4B5FD",
        "accent": "#6D28D9",
        "label": "iOS",
    },
    "Website": {
        "icon": "🌐",
        "badge_bg": "#FFF5EF",
        "badge_color": "#C04800",
        "badge_border": "#FFBF99",
        "accent": "#F26F21",
        "label": "Website",
    },
    "Không hiện mã lỗi_Dịch vụ": {
        "icon": "⚠️",
        "badge_bg": "#FFFBEB",
        "badge_color": "#92400E",
        "badge_border": "#FCD34D",
        "accent": "#D97706",
        "label": "Không hiện mã lỗi_Dịch vụ",
    },
    "Lỗi box 650 hiện hữu": {
        "icon": "📦",
        "badge_bg": "#FFF0F0",
        "badge_color": "#B91C1C",
        "badge_border": "#FCA5A5",
        "accent": "#DC2626",
        "label": "Lỗi box 650 hiện hữu",
    },
}

_DEFAULT_CONFIG = {
    "icon": "🔧",
    "badge_bg": "#F0F3F8",
    "badge_color": "#3A4454",
    "badge_border": "#C8D0DC",
    "accent": "#8896A5",
    "label": "Khác",
}

# ═══════════════════════════════════════════════════════════════
#  PARSE DỮ LIỆU THEO TỪNG SHEET
# ═══════════════════════════════════════════════════════════════

def _clean(val) -> str:
    """Chuẩn hóa giá trị ô thành chuỗi sạch."""
    if val is None:
        return ""
    return str(val).strip()


def _parse_sheet(ws, sheet_name: str) -> list[dict]:
    """
    Trả về list[dict] với keys: platform, ma_loi, mo_ta, nguyen_nhan, cach_xu_ly.
    Xử lý khác biệt cấu trúc cột từng sheet.
    """
    headers = [
        str(c.value).strip().lower() if c.value else ""
        for c in ws[1]
    ]

    rows: list[dict] = []

    # ── Sheet đặc biệt: Lỗi box 650 (không có cột chuẩn) ──────
    if sheet_name == "Lỗi box 650 hiện hữu":
        for r in range(2, ws.max_row + 1):
            text = _clean(ws.cell(r, 1).value)
            if not text:
                continue
            # Tách tiêu đề trường hợp
            lines   = text.split("\n")
            title   = lines[0].strip() if lines else text[:80]
            content = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
            rows.append({
                "platform": "Box 650",
                "ma_loi": "",
                "mo_ta": title,
                "nguyen_nhan": "",
                "cach_xu_ly": content,
            })
        return rows

    # ── Sheet "Không hiện mã lỗi_Dịch vụ" ────────────────────
    if sheet_name == "Không hiện mã lỗi_Dịch vụ":
        for r in range(2, ws.max_row + 1):
            stt     = _clean(ws.cell(r, 1).value)
            noi_dung = _clean(ws.cell(r, 2).value)
            xu_ly   = _clean(ws.cell(r, 3).value)
            if not noi_dung and not xu_ly:
                continue
            rows.append({
                "platform": "Dịch vụ",
                "ma_loi": stt,
                "mo_ta": noi_dung,
                "nguyen_nhan": "",
                "cach_xu_ly": xu_ly,
            })
        return rows

    # ── iOS: cột 3 = Nguyên nhân, cột 4 = Ghi chú thêm, cột 5 = Cách xử lý ──
    if sheet_name == "iOS":
        for r in range(2, ws.max_row + 1):
            platform  = _clean(ws.cell(r, 1).value)
            ma_loi    = _clean(ws.cell(r, 2).value)
            nn        = _clean(ws.cell(r, 3).value)
            ghi_chu   = _clean(ws.cell(r, 4).value)
            xu_ly     = _clean(ws.cell(r, 5).value)
            if not ma_loi:
                continue
            nguyen_nhan = "\n".join(filter(None, [nn, ghi_chu])) if ghi_chu else nn
            rows.append({
                "platform": platform or "iOS",
                "ma_loi": ma_loi,
                "mo_ta": nn[:80] if nn else "",
                "nguyen_nhan": nguyen_nhan,
                "cach_xu_ly": xu_ly,
            })
        return rows

    # ── Website: cột 4 chứa toàn bộ chi tiết (đã có cả Nguyên nhân + Cách xử lý) ──
    if sheet_name == "Website":
        for r in range(2, ws.max_row + 1):
            platform = _clean(ws.cell(r, 1).value)
            ma_loi   = _clean(ws.cell(r, 2).value)
            nn       = _clean(ws.cell(r, 3).value)
            detail   = _clean(ws.cell(r, 4).value)
            if not ma_loi:
                continue
            rows.append({
                "platform": platform or "Website",
                "ma_loi": ma_loi,
                "mo_ta": nn[:80] if nn else "",
                "nguyen_nhan": nn,
                "cach_xu_ly": detail,
            })
        return rows

    # ── SmartTV & Android: cấu trúc chuẩn 4 cột ──────────────
    for r in range(2, ws.max_row + 1):
        platform  = _clean(ws.cell(r, 1).value)
        ma_loi    = _clean(ws.cell(r, 2).value)
        nn        = _clean(ws.cell(r, 3).value)
        xu_ly     = _clean(ws.cell(r, 4).value)
        if not ma_loi:
            continue
        # Mô tả ngắn: dòng đầu tiên của nguyên nhân (không kể dấu "- ")
        first_line = nn.split("\n")[0].lstrip("- ").strip() if nn else ""
        rows.append({
            "platform": platform or sheet_name,
            "ma_loi": ma_loi,
            "mo_ta": first_line[:80] if first_line else "",
            "nguyen_nhan": nn,
            "cach_xu_ly": xu_ly,
        })
    return rows


# ═══════════════════════════════════════════════════════════════
#  FORMAT NỘI DUNG CHI TIẾT → HTML
# ═══════════════════════════════════════════════════════════════

def _format_detail_html(text: str, accent: str) -> str:
    """
    Chuyển nội dung multi-line thành HTML danh sách có định dạng.
    - Dòng bắt đầu bằng "B1:", "Bước 1:", "- " → list item
    - Dòng bắt đầu bằng "+" → sub item (thụt vào)
    - Còn lại → paragraph
    """
    if not text:
        return ""

    lines = text.split("\n")
    html_parts: list[str] = []
    in_list = False

    def _esc(s: str) -> str:
        return _html.escape(s.strip())

    step_pat  = re.compile(r"^(B\d+|Bước\s*\d+)\s*[:.]?\s*", re.IGNORECASE)
    bullet_pat = re.compile(r"^[-•]\s+")
    sub_pat    = re.compile(r"^\+\s+")

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if step_pat.match(line):
            if not in_list:
                html_parts.append("<ol class='ec-steps'>")
                in_list = True
            content = step_pat.sub("", line)
            html_parts.append(f"<li>{_esc(content)}</li>")

        elif bullet_pat.match(line):
            if not in_list:
                html_parts.append("<ul class='ec-bullets'>")
                in_list = True
            content = bullet_pat.sub("", line)
            html_parts.append(f"<li>{_esc(content)}</li>")

        elif sub_pat.match(line):
            content = sub_pat.sub("", line)
            html_parts.append(f"<li class='ec-sub'>{_esc(content)}</li>")

        else:
            if in_list:
                # Đóng list hiện tại trước
                html_parts.append("</ol>" if any("ec-steps" in p for p in html_parts[-10:]) else "</ul>")
                in_list = False
            html_parts.append(f"<p class='ec-para'>{_esc(line)}</p>")

    if in_list:
        html_parts.append("</ol>" if any("<ol" in p for p in html_parts[-20:]) else "</ul>")

    return "\n".join(html_parts)


# ═══════════════════════════════════════════════════════════════
#  CSS ACCORDION CARDS
# ═══════════════════════════════════════════════════════════════

_EC_CSS = """<style>
/* ══ ERROR CODE ACCORDION CARDS ══ */
.ec-card {
    background: #fff;
    border-radius: 14px;
    margin-bottom: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border: 1.5px solid #EDF0F5;
    font-family: 'Sora', sans-serif;
    transition: box-shadow 0.2s;
}
.ec-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.09); }

/* Dòng header (luôn hiển thị) */
.ec-header {
    display: flex;
    align-items: center;
    padding: 12px 14px;
    gap: 10px;
    cursor: pointer;
    user-select: none;
}
.ec-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 9px;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    white-space: nowrap;
    flex-shrink: 0;
    border: 1px solid transparent;
}
.ec-code {
    font-size: 1.0rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    flex-shrink: 0;
    min-width: 54px;
}
.ec-desc {
    font-size: 0.78rem;
    color: #5A6070;
    flex: 1;
    line-height: 1.4;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
.ec-arrow {
    font-size: 0.9rem;
    color: #B0BBC8;
    flex-shrink: 0;
    transition: transform 0.25s;
    margin-left: 2px;
}
.ec-arrow.open { transform: rotate(180deg); }

/* Nội dung chi tiết (khi mở) */
.ec-body {
    padding: 0 14px 14px 14px;
    border-top: 1px solid #F0F3F8;
    animation: ec-slide-down 0.2s ease-out;
}
@keyframes ec-slide-down {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.ec-section-title {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #A0AEBB;
    margin: 12px 0 6px 0;
}
.ec-bullets, .ec-steps {
    margin: 0 0 4px 0;
    padding-left: 18px;
}
.ec-bullets li, .ec-steps li {
    font-size: 0.82rem;
    color: #3A4454;
    line-height: 1.6;
    margin-bottom: 3px;
}
li.ec-sub {
    font-size: 0.78rem;
    color: #7A8899;
    margin-left: 12px;
    list-style-type: circle;
}
.ec-para {
    font-size: 0.82rem;
    color: #3A4454;
    line-height: 1.6;
    margin: 4px 0;
}
.ec-divider {
    height: 1px;
    background: #F0F3F8;
    margin: 10px 0;
}
.ec-empty {
    text-align: center;
    color: #B0BBC8;
    font-size: 0.82rem;
    padding: 24px 0;
    font-family: 'Sora', sans-serif;
}
.ec-count-badge {
    display: inline-block;
    background: #F0F3F8;
    color: #8896A5;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 10px;
    margin-left: 8px;
    font-family: 'Sora', sans-serif;
}
@media (max-width: 480px) {
    .ec-code { font-size: 0.9rem; }
    .ec-desc { font-size: 0.74rem; }
    .ec-header { padding: 11px 12px; gap: 8px; }
    .ec-body   { padding: 0 12px 12px 12px; }
}
</style>"""


# ═══════════════════════════════════════════════════════════════
#  RENDER MỘT CARD
# ═══════════════════════════════════════════════════════════════

def _render_card(row: dict, cfg: dict, card_key: str, is_open: bool) -> bool:
    """
    Render một accordion card. Trả về True nếu user vừa click toggle.
    Dùng st.button() làm trigger vì Streamlit không hỗ trợ HTML onClick.
    """
    badge_html = (
        f'<span class="ec-badge" style="'
        f'background:{cfg["badge_bg"]};'
        f'color:{cfg["badge_color"]};'
        f'border-color:{cfg["badge_border"]};'
        f'">{cfg["icon"]} {_html.escape(row["platform"])}</span>'
    )

    code_str = str(row["ma_loi"]) if row["ma_loi"] else "—"
    arrow_cls = "ec-arrow open" if is_open else "ec-arrow"

    header_html = (
        f'<div class="ec-header">'
        f'  {badge_html}'
        f'  <span class="ec-code" style="color:{cfg["accent"]};">{_html.escape(code_str)}</span>'
        f'  <span class="{arrow_cls}">▾</span>'
        f'</div>'
    )

    # Body (chỉ render khi mở)
    body_html = ""
    if is_open:
        nn_html = _format_detail_html(row["nguyen_nhan"], cfg["accent"])
        xu_ly_html = _format_detail_html(row["cach_xu_ly"], cfg["accent"])

        body_parts = ['<div class="ec-body">']
        if nn_html:
            body_parts.append(f'<div class="ec-section-title">🔍 Nguyên nhân</div>{nn_html}')
        if nn_html and xu_ly_html:
            body_parts.append('<div class="ec-divider"></div>')
        if xu_ly_html:
            body_parts.append(f'<div class="ec-section-title">🛠 Cách xử lý</div>{xu_ly_html}')
        if not nn_html and not xu_ly_html:
            body_parts.append('<p class="ec-para" style="color:#B0BBC8;">Chưa có thông tin chi tiết.</p>')
        body_parts.append('</div>')
        body_html = "\n".join(body_parts)

    card_border = cfg["accent"] if is_open else "#EDF0F5"
    st.markdown(
        f'<div class="ec-card" style="border-color:{card_border};">'
        f'{header_html}{body_html}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Nút ẩn để toggle (dùng st.button với label trống + CSS ẩn)
    return st.button(
        f"{'Thu gọn' if is_open else 'Xem chi tiết'} mã {code_str}",
        key=card_key,
        use_container_width=True,
        type="secondary",
    )


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT CHÍNH
# ═══════════════════════════════════════════════════════════════

@st.cache_data(ttl=120)
def _load_error_data(xlsx_path: str) -> dict[str, list[dict]]:
    """Load và parse tất cả sheet. Cache 2 phút."""
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    result = {}
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        result[sheet_name] = _parse_sheet(ws, sheet_name)
    wb.close()
    return result


def render_error_code_accordion(xlsx_path: str, session_prefix: str = "ec") -> None:
    """
    Render toàn bộ file Quy_hoach_ma_loi_FPT_Play.xlsx
    dưới dạng Accordion Cards tối ưu mobile.
    """
    if not os.path.isfile(xlsx_path):
        st.warning(f"⚠️ Chưa tìm thấy file: {os.path.basename(xlsx_path)}")
        return

    # Inject CSS (1 lần)
    st.markdown(_EC_CSS, unsafe_allow_html=True)

    # Load data
    all_data = _load_error_data(xlsx_path)
    sheet_names = list(all_data.keys())

    # ── Session state ──────────────────────────────────────────
    sk_sheet = f"{session_prefix}_sheet"
    sk_open  = f"{session_prefix}_open_card"
    sk_search = f"{session_prefix}_search"

    if st.session_state.get(sk_sheet) not in sheet_names:
        st.session_state[sk_sheet] = sheet_names[0]
    if sk_open not in st.session_state:
        st.session_state[sk_open] = None

    active_sheet = st.session_state[sk_sheet]

    # ── Tabs chọn sheet ────────────────────────────────────────
    st.markdown(
        "<p style='color:#8896A5;font-size:0.78rem;margin:10px 0 6px;"
        "font-family:Sora,sans-serif;'>📋 Chọn nền tảng / loại thiết bị:</p>",
        unsafe_allow_html=True,
    )

    for i in range(0, len(sheet_names), 3):
        chunk = sheet_names[i:i + 3]
        for col, name in zip(st.columns(len(chunk)), chunk):
            cfg = _SHEET_CONFIG.get(name, _DEFAULT_CONFIG)
            with col:
                if st.button(
                    cfg['label'],
                    key=f"{session_prefix}_tab_{name}",
                    type="primary" if name == active_sheet else "secondary",
                    use_container_width=True,
                ):
                    st.session_state[sk_sheet] = name
                    st.session_state[sk_open]  = None
                    st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Thanh tìm kiếm trong sheet ────────────────────────────
    search_kw = st.text_input(
        "",
        placeholder="🔍  Tìm mã lỗi hoặc từ khóa trong sheet này...",
        label_visibility="collapsed",
        key=sk_search,
    ).strip().lower()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Lọc dữ liệu ───────────────────────────────────────────
    rows = all_data[active_sheet]
    if search_kw:
        rows = [
            r for r in rows
            if (search_kw in str(r["ma_loi"]).lower()
                or search_kw in r["mo_ta"].lower()
                or search_kw in r["nguyen_nhan"].lower()
                or search_kw in r["cach_xu_ly"].lower())
        ]

    cfg = _SHEET_CONFIG.get(active_sheet, _DEFAULT_CONFIG)
    count_badge = f'<span class="ec-count-badge">{len(rows)} mục</span>'
    st.markdown(
        f"<p style='font-weight:700;color:{cfg['accent']};font-size:0.88rem;"
        f"font-family:Sora,sans-serif;margin-bottom:10px;'>"
        f"{active_sheet} {count_badge}</p>",
        unsafe_allow_html=True,
    )

    if not rows:
        st.markdown(
            '<div class="ec-empty">😕 Không tìm thấy kết quả.<br>'
            '<small>Thử từ khóa khác hoặc chọn sheet khác.</small></div>',
            unsafe_allow_html=True,
        )
        return

    # ── Render từng card ───────────────────────────────────────
    open_key = st.session_state[sk_open]

    for idx, row in enumerate(rows):
        card_key = f"{session_prefix}_card_{active_sheet}_{idx}"
        is_open  = (open_key == card_key)

        toggled = _render_card(row, cfg, card_key, is_open)
        if toggled:
            st.session_state[sk_open] = None if is_open else card_key
            st.rerun()

    # ── Nút tải file ──────────────────────────────────────────
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    with open(xlsx_path, "rb") as f:
        st.download_button(
            label="📥  Tải file Excel đầy đủ",
            data=f,
            file_name=os.path.basename(xlsx_path),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"{session_prefix}_dl",
        )