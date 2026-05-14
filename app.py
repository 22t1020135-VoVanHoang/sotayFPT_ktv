"""
SỔ TAY KTV FPT — Streamlit App
"""

import base64
import os
import streamlit as st

st.set_page_config(
    page_title="Sổ Tay KTV — FPT Telecom",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from styles import inject_css
from data_loader import load_data, FILE_PATH
from views.quy_trinh import render_quy_trinh, render_xu_ly_su_co
from views.ban_hang import render_ban_hang
from views.tai_lieu import render_tai_lieu

inject_css()

# ===== LOAD DỮ LIỆU =====
try:
    DATA = load_data()
except FileNotFoundError:
    st.error("❌ Không tìm thấy file **SO_TAY_KTV.xlsx**.")
    st.stop()
except ValueError as e:
    st.error(f"❌ File **SO_TAY_KTV.xlsx** {e}.")
    st.stop()
except Exception as e:
    st.error(f"❌ Lỗi đọc file SO_TAY_KTV.xlsx: {e}")
    st.stop()

# ===== NAV =====
def _load_logo_b64(filename: str = "logo.png") -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for path in [os.path.join(base_dir, filename), os.path.join(base_dir, "tailieu", filename)]:
        if os.path.isfile(path):
            try:
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:
                return ""
    return ""

_logo_b64 = _load_logo_b64()
_logo_img = (
    f'<img src="data:image/png;base64,{_logo_b64}" class="fpt-nav-logo" alt="FPT Telecom"/>'
    if _logo_b64 else
    '<span style="font-weight:800;color:#F26F21;font-size:1.1rem;">FPT</span>'
)

st.markdown(f"""
<div class="fpt-nav">
    <div class="fpt-nav-brand">
        {_logo_img}
        <div>
            <div class="fpt-nav-title">Sổ Tay KTV</div>
            <div class="fpt-nav-subtitle">Kỹ thuật viên — Tra cứu nhanh</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== HERO =====
st.markdown("""
<div class="fpt-hero">
    <span class="fpt-hero-eyebrow">Sổ tay kỹ thuật viên FPT Telecom</span>
    <div class="fpt-hero-title">Tra cứu nhanh — Làm việc<br><span>hiệu quả hơn mỗi ngày</span></div>
    <div class="fpt-hero-desc">Quy trình lắp đặt, xử lý sự cố, chính sách bán hàng và tài liệu kỹ thuật — cập nhật liên tục, luôn sẵn sàng.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
_, col_search, _ = st.columns([0.5, 3, 0.5])
with col_search:
    keyword = st.text_input(
        "",
        placeholder="🔍  Nhập tên quy trình, sự cố, tài liệu...",
        label_visibility="collapsed",
    )
kw = keyword.strip()

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

# ===== SESSION STATE =====
if "active_folder" not in st.session_state:
    st.session_state.active_folder = "Quy trình"
if "active_subfolder" not in st.session_state:
    st.session_state.active_subfolder = "Tài liệu tân binh"
if "_last_kw" not in st.session_state:
    st.session_state._last_kw = ""

_APP_BASE = os.path.dirname(os.path.abspath(__file__))

# ===== HÀM ĐẾM KẾT QUẢ CHO TỪNG TAB =====
# Nội dung tĩnh của tab Tài liệu — dùng để tìm kiếm
_TAI_LIEU_STATIC_CONTENT = [
    "tài liệu tân binh",
    "kỹ năng",
    "chuyên môn",
    "chính sách chế độ",
    "cấu hình thiết bị",
    "internet hub ax3000s",
    "skyworth wifi6",
    "hướng dẫn sử dụng",
    "đào tạo",
    "mesh wifi",
]

# Nội dung tĩnh của tab Xử lý sự cố
_XU_LY_STATIC_CONTENT = [
    "camera fpt life",
    "các vấn đề thường gặp",
    "mã lỗi fpt play",
    "smarttv",
    "android",
    "ios",
    "firmware",
]

def _count_hits_in_folder(folder_key: str, kw_lower: str) -> int:
    """Đếm số kết quả khớp trong một folder, bao gồm cả nội dung tĩnh."""
    if not kw_lower:
        return 0

    if folder_key in ("Quy trình", "Bán hàng"):
        rows = [r for r in DATA if r["folder"] == folder_key]
        return sum(
            1 for r in rows
            if kw_lower in r["ten"].lower() or kw_lower in r["buoc"].lower()
        )

    if folder_key == "Xử lý sự cố":
        rows = [r for r in DATA if r["folder"] == folder_key]
        data_hits = sum(
            1 for r in rows
            if kw_lower in r["ten"].lower() or kw_lower in r["buoc"].lower()
        )
        static_hits = sum(1 for s in _XU_LY_STATIC_CONTENT if kw_lower in s)
        return data_hits + static_hits

    if folder_key == "Tài liệu":
        # Tìm trong nội dung tĩnh của tab Tài liệu
        return sum(1 for s in _TAI_LIEU_STATIC_CONTENT if kw_lower in s)

    return 0


# ===== SMART SEARCH: tự động chuyển tab =====
if kw and kw != st.session_state._last_kw:
    kw_lower = kw.lower()
    folder_order = ["Quy trình", "Xử lý sự cố", "Bán hàng", "Tài liệu"]
    best_folder = None
    best_count = 0
    for folder_key in folder_order:
        count = _count_hits_in_folder(folder_key, kw_lower)
        if count > best_count:
            best_count = count
            best_folder = folder_key
    if best_folder:
        st.session_state.active_folder = best_folder
        # Nếu nhảy vào Tài liệu → tự chọn subfolder phù hợp
        if best_folder == "Tài liệu":
            cau_hinh_kw = ["cấu hình", "thiết bị", "ax3000s", "skyworth", "wifi6", "internet hub", "đào tạo", "mesh"]
            if any(k in kw_lower for k in cau_hinh_kw):
                st.session_state.active_subfolder = "Cấu hình thiết bị"
            else:
                st.session_state.active_subfolder = "Tài liệu tân binh"
    st.session_state._last_kw = kw

if not kw:
    st.session_state._last_kw = ""

# ===== BANNER KẾT QUẢ TÌM KIẾM =====
if kw:
    kw_lower = kw.lower()
    folder_order = ["Quy trình", "Xử lý sự cố", "Bán hàng", "Tài liệu"]
    total_hits = {
        fk: _count_hits_in_folder(fk, kw_lower)
        for fk in folder_order
    }
    grand_total = sum(total_hits.values())

    if grand_total > 0:
        parts = []
        for fk, cnt in total_hits.items():
            if cnt > 0:
                parts.append(f"<b>{fk}</b>: {cnt} kết quả")
        st.markdown(
            f"<div style='text-align:center;font-size:0.82rem;color:#005DA3;"
            f"font-family:Sora,sans-serif;margin-bottom:4px;'>"
            f"🔍 Tìm thấy tại: {' &nbsp;|&nbsp; '.join(parts)}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='text-align:center;font-size:0.82rem;color:#C8530D;"
            "font-family:Sora,sans-serif;margin-bottom:4px;'>"
            "😕 Không tìm thấy kết quả nào. Thử từ khóa khác như: <b>triển khai</b>, <b>camera</b>, <b>bán hàng</b>...</div>",
            unsafe_allow_html=True,
        )

# ===== ĐẾM TỔNG SỐ MỤC (không theo kw) =====
def _count_folder_total(folder_key: str) -> int:
    if folder_key == "Xử lý sự cố":
        rows = sum(1 for r in DATA if r["folder"] == folder_key)
        _xu_ly_dir = os.path.join(_APP_BASE, "tailieu", "xu_ly_su_co")
        _supported = {".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".docx", ".doc"}
        files = sum(
            1 for f in os.listdir(_xu_ly_dir)
            if os.path.splitext(f)[1].lower() in _supported
        ) if os.path.isdir(_xu_ly_dir) else 0
        return rows + files
    if folder_key == "Tài liệu":
        tan_binh = 3
        _cau_hinh_dir = os.path.join(_APP_BASE, "tailieu", "cau_hinh")
        _supported = {".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".docx", ".doc"}
        cau_hinh = sum(
            1 for f in os.listdir(_cau_hinh_dir)
            if os.path.splitext(f)[1].lower() in _supported
        ) if os.path.isdir(_cau_hinh_dir) else 0
        return tan_binh + cau_hinh
    return sum(1 for r in DATA if r["folder"] == folder_key)

# ===== FOLDER TABS =====
FOLDERS = {
    "📂  Quy trình":    "Quy trình",
    "🔧  Xử lý sự cố": "Xử lý sự cố",
    "🛒  Bán hàng":     "Bán hàng",
    "📁  Tài liệu":     "Tài liệu",
}

_, c1, c2, c3, c4, _ = st.columns([0.5, 1, 1, 1, 1, 0.5])
for col, (label, folder_key) in zip([c1, c2, c3, c4], FOLDERS.items()):
    with col:
        total = _count_folder_total(folder_key)
        if kw:
            hits = _count_hits_in_folder(folder_key, kw.lower())
            count_label = f"  ({hits}/{total})" if hits else f"  (0/{total})"
        else:
            count_label = f"  ({total})"
        is_active = st.session_state.active_folder == folder_key
        if st.button(
            f"{label}{count_label}",
            key=f"btn_{folder_key}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.active_folder = folder_key
            st.rerun()

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.markdown(
    "<hr style='border:none;border-top:1px solid #EDF0F5;margin:0 0 1.2rem 0;'>",
    unsafe_allow_html=True,
)

# ===== NỘI DUNG TỪNG FOLDER =====
active = st.session_state.active_folder
_, col_main, _ = st.columns([0.15, 3.7, 0.15])
with col_main:
    if active == "Quy trình":
        render_quy_trinh(DATA, kw)
    elif active == "Xử lý sự cố":
        render_xu_ly_su_co(DATA, kw)
    elif active == "Bán hàng":
        render_ban_hang(DATA, kw)
    elif active == "Tài liệu":
        render_tai_lieu(kw)