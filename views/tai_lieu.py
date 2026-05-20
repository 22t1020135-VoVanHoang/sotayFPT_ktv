"""
views/tai_lieu.py
Render tab "Tài liệu": subfolder Tân binh và Cấu hình thiết bị.
"""

import os
import streamlit as st

from utils.highlight_text import highlight_text
from views.quy_trinh import render_section_header

_BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CAU_HINH_DIR = os.path.join(_BASE_DIR, "tailieu", "cau_hinh")

_SUPPORTED_EXT = frozenset({".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".docx", ".doc"})
_MIME_MAP = {
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".ppt":  "application/vnd.ms-powerpoint",
    ".pdf":  "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".doc":  "application/msword",
}
_SUBFOLDERS = {
    "🎓  Tài liệu tân binh": "Tài liệu tân binh",
    "⚙️  Cấu hình thiết bị": "Cấu hình thiết bị",
}

_TAN_BINH_ITEMS = [
    {
        "icon": "💡", "title": "1.1  Kỹ Năng",
        "desc": "Kỹ năng mềm, giao tiếp, xử lý tình huống với khách hàng",
        "link": "https://drive.google.com/drive/folders/1LVBcFccDMTpCZOMW_iSiYuIBfkJ7oeOT",
        "color": "#F26F21", "bg": "#FFF5EF", "border": "rgba(242,111,33,0.2)",
        "search_tags": ["kỹ năng", "giao tiếp", "tình huống", "tân binh"],
    },
    {
        "icon": "🔬", "title": "1.2  Chuyên Môn",
        "desc": "Quy trình kỹ thuật, triển khai, xử lý sự cố chuyên sâu",
        "link": "https://drive.google.com/drive/folders/1mP531dZ0ZG-0FwuL75BNFEWRF_UfT4YY",
        "color": "#005DA3", "bg": "#EFF6FF", "border": "rgba(0,93,163,0.15)",
        "search_tags": ["chuyên môn", "kỹ thuật", "triển khai", "tân binh"],
    },
    {
        "icon": "📋", "title": "1.3  Chính Sách & Chế Độ",
        "desc": "Chính sách công ty, chế độ đãi ngộ, quy định nội bộ",
        "link": "https://drive.google.com/drive/folders/1dP5TtP7-CTqWa3VIqb3um6vP9BwMZbpY",
        "color": "#1A7A42", "bg": "#EFFAF4", "border": "rgba(26,122,66,0.15)",
        "search_tags": ["chính sách", "chế độ", "đãi ngộ", "quy định", "tân binh"],
    },
]

# Metadata tĩnh cho file PDF trong cau_hinh/
_PDF_META: dict[str, dict] = {
    "internethubax3000s.pdf": {
        "title": "Hướng dẫn sử dụng Internet Hub AX3000S",
        "desc":  "Thông số kỹ thuật, giao diện quang, LAN, WLAN và thông số vật lý thiết bị",
        "color": "#005DA3", "bg": "#EFF6FF", "border": "rgba(0,93,163,0.15)",
        "search_tags": ["ax3000s", "internet hub", "hướng dẫn", "cấu hình thiết bị", "wifi"],
    },
    "Skyworth WiFi6 ONT Internet Hub AX3000S Specification_V6.0.pdf": {
        "title": "Thông số kỹ thuật WiFi 6 ONT Internet Hub AX3000S — Skyworth (V6.0)",
        "desc":  "Đặc tả phần cứng từ nhà sản xuất Skyworth: chipset, sơ đồ khối, cổng và LED",
        "color": "#1A7A42", "bg": "#EFFAF4", "border": "rgba(26,122,66,0.15)",
        "search_tags": ["skyworth", "wifi6", "wifi 6", "ax3000s", "cấu hình thiết bị", "ont"],
    },
}
_PDF_META_FALLBACK = {
    "title": "Tài liệu đào tạo triển khai Mesh Wi-Fi 6 GPON Internet Hub AX3000S",
    "desc":  "Tài liệu nội bộ FPT Digital — hướng dẫn cấu hình và thực hành lab (v1.0)",
    "color": "#F26F21", "bg": "#FFF5EF", "border": "rgba(242,111,33,0.2)",
    "search_tags": ["đào tạo", "mesh", "wifi 6", "gpon", "ax3000s", "cấu hình thiết bị", "lab"],
}
_PDF_META_DEFAULT_FACTORY = lambda fname: {
    "title": os.path.splitext(fname)[0],
    "desc":  "Tài liệu kỹ thuật",
    "color": "#5A6070", "bg": "#F0F3F8", "border": "rgba(90,96,112,0.15)",
    "search_tags": ["cấu hình thiết bị"],
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_pdf_meta(fname: str) -> dict:
    if fname in _PDF_META:
        return _PDF_META[fname]
    fname_lower = fname.lower()
    if "đào" in fname_lower or "#u0111" in fname_lower or "T#U" in fname:
        return _PDF_META_FALLBACK
    return _PDF_META_DEFAULT_FACTORY(fname)


def _item_matches(item: dict, kw: str) -> bool:
    if not kw:
        return True
    return (
        any(kw in tag for tag in item.get("search_tags", []))
        or kw in item.get("title", "").lower()
        or kw in item.get("desc", "").lower()
    )


def _list_cau_hinh_files() -> list[tuple[str, str, str]]:
    if not os.path.isdir(_CAU_HINH_DIR):
        return []
    return [
        (fname, ext := os.path.splitext(fname)[1].lower(), os.path.join(_CAU_HINH_DIR, fname))
        for fname in sorted(os.listdir(_CAU_HINH_DIR))
        if (ext := os.path.splitext(fname)[1].lower()) in _SUPPORTED_EXT
    ]


def count_cau_hinh_files() -> int:
    return len(_list_cau_hinh_files())


# ── Render: Tài liệu tân binh ─────────────────────────────────────────────────

def _render_tan_binh(keyword: str = "") -> None:
    kw       = keyword.strip().lower()
    filtered = [item for item in _TAN_BINH_ITEMS if _item_matches(item, kw)]

    if not filtered:
        st.markdown(
            '<div class="empty-state">😕 Không tìm thấy tài liệu tân binh khớp với từ khóa.<br>'
            '<small style="color:#B0BBC8;">Thử: <b>kỹ năng</b>, <b>chuyên môn</b>, <b>chính sách</b></small></div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        "<p style='color:#8896A5;font-size:0.82rem;margin-bottom:14px;"
        "font-family:Sora,sans-serif;'>"
        "📌 Bấm vào từng mục để mở thư mục Google Drive tương ứng.</p>",
        unsafe_allow_html=True,
    )

    for item in filtered:
        st.markdown(
            f'<a href="{item["link"]}" target="_blank" style="text-decoration:none;display:block;">'
            f'  <div class="doc-card" style="border-color:{item["border"]};border-left:3px solid {item["color"]};">'
            f'    <div class="doc-card-icon" style="background:{item["bg"]};">{item["icon"]}</div>'
            f'    <div style="flex:1;">'
            f'      <div class="doc-card-title" style="color:{item["color"]};">{highlight_text(item["title"], keyword)}</div>'
            f'      <div class="doc-card-desc">{highlight_text(item["desc"], keyword)}</div>'
            f'    </div>'
            f'    <div class="doc-card-arrow" style="color:{item["color"]};">↗</div>'
            f'  </div>'
            f'</a>',
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div style='margin-top:8px;text-align:center;'>"
        "<a href='https://drive.google.com/drive/folders/1-C5YrCV7UGPL0NOf7e8dWWurAHodJ7qr' "
        "target='_blank' style='color:#B0BBC8;font-size:0.78rem;text-decoration:none;"
        "font-family:Sora,sans-serif;'>📂 Xem toàn bộ thư mục →</a></div>",
        unsafe_allow_html=True,
    )


# ── Render: Cấu hình thiết bị ─────────────────────────────────────────────────

def _render_cau_hinh(keyword: str = "") -> None:
    kw        = keyword.strip().lower()
    all_files = _list_cau_hinh_files()

    if not all_files:
        st.markdown(
            f'<div class="doc-placeholder">'
            f'  <div style="font-size:2.2rem;margin-bottom:10px;">⚙️</div>'
            f'  <b style="color:#3A4454;font-family:Sora,sans-serif;">Chưa có tài liệu nào</b><br><br>'
            f'  <span style="color:#8896A5;font-family:Sora,sans-serif;font-size:0.85rem;">'
            f'    Đặt file PDF vào thư mục '
            f'    <code style="background:#F0F3F8;padding:2px 7px;border-radius:5px;color:#005DA3;">{_CAU_HINH_DIR}</code>'
            f'  </span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    files_to_show = (
        [
            (fname, ext, fpath) for fname, ext, fpath in all_files
            if _item_matches(_get_pdf_meta(fname), kw) or kw in fname.lower()
        ]
        if kw else all_files
    )

    if not files_to_show:
        st.markdown(
            '<div class="empty-state">😕 Không tìm thấy tài liệu cấu hình khớp với từ khóa.<br>'
            '<small style="color:#B0BBC8;">Thử: <b>ax3000s</b>, <b>skyworth</b>, <b>wifi 6</b>, <b>đào tạo</b></small></div>',
            unsafe_allow_html=True,
        )
        return

    for fname, ext, fpath in files_to_show:
        meta = _get_pdf_meta(fname)
        st.markdown(
            f'<div class="doc-card" style="border-color:{meta["border"]};border-left:3px solid {meta["color"]};">'
            f'  <div class="doc-card-icon" style="background:{meta["bg"]};">📄</div>'
            f'  <div style="flex:1;">'
            f'    <div class="doc-card-title" style="color:{meta["color"]};">{highlight_text(meta["title"], keyword)}</div>'
            f'    <div class="doc-card-desc">{highlight_text(meta["desc"], keyword)}</div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        with open(fpath, "rb") as f:
            st.download_button(
                label=f"📥  Tải về — {fname}",
                data=f, file_name=fname,
                mime=_MIME_MAP.get(ext, "application/octet-stream"),
                key=f"dl_{fname}",
            )
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


# ── Entry point ───────────────────────────────────────────────────────────────

def render_tai_lieu(keyword: str = "") -> None:
    total = len(_TAN_BINH_ITEMS) + count_cau_hinh_files()
    render_section_header("📁", "Tài liệu", total)

    _, sf1, sf2, _ = st.columns([1, 1, 1, 1])
    for col, (label, sf_key) in zip([sf1, sf2], _SUBFOLDERS.items()):
        with col:
            if st.button(
                label, key=f"sf_{sf_key}",
                type="primary" if st.session_state.active_subfolder == sf_key else "secondary",
                use_container_width=True,
            ):
                st.session_state.active_subfolder = sf_key
                st.rerun()

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    active_sf = st.session_state.active_subfolder
    if active_sf == "Tài liệu tân binh":
        _render_tan_binh(keyword)
    elif active_sf == "Cấu hình thiết bị":
        _render_cau_hinh(keyword)
