"""
views/quy_trinh.py
Render tab "Quy trình" và tab "Xử lý sự cố".
"""

import os
import streamlit as st

from utils.highlight_text import highlight_text
from error_code_renderer import render_error_code_accordion

_BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_XU_LY_DIR = os.path.join(_BASE, "tailieu", "xu_ly_su_co")
_PPTX_PATH = os.path.join(_XU_LY_DIR, "CAC_VAN_DE_THUONG_GAP_Camera.pptx")
_XLSX_PATH = os.path.join(_XU_LY_DIR, "Quy_hoach_ma_loi_FPT_Play.xlsx")
_SUPPORTED = frozenset({".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".docx", ".doc"})

_EMPTY_HTML = (
    '<div class="empty-state">😕 Không tìm thấy kết quả nào.<br>'
    '<small style="color:#B0BBC8;font-size:0.8rem">Thử từ khóa khác.</small></div>'
)


# ── Shared helpers ────

def render_section_header(icon: str, title: str, count: int | None = None) -> None:
    count_html = f"<span class='fpt-section-count'>{count} mục</span>" if count is not None else ""
    st.markdown(
        f'<div class="fpt-section-header">'
        f'<div class="fpt-section-icon">{icon}</div>'
        f'<span class="fpt-section-title">{title}</span>'
        f'{count_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_expander_list(rows: list[dict], keyword: str = "", show_empty: bool = True) -> None:
    """Lọc theo keyword và hiển thị danh sách expander."""
    kw = keyword.strip().lower()
    filtered = [
        r for r in rows
        if not kw or kw in r["ten"].lower() or kw in r["buoc"].lower()
    ]

    if not filtered:
        if show_empty:
            st.markdown(_EMPTY_HTML, unsafe_allow_html=True)
        return

    auto_expand = bool(kw)
    for row in filtered:
        if not row["ten"]:
            continue
        label = f"🔎  {row['ten']}" if (kw and kw in row["ten"].lower()) else f"🛠  {row['ten']}"
        with st.expander(label, expanded=auto_expand):
            st.markdown(highlight_text(row["buoc"], keyword), unsafe_allow_html=True)


# ── Tab Quy trình ───

def render_quy_trinh(data: list[dict], keyword: str = "") -> None:
    rows = [r for r in data if r["folder"] == "Quy trình"]
    kw   = keyword.strip().lower()
    count = (
        sum(1 for r in rows if kw in r["ten"].lower() or kw in r["buoc"].lower())
        if kw else len(rows)
    )
    render_section_header("📂", "Quy trình", count)
    render_expander_list(rows, keyword)


# ── Tab Xử lý sự cố ───

def _doc_card_html(icon: str, title: str, desc: str,
                   color: str, bg: str, border: str) -> str:
    return (
        f'<div class="doc-card" style="border-color:{border};border-left:3px solid {color};margin-bottom:10px;">'
        f'  <div class="doc-card-icon" style="background:{bg};">{icon}</div>'
        f'  <div style="flex:1;">'
        f'    <div class="doc-card-title" style="color:{color};">{title}</div>'
        f'    <div class="doc-card-desc">{desc}</div>'
        f'  </div>'
        f'</div>'
    )


def _render_xu_ly_docs() -> None:
    """Render tài liệu đính kèm: PPTX Camera + Accordion mã lỗi FPT Play."""
    st.markdown(
        "<hr style='border:none;border-top:1px solid #EDF0F5;margin:1.4rem 0 1.2rem 0;'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#F26F21;font-weight:700;font-size:0.9rem;"
        "font-family:Sora,sans-serif;margin-bottom:14px;'>📎 Tài liệu xử lý sự cố</p>",
        unsafe_allow_html=True,
    )

    # PPTX Camera
    st.markdown(
        _doc_card_html(
            icon="📷",
            title="Các vấn đề thường gặp &amp; cách xử lý — Camera FPT Life",
            desc="Hướng dẫn xử lý lỗi đăng nhập, thêm camera, OTP, firmware — dành cho KTV",
            color="#F26F21", bg="#FFF5EF", border="rgba(242,111,33,0.2)",
        ),
        unsafe_allow_html=True,
    )
    if os.path.isfile(_PPTX_PATH):
        with open(_PPTX_PATH, "rb") as f:
            st.download_button(
                label="📥  Tải về — CAC_VAN_DE_THUONG_GAP_Camera.pptx",
                data=f,
                file_name="CAC_VAN_DE_THUONG_GAP_Camera.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key="dl_camera_pptx",
            )
    else:
        st.warning("⚠️ Chưa tìm thấy file PPTX. Đặt file vào tailieu/xu_ly_su_co/")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Accordion mã lỗi FPT Play
    st.markdown(
        _doc_card_html(
            icon="📺",
            title="Quy hoạch mã lỗi FPT Play",
            desc="Tra cứu mã lỗi theo nền tảng: SmartTV HTML, Android, iOS — nguyên nhân &amp; cách xử lý",
            color="#005DA3", bg="#EFF6FF", border="rgba(0,93,163,0.15)",
        ),
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    render_error_code_accordion(_XLSX_PATH, session_prefix="ec_fptplay")


def render_xu_ly_su_co(data: list[dict], keyword: str = "") -> None:
    rows = [r for r in data if r["folder"] == "Xử lý sự cố"]
    file_count = (
        sum(1 for f in os.listdir(_XU_LY_DIR) if os.path.splitext(f)[1].lower() in _SUPPORTED)
        if os.path.isdir(_XU_LY_DIR) else 0
    )
    render_section_header("🔧", "Xử lý sự cố", len(rows) + file_count)
    render_expander_list(rows, keyword, show_empty=bool(rows))
    _render_xu_ly_docs()
