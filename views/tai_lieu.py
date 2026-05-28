"""
views/tai_lieu.py
Render tab "Tài liệu": subfolder Chương Trình 4XL, Tân binh và Cấu hình thiết bị.
"""

import base64
import os
import streamlit as st

from utils.highlight_text import highlight_text
from views.quy_trinh import render_section_header

_BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CAU_HINH_DIR = os.path.join(_BASE_DIR, "tailieu", "cau_hinh")
_4XL_DIR      = os.path.join(_BASE_DIR, "tailieu", "4xl")

_SUPPORTED_EXT = frozenset({".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".docx", ".doc"})
_MIME_MAP = {
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".ppt":  "application/vnd.ms-powerpoint",
    ".pdf":  "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".doc":  "application/msword",
}
_SUBFOLDERS = {
    "💡  Chương Trình 4XL":  "Chương Trình 4XL",
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

# Metadata tĩnh cho file PDF trong cau_hinh/ — key là tên file chính xác
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
# Metadata cho file đào tạo (tên file có ký tự Unicode URL-encoded)
_PDF_META_TRAINING = {
    "title": "Tài liệu đào tạo triển khai Mesh Wi-Fi 6 GPON Internet Hub AX3000S",
    "desc":  "Tài liệu nội bộ FPT Digital — hướng dẫn cấu hình và thực hành lab (v1.0)",
    "color": "#F26F21", "bg": "#FFF5EF", "border": "rgba(242,111,33,0.2)",
    "search_tags": ["đào tạo", "mesh", "wifi 6", "gpon", "ax3000s", "cấu hình thiết bị", "lab"],
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_pdf_meta(fname: str) -> dict:
    """Trả về metadata cho file PDF. Fallback theo tên file nếu không có trong _PDF_META."""
    if fname in _PDF_META:
        return _PDF_META[fname]
    fname_lower = fname.lower()
    if "đào" in fname_lower or "#u0111" in fname_lower or "T#U" in fname:
        return _PDF_META_TRAINING
    return {
        "title": os.path.splitext(fname)[0],
        "desc":  "Tài liệu kỹ thuật",
        "color": "#5A6070", "bg": "#F0F3F8", "border": "rgba(90,96,112,0.15)",
        "search_tags": ["cấu hình thiết bị"],
    }


def _item_matches(item: dict, kw: str) -> bool:
    """Kiểm tra item có khớp với keyword không (tìm trong tags, title, desc)."""
    if not kw:
        return True
    return (
        any(kw in tag for tag in item.get("search_tags", []))
        or kw in item.get("title", "").lower()
        or kw in item.get("desc", "").lower()
    )


def _list_cau_hinh_files() -> list[tuple[str, str, str]]:
    """Trả về list[(fname, ext, fpath)] cho tất cả file hỗ trợ trong _CAU_HINH_DIR."""
    if not os.path.isdir(_CAU_HINH_DIR):
        return []
    result = []
    for fname in sorted(os.listdir(_CAU_HINH_DIR)):
        ext = os.path.splitext(fname)[1].lower()
        if ext in _SUPPORTED_EXT:
            result.append((fname, ext, os.path.join(_CAU_HINH_DIR, fname)))
    return result


def count_cau_hinh_files() -> int:
    return len(_list_cau_hinh_files())


# ── Helpers: ảnh base64 ───────────────────────────────────────────────────────

def _img_b64(fpath: str) -> str:
    """Đọc file ảnh, trả về chuỗi base64 data-URI. Trả về chuỗi rỗng nếu lỗi."""
    try:
        ext = os.path.splitext(fpath)[1].lower().lstrip(".")
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(ext, "image/jpeg")
        with open(fpath, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{data}"
    except Exception:
        return ""


# ── Render: Chương Trình 4XL ──────────────────────────────────────────────────

_4XL_ITEMS = [
    {
        "num": "1",
        "title": "Tác Phong Giao Tiếp 4XL",
        "desc": "Hướng dẫn tác phong, giao tiếp nâng cao dành cho KTV/NVKD — Chương trình 4XL FPT Telecom",
        "icon": "🌟",
        "color": "#C8530D",
        "bg": "#FFF5EF",
        "border": "rgba(242,111,33,0.25)",
        "pdf_file": "tác phong giao tiếp 4XL.pdf",
        "pdf_label": "Tác phong giao tiếp 4XL",
        "images": [],
        "search_tags": ["4xl", "tác phong", "giao tiếp", "chương trình", "ktv"],
    },
    {
        "num": "2",
        "title": "KTV Giao Tiếp Qua Điện Thoại Với KHG",
        "desc": "Mẫu câu giao tiếp với khách hàng qua điện thoại: xin đến trễ, xin hẹn lại",
        "icon": "📞",
        "color": "#005DA3",
        "bg": "#EFF6FF",
        "border": "rgba(0,93,163,0.2)",
        "pdf_file": "TỔNG HỢP MẪU GIAO TIẾP QUA ĐIỆN THOẠI VỚI KHÁCH HÀNG.pdf",
        "pdf_label": "Tổng hợp mẫu giao tiếp qua điện thoại",
        "images": ["dienthoai_xindentze.jpg", "dienthoai_xinhenlai.jpg"],
        "search_tags": ["4xl", "điện thoại", "giao tiếp", "mẫu câu", "hẹn lại", "đến trễ", "ktv"],
    },
    {
        "num": "3",
        "title": "Giao Tiếp Trực Tiếp Với KHG Khi KTV Triển Khai Mới",
        "desc": "Mẫu câu giao tiếp tình huống triển khai, lắp đặt mới tại nhà khách hàng",
        "icon": "🏠",
        "color": "#1A7A42",
        "bg": "#EFFAF4",
        "border": "rgba(26,122,66,0.2)",
        "pdf_file": "Mẫu giao tiếp khi triển khai mới.pdf",
        "pdf_label": "Mẫu giao tiếp khi triển khai mới",
        "images": [],
        "search_tags": ["4xl", "triển khai", "lắp đặt", "giao tiếp", "tại nhà", "ktv"],
    },
    {
        "num": "4",
        "title": "Tin Nhắn KTV Giao Tiếp Với KHG",
        "desc": "Bộ mẫu tin nhắn SMS KTV gửi khách hàng: thông báo lịch hẹn, trễ lịch, dời lịch, đến nơi không liên hệ được",
        "icon": "💬",
        "color": "#6D28D9",
        "bg": "#F3EEFF",
        "border": "rgba(109,40,217,0.2)",
        "pdf_file": "Tổng hợp tất cả mẫu tin nhắn KTV gửi KHG.pdf",
        "pdf_label": "Tổng hợp tất cả mẫu tin nhắn KTV gửi KHG",
        "images": ["sms_lichhen.jpg", "sms_trelihen.jpg", "sms_doilihen.jpg", "sms_dennoikhonglienhe.jpg"],
        "search_tags": ["4xl", "tin nhắn", "sms", "lịch hẹn", "trễ lịch", "dời lịch", "ktv", "khách hàng"],
    },
]


def _render_4xl(keyword: str = "") -> None:
    kw = keyword.strip().lower()
    filtered = [
        item for item in _4XL_ITEMS
        if not kw
        or any(kw in tag for tag in item["search_tags"])
        or kw in item["title"].lower()
        or kw in item["desc"].lower()
    ]

    if not filtered:
        st.markdown(
            '<div class="empty-state">😕 Không tìm thấy nội dung 4XL khớp với từ khóa.<br>'
            '<small style="color:#B0BBC8;">Thử: <b>tác phong</b>, <b>điện thoại</b>, <b>tin nhắn</b>, <b>triển khai</b></small></div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        "<p style='color:#8896A5;font-size:0.82rem;margin-bottom:16px;"
        "font-family:Sora,sans-serif;'>"
        "💡 Chương trình 4XL — Hành trình chinh phục triệu trái tim khách hàng của FPT Telecom.</p>",
        unsafe_allow_html=True,
    )

    for item in filtered:
        pdf_path = os.path.join(_4XL_DIR, item["pdf_file"])

        # ── Card tiêu đề ──
        st.markdown(
            f'<div class="doc-card" style="border-color:{item["border"]};border-left:3px solid {item["color"]};">'
            f'  <div class="doc-card-icon" style="background:{item["bg"]};font-size:1.3rem;">{item["icon"]}</div>'
            f'  <div style="flex:1;">'
            f'    <div class="doc-card-title" style="color:{item["color"]};">'
            f'      <span style="background:{item["bg"]};color:{item["color"]};border-radius:4px;'
            f'      padding:1px 7px;font-size:0.72rem;font-weight:800;margin-right:6px;">{item["num"]}</span>'
            f'      {highlight_text(item["title"], keyword)}</div>'
            f'    <div class="doc-card-desc">{highlight_text(item["desc"], keyword)}</div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── Hiển thị ảnh dạng swipe carousel (vuốt tay trái/phải) ──
        if item["images"]:
            img_paths = [
                os.path.join(_4XL_DIR, fname)
                for fname in item["images"]
                if os.path.isfile(os.path.join(_4XL_DIR, fname))
            ]
            if img_paths:
                # Encode tất cả ảnh sang base64
                imgs_b64 = [_img_b64(p) for p in img_paths]
                imgs_b64 = [u for u in imgs_b64 if u]  # bỏ ảnh lỗi

                if imgs_b64:
                    total = len(imgs_b64)
                    # Build danh sách src JS
                    imgs_js = "[" + ",".join(f'"{u}"' for u in imgs_b64) + "]"
                    border_color = item["border"]

                    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  html, body {{
    margin: 0; padding: 0;
    background: transparent;
    overflow: hidden;
  }}
  #carousel_{item['num']} {{
    position: relative;
    overflow: hidden;
    width: 100%;
    border-radius: 12px;
    border: 1px solid {border_color};
    touch-action: pan-y;
    user-select: none;
    margin-bottom: 0;
  }}
  #track_{item['num']} {{
    display: flex;
    transition: transform 0.3s ease;
    width: {total * 100}%;
  }}
  .slide-item {{
    width: {100 / total}%;
    flex-shrink: 0;
  }}
  .slide-item img {{
    width: 100%;
    display: block;
    border-radius: 12px;
    height: auto;
  }}
  #dots_{item['num']} {{
    position: absolute;
    bottom: 8px;
    left: 0; right: 0;
    display: flex;
    justify-content: center;
    gap: 6px;
  }}
</style>
</head>
<body>
<div id="carousel_{item['num']}">
  <div id="track_{item['num']}">
    {''.join(
        f'<div class="slide-item"><img src="{u}" id="img_{item["num"]}_{i}" /></div>'
        for i, u in enumerate(imgs_b64)
    )}
  </div>
  <div id="dots_{item['num']}">
    {''.join(
        f'<span id="dot_{item["num"]}_{i}" style="'
        f'width:7px;height:7px;border-radius:50%;background:{"rgba(255,255,255,0.95)" if i==0 else "rgba(255,255,255,0.45)"};'
        f'display:inline-block;transition:background 0.2s;"></span>'
        for i in range(total)
    )}
  </div>
</div>

<script>
(function(){{
  var num   = "{item['num']}";
  var total = {total};
  var cur   = 0;
  var track = document.getElementById("track_" + num);
  var carousel = document.getElementById("carousel_" + num);
  var startX, isDragging = false, diffX = 0;

  // Tự động resize iframe theo chiều cao ảnh hiện tại
  function updateHeight() {{
    var img = document.getElementById("img_" + num + "_" + cur);
    if (img && img.complete && img.naturalHeight > 0) {{
      var h = carousel.offsetHeight;
      if (h > 0) {{
        // Gửi chiều cao lên parent Streamlit
        window.parent.postMessage({{
          type: "streamlit:setFrameHeight",
          height: h + 4
        }}, "*");
      }}
    }}
  }}

  function goTo(i) {{
    if (i < 0) i = 0;
    if (i >= total) i = total - 1;
    cur = i;
    track.style.transition = "transform 0.3s ease";
    track.style.transform  = "translateX(-" + (cur * 100 / total) + "%)";
    for (var j = 0; j < total; j++) {{
      var dot = document.getElementById("dot_" + num + "_" + j);
      if (dot) dot.style.background = j === cur
        ? "rgba(255,255,255,0.95)" : "rgba(255,255,255,0.45)";
    }}
    setTimeout(updateHeight, 350);
  }}

  // Chờ tất cả ảnh load xong rồi set chiều cao
  var imgs = document.querySelectorAll("#track_" + num + " img");
  var loaded = 0;
  function onImgLoad() {{
    loaded++;
    if (loaded === imgs.length) {{
      updateHeight();
    }}
  }}
  imgs.forEach(function(img) {{
    if (img.complete) {{ onImgLoad(); }}
    else {{ img.addEventListener("load", onImgLoad); }}
  }});

  // Fallback: update sau 1s và 2s phòng trường hợp base64 chậm
  setTimeout(updateHeight, 800);
  setTimeout(updateHeight, 1800);

  // Resize observer theo dõi thay đổi kích thước
  if (window.ResizeObserver) {{
    new ResizeObserver(function() {{
      updateHeight();
    }}).observe(carousel);
  }}

  track.addEventListener("touchstart", function(e) {{
    startX = e.touches[0].clientX;
    isDragging = true;
    diffX = 0;
    track.style.transition = "none";
  }}, {{passive:true}});

  track.addEventListener("touchmove", function(e) {{
    if (!isDragging) return;
    diffX = e.touches[0].clientX - startX;
    var base = -cur * 100 / total;
    track.style.transform = "translateX(calc(" + base + "% + " + diffX + "px))";
  }}, {{passive:true}});

  track.addEventListener("touchend", function() {{
    isDragging = false;
    if (diffX < -50)      goTo(cur + 1);
    else if (diffX > 50)  goTo(cur - 1);
    else                  goTo(cur);
  }});
}})();
</script>
</body>
</html>
"""
                    import streamlit.components.v1 as components
                    # height=0 + scrolling=False để Streamlit dùng postMessage tự resize
                    # Đặt height đủ lớn ban đầu để không bị cắt, JS sẽ resize về đúng
                    height_px = 1200 if total <= 2 else 1400
                    components.html(html, height=height_px, scrolling=False)

        # ── Nút tải PDF ──
        if os.path.isfile(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=f"📥  Tải về — {item['pdf_label']}.pdf",
                    data=f,
                    file_name=f"{item['pdf_label']}.pdf",
                    mime="application/pdf",
                    key=f"dl_4xl_{item['num']}",
                )
        else:
            st.warning(f"⚠️ Chưa tìm thấy file: {item['pdf_file']}. Đặt vào thư mục tailieu/4xl/")

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)


# ── Render: Tài liệu tân binh ─────────────────────────────────────────────────

def _render_tan_binh(keyword: str = "") -> None:
    kw = keyword.strip().lower()
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
    kw = keyword.strip().lower()
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
    total = len(_4XL_ITEMS) + len(_TAN_BINH_ITEMS) + count_cau_hinh_files()
    render_section_header("📁", "Tài liệu", total)

    sf1, sf2, sf3 = st.columns(3)
    for col, (label, sf_key) in zip([sf1, sf2, sf3], _SUBFOLDERS.items()):
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
    if active_sf == "Chương Trình 4XL":
        _render_4xl(keyword)
    elif active_sf == "Tài liệu tân binh":
        _render_tan_binh(keyword)
    elif active_sf == "Cấu hình thiết bị":
        _render_cau_hinh(keyword)