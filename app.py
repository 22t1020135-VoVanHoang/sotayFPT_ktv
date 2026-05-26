"""
app.py — Sổ Tay KTV FPT Telecom
Entry point của ứng dụng Streamlit.
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
from data_loader import load_data, get_file_mtime
from views.quy_trinh import render_quy_trinh, render_xu_ly_su_co
from views.ban_hang import render_ban_hang
from views.tai_lieu import render_tai_lieu, count_cau_hinh_files

inject_css()

# ── Auto-refresh: cứ 3 giây tự kiểm tra file Excel thay đổi chưa ──
# Dùng st.fragment + time.sleep — không cần cài thêm thư viện nào.
import time as _time

@st.fragment(run_every=3)
def _watch_excel():
    """Fragment này rerun mỗi 3 giây, kiểm tra mtime file Excel.
    Nếu file thay đổi → xóa cache load_data → rerun toàn app."""
    current_mtime = get_file_mtime()
    if "_excel_mtime" not in st.session_state:
        st.session_state._excel_mtime = current_mtime
    if current_mtime != st.session_state._excel_mtime:
        st.session_state._excel_mtime = current_mtime
        load_data.clear()   # xóa cache cũ
        st.rerun()          # rerun toàn bộ app

_watch_excel()

# ── Load dữ liệu ──
# get_file_mtime() chạy mỗi lần rerun (không cache) để phát hiện file thay đổi.
# load_data() cache theo mtime — tự reload khi file Excel được lưu.

try:
    DATA = load_data(get_file_mtime())
except FileNotFoundError:
    st.error("❌ Không tìm thấy file **SO_TAY_KTV.xlsx**.")
    st.stop()
except ValueError as e:
    st.error(f"❌ File **SO_TAY_KTV.xlsx** {e}.")
    st.stop()
except Exception as e:
    st.error(f"❌ Lỗi đọc file SO_TAY_KTV.xlsx: {e}")
    st.stop()

# ── Logo ──

_APP_BASE = os.path.dirname(os.path.abspath(__file__))


@st.cache_data
def _logo_b64() -> str:
    for path in (
        os.path.join(_APP_BASE, "logo.png"),
        os.path.join(_APP_BASE, "tailieu", "logo.png"),
    ):
        if os.path.isfile(path):
            try:
                return base64.b64encode(open(path, "rb").read()).decode()
            except Exception:
                pass
    return ""


_logo = _logo_b64()
_logo_img = (
    f'<img src="data:image/png;base64,{_logo}" class="fpt-nav-logo" alt="FPT Telecom"/>'
    if _logo
    else '<span style="font-weight:800;color:#F26F21;font-size:1.1rem;">FPT</span>'
)

# ── Navbar ──

st.markdown(
    f'<div class="fpt-nav"><div class="fpt-nav-brand">{_logo_img}'
    f'<div><div class="fpt-nav-title">Sổ Tay KTV</div>'
    f'<div class="fpt-nav-subtitle">Kỹ thuật viên — Tra cứu nhanh</div></div></div></div>',
    unsafe_allow_html=True,
)

# ── Hero ──

st.markdown("""
<div class="fpt-hero">
    <span class="fpt-hero-eyebrow">Sổ tay kỹ thuật viên FPT Telecom</span>
    <div class="fpt-hero-title">Tra cứu nhanh — Làm việc<br><span>hiệu quả hơn mỗi ngày</span></div>
    <div class="fpt-hero-desc">Quy trình lắp đặt, xử lý sự cố, chính sách bán hàng và tài liệu kỹ thuật — cập nhật liên tục, luôn sẵn sàng.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ── Thanh tìm kiếm ──

_, col_search, _ = st.columns([0.5, 3, 0.5])
with col_search:
    keyword = st.text_input(
        "",
        placeholder="🔍  Nhập tên quy trình, sự cố, tài liệu...",
        label_visibility="collapsed",
    )
kw = keyword.strip()

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

# ── Session state ──

st.session_state.setdefault("active_folder",    "Quy trình")
st.session_state.setdefault("active_subfolder", "Tài liệu tân binh")
st.session_state.setdefault("_last_kw",         "")

# ── Tags tĩnh cho smart search ──

_XU_LY_TAGS  = frozenset({"camera fpt life", "các vấn đề thường gặp", "mã lỗi fpt play",
                           "smarttv", "android", "ios", "firmware"})
_TAI_LIEU_TAGS = frozenset({"tài liệu tân binh", "kỹ năng", "chuyên môn", "chính sách chế độ",
                             "cấu hình thiết bị", "internet hub ax3000s", "skyworth wifi6",
                             "hướng dẫn sử dụng", "đào tạo", "mesh wifi"})
_CAU_HINH_KW = frozenset({"cấu hình", "thiết bị", "ax3000s", "skyworth", "wifi6",
                           "internet hub", "đào tạo", "mesh"})

FOLDER_KEYS = ["Quy trình", "Xử lý sự cố", "Bán hàng", "Tài liệu"]
FOLDERS = {
    "📂  Quy trình":    "Quy trình",
    "🔧  Xử lý sự cố": "Xử lý sự cố",
    "🛒  Bán hàng":     "Bán hàng",
    "📁  Tài liệu":     "Tài liệu",
}

_XU_LY_DIR  = os.path.join(_APP_BASE, "tailieu", "xu_ly_su_co")
_XU_LY_EXTS = frozenset({".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".docx", ".doc"})
_TAN_BINH_COUNT = 3


# ── Helpers đếm hits / tổng ──

def _data_hits(folder_key: str, kw_lower: str) -> int:
    return sum(
        1 for r in DATA
        if r["folder"] == folder_key
        and (kw_lower in r["ten"].lower() or kw_lower in r["buoc"].lower())
    )


def _count_hits(folder_key: str, kw_lower: str) -> int:
    if not kw_lower:
        return 0
    data_count = _data_hits(folder_key, kw_lower)
    if folder_key == "Xử lý sự cố":
        return data_count + sum(1 for s in _XU_LY_TAGS if kw_lower in s)
    if folder_key == "Tài liệu":
        return sum(1 for s in _TAI_LIEU_TAGS if kw_lower in s)
    return data_count


def _count_total(folder_key: str) -> int:
    if folder_key == "Xử lý sự cố":
        file_count = (
            sum(1 for f in os.listdir(_XU_LY_DIR) if os.path.splitext(f)[1].lower() in _XU_LY_EXTS)
            if os.path.isdir(_XU_LY_DIR) else 0
        )
        return sum(1 for r in DATA if r["folder"] == folder_key) + file_count
    if folder_key == "Tài liệu":
        return _TAN_BINH_COUNT + count_cau_hinh_files()
    return sum(1 for r in DATA if r["folder"] == folder_key)


# ── Smart search: tự động chuyển tab phù hợp nhất ──

if kw and kw != st.session_state._last_kw:
    kw_lower   = kw.lower()
    hit_counts = {fk: _count_hits(fk, kw_lower) for fk in FOLDER_KEYS}
    best       = max(hit_counts, key=hit_counts.get)
    if hit_counts[best] > 0:
        st.session_state.active_folder = best
        if best == "Tài liệu":
            st.session_state.active_subfolder = (
                "Cấu hình thiết bị"
                if any(k in kw_lower for k in _CAU_HINH_KW)
                else "Tài liệu tân binh"
            )
    st.session_state._last_kw = kw

if not kw:
    st.session_state._last_kw = ""

# ── Banner kết quả tìm kiếm ──

if kw:
    kw_lower   = kw.lower()
    hit_counts = {fk: _count_hits(fk, kw_lower) for fk in FOLDER_KEYS}
    total_hits = sum(hit_counts.values())

    if total_hits > 0:
        parts = [f"<b>{fk}</b>: {cnt} kết quả" for fk, cnt in hit_counts.items() if cnt > 0]
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

# ── Folder tabs ──

_, c1, c2, c3, c4, _ = st.columns([0.5, 1, 1, 1, 1, 0.5])
for col, (label, folder_key) in zip([c1, c2, c3, c4], FOLDERS.items()):
    with col:
        total = _count_total(folder_key)
        count_label = (
            f"  ({_count_hits(folder_key, kw.lower())}/{total})" if kw
            else f"  ({total})"
        )
        if st.button(
            f"{label}{count_label}",
            key=f"btn_{folder_key}",
            type="primary" if st.session_state.active_folder == folder_key else "secondary",
            use_container_width=True,
        ):
            st.session_state.active_folder = folder_key
            st.rerun()

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.markdown(
    "<hr style='border:none;border-top:1px solid #EDF0F5;margin:0 0 1.2rem 0;'>",
    unsafe_allow_html=True,
)

# ── Nội dung folder ──

_RENDER_MAP = {
    "Quy trình":    lambda: render_quy_trinh(DATA, kw),
    "Xử lý sự cố": lambda: render_xu_ly_su_co(DATA, kw),
    "Bán hàng":     lambda: render_ban_hang(DATA, kw),
    "Tài liệu":     lambda: render_tai_lieu(kw),
}

_, col_main, _ = st.columns([0.15, 3.7, 0.15])
with col_main:
    _RENDER_MAP[st.session_state.active_folder]()