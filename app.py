"""
SỔ TAY KTV FPT — Streamlit App
Phiên bản giao diện: Modern Corporate & Premium Tech

Entry point: chạy bằng lệnh
    streamlit run app.py
"""

import base64
import streamlit as st

# ── Cấu hình trang (phải gọi đầu tiên) ──
st.set_page_config(
    page_title="Sổ Tay KTV — FPT Telecom",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Import các module nội bộ ──
from styles import inject_css
from data_loader import load_data, FILE_PATH
from views.quy_trinh import render_quy_trinh, render_xu_ly_su_co
from views.ban_hang import render_ban_hang
from views.tai_lieu import render_tai_lieu


# ===== INJECT CSS =====
inject_css()


# ===== LOAD DỮ LIỆU =====
try:
    DATA = load_data()
except FileNotFoundError:
    st.error("❌ Không tìm thấy file **SO_TAY_KTV.xlsx**. Hãy đặt file vào cùng thư mục với app.")
    st.stop()
except ValueError as e:
    st.error(
        f"❌ File **SO_TAY_KTV.xlsx** {e}.\n\n"
        "Hàng đầu tiên phải có đúng tên cột: `ten` | `buoc` | `folder`"
    )
    st.stop()
except Exception as e:
    st.error(f"❌ Lỗi đọc file SO_TAY_KTV.xlsx: {e}")
    st.stop()


# ===== NAVIGATION BAR =====
def _load_logo_b64(filename: str = "logo.png") -> str:
    """Đọc logo.png và trả về chuỗi base64 để nhúng thẳng vào HTML."""
    import os
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


# ===== HERO + SEARCH =====
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
        placeholder="🔍  Nhập tên quy trình, sự cố...",
        label_visibility="collapsed",
    )
kw = keyword.strip()

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)


# ===== FOLDER TABS =====
FOLDERS = {
    "📂  Quy trình":    "Quy trình",
    "🔧  Xử lý sự cố": "Xử lý sự cố",
    "🛒  Bán hàng":     "Bán hàng",
    "📁  Tài liệu":     "Tài liệu",
}

if "active_folder" not in st.session_state:
    st.session_state.active_folder = "Quy trình"
if "active_subfolder" not in st.session_state:
    st.session_state.active_subfolder = "Tài liệu tân binh"

_, c1, c2, c3, c4, _ = st.columns([0.5, 1, 1, 1, 1, 0.5])
for col, (label, folder_key) in zip([c1, c2, c3, c4], FOLDERS.items()):
    with col:
        folder_count = sum(1 for r in DATA if r["folder"] == folder_key)
        count_label  = "" if folder_key == "Tài liệu" else f"  ({folder_count})"
        is_active    = st.session_state.active_folder == folder_key
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
        render_tai_lieu()
