"""
views/ban_hang.py
Render tab "Bán hàng": Accordion khu vực → Cards gói cước.
"""

import streamlit as st
from views.quy_trinh import render_section_header

# ── Màu sắc theo gói ─────────────────────────────────────────────────────────
_C = {
    "GIGA":     {"bg": "#EFF6FF", "border": "#005DA3", "text": "#005DA3", "sub_bg": "#E8F2FF"},
    "SKY":      {"bg": "#FFF5EF", "border": "#F26F21", "text": "#C04800", "sub_bg": "#FFF0E8"},
    "META":     {"bg": "#EFFAF4", "border": "#1A7A42", "text": "#1A7A42", "sub_bg": "#E8F6ED"},
    "GIGA_CAM": {"bg": "#FFFBEB", "border": "#D97706", "text": "#92400E", "sub_bg": "#FFF8E0"},
}

# ── Dữ liệu gói cước ─────────────────────────────────────────────────────────
# Để gọn, helper tạo item gói
def _goi(label, net, app, box, phi_list):
    return {"label": label, "net": net, "combo_app": app, "combo_box": box, "phi": phi_list}

def _phi(label, net, app, box):
    return {"label": label, "net": net, "app": app, "box": box}

_PHM_SAU_300  = _phi("Phí hoà mạng trả sau",        "300K", "300K", "500K")
_PHM_TRUOC_300 = _phi("Phí hoà mạng trả trước ≥ 3T", "300K", "300K", "400K")
_PHM_SAU_500  = _phi("Phí hoà mạng trả sau",        "500K", "500K", "700K")
_PHM_TRUOC_500 = _phi("Phí hoà mạng trả trước ≥ 3T", "500K", "500K", "600K")
_PHM_SAU_700  = _phi("Phí hoà mạng trả sau",        "700K", "700K", "900K")
_PHM_TRUOC_700 = _phi("Phí hoà mạng trả trước ≥ 3T", "700K", "700K", "800K")

_PHM_XA_SAU_300   = _phi("Phí hoà mạng trả sau",        "300K", "300K", "400K")
_PHM_XA_TRUOC_300 = _phi("Phí hoà mạng trả trước ≥ 3T", "300K", "300K", "300K")
_PHM_XA_SAU_500   = _phi("Phí hoà mạng trả sau",        "500K", "500K", "600K")
_PHM_XA_TRUOC_500 = _phi("Phí hoà mạng trả trước ≥ 3T", "500K", "500K", "500K")
_PHM_XA_SAU_700   = _phi("Phí hoà mạng trả sau",        "700K", "700K", "800K")
_PHM_XA_TRUOC_700 = _phi("Phí hoà mạng trả trước ≥ 3T", "700K", "700K", "700K")

_DATA: dict[str, list[dict]] = {
    "Phường": [
        {
            "goi": "GIGA", "icon": "🔵", "color": _C["GIGA"],
            "bang_thong": "Upload – Download 300 Mbps",
            "items": [
                _goi("1 Modem",           "195K", "200K", "210K", [_PHM_SAU_300, _PHM_TRUOC_300]),
                _goi("1 Modem + 1 Mesh",  "205K", "210K", "220K", [_PHM_SAU_500, _PHM_TRUOC_500]),
                _goi("1 Modem + 2 Mesh",  "225K", "230K", "240K", [_PHM_SAU_700, _PHM_TRUOC_700]),
            ],
        },
        {
            "goi": "SKY", "icon": "🟡", "color": _C["SKY"],
            "bang_thong": "Upload 300 Mbps – Download 1024 Mbps",
            "items": [
                _goi("1 Modem",           "200K", "240K", "240K", [_PHM_SAU_300, _PHM_TRUOC_300]),
                _goi("1 Modem + 1 Mesh",  "210K", "250K", "250K", [_PHM_SAU_500, _PHM_TRUOC_500]),
                _goi("1 Modem + 2 Mesh",  "230K", "270K", "270K", [_PHM_SAU_700, _PHM_TRUOC_700]),
            ],
        },
        {
            "goi": "META", "icon": "🟢", "color": _C["META"],
            "bang_thong": "Upload – Download 1024 Mbps",
            "items": [
                _goi("1 Modem + 1 Mesh",  "330K", "380K", "380K", [_phi("Phí hoà mạng trả trước ≥ 3T", "500K", "500K", "600K")]),
                _goi("1 Modem + 2 Mesh",  "350K", "400K", "400K", [_phi("Phí hoà mạng trả trước ≥ 3T", "700K", "700K", "800K")]),
            ],
        },
    ],
    "Xã, Vùng ven": [
        {
            "goi": "GIGA", "icon": "🔵", "color": _C["GIGA"],
            "bang_thong": "Upload – Download 300 Mbps",
            "items": [
                _goi("1 Modem",           "195K", "200K", "210K", [_PHM_XA_SAU_300, _PHM_XA_TRUOC_300]),
                _goi("1 Modem + 1 Mesh",  "205K", "210K", "220K", [_PHM_XA_SAU_500, _PHM_XA_TRUOC_500]),
                _goi("1 Modem + 2 Mesh",  "225K", "230K", "240K", [_PHM_XA_SAU_700, _PHM_XA_TRUOC_700]),
            ],
        },
        {
            "goi": "SKY", "icon": "🟡", "color": _C["SKY"],
            "bang_thong": "Upload 300 Mbps – Download 1024 Mbps",
            "items": [
                _goi("1 Modem",           "200K", "240K", "240K", [_PHM_XA_SAU_300, _PHM_XA_TRUOC_300]),
                _goi("1 Modem + 1 Mesh",  "210K", "250K", "250K", [_PHM_XA_SAU_500, _PHM_XA_TRUOC_500]),
                _goi("1 Modem + 2 Mesh",  "230K", "270K", "270K", [_PHM_XA_SAU_700, _PHM_XA_TRUOC_700]),
            ],
        },
        {
            "goi": "META", "icon": "🟢", "color": _C["META"],
            "bang_thong": "Upload – Download 1024 Mbps",
            "items": [
                _goi("1 Modem + 1 Mesh",  "330K", "380K", "380K", [_phi("Phí hoà mạng trả trước ≥ 3T", "500K", "500K", "500K")]),
                _goi("1 Modem + 2 Mesh",  "350K", "400K", "400K", [_phi("Phí hoà mạng trả trước ≥ 3T", "700K", "700K", "700K")]),
            ],
        },
    ],
    "Toàn Thành Phố": [
        {
            "goi": "GIGA + CAM", "icon": "📷", "color": _C["GIGA_CAM"],
            "bang_thong": "",
            "ghi_chu": "Ưu đãi Camera cước tăng 10K sau 12T và sử dụng Camera IQ3S hoặc Play 4",
            "items": [
                _goi("Giga 1 Modem + CAM", "200K", "220K", "230K", [_phi("Phí hoà mạng", "400K", "400K", "800K")]),
            ],
        },
    ],
    "Xã Đặc Biệt": [
        {
            "goi": "GIGA + CAM", "icon": "📷", "color": _C["GIGA_CAM"],
            "bang_thong": "",
            "ghi_chu": "Ưu đãi Camera cước tăng 10K sau 12T và sử dụng Camera IQ3S hoặc Play 4",
            "items": [
                _goi("Giga 1 Modem Tặng CAM", "195K", "200K", "210K", [_phi("Phí hoà mạng", "300K", "300K", "400K")]),
            ],
        },
    ],
}

_COMBO_SPORT = {
    "ghi_chu": "Gói Combo Thể Thao có voucher giảm 30K trong vòng 12 tháng, sau đó về lại giá gốc.",
    "goi": [
        {
            "ten": "SKY", "icon": "🟡", "color": _C["SKY"],
            "items": [
                {"combo": "SKY V.VIP",    "gia_cuoc": "239K", "phm": "300K"},
                {"combo": "SKY V.VIP F1", "gia_cuoc": "249K", "phm": "500K"},
                {"combo": "SKY V.VIP F2", "gia_cuoc": "269K", "phm": "700K"},
            ],
        },
        {
            "ten": "META", "icon": "🟢", "color": _C["META"],
            "items": [
                {"combo": "META V.VIP",    "gia_cuoc": "339K", "phm": "300K"},
                {"combo": "META V.VIP F1", "gia_cuoc": "349K", "phm": "500K"},
                {"combo": "META V.VIP F2", "gia_cuoc": "369K", "phm": "700K"},
            ],
        },
    ],
}

_AREA_CONFIG = [
    ("Phường",          "Phường",                   None),
    ("Xã, Vùng ven",   "Xã, Vùng ven",              None),
    ("Toàn Thành Phố", "Đặc Biệt Toàn Thành Phố",  None),
    ("Xã Đặc Biệt",    "Xã Đặc Biệt",
     "Xã Phú Vang, Xã Phú Lộc, Xã Phú Vinh, Xã Chân Mây Lăng Cô, Xã Lộc An, "
     "Xã Đan Điền, Xã Bình Điền, Phường Thuận An, Phường Thanh Thuỷ, "
     "Phường Phong Quảng, Phường Phong Dinh, Phường Phú Bài"),
    ("Combo Thể Thao",  "Combo Thể Thao",            None),
]

_BH_CSS = """<style>
.bh-card{background:#fff;border-radius:16px;margin-bottom:18px;overflow:hidden;
  box-shadow:0 2px 14px rgba(0,0,0,0.06);border:1.5px solid #EDF0F5;font-family:'Sora',sans-serif}
.bh-card-header{padding:16px 20px 13px;border-bottom:1px solid rgba(0,0,0,0.06)}
.bh-card-title{font-size:1.02rem;font-weight:800;letter-spacing:-0.3px;margin-bottom:2px}
.bh-card-bw{font-size:0.74rem;color:#8896A5;font-weight:400}
.bh-note-badge{display:inline-block;margin-top:9px;background:rgba(217,119,6,0.09);
  color:#92400E;font-size:0.74rem;font-weight:600;padding:4px 11px;border-radius:8px;
  border:1px solid rgba(217,119,6,0.22);line-height:1.45}
.bh-col-header{display:flex;align-items:center;padding:8px 20px;
  background:#F7F8FA;border-bottom:1px solid #EDF0F5;gap:0}
.bh-col-h-label{flex:2 1 0;font-size:0.68rem;font-weight:700;color:#A0AEBB;
  text-transform:uppercase;letter-spacing:0.6px}
.bh-col-h-price{flex:1 1 0;font-size:0.68rem;font-weight:700;color:#A0AEBB;
  text-transform:uppercase;letter-spacing:0.6px;text-align:center}
.bh-item-row{display:flex;align-items:center;padding:12px 20px;
  border-bottom:1px solid #F2F5F8;gap:0;transition:background 0.15s}
.bh-item-row:hover{background:#FAFBFD}
.bh-item-label{flex:2 1 0;font-size:0.9rem;font-weight:700;line-height:1.3}
.bh-item-price{flex:1 1 0;text-align:center;font-size:0.95rem;font-weight:800;letter-spacing:-0.3px}
.bh-sub-row{display:flex;align-items:center;padding:7px 20px 7px 32px;
  border-bottom:1px solid #F2F5F8;background:#FAFBFD;gap:0}
.bh-sub-row:last-child{border-bottom:2px solid #EDF0F5}
.bh-sub-label{flex:2 1 0;font-size:0.76rem;color:#8896A5;font-weight:400;line-height:1.3}
.bh-sub-price{flex:1 1 0;text-align:center;font-size:0.8rem;color:#8896A5;font-weight:500}
.bh-item-sep{height:1px;background:linear-gradient(90deg,transparent,#E8EDF5 20%,#E8EDF5 80%,transparent);margin:0 20px}
.bh-sport-row{display:flex;align-items:center;padding:12px 20px;
  border-bottom:1px solid #F2F5F8;gap:0;transition:background 0.15s}
.bh-sport-row:hover{background:#FAFBFD}
.bh-sport-label{flex:2 1 0;font-size:0.9rem;font-weight:700}
.bh-sport-price{flex:1 1 0;text-align:center;font-size:0.95rem;font-weight:800;letter-spacing:-0.3px}
.bh-sport-phm{flex:1 1 0;text-align:center;font-size:0.82rem;color:#8896A5;font-weight:500}
.bh-global-note{background:linear-gradient(135deg,#EDE9FE 0%,#F5F3FF 100%);
  border:1px solid #C4B5FD;border-radius:12px;padding:13px 18px;margin-bottom:18px;
  font-size:0.82rem;color:#5B21B6;font-weight:500;font-family:'Sora',sans-serif;line-height:1.5}
@media(max-width:600px){
  .bh-card-header,.bh-col-header{padding:13px 14px 11px}
  .bh-item-row,.bh-sport-row{padding:11px 14px}
  .bh-sub-row{padding:6px 14px 6px 24px}
  .bh-item-label,.bh-sport-label{font-size:0.82rem}
  .bh-item-price,.bh-sport-price{font-size:0.88rem}
  .bh-sub-label{font-size:0.72rem}}
</style>"""


# ── HTML builders ─────────────────────────────────────────────────────────────

def _col_header(sport: bool = False) -> str:
    if sport:
        return (
            '<div class="bh-col-header">'
            '<div class="bh-col-h-label">Combo Thể Thao</div>'
            '<div class="bh-col-h-price">Giá cước</div>'
            '<div class="bh-col-h-price">PHM</div>'
            '</div>'
        )
    return (
        '<div class="bh-col-header">'
        '<div class="bh-col-h-label">Loại thiết bị</div>'
        '<div class="bh-col-h-price">NET</div>'
        '<div class="bh-col-h-price">Combo App</div>'
        '<div class="bh-col-h-price">Combo Box</div>'
        '</div>'
    )


def _item_block(item: dict, color: dict) -> str:
    t = color["text"]
    rows = [
        f'<div class="bh-item-row">'
        f'<div class="bh-item-label" style="color:{t};">{item["label"]}</div>'
        f'<div class="bh-item-price" style="color:{t};">{item["net"]}</div>'
        f'<div class="bh-item-price" style="color:{t};">{item["combo_app"]}</div>'
        f'<div class="bh-item-price" style="color:{t};">{item["combo_box"]}</div>'
        f'</div>'
    ]
    for phi in item.get("phi", []):
        rows.append(
            f'<div class="bh-sub-row">'
            f'<div class="bh-sub-label">↳ {phi["label"]}</div>'
            f'<div class="bh-sub-price">{phi["net"]}</div>'
            f'<div class="bh-sub-price">{phi["app"]}</div>'
            f'<div class="bh-sub-price">{phi["box"]}</div>'
            f'</div>'
        )
    return "".join(rows)


def _render_goi_card(goi: dict) -> str:
    c    = goi["color"]
    bw   = f"<div class='bh-card-bw'>{goi['bang_thong']}</div>" if goi["bang_thong"] else ""
    body = _col_header() + "".join(
        (f"<div class='bh-item-sep'></div>" if i else "") + _item_block(item, c)
        for i, item in enumerate(goi["items"])
    )
    return (
        f'<div class="bh-card" style="border-color:{c["border"]};">'
        f'  <div class="bh-card-header" style="background:{c["bg"]};">'
        f'    <div class="bh-card-title" style="color:{c["text"]};">{goi["icon"]}&nbsp; Gói {goi["goi"]}</div>'
        f'    {bw}'
        f'  </div>'
        f'  {body}'
        f'</div>'
    )


def _render_sport_card(goi: dict) -> str:
    c    = goi["color"]
    rows = "".join(
        f'<div class="bh-sport-row">'
        f'<div class="bh-sport-label" style="color:{c["text"]};">{item["combo"]}</div>'
        f'<div class="bh-sport-price" style="color:{c["text"]};">{item["gia_cuoc"]}</div>'
        f'<div class="bh-sport-phm">{item["phm"]}</div>'
        f'</div>'
        for item in goi["items"]
    )
    return (
        f'<div class="bh-card" style="border-color:{c["border"]};">'
        f'  <div class="bh-card-header" style="background:{c["bg"]};">'
        f'    <div class="bh-card-title" style="color:{c["text"]};">{goi["icon"]}&nbsp; {goi["ten"]} — Combo Thể Thao</div>'
        f'    <div class="bh-card-bw">Xem thể thao trực tiếp với voucher ưu đãi</div>'
        f'  </div>'
        f'  {_col_header(sport=True)}{rows}'
        f'</div>'
    )


# ── Accordion: nội dung khu vực ───────────────────────────────────────────────

def _render_area_content(area_key: str) -> None:
    if area_key == "Combo Thể Thao":
        st.markdown(
            f"<div class='bh-global-note'>🎫&nbsp; {_COMBO_SPORT['ghi_chu']}</div>",
            unsafe_allow_html=True,
        )
        for goi in _COMBO_SPORT["goi"]:
            st.markdown(_render_sport_card(goi), unsafe_allow_html=True)

    elif area_key in _DATA:
        for goi in _DATA[area_key]:
            if goi.get("ghi_chu"):
                st.markdown(
                    f"<div class='bh-global-note'>📷&nbsp; {goi['ghi_chu']}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown(_render_goi_card(goi), unsafe_allow_html=True)


# ── Entry point ───────────────────────────────────────────────────────────────

def render_ban_hang(data: list, keyword: str = "") -> None:
    st.markdown(_BH_CSS, unsafe_allow_html=True)
    render_section_header("💼", "Chương trình bán hàng")

    st.session_state.setdefault("bh_parent_open", False)
    st.session_state.setdefault("bh_open_areas", [])

    parent_open = st.session_state.bh_parent_open
    if st.button(
        f"{'▾' if parent_open else '▸'}  📍 CHỌN KHU VỰC",
        key="acc_parent_khu_vuc",
        type="primary" if parent_open else "secondary",
        use_container_width=True,
    ):
        st.session_state.bh_parent_open = not parent_open
        if parent_open:
            st.session_state.bh_open_areas = []
        st.rerun()

    if not parent_open:
        return

    open_set = set(st.session_state.bh_open_areas)
    st.markdown(
        "<p style='color:#8896A5;font-size:0.8rem;font-family:Sora,sans-serif;"
        "margin:8px 0 10px 12px;'>Chọn khu vực để xem giá cước tương ứng:</p>",
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown(
            "<div style='border-left:3px solid #F26F21;margin-left:8px;padding-left:12px;'>",
            unsafe_allow_html=True,
        )
        for area_key, area_label, area_desc in _AREA_CONFIG:
            is_open = area_key in open_set
            if st.button(
                f"{'▾' if is_open else '▸'}  {area_label}",
                key=f"acc_{area_key}",
                type="primary" if is_open else "secondary",
                use_container_width=True,
            ):
                open_set.discard(area_key) if is_open else open_set.add(area_key)
                st.session_state.bh_open_areas = list(open_set)
                st.rerun()

            if is_open:
                if area_desc:
                    st.markdown(
                        f"<p style='font-size:0.74rem;color:#8896A5;font-family:Sora,sans-serif;"
                        f"margin:6px 0 10px 4px;line-height:1.6;'>📍 {area_desc}</p>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                _render_area_content(area_key)
                st.markdown(
                    "<hr style='border:none;border-top:1px solid #EDF0F5;margin:4px 0 14px 0;'>",
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

    if open_set:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("✕  Thu gọn tất cả", key="acc_collapse_all", use_container_width=True):
            st.session_state.bh_open_areas = []
            st.rerun()
