"""
views/tai_lieu.py
Render tab "Tài liệu": subfolder Tân binh và Cấu hình thiết bị.
"""

import os
import streamlit as st
from excel_renderer import show_excel_inline
from views.quy_trinh import render_section_header


# ── Dữ liệu tĩnh ──
_TAN_BINH_SUBS = [
    {
        "icon": "💡", "title": "1.1  Kỹ Năng",
        "desc": "Kỹ năng mềm, giao tiếp, xử lý tình huống với khách hàng",
        "link": "https://drive.google.com/drive/folders/1LVBcFccDMTpCZOMW_iSiYuIBfkJ7oeOT",
        "color": "#F26F21", "bg": "#FFF5EF", "border": "rgba(242,111,33,0.2)",
    },
    {
        "icon": "🔬", "title": "1.2  Chuyên Môn",
        "desc": "Quy trình kỹ thuật, triển khai, xử lý sự cố chuyên sâu",
        "link": "https://drive.google.com/drive/folders/1mP531dZ0ZG-0FwuL75BNFEWRF_UfT4YY",
        "color": "#005DA3", "bg": "#EFF6FF", "border": "rgba(0,93,163,0.15)",
    },
    {
        "icon": "📋", "title": "1.3  Chính Sách & Chế Độ",
        "desc": "Chính sách công ty, chế độ đãi ngộ, quy định nội bộ",
        "link": "https://drive.google.com/drive/folders/1dP5TtP7-CTqWa3VIqb3um6vP9BwMZbpY",
        "color": "#1A7A42", "bg": "#EFFAF4", "border": "rgba(26,122,66,0.15)",
    },
]

_SUBFOLDERS = {
    "🎓  Tài liệu tân binh": "Tài liệu tân binh",
    "⚙️  Cấu hình thiết bị": "Cấu hình thiết bị",
}

_SUPPORTED_EXT = [".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".docx", ".doc"]
_MIME_MAP = {
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".ppt":  "application/vnd.ms-powerpoint",
    ".pdf":  "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".doc":  "application/msword",
}

# ── Tiêu đề và mô tả cho từng file PDF ──
_PDF_TITLES = {
    "internethubax3000s.pdf": {
        "title": "Hướng dẫn sử dụng Internet Hub AX3000S",
        "desc":  "Thông số kỹ thuật, giao diện quang, LAN, WLAN và thông số vật lý thiết bị",
        "color": "#005DA3", "bg": "#EFF6FF", "border": "rgba(0,93,163,0.15)",
    },
    "Skyworth WiFi6 ONT Internet Hub AX3000S Specification_V6.0.pdf": {
        "title": "Thông số kỹ thuật WiFi 6 ONT Internet Hub AX3000S — Skyworth (V6.0)",
        "desc":  "Đặc tả phần cứng từ nhà sản xuất Skyworth: chipset, sơ đồ khối, cổng và LED",
        "color": "#1A7A42", "bg": "#EFFAF4", "border": "rgba(26,122,66,0.15)",
    },
}
# File thứ 3 có tên tiếng Việt bị encode, dùng fallback theo từ khóa
_PDF_TITLE_FALLBACK = {
    "title": "Tài liệu đào tạo triển khai Mesh Wi-Fi 6 GPON Internet Hub AX3000S",
    "desc":  "Tài liệu nội bộ FPT Digital — hướng dẫn cấu hình và thực hành lab (v1.0)",
    "color": "#F26F21", "bg": "#FFF5EF", "border": "rgba(242,111,33,0.2)",
}


def _get_pdf_meta(fname: str) -> dict:
    """Trả về tiêu đề/màu cho file PDF. Dùng fallback nếu tên file chứa ký tự encode."""
    if fname in _PDF_TITLES:
        return _PDF_TITLES[fname]
    # File tên tiếng Việt bị encode — nhận diện qua từ khóa
    if "đào" in fname.lower() or "#u0111" in fname.lower() or "T#U" in fname:
        return _PDF_TITLE_FALLBACK
    # File không rõ — dùng tên file làm tiêu đề
    return {
        "title": os.path.splitext(fname)[0],
        "desc":  "Tài liệu kỹ thuật",
        "color": "#5A6070", "bg": "#F0F3F8", "border": "rgba(90,96,112,0.15)",
    }


def _render_tan_binh():
    """Hiển thị subfolder Tài liệu tân binh."""
    st.markdown(
        "<p style='color:#8896A5;font-size:0.82rem;margin-bottom:14px;"
        "font-family:Sora,sans-serif;'>"
        "📌 Bấm vào từng mục để mở thư mục Google Drive tương ứng.</p>",
        unsafe_allow_html=True,
    )
    for item in _TAN_BINH_SUBS:
        st.markdown(f"""
        <a href="{item['link']}" target="_blank" style="text-decoration:none;display:block;">
            <div class="doc-card" style="border-color:{item['border']};border-left:3px solid {item['color']};">
                <div class="doc-card-icon" style="background:{item['bg']};">{item['icon']}</div>
                <div style="flex:1;">
                    <div class="doc-card-title" style="color:{item['color']};">{item['title']}</div>
                    <div class="doc-card-desc">{item['desc']}</div>
                </div>
                <div class="doc-card-arrow" style="color:{item['color']};">↗</div>
            </div>
        </a>""", unsafe_allow_html=True)

    st.markdown(
        "<div style='margin-top:8px;text-align:center;'>"
        "<a href='https://drive.google.com/drive/folders/1-C5YrCV7UGPL0NOf7e8dWWurAHodJ7qr' "
        "target='_blank' style='color:#B0BBC8;font-size:0.78rem;text-decoration:none;"
        "font-family:Sora,sans-serif;'>"
        "📂 Xem toàn bộ thư mục →</a></div>",
        unsafe_allow_html=True,
    )


def _render_cau_hinh():
    """Hiển thị subfolder Cấu hình thiết bị — đọc từ tailieu/cau_hinh/."""
    _base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder_dir = os.path.join(_base, "tailieu", "cau_hinh")  # ← thư mục chứa 3 file PDF

    files_found = []
    if os.path.exists(folder_dir):
        for fname in sorted(os.listdir(folder_dir)):
            ext = os.path.splitext(fname)[1].lower()
            if ext in _SUPPORTED_EXT:
                files_found.append((fname, ext, os.path.join(folder_dir, fname)))

    if not files_found:
        st.markdown(f"""
        <div class="doc-placeholder">
            <div style="font-size:2.2rem;margin-bottom:10px;">⚙️</div>
            <b style="color:#3A4454;font-family:Sora,sans-serif;">Chưa có tài liệu nào</b><br><br>
            <span style="color:#8896A5;font-family:Sora,sans-serif;font-size:0.85rem;">
                Đặt file PDF vào thư mục
                <code style="background:#F0F3F8;padding:2px 7px;
                border-radius:5px;color:#005DA3;">{folder_dir}</code>
            </span>
        </div>""", unsafe_allow_html=True)
        return

    for fname, ext, fpath in files_found:
        meta = _get_pdf_meta(fname)

        # Card hiển thị tiêu đề + mô tả
        st.markdown(f"""
        <div class="doc-card" style="border-color:{meta['border']};
             border-left:3px solid {meta['color']};">
            <div class="doc-card-icon" style="background:{meta['bg']};">📄</div>
            <div style="flex:1;">
                <div class="doc-card-title" style="color:{meta['color']};">
                    {meta['title']}
                </div>
                <div class="doc-card-desc">{meta['desc']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Nút tải về
        with open(fpath, "rb") as f:
            st.download_button(
                label=f"📥  Tải về — {fname}",
                data=f,
                file_name=fname,
                mime=_MIME_MAP.get(ext, "application/octet-stream"),
                key=f"dl_{fname}",
            )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


def render_tai_lieu():
    """Render toàn bộ tab Tài liệu gồm 2 subfolder."""
    # Đếm tổng: 3 link tân binh + số file trong cau_hinh
    _cau_hinh_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "tailieu", "cau_hinh"
    )
    cau_hinh_count = sum(
        1 for f in os.listdir(_cau_hinh_dir)
        if os.path.splitext(f)[1].lower() in _SUPPORTED_EXT
    ) if os.path.isdir(_cau_hinh_dir) else 0
    total = len(_TAN_BINH_SUBS) + cau_hinh_count
    render_section_header("📁", "Tài liệu", total)

    # Subfolder buttons
    _, sf1, sf2, _ = st.columns([1, 1, 1, 1])
    for col, (label, sf_key) in zip([sf1, sf2], _SUBFOLDERS.items()):
        with col:
            is_sf = st.session_state.active_subfolder == sf_key
            if st.button(
                label, key=f"sf_{sf_key}",
                type="primary" if is_sf else "secondary",
                use_container_width=True,
            ):
                st.session_state.active_subfolder = sf_key
                st.rerun()

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    active_sf = st.session_state.active_subfolder

    if active_sf == "Tài liệu tân binh":
        _render_tan_binh()
    elif active_sf == "Cấu hình thiết bị":
        _render_cau_hinh()