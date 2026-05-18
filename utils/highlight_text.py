"""
utils/highlight_text.py
Single source of truth cho logic highlight keyword trong HTML.
Được dùng bởi tất cả các view — không duplicate ở đâu khác.
"""

import re
import html as _html

# Style dùng chung, định nghĩa 1 lần
_MARK_STYLE = (
    "background:#FFF3CD;color:#856404;"
    "padding:1px 3px;border-radius:3px;font-weight:600;"
)


def highlight_text(text: str, keyword: str = "") -> str:
    """
    Escape HTML, highlight keyword (không phân biệt hoa/thường),
    và chuyển newline thành <br>.

    Returns:
        Chuỗi HTML an toàn để dùng với unsafe_allow_html=True.
    """
    if not text:
        return ""

    escaped = _html.escape(str(text))

    if not keyword or not keyword.strip():
        return escaped.replace("\n", "<br>")

    pattern = re.compile(re.escape(keyword.strip()), re.IGNORECASE)
    return pattern.sub(
        lambda m: f'<mark style="{_MARK_STYLE}">{_html.escape(m.group())}</mark>',
        escaped,
    ).replace("\n", "<br>")