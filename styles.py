"""
styles.py
Chứa toàn bộ CSS của ứng dụng và hàm inject vào Streamlit.
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    color: #1A1D23;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── Nền tổng thể ── */
.stApp {
    background: #F7F8FA;
    min-height: 100vh;
}

/* ── Container ── */
.block-container {
    padding: 0 0 4rem 0 !important;
    max-width: 100% !important;
}

/* ════════════════ GLASSMORPHISM NAVIGATION BAR ══════════════════ */
.fpt-nav {
    position: sticky;
    top: 0;
    z-index: 999;
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(242, 111, 33, 0.12);
    padding: 0 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    box-shadow: 0 1px 24px rgba(0, 0, 0, 0.06);
}

.fpt-nav-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.fpt-nav-logo {
    height: 40px;
    width: auto;
    max-width: 140px;
    flex-shrink: 0;
    display: block;
    object-fit: contain;
}

.fpt-nav-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1A1D23;
    letter-spacing: -0.2px;
    line-height: 1;
}

.fpt-nav-subtitle {
    font-size: 0.72rem;
    color: #8896A5;
    font-weight: 400;
    margin-top: 2px;
}


/* ══════════════ HERO / SEARCH SECTION ══════════════ */
.fpt-hero {
    background: linear-gradient(135deg, #fff 0%, #FFF5EF 100%);
    border-bottom: 1px solid #F0E8E1;
    padding: 2.8rem 2.5rem 2.2rem;
    text-align: center;
}

.fpt-hero-eyebrow {
    display: inline-block;
    background: rgba(242, 111, 33, 0.08);
    color: #C8530D;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    border: 1px solid rgba(242, 111, 33, 0.15);
    margin-bottom: 1rem;
}

.fpt-hero-title {
    font-size: clamp(1.6rem, 4vw, 2.2rem);
    font-weight: 800;
    color: #0F1217;
    letter-spacing: -0.8px;
    line-height: 1.2;
    margin-bottom: 0.6rem;
}

.fpt-hero-title span {
    background: linear-gradient(135deg, #F26F21, #C8530D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.fpt-hero-desc {
    font-size: 0.9rem;
    color: #7A8899;
    font-weight: 400;
    max-width: 500px;
    margin: 0 auto 1.8rem;
    line-height: 1.6;
}

/* ── Search box ── */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1.5px solid #E4E9F0 !important;
    border-radius: 14px !important;
    color: #1A1D23 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 1.2rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05), 0 0 0 0px rgba(242,111,33,0) !important;
    transition: all 0.22s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #F26F21 !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05), 0 0 0 4px rgba(242,111,33,0.10) !important;
}
.stTextInput > div > div > input::placeholder { color: #B0BBC8 !important; font-weight: 400 !important; }

/* ══════════════ NAV TABS (folder buttons) ═════════════ */
.fpt-tabs-wrap {
    background: #fff;
    border-bottom: 1px solid #EDF0F5;
    padding: 0 2.5rem;
    display: flex;
    gap: 4px;
    align-items: flex-end;
}

.stButton > button {
    font-family: 'Sora', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
    min-height: 42px !important;
    letter-spacing: -0.1px !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #F26F21 0%, #D95F10 100%) !important;
    border: none !important;
    color: #ffffff !important;
    box-shadow: 0 4px 16px rgba(242, 111, 33, 0.35) !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 22px rgba(242, 111, 33, 0.45) !important;
    transform: translateY(-1px) !important;
}

.stButton > button[kind="secondary"] {
    background: #F7F8FA !important;
    border: 1.5px solid #E4E9F0 !important;
    color: #5A6476 !important;
}

.stButton > button[kind="secondary"]:hover {
    background: #FFF5EF !important;
    border-color: rgba(242,111,33,0.35) !important;
    color: #C8530D !important;
}

/* ═════════════ CONTENT AREA ════════════ */
.fpt-content {
    padding: 1.8rem 2.5rem;
    max-width: 960px;
    margin: 0 auto;
}

/* ── Section header ── */
.fpt-section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.4rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #EDF0F5;
}

.fpt-section-icon {
    width: 34px;
    height: 34px;
    background: rgba(242, 111, 33, 0.08);
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}

.fpt-section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #0F1217;
}

.fpt-section-count {
    font-size: 0.75rem;
    color: #8896A5;
    font-weight: 400;
    background: #F0F2F5;
    padding: 2px 8px;
    border-radius: 8px;
    margin-left: auto;
}

/* ═════════════ EXPANDER — PREMIUM CARDS ═════════════ */
.stExpander {
    background: #ffffff !important;
    border: 1.5px solid #EDF0F5 !important;
    border-radius: 14px !important;
    margin-bottom: 10px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 8px rgba(0,0,0,0.04) !important;
    transition: all 0.2s ease !important;
}

.stExpander:hover {
    border-color: rgba(242, 111, 33, 0.25) !important;
    box-shadow: 0 4px 20px rgba(242, 111, 33, 0.08) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stExpander"] summary {
    color: #1A1D23 !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 16px 20px !important;
    min-height: 52px !important;
    background: #ffffff !important;
    font-family: 'Sora', sans-serif !important;
    letter-spacing: -0.1px !important;
}

[data-testid="stExpander"] summary:hover { color: #F26F21 !important; }

[data-testid="stExpanderDetails"] {
    background: #FAFBFD !important;
    padding: 16px 22px !important;
    border-top: 1px solid #EDF0F5 !important;
    color: #3A4454 !important;
    font-size: 0.88rem !important;
    line-height: 1.85 !important;
    font-family: 'Sora', sans-serif !important;
}

/* ══════════ BADGES ═══════════ */
.tag-ok {
    display: inline-block;
    background: #E8FAF0; color: #1A7A42;
    font-weight: 700; font-size: 0.78rem;
    padding: 2px 9px; border-radius: 6px;
    border: 1px solid #A8DFC0;
}
.tag-err {
    display: inline-block;
    background: #FDECEA; color: #C0392B;
    font-weight: 700; font-size: 0.78rem;
    padding: 2px 9px; border-radius: 6px;
    border: 1px solid #F5C6C2;
}
.tag-note {
    display: inline-block;
    background: #F3EEFF; color: #6C3FC7;
    font-weight: 700; font-size: 0.78rem;
    padding: 2px 9px; border-radius: 6px;
    border: 1px solid #D4B8F5;
}

/* ═════════ EMPTY STATE ═════════ */
.empty-state {
    text-align: center;
    padding: 4rem 1rem;
    color: #8896A5;
    font-size: 0.92rem;
    background: #ffffff;
    border-radius: 16px;
    border: 1.5px dashed #DDE3ED;
}

/* ══════════════ TÀI LIỆU CARDS ═══════════════ */
.doc-card {
    background: #fff;
    border: 1.5px solid #EDF0F5;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 16px;
    text-decoration: none;
    transition: all 0.2s ease;
    box-shadow: 0 1px 8px rgba(0,0,0,0.04);
}

.doc-card:hover {
    border-color: rgba(242,111,33,0.3);
    box-shadow: 0 6px 24px rgba(242,111,33,0.10);
    transform: translateY(-1px);
}

.doc-card-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}

.doc-card-title {
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 3px;
    line-height: 1.3;
}

.doc-card-desc {
    font-size: 0.8rem;
    color: #7A8899;
    font-weight: 400;
}

.doc-card-arrow {
    margin-left: auto;
    font-size: 1.1rem;
    font-weight: 700;
    flex-shrink: 0;
}

/* ── Doc placeholder ── */
.doc-placeholder {
    background: #fff;
    border: 2px dashed #D8DEE9;
    border-radius: 16px;
    padding: 3rem 1rem;
    text-align: center;
    color: #8896A5;
    font-size: 0.9rem;
}

/* ═══════════════════ BẢNG EXCEL INLINE ════════════════════ */
.xl-wrap {
    overflow-x: auto;
    border-radius: 12px;
    margin-top: 12px;
    border: 1px solid #E4E9F0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.xl-wrap table {
    border-collapse: collapse;
    width: 100%;
    font-size: 0.82rem;
    font-family: 'Sora', sans-serif;
}
.xl-wrap tbody td {
    background: #ffffff;
    color: #2D3748;
    padding: 8px 14px;
    border-bottom: 1px solid #F0F3F8;
    border-right: 1px solid #F0F3F8;
    vertical-align: middle;
    line-height: 1.5;
}
.xl-wrap tbody td:last-child { border-right: none; }
.xl-wrap tbody tr:last-child td { border-bottom: none; }
.xl-wrap tbody tr:nth-child(even) td { background: #FAFBFD; }
.xl-wrap tbody tr:hover td { background: #FFF5EF !important; color: #C04800 !important; }

/* ── Bảng giá cước ── */
.bg-excel-wrap {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border-radius: 14px;
    border: 1px solid #E4E9F0;
    box-shadow: 0 2px 16px rgba(0, 93, 163, 0.07);
    margin-top: 4px;
}
.bg-excel {
    border-collapse: collapse;
    width: 100%;
    min-width: 680px;
    font-size: 0.8rem;
    font-family: 'Sora', sans-serif;
}
.bg-excel td {
    border: 1px solid #E4E9F0;
    padding: 8px 12px;
    text-align: center;
    vertical-align: middle;
    white-space: normal;
    word-break: break-word;
    max-width: 220px;
}
.bg-excel tbody tr:hover td { filter: brightness(0.95); transition: filter 0.12s; }

/* ══════════ DOWNLOAD BUTTON ═══════════ */
.stDownloadButton > button {
    background: #F7F8FA !important;
    border: 1.5px solid #E4E9F0 !important;
    color: #5A6476 !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.18s !important;
}
.stDownloadButton > button:hover {
    background: #FFF5EF !important;
    border-color: rgba(242,111,33,0.35) !important;
    color: #C8530D !important;
}

/* Padding cho content area nằm trong block-container */
.fpt-pad {
    padding: 1.8rem 2.5rem;
}

@media (max-width: 768px) {
    .fpt-nav { padding: 0 1.2rem; }
    .fpt-hero { padding: 2rem 1.2rem 1.6rem; }
    .fpt-pad { padding: 1.2rem 1rem; }
    .fpt-tabs-wrap { padding: 0 1rem; overflow-x: auto; }
}
</style>
"""


def inject_css():
    """Inject toàn bộ CSS vào trang Streamlit."""
    st.markdown(_CSS, unsafe_allow_html=True)
