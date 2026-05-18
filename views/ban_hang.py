"""
views/ban_hang.py
Render tab "Bán hàng": Card gói cước + filter khu vực.
Dùng div/flexbox thay table để tương thích hoàn toàn với st.markdown().
"""

import streamlit as st
from views.quy_trinh import render_section_header
from utils.highlight_text import highlight_text

# ──────────────────────────────────────────────────────────────
#  MÀU SẮC
# ──────────────────────────────────────────────────────────────

_COLORS = {
    "GIGA":     {"bg": "#EFF6FF", "border": "#005DA3", "text": "#005DA3", "sub_bg": "#E8F2FF"},
    "SKY":      {"bg": "#FFF5EF", "border": "#F26F21", "text": "#C04800", "sub_bg": "#FFF0E8"},
    "META":     {"bg": "#EFFAF4", "border": "#1A7A42", "text": "#1A7A42", "sub_bg": "#E8F6ED"},
    "GIGA_CAM": {"bg": "#FFFBEB", "border": "#D97706", "text": "#92400E", "sub_bg": "#FFF8E0"},
}

# ──────────────────────────────────────────────────────────────
#  DỮ LIỆU GIÁ CƯỚC
# ──────────────────────────────────────────────────────────────

_DATA = {
    "Phường": [
        {
            "goi": "GIGA", "icon": "🔵", "color": _COLORS["GIGA"],
            "bang_thong": "Upload – Download 300 Mbps",
            "items": [
                {
                    "label": "1 Modem",
                    "net": "195K", "combo_app": "200K", "combo_box": "210K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "300K", "app": "300K", "box": "500K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "300K", "app": "300K", "box": "400K"},
                    ],
                },
                {
                    "label": "1 Modem + 1 Mesh",
                    "net": "205K", "combo_app": "210K", "combo_box": "220K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "500K", "app": "500K", "box": "700K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "500K", "app": "500K", "box": "600K"},
                    ],
                },
                {
                    "label": "1 Modem + 2 Mesh",
                    "net": "225K", "combo_app": "230K", "combo_box": "240K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "700K", "app": "700K", "box": "900K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "700K", "app": "700K", "box": "800K"},
                    ],
                },
            ],
        },
        {
            "goi": "SKY", "icon": "🟡", "color": _COLORS["SKY"],
            "bang_thong": "Upload 300 Mbps – Download 1024 Mbps",
            "items": [
                {
                    "label": "1 Modem",
                    "net": "200K", "combo_app": "240K", "combo_box": "240K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "300K", "app": "300K", "box": "500K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "300K", "app": "300K", "box": "400K"},
                    ],
                },
                {
                    "label": "1 Modem + 1 Mesh",
                    "net": "210K", "combo_app": "250K", "combo_box": "250K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "500K", "app": "500K", "box": "700K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "500K", "app": "500K", "box": "600K"},
                    ],
                },
                {
                    "label": "1 Modem + 2 Mesh",
                    "net": "230K", "combo_app": "270K", "combo_box": "270K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "700K", "app": "700K", "box": "900K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "700K", "app": "700K", "box": "800K"},
                    ],
                },
            ],
        },
        {
            "goi": "META", "icon": "🟢", "color": _COLORS["META"],
            "bang_thong": "Upload – Download 1024 Mbps",
            "items": [
                {
                    "label": "1 Modem + 1 Mesh",
                    "net": "330K", "combo_app": "380K", "combo_box": "380K",
                    "phi": [
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "500K", "app": "500K", "box": "600K"},
                    ],
                },
                {
                    "label": "1 Modem + 2 Mesh",
                    "net": "350K", "combo_app": "400K", "combo_box": "400K",
                    "phi": [
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "700K", "app": "700K", "box": "800K"},
                    ],
                },
            ],
        },
    ],
    "Xã, Vùng ven": [
        {
            "goi": "GIGA", "icon": "🔵", "color": _COLORS["GIGA"],
            "bang_thong": "Upload – Download 300 Mbps",
            "items": [
                {
                    "label": "1 Modem",
                    "net": "195K", "combo_app": "200K", "combo_box": "210K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "300K", "app": "300K", "box": "400K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "300K", "app": "300K", "box": "300K"},
                    ],
                },
                {
                    "label": "1 Modem + 1 Mesh",
                    "net": "205K", "combo_app": "210K", "combo_box": "220K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "500K", "app": "500K", "box": "600K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "500K", "app": "500K", "box": "500K"},
                    ],
                },
                {
                    "label": "1 Modem + 2 Mesh",
                    "net": "225K", "combo_app": "230K", "combo_box": "240K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "700K", "app": "700K", "box": "800K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "700K", "app": "700K", "box": "700K"},
                    ],
                },
            ],
        },
        {
            "goi": "SKY", "icon": "🟡", "color": _COLORS["SKY"],
            "bang_thong": "Upload 300 Mbps – Download 1024 Mbps",
            "items": [
                {
                    "label": "1 Modem",
                    "net": "200K", "combo_app": "240K", "combo_box": "240K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "300K", "app": "300K", "box": "400K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "300K", "app": "300K", "box": "300K"},
                    ],
                },
                {
                    "label": "1 Modem + 1 Mesh",
                    "net": "210K", "combo_app": "250K", "combo_box": "250K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "500K", "app": "500K", "box": "600K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "500K", "app": "500K", "box": "500K"},
                    ],
                },
                {
                    "label": "1 Modem + 2 Mesh",
                    "net": "230K", "combo_app": "270K", "combo_box": "270K",
                    "phi": [
                        {"label": "Phí hoà mạng trả sau",        "net": "700K", "app": "700K", "box": "800K"},
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "700K", "app": "700K", "box": "700K"},
                    ],
                },
            ],
        },
        {
            "goi": "META", "icon": "🟢", "color": _COLORS["META"],
            "bang_thong": "Upload – Download 1024 Mbps",
            "items": [
                {
                    "label": "1 Modem + 1 Mesh",
                    "net": "330K", "combo_app": "380K", "combo_box": "380K",
                    "phi": [
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "500K", "app": "500K", "box": "500K"},
                    ],
                },
                {
                    "label": "1 Modem + 2 Mesh",
                    "net": "350K", "combo_app": "400K", "combo_box": "400K",
                    "phi": [
                        {"label": "Phí hoà mạng trả trước ≥ 3T", "net": "700K", "app": "700K", "box": "700K"},
                    ],
                },
            ],
        },
    ],
    "Toàn Thành Phố": [
        {
            "goi": "GIGA + CAM", "icon": "📷", "color": _COLORS["GIGA_CAM"],
            "bang_thong": "Ưu đãi Camera — cước tăng 10K sau 12 tháng",
            "ghi_chu": "Sử dụng Camera IQ3S hoặc Play 4",
            "items": [
                {
                    "label": "Giga 1 Modem + CAM",
                    "net": "200K", "combo_app": "220K", "combo_box": "230K",
                    "phi": [
                        {"label": "Phí hoà mạng", "net": "400K", "app": "400K", "box": "800K"},
                    ],
                },
            ],
        },
    ],
    "Xã Đặc Biệt": [
        {
            "goi": "GIGA + CAM", "icon": "📷", "color": _COLORS["GIGA_CAM"],
            "bang_thong": "Ưu đãi Camera — cước tăng 10K sau 12 tháng",
            "ghi_chu": "Sử dụng Camera IQ3S hoặc Play 4",
            "items": [
                {
                    "label": "Giga 1 Modem Tặng CAM",
                    "net": "195K", "combo_app": "200K", "combo_box": "210K",
                    "phi": [
                        {"label": "Phí hoà mạng", "net": "300K", "app": "300K", "box": "400K"},
                    ],
                },
            ],
        },
    ],
}

_COMBO_SPORT = {
    "ghi_chu": "Gói Combo Thể Thao có voucher giảm 30K trong vòng 12 tháng, sau đó về lại giá gốc.",
    "goi": [
        {
            "ten": "SKY", "icon": "🟡", "color": _COLORS["SKY"],
            "items": [
                {"combo": "SKY V.VIP",    "gia_cuoc": "239K", "phm": "300K"},
                {"combo": "SKY V.VIP F1", "gia_cuoc": "249K", "phm": "500K"},
                {"combo": "SKY V.VIP F2", "gia_cuoc": "269K", "phm": "700K"},
            ],
        },
        {
            "ten": "META", "icon": "🟢", "color": _COLORS["META"],
            "items": [
                {"combo": "META V.VIP",    "gia_cuoc": "339K", "phm": "300K"},
                {"combo": "META V.VIP F1", "gia_cuoc": "349K", "phm": "500K"},
                {"combo": "META V.VIP F2", "gia_cuoc": "369K", "phm": "700K"},
            ],
        },
    ],
}

# ──────────────────────────────────────────────────────────────
#  CSS
# ──────────────────────────────────────────────────────────────

_BH_CSS = """<style>
/* ══ BAN HANG CARD LAYOUT ══ */
.bh-card {
    background:#fff;
    border-radius:16px;
    margin-bottom:18px;
    overflow:hidden;
    box-shadow:0 2px 14px rgba(0,0,0,0.06);
    border:1.5px solid #EDF0F5;
    font-family:'Sora',sans-serif;
}
.bh-card-header {
    padding:16px 20px 13px;
    border-bottom:1px solid rgba(0,0,0,0.06);
}
.bh-card-title {
    font-size:1.02rem;
    font-weight:800;
    letter-spacing:-0.3px;
    margin-bottom:2px;
}
.bh-card-bw {
    font-size:0.74rem;
    color:#8896A5;
    font-weight:400;
}
.bh-note-badge {
    display:inline-block;
    margin-top:9px;
    background:rgba(217,119,6,0.09);
    color:#92400E;
    font-size:0.74rem;
    font-weight:600;
    padding:4px 11px;
    border-radius:8px;
    border:1px solid rgba(217,119,6,0.22);
    line-height:1.45;
}

/* ── Column header row ── */
.bh-col-header {
    display:flex;
    align-items:center;
    padding:8px 20px;
    background:#F7F8FA;
    border-bottom:1px solid #EDF0F5;
    gap:0;
}
.bh-col-h-label {
    flex:2 1 0;
    font-size:0.68rem;
    font-weight:700;
    color:#A0AEBB;
    text-transform:uppercase;
    letter-spacing:0.6px;
}
.bh-col-h-price {
    flex:1 1 0;
    font-size:0.68rem;
    font-weight:700;
    color:#A0AEBB;
    text-transform:uppercase;
    letter-spacing:0.6px;
    text-align:center;
}

/* ── Item row (giá cước chính) ── */
.bh-item-row {
    display:flex;
    align-items:center;
    padding:12px 20px;
    border-bottom:1px solid #F2F5F8;
    gap:0;
    transition:background 0.15s;
}
.bh-item-row:hover { background:#FAFBFD; }
.bh-item-label {
    flex:2 1 0;
    font-size:0.9rem;
    font-weight:700;
    line-height:1.3;
}
.bh-item-price {
    flex:1 1 0;
    text-align:center;
    font-size:0.95rem;
    font-weight:800;
    letter-spacing:-0.3px;
}

/* ── Sub row (phí hòa mạng) ── */
.bh-sub-row {
    display:flex;
    align-items:center;
    padding:7px 20px 7px 32px;
    border-bottom:1px solid #F2F5F8;
    background:#FAFBFD;
    gap:0;
}
.bh-sub-row:last-child { border-bottom:2px solid #EDF0F5; }
.bh-sub-label {
    flex:2 1 0;
    font-size:0.76rem;
    color:#8896A5;
    font-weight:400;
    line-height:1.3;
}
.bh-sub-price {
    flex:1 1 0;
    text-align:center;
    font-size:0.8rem;
    color:#8896A5;
    font-weight:500;
}

/* ── Separator between items ── */
.bh-item-sep {
    height:1px;
    background:linear-gradient(90deg,transparent,#E8EDF5 20%,#E8EDF5 80%,transparent);
    margin:0 20px;
}

/* ── Combo Sport card ── */
.bh-sport-row {
    display:flex;
    align-items:center;
    padding:12px 20px;
    border-bottom:1px solid #F2F5F8;
    gap:0;
    transition:background 0.15s;
}
.bh-sport-row:hover { background:#FAFBFD; }
.bh-sport-label {
    flex:2 1 0;
    font-size:0.9rem;
    font-weight:700;
}
.bh-sport-price {
    flex:1 1 0;
    text-align:center;
    font-size:0.95rem;
    font-weight:800;
    letter-spacing:-0.3px;
}
.bh-sport-phm {
    flex:1 1 0;
    text-align:center;
    font-size:0.82rem;
    color:#8896A5;
    font-weight:500;
}

/* ── Global note ── */
.bh-global-note {
    background:linear-gradient(135deg,#EDE9FE 0%,#F5F3FF 100%);
    border:1px solid #C4B5FD;
    border-radius:12px;
    padding:13px 18px;
    margin-bottom:18px;
    font-size:0.82rem;
    color:#5B21B6;
    font-weight:500;
    font-family:'Sora',sans-serif;
    line-height:1.5;
}

/* ── Quy trinh section divider ── */
.bh-section-label {
    font-size:0.75rem;
    font-weight:700;
    color:#B0BBC8;
    text-transform:uppercase;
    letter-spacing:1px;
    margin:22px 0 12px;
    font-family:'Sora',sans-serif;
    display:flex;
    align-items:center;
    gap:8px;
}
.bh-section-label::after {
    content:'';
    flex:1;
    height:1px;
    background:#EDF0F5;
}

/* ── Mobile tweaks ── */
@media (max-width:600px) {
    .bh-card-header { padding:13px 14px 11px; }
    .bh-col-header  { padding:8px 14px; }
    .bh-item-row    { padding:11px 14px; }
    .bh-sub-row     { padding:6px 14px 6px 24px; }
    .bh-sport-row   { padding:11px 14px; }
    .bh-item-label, .bh-sport-label { font-size:0.82rem; }
    .bh-item-price, .bh-sport-price { font-size:0.88rem; }
    .bh-sub-label   { font-size:0.72rem; }
}
</style>"""

# ──────────────────────────────────────────────────────────────
#  HTML BUILDERS — dùng div/flex, KHÔNG dùng table
# ──────────────────────────────────────────────────────────────

def _col_header(col3=True) -> str:
    """Hàng tiêu đề cột."""
    if col3:
        return """
<div class="bh-col-header">
  <div class="bh-col-h-label">Loại thiết bị</div>
  <div class="bh-col-h-price">NET</div>
  <div class="bh-col-h-price">Combo App</div>
  <div class="bh-col-h-price">Combo Box</div>
</div>"""
    return """
<div class="bh-col-header">
  <div class="bh-col-h-label">Combo Thể Thao</div>
  <div class="bh-col-h-price">Giá cước</div>
  <div class="bh-col-h-price">PHM</div>
</div>"""


def _item_block(item: dict, color: dict) -> str:
    """Hàng giá chính + các hàng phí hòa mạng."""
    html = f"""
<div class="bh-item-row">
  <div class="bh-item-label" style="color:{color['text']};">{item['label']}</div>
  <div class="bh-item-price" style="color:{color['text']};">{item['net']}</div>
  <div class="bh-item-price" style="color:{color['text']};">{item['combo_app']}</div>
  <div class="bh-item-price" style="color:{color['text']};">{item['combo_box']}</div>
</div>"""
    for phi in item.get("phi", []):
        html += f"""
<div class="bh-sub-row">
  <div class="bh-sub-label">↳ {phi['label']}</div>
  <div class="bh-sub-price">{phi['net']}</div>
  <div class="bh-sub-price">{phi['app']}</div>
  <div class="bh-sub-price">{phi['box']}</div>
</div>"""
    return html


def _render_goi_card(goi: dict) -> str:
    c = goi["color"]
    ghi_chu_html = (
        f"<div class='bh-note-badge'>⚠️ {goi['ghi_chu']}</div>"
        if goi.get("ghi_chu") else ""
    )
    body = _col_header(col3=True)
    for i, item in enumerate(goi["items"]):
        if i > 0:
            body += "<div class='bh-item-sep'></div>"
        body += _item_block(item, c)

    return f"""
<div class="bh-card" style="border-color:{c['border']};">
  <div class="bh-card-header" style="background:{c['bg']};">
    <div class="bh-card-title" style="color:{c['text']};">{goi['icon']}&nbsp; Gói {goi['goi']}</div>
    <div class="bh-card-bw">{goi['bang_thong']}</div>
    {ghi_chu_html}
  </div>
  {body}
</div>"""


def _render_sport_card(goi: dict) -> str:
    c = goi["color"]
    body = _col_header(col3=False)
    for item in goi["items"]:
        body += f"""
<div class="bh-sport-row">
  <div class="bh-sport-label" style="color:{c['text']};">{item['combo']}</div>
  <div class="bh-sport-price" style="color:{c['text']};">{item['gia_cuoc']}</div>
  <div class="bh-sport-phm">{item['phm']}</div>
</div>"""

    return f"""
<div class="bh-card" style="border-color:{c['border']};">
  <div class="bh-card-header" style="background:{c['bg']};">
    <div class="bh-card-title" style="color:{c['text']};">{goi['icon']}&nbsp; {goi['ten']} — Combo Thể Thao</div>
    <div class="bh-card-bw">Xem thể thao trực tiếp với voucher ưu đãi</div>
  </div>
  {body}
</div>"""


# ──────────────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────────────

def render_ban_hang(data: list, keyword: str = "") -> None:
    """Render toàn bộ tab Bán hàng."""
    st.markdown(_BH_CSS, unsafe_allow_html=True)
    render_section_header("🛒", "Bán hàng — Chương trình giá cước")

    # ── Filter khu vực ──
    st.session_state.setdefault("bh_area", "Phường")

    area_labels = {
        "Phường":         "🏙️ Phường",
        "Xã, Vùng ven":  "🌿 Xã, Vùng ven",
        "Toàn Thành Phố": "🏆 Toàn TP",
        "Xã Đặc Biệt":   "⭐ Xã Đặc Biệt",
        "Combo Thể Thao": "⚽ Thể Thao",
    }

    cols = st.columns(len(area_labels))
    for col, (area_key, area_label) in zip(cols, area_labels.items()):
        with col:
            is_active = st.session_state.bh_area == area_key
            if st.button(
                area_label, key=f"bh_area_{area_key}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                st.session_state.bh_area = area_key
                st.rerun()

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    active = st.session_state.bh_area

    # ── Render cards ──
    if active == "Combo Thể Thao":
        st.markdown(
            f"<div class='bh-global-note'>🎫&nbsp; {_COMBO_SPORT['ghi_chu']}</div>",
            unsafe_allow_html=True,
        )
        for goi in _COMBO_SPORT["goi"]:
            st.markdown(_render_sport_card(goi), unsafe_allow_html=True)

    elif active in _DATA:
        for goi in _DATA[active]:
            st.markdown(_render_goi_card(goi), unsafe_allow_html=True)

    # ── Quy trình từ Excel (nếu có) ──
    rows = [r for r in data if r["folder"] == "Bán hàng"]
    if not rows:
        return
    kw_lower = keyword.strip().lower()
    filtered = [
        r for r in rows
        if not kw_lower
        or kw_lower in r["ten"].lower()
        or kw_lower in r["buoc"].lower()
    ]
    if not filtered:
        return

    st.markdown(
        "<div class='bh-section-label'>Quy trình &amp; hướng dẫn</div>",
        unsafe_allow_html=True,
    )
    auto_expand = bool(kw_lower)
    for row in filtered:
        if not row["ten"]:
            continue
        label = (
            f"🔎  {row['ten']}"
            if (kw_lower and kw_lower in row["ten"].lower())
            else f"🛠  {row['ten']}"
        )
        with st.expander(label, expanded=auto_expand):
            st.markdown(highlight_text(row["buoc"], keyword), unsafe_allow_html=True)