"""
views/ban_hang.py
Render tab "Bán hàng": danh sách expander + bảng giá cước inline.
"""

import os
import streamlit as st
from utils.highlight_text import highlight_text
from excel_renderer import show_excel_inline
from views.quy_trinh import render_section_header

import os as _os_bh
_BH_BASE = _os_bh.path.dirname(_os_bh.path.dirname(_os_bh.path.abspath(__file__)))
def _find_bh_file(name):
    for p in [_os_bh.path.join(_BH_BASE, name), _os_bh.path.join(_BH_BASE, "tailieu", name)]:
        if _os_bh.path.isfile(p): return p
    return _os_bh.path.join(_BH_BASE, name)
BANG_GIA_FILE = _find_bh_file("Chuong_Trinh_Ban_Hang.xlsx")


def render_ban_hang(data: list, keyword: str = ""):
    """Render toàn bộ tab Bán hàng."""
    rows = [r for r in data if r["folder"] == "Bán hàng"]
    kw_lower = keyword.strip().lower()

    filtered = [
        r for r in rows
        if not kw_lower
        or kw_lower in r["ten"].lower()
        or kw_lower in r["buoc"].lower()
    ]

    # Header: hiện số kết quả khi tìm kiếm
    if kw_lower:
        render_section_header("🛒", "Bán hàng", len(filtered))
    else:
        render_section_header("🛒", "Bán hàng", len(rows))

    if not filtered:
        st.markdown(
            '<div class="empty-state">😕 Không tìm thấy kết quả nào.<br>'
            '<small style="color:#B0BBC8;font-size:0.8rem">Thử từ khóa khác.</small></div>',
            unsafe_allow_html=True,
        )
        return

    # Scroll anchor khi có tìm kiếm
    if kw_lower:
        st.markdown(
            '<div id="search-result-anchor" style="height:0;margin:0;padding:0;"></div>',
            unsafe_allow_html=True,
        )

    for row in filtered:
        if row["ten"]:
            # Đánh dấu kết quả khớp
            if kw_lower and kw_lower in row["ten"].lower():
                expander_label = f"🔎  {row['ten']}"
            else:
                expander_label = f"🛠  {row['ten']}"

            auto_expand = bool(kw_lower)

            with st.expander(expander_label, expanded=auto_expand):
                st.markdown(highlight_text(row["buoc"], keyword), unsafe_allow_html=True)

                if row["ten"].strip() == "Chương trình bán hàng":
                    st.markdown(
                        "<p style='color:#005DA3;font-weight:700;"
                        "margin:12px 0 8px;font-size:0.9rem;"
                        "font-family:Sora,sans-serif;'>📊 Bảng giá cước FPT</p>",
                        unsafe_allow_html=True,
                    )
                    show_excel_inline(BANG_GIA_FILE, css_class="bg-excel-wrap")
                    if not os.path.exists(BANG_GIA_FILE):
                        st.warning(
                            f"⚠️ Chưa có file **{BANG_GIA_FILE}**. "
                            "Hãy đặt file vào cùng thư mục với app."
                        )

    # JS scroll đến kết quả
    if kw_lower and filtered:
        st.markdown("""
        <script>
        (function() {
            function scrollToResults() {
                var anchor = document.getElementById('search-result-anchor');
                if (anchor) {
                    anchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
            if (document.readyState === 'complete') {
                setTimeout(scrollToResults, 300);
            } else {
                window.addEventListener('load', function() {
                    setTimeout(scrollToResults, 300);
                });
            }
        })();
        </script>
        """, unsafe_allow_html=True)