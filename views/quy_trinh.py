"""
views/quy_trinh.py
Render section header + danh sách expander dùng chung
cho tab "Quy trình" và tab "Xử lý sự cố".
"""

import os
import streamlit as st
import openpyxl
from utils.highlight_text import highlight_text
from excel_renderer import render_excel_file

_BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_XU_LY_DIR = os.path.join(_BASE, "tailieu", "xu_ly_su_co")
_PPTX_PATH = os.path.join(_XU_LY_DIR, "CAC_VAN_DE_THUONG_GAP_Camera.pptx")
_XLSX_PATH = os.path.join(_XU_LY_DIR, "Quy_hoach_ma_loi_FPT_Play.xlsx")
_SUPPORTED = {".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".docx", ".doc"}


# ──────────────────────────────────────────────────────────────
#  Helpers dùng chung
# ──────────────────────────────────────────────────────────────

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


def render_expander_list(rows: list, keyword: str = "", show_empty: bool = True):
    """
    Lọc danh sách theo keyword và hiển thị từng mục dưới dạng expander.
    - Khi có keyword: tự động mở rộng (expanded=True) các mục khớp và highlight.
    - show_empty=False → không hiện thông báo trống khi folder còn có tài liệu riêng.
    """
    kw_lower = keyword.strip().lower()
    filtered = [
        r for r in rows
        if not kw_lower
        or kw_lower in r["ten"].lower()
        or kw_lower in r["buoc"].lower()
    ]

    if not filtered:
        if show_empty:
            st.markdown(
                '<div class="empty-state">😕 Không tìm thấy kết quả nào.<br>'
                '<small style="color:#B0BBC8;font-size:0.8rem">Thử từ khóa khác.</small></div>',
                unsafe_allow_html=True,
            )
        return

    # Khi đang tìm kiếm → thêm anchor để JS có thể scroll đến
    if kw_lower and filtered:
        st.markdown(
            '<div id="search-result-anchor" style="height:0;margin:0;padding:0;"></div>',
            unsafe_allow_html=True,
        )

    for row in filtered:
        if row["ten"]:
            # Highlight tên trong tiêu đề expander nếu khớp keyword
            if kw_lower and kw_lower in row["ten"].lower():
                # Thêm dấu hiệu trực quan vào title
                expander_label = f"🔎  {row['ten']}"
            else:
                expander_label = f"🛠  {row['ten']}"

            # Tự động mở expander khi có từ khóa
            auto_expand = bool(kw_lower)

            with st.expander(expander_label, expanded=auto_expand):
                st.markdown(highlight_text(row["buoc"], keyword), unsafe_allow_html=True)

    # Inject JS scroll khi có keyword và có kết quả
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
            // Thử scroll sau khi render xong
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


# ──────────────────────────────────────────────────────────────
#  Quy trình
# ──────────────────────────────────────────────────────────────

def render_quy_trinh(data: list, keyword: str = ""):
    """Render toàn bộ tab Quy trình."""
    rows = [r for r in data if r["folder"] == "Quy trình"]
    kw_lower = keyword.strip().lower()

    # Khi tìm kiếm: chỉ đếm kết quả khớp
    if kw_lower:
        matched = [r for r in rows if kw_lower in r["ten"].lower() or kw_lower in r["buoc"].lower()]
        render_section_header("📂", "Quy trình", len(matched))
    else:
        render_section_header("📂", "Quy trình", len(rows))

    render_expander_list(rows, keyword)


# ──────────────────────────────────────────────────────────────
#  Xử lý sự cố — tài liệu đính kèm
# ──────────────────────────────────────────────────────────────

def _doc_card_html(icon: str, title: str, desc: str,
                   color: str, bg: str, border: str) -> str:
    return f"""
    <div class="doc-card" style="border-color:{border};border-left:3px solid {color};margin-bottom:10px;">
        <div class="doc-card-icon" style="background:{bg};">{icon}</div>
        <div style="flex:1;">
            <div class="doc-card-title" style="color:{color};">{title}</div>
            <div class="doc-card-desc">{desc}</div>
        </div>
    </div>"""


@st.cache_data(ttl=30)
def _get_sheet_names(path: str) -> list:
    """Đọc tên các Sheet trong file Excel. Cache 30s — tự cập nhật khi file thay đổi."""
    try:
        wb = openpyxl.load_workbook(path, read_only=True)
        names = wb.sheetnames
        wb.close()
        return names
    except Exception:
        return []


def _render_excel_with_sheet_tabs(xlsx_path: str, session_key: str):
    """
    Hiển thị Excel với các nút tab theo tên Sheet.
    Bấm nút → chỉ hiện Sheet đó.
    Tự động cập nhật khi file Excel thay đổi (thêm/xóa/đổi tên sheet).
    """
    if not os.path.exists(xlsx_path):
        st.warning(f"⚠️ Chưa tìm thấy file: {os.path.basename(xlsx_path)}")
        return

    sheet_names = _get_sheet_names(xlsx_path)
    if not sheet_names:
        st.warning("⚠️ Không đọc được sheet nào từ file Excel.")
        return

    if session_key not in st.session_state or st.session_state[session_key] not in sheet_names:
        st.session_state[session_key] = sheet_names[0]

    active_sheet = st.session_state[session_key]

    st.markdown(
        "<p style='color:#8896A5;font-size:0.78rem;margin:10px 0 6px;"
        "font-family:Sora,sans-serif;'>📋 Chọn nền tảng / loại thiết bị:</p>",
        unsafe_allow_html=True,
    )
    chunk = 4
    for i in range(0, len(sheet_names), chunk):
        batch = sheet_names[i:i + chunk]
        cols = st.columns(len(batch))
        for col, sname in zip(cols, batch):
            with col:
                if st.button(
                    sname,
                    key=f"{session_key}_sheet_{sname}",
                    type="primary" if sname == active_sheet else "secondary",
                    use_container_width=True,
                ):
                    st.session_state[session_key] = sname
                    st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    all_sheets = render_excel_file(xlsx_path, css_class="bg-excel-wrap")
    sheet_map  = {name: html for name, html in all_sheets}
    html = sheet_map.get(active_sheet, "<p style='color:red'>Không tìm thấy sheet.</p>")
    st.markdown(html, unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    with open(xlsx_path, "rb") as f:
        st.download_button(
            label="📥  Tải file Excel",
            data=f,
            file_name=os.path.basename(xlsx_path),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_{session_key}",
        )


def _render_xu_ly_docs():
    """Render 2 tài liệu: PPTX Camera + Excel mã lỗi FPT Play."""
    st.markdown(
        "<hr style='border:none;border-top:1px solid #EDF0F5;margin:1.4rem 0 1.2rem 0;'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#F26F21;font-weight:700;font-size:0.9rem;"
        "font-family:Sora,sans-serif;margin-bottom:14px;'>"
        "📎 Tài liệu xử lý sự cố</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        _doc_card_html(
            icon="📷",
            title="Các vấn đề thường gặp &amp; cách xử lý — Camera FPT Life",
            desc="Hướng dẫn xử lý lỗi đăng nhập, thêm camera, OTP, firmware — dành cho KTV",
            color="#F26F21", bg="#FFF5EF", border="rgba(242,111,33,0.2)",
        ),
        unsafe_allow_html=True,
    )
    if os.path.exists(_PPTX_PATH):
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

    st.markdown(
        _doc_card_html(
            icon="📺",
            title="Quy hoạch mã lỗi FPT Play",
            desc="Tra cứu mã lỗi theo nền tảng: SmartTV HTML, Android, iOS — nguyên nhân &amp; cách xử lý",
            color="#005DA3", bg="#EFF6FF", border="rgba(0,93,163,0.15)",
        ),
        unsafe_allow_html=True,
    )
    _render_excel_with_sheet_tabs(_XLSX_PATH, session_key="xu_ly_xlsx_sheet")


def render_xu_ly_su_co(data: list, keyword: str = ""):
    """Render toàn bộ tab Xử lý sự cố."""
    rows = [r for r in data if r["folder"] == "Xử lý sự cố"]

    file_count = sum(
        1 for f in os.listdir(_XU_LY_DIR)
        if os.path.splitext(f)[1].lower() in _SUPPORTED
    ) if os.path.isdir(_XU_LY_DIR) else 0
    total = len(rows) + file_count

    render_section_header("🔧", "Xử lý sự cố", total)
    render_expander_list(rows, keyword, show_empty=(len(rows) > 0))
    _render_xu_ly_docs()