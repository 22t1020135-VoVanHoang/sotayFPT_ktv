"""
data_loader.py
Chứa logic đọc và parse file SO_TAY_KTV.xlsx bằng openpyxl.
"""

import openpyxl
import os

# Thư mục chứa file data_loader.py (tức là thư mục sotay_ktv/)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _find_file(filename: str) -> str:
    """
    Tìm file theo thứ tự ưu tiên:
    1. Cùng thư mục với app.py (BASE_DIR)
    2. Thư mục con tailieu/
    3. Trả về đường dẫn mặc định để app.py báo lỗi đúng cách
    """
    candidates = [
        os.path.join(_BASE_DIR, filename),
        os.path.join(_BASE_DIR, "tailieu", filename),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return os.path.join(_BASE_DIR, filename)  # fallback → sẽ raise FileNotFoundError

FILE_PATH     = _find_file("SO_TAY_KTV.xlsx")
REQUIRED_COLS = {"ten", "buoc"}


def _load_sotay(file_path: str) -> list:
    """
    Đọc file Excel SO_TAY_KTV.xlsx và trả về danh sách dict.
    Mỗi dict gồm: {'ten': str, 'buoc': str, 'folder': str}
    """
    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb.active

    headers = []
    for cell in ws[1]:
        val = cell.value
        headers.append(str(val).strip().lower() if val is not None else "")

    missing = REQUIRED_COLS - set(headers)
    if missing:
        raise ValueError(f"Thiếu cột bắt buộc: {', '.join(sorted(missing))}")

    idx_ten    = headers.index("ten")
    idx_buoc   = headers.index("buoc")
    idx_folder = headers.index("folder") if "folder" in headers else None

    rows = []
    for r in range(2, ws.max_row + 1):
        def cell_val(col_idx):
            v = ws.cell(r, col_idx + 1).value
            return str(v).strip() if v is not None else ""

        ten    = cell_val(idx_ten)
        buoc   = cell_val(idx_buoc)
        folder = cell_val(idx_folder) if idx_folder is not None else ""

        if not ten and not buoc:
            continue

        rows.append({
            "ten":    ten,
            "buoc":   buoc,
            "folder": folder if folder else "Quy trình",
        })

    return rows


def load_data() -> list:
    """
    Hàm public: load dữ liệu từ FILE_PATH.
    Trả về list rows, hoặc raise exception để app.py xử lý.
    """
    return _load_sotay(FILE_PATH)
