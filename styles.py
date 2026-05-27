"""
styles.py
Toàn bộ CSS của ứng dụng — hỗ trợ Light Mode & Dark Mode.

Hệ thống màu sắc:
  Light Mode: Nền trắng tinh khiết, chữ xanh đậm (#0F1827), cam FPT chủ đạo.
  Dark Mode : Nền graphite (#0D1117), chữ trắng ngà (#E8ECF0), cam FPT vẫn nổi bật.

Tất cả màu quản lý qua CSS Custom Properties trên :root[data-theme].
Toggle bằng JavaScript — lưu preference vào localStorage.
"""

import streamlit as st

_CSS = """
<style>

/* ══════════════════════════════════════════════════════════════
   0. GOOGLE FONTS
══════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

/* ══════════════════════════════════════════════════════════════
   1. DESIGN TOKENS — LIGHT MODE (mặc định)
   Cam FPT: #F26F21  |  Cam đậm: #C8530D  |  Cam nhạt: #FFF5EF
   Xanh dương: #005DA3 (accent phụ cho badges info)
   Nền: #F4F6F9  |  Surface: #FFFFFF  |  Chữ: #0F1827
   Contrast ratio chữ/nền: ≥ 7:1 (WCAG AAA)
══════════════════════════════════════════════════════════════ */
:root {
  /* — Brand — */
  --fpt-orange:        #F26F21;
  --fpt-orange-dark:   #C8530D;
  --fpt-orange-deep:   #A34208;
  --fpt-orange-glow:   rgba(242, 111, 33, 0.15);
  --fpt-orange-tint:   #FFF5EF;
  --fpt-orange-tint2:  #FDEADE;
  --fpt-blue:          #005DA3;
  --fpt-blue-tint:     #EFF6FF;
  --fpt-green:         #1A7A42;
  --fpt-green-tint:    #EFFAF4;

  /* — Background — */
  --bg-page:           #F4F6F9;
  --bg-surface:        #FFFFFF;
  --bg-surface-alt:    #FAFBFD;
  --bg-overlay:        rgba(255,255,255,0.88);

  /* — Text — */
  --text-primary:      #0F1827;
  --text-secondary:    #3A4558;
  --text-muted:        #6B7A8D;
  --text-hint:         #9BAABB;
  --text-inverse:      #FFFFFF;

  /* — Border — */
  --border-default:    #E2E8F2;
  --border-subtle:     #EDF0F5;
  --border-focus:      rgba(242,111,33,0.45);

  /* — Nav — */
  --nav-bg:            rgba(255,255,255,0.88);
  --nav-border:        rgba(242,111,33,0.12);
  --nav-shadow:        0 1px 24px rgba(0,0,0,0.06);

  /* — Hero — */
  --hero-bg:           linear-gradient(145deg,#fff 0%,#FFF5EF 55%,#FFE8D6 100%);
  --hero-border:       #EDD8C8;

  /* — Card / Expander — */
  --card-bg:           #FFFFFF;
  --card-border:       #E2E8F2;
  --card-shadow:       0 1px 8px rgba(0,0,0,0.05);
  --card-hover-shadow: 0 6px 24px rgba(242,111,33,0.10);
  --card-hover-border: rgba(242,111,33,0.28);

  /* — Table — */
  --tbl-head-bg:       #EEF2F8;
  --tbl-head-text:     #1A2A3A;
  --tbl-head-border:   #CDD5E0;
  --tbl-row-alt:       #F8FAFD;
  --tbl-row-hover-bg:  #FFF5EF;
  --tbl-row-hover-text:#A34208;
  --tbl-cell-border:   #EDF1F8;
  --tbl-sticky-head:   #E3EAF5;
  --tbl-sticky-first:  #F4F7FC;

  /* — Button secondary — */
  --btn-sec-bg:        #F4F6F9;
  --btn-sec-border:    #D8E0EC;
  --btn-sec-text:      #3A4558;
  --btn-sec-hover-bg:  #FFF5EF;
  --btn-sec-hover-bd:  rgba(242,111,33,0.35);
  --btn-sec-hover-txt: #C8530D;

  /* — Download button — */
  --dl-bg:             #F4F6F9;
  --dl-border:         #D8E0EC;
  --dl-text:           #3A4558;
  --dl-hover-bg:       #FFF5EF;
  --dl-hover-border:   rgba(242,111,33,0.35);
  --dl-hover-text:     #C8530D;

  /* — Empty state — */
  --empty-bg:          #FFFFFF;
  --empty-border:      #D8E0EC;
  --empty-text:        #6B7A8D;

  /* — Expander detail — */
  --exp-detail-bg:     #FAFBFD;
  --exp-detail-text:   #3A4558;
  --exp-detail-border: #EDF0F5;
  --exp-head-bg:       #FFFFFF;
  --exp-head-text:     #0F1827;

  /* — Section count badge — */
  --badge-bg:          #EEF2F8;
  --badge-text:        #6B7A8D;

  /* — Tags — */
  --tag-ok-bg:    #E8FAF0; --tag-ok-text:    #1A7A42; --tag-ok-bd:    #A8DFC0;
  --tag-err-bg:   #FDECEA; --tag-err-text:   #C0392B; --tag-err-bd:   #F5C6C2;
  --tag-note-bg:  #F3EEFF; --tag-note-text:  #6C3FC7; --tag-note-bd:  #D4B8F5;

  /* — Toggle button — */
  --toggle-bg:         #EEF2F8;
  --toggle-icon:       #6B7A8D;
  --toggle-hover-bg:   #FFF5EF;
  --toggle-hover-icon: #F26F21;

  /* — Scrollbar — */
  --scrollbar-track:   #F4F6F9;
  --scrollbar-thumb:   #CDD5E0;
  --scrollbar-hover:   #F26F21;
}

/* ══════════════════════════════════════════════════════════════
   2. DESIGN TOKENS — DARK MODE
   Nền graphite #0D1117 (GitHub dark — dễ nhìn, chuyên nghiệp)
   Surface  #161B22  |  Surface-alt #1C2330
   Chữ chính #E8ECF0 (không trắng 100% — bớt mỏi mắt)
   Cam FPT vẫn giữ #F26F21 — nổi bật trên nền tối
   Contrast ratio chữ/nền: ≥ 7:1 (WCAG AAA)
══════════════════════════════════════════════════════════════ */
[data-fpt-theme="dark"] {
  /* — Brand vẫn giữ cam gốc, chỉ điều chỉnh tint — */
  --fpt-orange:        #F26F21;
  --fpt-orange-dark:   #FF8C42;
  --fpt-orange-deep:   #FFB07A;
  --fpt-orange-glow:   rgba(242,111,33,0.22);
  --fpt-orange-tint:   #1E1208;
  --fpt-orange-tint2:  #2A180A;
  --fpt-blue:          #4DA3E8;
  --fpt-blue-tint:     #0A1929;
  --fpt-green:         #3DD68C;
  --fpt-green-tint:    #0A1F14;

  /* — Background — */
  --bg-page:           #0D1117;
  --bg-surface:        #161B22;
  --bg-surface-alt:    #1C2330;
  --bg-overlay:        rgba(22,27,34,0.92);

  /* — Text — */
  --text-primary:      #E8ECF0;
  --text-secondary:    #B0BCCC;
  --text-muted:        #7C8FA3;
  --text-hint:         #4E5F72;
  --text-inverse:      #0D1117;

  /* — Border — */
  --border-default:    #2A3444;
  --border-subtle:     #1F2A38;
  --border-focus:      rgba(242,111,33,0.55);

  /* — Nav — */
  --nav-bg:            rgba(13,17,23,0.92);
  --nav-border:        rgba(242,111,33,0.18);
  --nav-shadow:        0 1px 24px rgba(0,0,0,0.4);

  /* — Hero — */
  --hero-bg:           linear-gradient(145deg,#0D1117 0%,#1A110A 55%,#200E05 100%);
  --hero-border:       #2A1A0F;

  /* — Card / Expander — */
  --card-bg:           #161B22;
  --card-border:       #2A3444;
  --card-shadow:       0 1px 8px rgba(0,0,0,0.3);
  --card-hover-shadow: 0 6px 24px rgba(242,111,33,0.14);
  --card-hover-border: rgba(242,111,33,0.35);

  /* — Table — */
  --tbl-head-bg:       #1C2330;
  --tbl-head-text:     #C4CDD8;
  --tbl-head-border:   #2A3444;
  --tbl-row-alt:       #1A1F2B;
  --tbl-row-hover-bg:  #2A1A0A;
  --tbl-row-hover-text:#FF8C42;
  --tbl-cell-border:   #1F2A38;
  --tbl-sticky-head:   #1F2A38;
  --tbl-sticky-first:  #1C2330;

  /* — Button secondary — */
  --btn-sec-bg:        #1C2330;
  --btn-sec-border:    #2A3444;
  --btn-sec-text:      #B0BCCC;
  --btn-sec-hover-bg:  #2A1A0A;
  --btn-sec-hover-bd:  rgba(242,111,33,0.45);
  --btn-sec-hover-txt: #FF8C42;

  /* — Download button — */
  --dl-bg:             #1C2330;
  --dl-border:         #2A3444;
  --dl-text:           #B0BCCC;
  --dl-hover-bg:       #2A1A0A;
  --dl-hover-border:   rgba(242,111,33,0.45);
  --dl-hover-text:     #FF8C42;

  /* — Empty state — */
  --empty-bg:          #161B22;
  --empty-border:      #2A3444;
  --empty-text:        #7C8FA3;

  /* — Expander detail — */
  --exp-detail-bg:     #1A1F2B;
  --exp-detail-text:   #B0BCCC;
  --exp-detail-border: #2A3444;
  --exp-head-bg:       #161B22;
  --exp-head-text:     #E8ECF0;

  /* — Section count badge — */
  --badge-bg:          #1C2330;
  --badge-text:        #7C8FA3;

  /* — Tags — */
  --tag-ok-bg:   #0A1F14; --tag-ok-text:   #3DD68C; --tag-ok-bd:   #1A4A2E;
  --tag-err-bg:  #1F0808; --tag-err-text:  #F07070; --tag-err-bd:  #4A1818;
  --tag-note-bg: #120A2A; --tag-note-text: #B09EF5; --tag-note-bd: #2E1F5A;

  /* — Toggle button — */
  --toggle-bg:         #1C2330;
  --toggle-icon:       #7C8FA3;
  --toggle-hover-bg:   #2A1A0A;
  --toggle-hover-icon: #F26F21;

  /* — Scrollbar — */
  --scrollbar-track:   #0D1117;
  --scrollbar-thumb:   #2A3444;
  --scrollbar-hover:   #F26F21;
}

/* ══════════════════════════════════════════════════════════════
   3. BASE RESET & TYPOGRAPHY
══════════════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
  font-family: 'Sora', sans-serif;
  color: var(--text-primary);
  transition: color 0.25s ease, background-color 0.25s ease;
}

#MainMenu, footer, header { visibility: hidden; }

/* Scrollbar tùy chỉnh */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--scrollbar-track); }
::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--scrollbar-hover); }

/* ══════════════════════════════════════════════════════════════
   4. STREAMLIT APP SHELL
══════════════════════════════════════════════════════════════ */
.stApp {
  background: var(--bg-page) !important;
  min-height: 100vh;
  transition: background 0.25s ease;
}

.block-container {
  padding: 0 0 4rem 0 !important;
  max-width: 100% !important;
}

/* ══════════════════════════════════════════════════════════════
   5. NAVIGATION BAR — GLASSMORPHISM
══════════════════════════════════════════════════════════════ */
.fpt-nav {
  position: sticky;
  top: 0;
  z-index: 999;
  background: var(--nav-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--nav-border);
  padding: 0 2.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  box-shadow: var(--nav-shadow);
  transition: background 0.25s ease, border-color 0.25s ease;
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
  color: var(--text-primary);
  letter-spacing: -0.2px;
  line-height: 1;
  transition: color 0.25s ease;
}

.fpt-nav-subtitle {
  font-size: 0.72rem;
  color: var(--text-muted);
  font-weight: 400;
  margin-top: 2px;
  transition: color 0.25s ease;
}

/* ── Dark Mode Toggle Button ── */
.fpt-theme-toggle {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  border: 1.5px solid var(--border-default);
  background: var(--toggle-bg);
  color: var(--toggle-icon);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.2s ease;
  flex-shrink: 0;
  user-select: none;
}
.fpt-theme-toggle:hover {
  background: var(--toggle-hover-bg);
  border-color: var(--fpt-orange);
  color: var(--toggle-hover-icon);
  transform: rotate(15deg) scale(1.05);
}

/* ══════════════════════════════════════════════════════════════
   6. HERO SECTION
══════════════════════════════════════════════════════════════ */
.fpt-hero {
  background: var(--hero-bg);
  border-bottom: 1px solid var(--hero-border);
  padding: 2.8rem 2.5rem 2.2rem;
  text-align: center;
  transition: background 0.25s ease, border-color 0.25s ease;
}

.fpt-hero-eyebrow {
  display: inline-block;
  background: var(--fpt-orange-glow);
  color: var(--fpt-orange-dark);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 5px 14px;
  border-radius: 20px;
  border: 1px solid rgba(242,111,33,0.2);
  margin-bottom: 1rem;
}

.fpt-hero-title {
  font-size: clamp(1.6rem, 4vw, 2.2rem);
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.8px;
  line-height: 1.2;
  margin-bottom: 0.6rem;
  transition: color 0.25s ease;
}

.fpt-hero-title span {
  background: linear-gradient(135deg, var(--fpt-orange), var(--fpt-orange-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.fpt-hero-desc {
  font-size: 0.9rem;
  color: var(--text-muted);
  font-weight: 400;
  max-width: 500px;
  margin: 0 auto 1.8rem;
  line-height: 1.65;
  transition: color 0.25s ease;
}

/* ══════════════════════════════════════════════════════════════
   7. SEARCH BOX
══════════════════════════════════════════════════════════════ */
.stTextInput > div > div > input {
  background: var(--bg-surface) !important;
  border: 1.5px solid var(--border-default) !important;
  border-radius: 14px !important;
  color: var(--text-primary) !important;
  font-family: 'Sora', sans-serif !important;
  font-size: 0.95rem !important;
  padding: 0.85rem 1.2rem !important;
  box-shadow: var(--card-shadow) !important;
  transition: all 0.22s ease !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--fpt-orange) !important;
  box-shadow: var(--card-shadow), 0 0 0 4px var(--fpt-orange-glow) !important;
}
.stTextInput > div > div > input::placeholder {
  color: var(--text-hint) !important;
  font-weight: 400 !important;
}

/* ══════════════════════════════════════════════════════════════
   8. BUTTONS — PRIMARY & SECONDARY
══════════════════════════════════════════════════════════════ */
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
  color: #FFFFFF !important;
  box-shadow: 0 4px 16px rgba(242,111,33,0.38) !important;
}
.stButton > button[kind="primary"]:hover {
  box-shadow: 0 6px 22px rgba(242,111,33,0.50) !important;
  transform: translateY(-1px) !important;
  filter: brightness(1.05) !important;
}

.stButton > button[kind="secondary"] {
  background: var(--btn-sec-bg) !important;
  border: 1.5px solid var(--btn-sec-border) !important;
  color: var(--btn-sec-text) !important;
}
.stButton > button[kind="secondary"]:hover {
  background: var(--btn-sec-hover-bg) !important;
  border-color: var(--btn-sec-hover-bd) !important;
  color: var(--btn-sec-hover-txt) !important;
}

/* ══════════════════════════════════════════════════════════════
   9. SECTION HEADER
══════════════════════════════════════════════════════════════ */
.fpt-section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1.4rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid var(--border-subtle);
}

.fpt-section-icon {
  width: 34px;
  height: 34px;
  background: var(--fpt-orange-glow);
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
  color: var(--text-primary);
  transition: color 0.25s ease;
}

.fpt-section-count {
  font-size: 0.75rem;
  color: var(--badge-text);
  font-weight: 500;
  background: var(--badge-bg);
  padding: 2px 8px;
  border-radius: 8px;
  margin-left: auto;
  transition: background 0.25s ease, color 0.25s ease;
}

/* ══════════════════════════════════════════════════════════════
   10. EXPANDER — PREMIUM CARDS
══════════════════════════════════════════════════════════════ */
.stExpander {
  background: var(--card-bg) !important;
  border: 1.5px solid var(--card-border) !important;
  border-radius: 14px !important;
  margin-bottom: 10px !important;
  overflow: hidden !important;
  box-shadow: var(--card-shadow) !important;
  transition: all 0.2s ease !important;
}
.stExpander:hover {
  border-color: var(--card-hover-border) !important;
  box-shadow: var(--card-hover-shadow) !important;
  transform: translateY(-1px) !important;
}

[data-testid="stExpander"] summary {
  color: var(--exp-head-text) !important;
  font-weight: 600 !important;
  font-size: 0.92rem !important;
  padding: 16px 20px !important;
  min-height: 52px !important;
  background: var(--exp-head-bg) !important;
  font-family: 'Sora', sans-serif !important;
  letter-spacing: -0.1px !important;
  transition: color 0.2s ease, background 0.25s ease !important;
}
[data-testid="stExpander"] summary:hover { color: var(--fpt-orange) !important; }

[data-testid="stExpanderDetails"] {
  background: var(--exp-detail-bg) !important;
  padding: 16px 22px !important;
  border-top: 1px solid var(--exp-detail-border) !important;
  color: var(--exp-detail-text) !important;
  font-size: 0.88rem !important;
  line-height: 1.85 !important;
  font-family: 'Sora', sans-serif !important;
  transition: background 0.25s ease, color 0.25s ease !important;
}

/* ══════════════════════════════════════════════════════════════
   11. BADGES / TAGS
══════════════════════════════════════════════════════════════ */
.tag-ok {
  display: inline-block;
  background: var(--tag-ok-bg); color: var(--tag-ok-text);
  font-weight: 700; font-size: 0.78rem;
  padding: 2px 9px; border-radius: 6px;
  border: 1px solid var(--tag-ok-bd);
  transition: all 0.25s ease;
}
.tag-err {
  display: inline-block;
  background: var(--tag-err-bg); color: var(--tag-err-text);
  font-weight: 700; font-size: 0.78rem;
  padding: 2px 9px; border-radius: 6px;
  border: 1px solid var(--tag-err-bd);
  transition: all 0.25s ease;
}
.tag-note {
  display: inline-block;
  background: var(--tag-note-bg); color: var(--tag-note-text);
  font-weight: 700; font-size: 0.78rem;
  padding: 2px 9px; border-radius: 6px;
  border: 1px solid var(--tag-note-bd);
  transition: all 0.25s ease;
}

/* ══════════════════════════════════════════════════════════════
   12. EMPTY STATE
══════════════════════════════════════════════════════════════ */
.empty-state {
  text-align: center;
  padding: 4rem 1rem;
  color: var(--empty-text);
  font-size: 0.92rem;
  background: var(--empty-bg);
  border-radius: 16px;
  border: 1.5px dashed var(--empty-border);
  transition: background 0.25s ease, border-color 0.25s ease, color 0.25s ease;
}

/* ══════════════════════════════════════════════════════════════
   13. DOCUMENT CARDS
══════════════════════════════════════════════════════════════ */
.doc-card {
  background: var(--card-bg);
  border: 1.5px solid var(--card-border);
  border-radius: 14px;
  padding: 18px 22px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: var(--card-shadow);
}
.doc-card:hover {
  border-color: var(--card-hover-border);
  box-shadow: var(--card-hover-shadow);
  transform: translateY(-1px);
}
.doc-card-icon {
  width: 44px; height: 44px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.3rem; flex-shrink: 0;
}
.doc-card-title {
  font-size: 0.95rem; font-weight: 700;
  margin-bottom: 3px; line-height: 1.3;
}
.doc-card-desc {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 400;
  transition: color 0.25s ease;
}
.doc-card-arrow {
  margin-left: auto;
  font-size: 1.1rem; font-weight: 700; flex-shrink: 0;
}
.doc-placeholder {
  background: var(--card-bg);
  border: 2px dashed var(--border-default);
  border-radius: 16px;
  padding: 3rem 1rem;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
  transition: background 0.25s ease, border-color 0.25s ease;
}

/* ══════════════════════════════════════════════════════════════
   14. BẢNG EXCEL INLINE — xl-wrap (mã lỗi / dữ liệu)
══════════════════════════════════════════════════════════════ */
.xl-wrap thead th, .bg-excel thead th {
  position: sticky; top: 0; z-index: 2;
  font-weight: 700; white-space: nowrap;
}
.xl-wrap {
  overflow-x: auto; -webkit-overflow-scrolling: touch;
  border-radius: 12px; margin-top: 12px;
  border: 1px solid var(--border-default);
  box-shadow: var(--card-shadow);
  transition: border-color 0.25s ease;
}
.xl-wrap table {
  border-collapse: collapse;
  width: max-content; min-width: 100%;
  font-size: 0.88rem; font-family: 'Sora', sans-serif;
}
.xl-wrap tbody td {
  background: var(--card-bg);
  color: var(--text-secondary);
  padding: 10px 16px;
  border-bottom: 1px solid var(--tbl-cell-border);
  border-right: 1px solid var(--tbl-cell-border);
  vertical-align: middle; line-height: 1.6;
  white-space: nowrap; min-width: 80px;
  transition: background 0.25s ease, color 0.25s ease;
}
.xl-wrap tbody td:first-child {
  position: sticky; left: 0; z-index: 1;
  background: var(--card-bg);
  border-right: 2px solid var(--border-default);
  font-weight: 600;
}
.xl-wrap thead th {
  background: var(--tbl-head-bg);
  color: var(--tbl-head-text);
  border-bottom: 2px solid var(--tbl-head-border);
  padding: 11px 16px;
  transition: background 0.25s ease, color 0.25s ease;
}
.xl-wrap thead th:first-child {
  position: sticky; left: 0; z-index: 3;
  background: var(--tbl-sticky-head);
}
.xl-wrap tbody td:last-child { border-right: none; }
.xl-wrap tbody tr:last-child td { border-bottom: none; }
.xl-wrap tbody tr:nth-child(even) td { background: var(--tbl-row-alt); }
.xl-wrap tbody tr:nth-child(even) td:first-child { background: var(--tbl-sticky-first); }
.xl-wrap tbody tr:hover td {
  background: var(--tbl-row-hover-bg) !important;
  color: var(--tbl-row-hover-text) !important;
}

/* ══════════════════════════════════════════════════════════════
   15. BẢNG GIÁ CƯỚC — bg-excel
══════════════════════════════════════════════════════════════ */
.bg-excel-wrap {
  overflow-x: auto; -webkit-overflow-scrolling: touch;
  border-radius: 14px;
  border: 1px solid var(--border-default);
  box-shadow: 0 2px 16px rgba(0,93,163,0.07);
  margin-top: 4px;
  transition: border-color 0.25s ease;
}
.bg-excel-wrap::after {
  content: "← Vuốt ngang để xem thêm →";
  display: none;
  text-align: center;
  font-size: 0.72rem;
  color: var(--text-hint);
  padding: 6px 0 2px;
  font-family: 'Sora', sans-serif;
}
@media (max-width: 640px) { .bg-excel-wrap::after { display: block; } }

.bg-excel {
  border-collapse: collapse;
  width: max-content; min-width: 100%;
  font-size: 0.9rem; font-family: 'Sora', sans-serif;
  line-height: 1.5;
}
.bg-excel td {
  border: 1px solid var(--border-default);
  padding: 10px 14px;
  text-align: center; vertical-align: middle;
  white-space: nowrap; min-width: 90px;
  color: var(--text-secondary);
  transition: all 0.25s ease;
}
.bg-excel td:first-child {
  position: sticky; left: 0; z-index: 1;
  background: inherit;
  border-right: 2px solid var(--tbl-head-border);
  font-weight: 700; text-align: left; min-width: 110px;
}
.bg-excel thead th {
  background: var(--tbl-head-bg);
  color: var(--tbl-head-text);
  border-bottom: 2px solid var(--tbl-head-border);
  padding: 11px 14px; text-align: center;
  transition: background 0.25s ease, color 0.25s ease;
}
.bg-excel thead th:first-child {
  position: sticky; left: 0; z-index: 3;
  background: var(--tbl-sticky-head); text-align: left;
}
.bg-excel tbody tr:hover td { filter: brightness(0.94); transition: filter 0.12s; }
.bg-excel tr:first-child td, .bg-excel tr:nth-child(2) td {
  font-weight: 700; font-size: 0.88rem;
}

/* ══════════════════════════════════════════════════════════════
   16. DOWNLOAD BUTTON
══════════════════════════════════════════════════════════════ */
.stDownloadButton > button {
  background: var(--dl-bg) !important;
  border: 1.5px solid var(--dl-border) !important;
  color: var(--dl-text) !important;
  border-radius: 10px !important;
  font-family: 'Sora', sans-serif !important;
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  padding: 0.5rem 1rem !important;
  transition: all 0.18s ease !important;
}
.stDownloadButton > button:hover {
  background: var(--dl-hover-bg) !important;
  border-color: var(--dl-hover-border) !important;
  color: var(--dl-hover-text) !important;
}

/* ══════════════════════════════════════════════════════════════
   17. BAN HANG — Dark mode thêm cho .bh-card wrapper
   (Phần còn lại đã tích hợp vào _BH_CSS trong ban_hang.py)
══════════════════════════════════════════════════════════════ */
[data-fpt-theme="dark"] .bh-card {
  box-shadow: 0 2px 16px rgba(0,0,0,0.45) !important;
}

/* ── EC Card (mã lỗi) dark mode ── */
[data-fpt-theme="dark"] .ec-card {
  background: var(--card-bg) !important;
  border-color: var(--card-border) !important;
}
[data-fpt-theme="dark"] .ec-desc {
  color: var(--text-secondary) !important;
}
[data-fpt-theme="dark"] .ec-section-title {
  color: var(--text-muted) !important;
}
[data-fpt-theme="dark"] .ec-para,
[data-fpt-theme="dark"] .ec-bullets li,
[data-fpt-theme="dark"] .ec-steps li {
  color: var(--text-secondary) !important;
}
[data-fpt-theme="dark"] li.ec-sub {
  color: var(--text-muted) !important;
}
[data-fpt-theme="dark"] .ec-body {
  border-top-color: var(--border-subtle) !important;
}
[data-fpt-theme="dark"] .ec-divider {
  background: var(--border-subtle) !important;
}

/* ══════════════════════════════════════════════════════════════
   18. RESPONSIVE
══════════════════════════════════════════════════════════════ */
@media (max-width: 768px) {
  .fpt-nav { padding: 0 1.2rem; }
  .fpt-hero { padding: 2rem 1.2rem 1.6rem; }
  .fpt-pad  { padding: 1.2rem 1rem; }
}

/* Ban hàng — 5 nút khu vực */
@media (max-width: 900px) and (min-width: 640px) {
  [data-testid="stHorizontalBlock"] .stButton > button {
    font-size: 0.78rem !important;
    padding: 0.4rem 0.3rem !important;
    min-height: 38px !important;
  }
}
@media (max-width: 640px) {
  [data-testid="stHorizontalBlock"] .stButton > button {
    font-size: 0.72rem !important;
    padding: 0.35rem 0.2rem !important;
    min-height: 36px !important;
    letter-spacing: -0.3px !important;
  }
}

/* ══════════════════════════════════════════════════════════════
   19. PADDING HELPER
══════════════════════════════════════════════════════════════ */
.fpt-pad { padding: 1.8rem 2.5rem; }

</style>
"""

_TOGGLE_BTN_HTML = """
<button
  id="fpt-toggle-btn"
  class="fpt-theme-toggle"
  title="Chuyển chế độ sáng / tối"
  aria-label="Toggle dark mode"
>🌙</button>
"""


def inject_css():
    """Inject toàn bộ CSS vào Streamlit."""
    st.markdown(_CSS, unsafe_allow_html=True)


def render_theme_toggle() -> str:
    """Trả về HTML nút toggle để nhúng vào navbar."""
    return _TOGGLE_BTN_HTML