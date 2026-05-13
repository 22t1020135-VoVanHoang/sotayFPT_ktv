"""
views/quy_trinh.py
Render section header + danh sách expander dùng chung
cho tab "Quy trình" và tab "Xử lý sự cố".
"""

import streamlit as st
from utils.highlight_text import highlight_text


def render_section_header(icon: str, title: str, count: int = None):
    """Hiển thị tiêu đề section kèm số lượng mục."""
    count_html = f"<span class='fpt-section-count'>{count} mục</span>" if count is not None else ""
    st.markdown(f"""
    <div class="fpt-section-header">
        <div class="fpt-section-icon">{icon}</div>
        <span class="fpt-section-title">{title}</span>
        {count_html}
    </div>
    """, unsafe_allow_html=True)


def render_expander_list(rows: list, keyword: str = ""):
    """
    Lọc danh sách theo keyword và hiển thị từng mục dưới dạng expander.
    """
    kw_lower = keyword.lower()
    filtered = [
        r for r in rows
        if not kw_lower
        or kw_lower in r["ten"].lower()
        or kw_lower in r["buoc"].lower()
    ]
    if not filtered:
        st.markdown(
            '<div class="empty-state">😕 Không tìm thấy kết quả nào.<br>'
            '<small style="color:#B0BBC8;font-size:0.8rem">Thử từ khóa khác.</small></div>',
            unsafe_allow_html=True,
        )
        return
    for row in filtered:
        if row["ten"]:
            with st.expander(f"🛠  {row['ten']}"):
                st.markdown(highlight_text(row["buoc"]), unsafe_allow_html=True)


def render_quy_trinh(data: list, keyword: str = ""):
    """Render toàn bộ tab Quy trình."""
    rows = [r for r in data if r["folder"] == "Quy trình"]
    render_section_header("📂", "Quy trình", len(rows))
    render_expander_list(rows, keyword)


def render_xu_ly_su_co(data: list, keyword: str = ""):
    """Render toàn bộ tab Xử lý sự cố."""
    rows = [r for r in data if r["folder"] == "Xử lý sự cố"]
    render_section_header("🔧", "Xử lý sự cố", len(rows))
    render_expander_list(rows, keyword)
