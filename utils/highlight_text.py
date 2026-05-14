"""
utils/highlight_text.py
Highlight từ khóa tìm kiếm trong văn bản thuần túy.
"""

import re
import html as html_lib


def highlight_text(text: str, keyword: str = "") -> str:
    """
    Escape HTML, highlight keyword (không phân biệt hoa/thường),
    và chuyển newline thành <br>.

    Args:
        text:    Nội dung cần hiển thị.
        keyword: Từ khóa cần highlight (rỗng = không highlight).

    Returns:
        Chuỗi HTML an toàn để dùng với unsafe_allow_html=True.
    """
    if not text:
        return ""

    escaped = html_lib.escape(text)

    if not keyword or not keyword.strip():
        return escaped.replace("\n", "<br>")

    pattern = re.compile(re.escape(keyword.strip()), re.IGNORECASE)

    def _replacer(m: re.Match) -> str:
        return (
            '<mark style="background:#FFF3CD;color:#856404;'
            'padding:1px 3px;border-radius:3px;font-weight:600;">'
            f'{html_lib.escape(m.group())}</mark>'
        )

    return pattern.sub(_replacer, escaped).replace("\n", "<br>")
