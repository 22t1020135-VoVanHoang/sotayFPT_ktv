"""
utils/highlight_text.py
Highlight từ khóa tìm kiếm trong nội dung văn bản.
"""

import re
import html as html_lib


def highlight_text(text: str, keyword: str = "") -> str:
    """
    Highlight keyword trong text bằng thẻ <mark>.
    - Nếu keyword rỗng: trả về text gốc (đã escape HTML).
    - Không phân biệt hoa/thường.
    - Giữ nguyên ký tự xuống dòng → <br>.
    """
    if not text:
        return ""

    # Escape HTML trước để tránh XSS
    escaped = html_lib.escape(text)

    if not keyword or not keyword.strip():
        # Không có keyword → chỉ chuyển newline thành <br>
        return escaped.replace("\n", "<br>")

    kw = keyword.strip()
    # Escape ký tự đặc biệt trong regex
    pattern = re.compile(re.escape(kw), re.IGNORECASE)

    def replacer(m):
        return (
            f'<mark style="background:#FFF3CD;color:#856404;'
            f'padding:1px 3px;border-radius:3px;font-weight:600;">'
            f'{html_lib.escape(m.group())}</mark>'
        )

    highlighted = pattern.sub(replacer, escaped)
    return highlighted.replace("\n", "<br>")