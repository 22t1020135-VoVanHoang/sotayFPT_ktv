"""
views/quy_trinh.py
Render tab "Quy trình" và tab "Xử lý sự cố".
Exports helpers dùng chung: render_section_header, render_expander_list.
"""

import os
import streamlit as st
import openpyxl

from utils.highlight_text import highlight_text
from excel_renderer import render_excel_file

_BASE       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_XU_LY_DIR  = os.path.join(_BASE, "tailieu", "xu_ly_su_co")
_PPTX_PATH  = os.path.join(_XU_LY_DIR, "CAC_VAN_DE_THUONG_GAP_Camera.pptx")
_XLSX_PATH  = os.path.join(_XU_LY_DIR, "Quy_hoach_ma_loi_FPT_Play.xlsx")
_SUPPORTED  = {".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".docx", ".doc"}


# ──────────────────────────────────────────────────────────────
#  Helpers dùng chung
# ──────────────────────────────────────────────────────────────

def render_section_header(icon: str, title: str, count: int | None = None) -> None:
    # QUAN TRỌNG: Không được có dòng trắng bên trong HTML block.
    # Marked.js (Streamlit's parser) sẽ thoát khỏi HTML mode khi gặp blank line
    # và render phần còn lại (</div>) thành plain text hiển thị trên màn hình.
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
    """
    Lọc danh sách theo keyword và hiển thị dưới dạng expander.
    Khi có keyword: tự mở rộng và highlight kết quả.
    """
    kw = keyword.strip().lower()
    filtered = [
        r for r in rows
        if not kw or kw in r["ten"].lower() or kw in r["buoc"].lower()
    ]

    if not filtered:
        if show_empty:
            st.markdown(
                '<div class="empty-state">😕 Không tìm thấy kết quả nào.<br>'
                '<small style="color:#B0BBC8;font-size:0.8rem">Thử từ khóa khác.</small></div>',
                unsafe_allow_html=True,
            )
        return

    auto_expand = bool(kw)
    for row in filtered:
        if not row["ten"]:
            continue
        label = f"🔎  {row['ten']}" if (kw and kw in row["ten"].lower()) else f"🛠  {row['ten']}"
        with st.expander(label, expanded=auto_expand):
            st.markdown(highlight_text(row["buoc"], keyword), unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  Tab Quy trình
# ──────────────────────────────────────────────────────────────

def render_quy_trinh(data: list[dict], keyword: str = "") -> None:
    rows = [r for r in data if r["folder"] == "Quy trình"]
    kw   = keyword.strip().lower()
    count = sum(1 for r in rows if not kw or kw in r["ten"].lower() or kw in r["buoc"].lower()) if kw else len(rows)
    render_section_header("📂", "Quy trình", count)
    render_expander_list(rows, keyword)


# ──────────────────────────────────────────────────────────────
#  Tab Xử lý sự cố — helpers nội bộ
# ──────────────────────────────────────────────────────────────

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


@st.cache_data(ttl=60)
def _get_sheet_names(path: str) -> list[str]:
    """Đọc tên sheet (cache 60s, đồng bộ ttl với render_excel_file)."""
    try:
        wb = openpyxl.load_workbook(path, read_only=True)
        names = wb.sheetnames
        wb.close()
        return names
    except Exception:
        return []


def _render_excel_with_sheet_tabs(xlsx_path: str, session_key: str) -> None:
    """Hiển thị Excel với tab chọn sheet + nút tải về."""
    if not os.path.isfile(xlsx_path):
        st.warning(f"⚠️ Chưa tìm thấy file: {os.path.basename(xlsx_path)}")
        return

    sheet_names = _get_sheet_names(xlsx_path)
    if not sheet_names:
        st.warning("⚠️ Không đọc được sheet nào từ file Excel.")
        return

    if st.session_state.get(session_key) not in sheet_names:
        st.session_state[session_key] = sheet_names[0]

    active_sheet = st.session_state[session_key]

    st.markdown(
        "<p style='color:#8896A5;font-size:0.78rem;margin:10px 0 6px;"
        "font-family:Sora,sans-serif;'>📋 Chọn nền tảng / loại thiết bị:</p>",
        unsafe_allow_html=True,
    )

    for i in range(0, len(sheet_names), 4):
        chunk = sheet_names[i:i + 4]
        for col, name in zip(st.columns(len(chunk)), chunk):
            with col:
                if st.button(
                    name, key=f"{session_key}_sheet_{name}",
                    type="primary" if name == active_sheet else "secondary",
                    use_container_width=True,
                ):
                    st.session_state[session_key] = name
                    st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    sheet_map = dict(render_excel_file(xlsx_path))
    st.markdown(
        sheet_map.get(active_sheet, "<p style='color:red'>Không tìm thấy sheet.</p>"),
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    with open(xlsx_path, "rb") as f:
        st.download_button(
            label="📥  Tải file Excel",
            data=f,
            file_name=os.path.basename(xlsx_path),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_{session_key}",
        )


def _render_xu_ly_docs() -> None:
    """Render 2 tài liệu đính kèm: PPTX Camera + Excel mã lỗi FPT Play."""
    st.markdown(
        "<hr style='border:none;border-top:1px solid #EDF0F5;margin:1.4rem 0 1.2rem 0;'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#F26F21;font-weight:700;font-size:0.9rem;"
        "font-family:Sora,sans-serif;margin-bottom:14px;'>📎 Tài liệu xử lý sự cố</p>",
        unsafe_allow_html=True,
    )

    # --- PPTX Camera ---
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

    # --- Excel mã lỗi FPT Play ---
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


# ──────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────

def render_xu_ly_su_co(data: list[dict], keyword: str = "") -> None:
    rows = [r for r in data if r["folder"] == "Xử lý sự cố"]
    file_count = (
        sum(1 for f in os.listdir(_XU_LY_DIR) if os.path.splitext(f)[1].lower() in _SUPPORTED)
        if os.path.isdir(_XU_LY_DIR) else 0
    )
    render_section_header("🔧", "Xử lý sự cố", len(rows) + file_count)
    render_expander_list(rows, keyword, show_empty=bool(rows))
    _render_xu_ly_docs()