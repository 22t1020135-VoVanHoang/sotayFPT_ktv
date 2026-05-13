"""
utils/highlight_text.py
Hàm tô màu nội dung văn bản trong expander:
OK, Notok, Ghi chú, B1/B2..., TH1/TH2...
"""

import re


def highlight_text(text: str) -> str:
    """
    Chuyển đổi văn bản thuần thành HTML có màu,
    giúp kỹ thuật viên đọc nhanh hơn.
    """
    html = str(text)
    html = html.replace("Notok",   "<span class='tag-err'>❌ Notok</span>")
    html = html.replace("OK",      "<span class='tag-ok'>✅ OK</span>")
    html = html.replace("Ghi chú", "<span class='tag-note'>📝 Ghi chú</span>")
    html = html.replace(
        "chốt phương án và số tiền thu nếu có",
        "<strong style='color:#c04800'>chốt phương án và số tiền thu nếu có</strong>",
    )
    html = re.sub(r'\b(B\d+)\b',  r"<strong style='color:#005DA3'>\1</strong>", html)
    html = re.sub(r'\b(TH\d+)\b', r"<strong style='color:#1a7a3c'>\1</strong>", html)
    html = html.replace("\n", "<br>")
    return html
