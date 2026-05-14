"""
data_loader.py
Load và parse file SO_TAY_KTV.xlsx bằng openpyxl.
"""

import os
import openpyxl

_BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
REQUIRED_COLS = {"ten", "buoc"}


def _find_file(filename: str) -> str:
    """
    Tìm file theo thứ tự ưu tiên:
    1. Cùng thư mục với app.py
    2. Thư mục con tailieu/
    Trả về đường dẫn mặc định (sẽ raise FileNotFoundError nếu không tồn tại).
    """
    candidates = [
        os.path.join(_BASE_DIR, filename),
        os.path.join(_BASE_DIR, "tailieu", filename),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return candidates[0]  # fallback → app.py báo lỗi


FILE_PATH = _find_file("SO_TAY_KTV.xlsx")


def load_data() -> list:
    """
    Đọc file Excel SO_TAY_KTV.xlsx.
    Trả về list[dict] với keys: 'ten', 'buoc', 'folder'.
    Raise FileNotFoundError / ValueError nếu có lỗi.
    """
    if not os.path.isfile(FILE_PATH):
        raise FileNotFoundError(FILE_PATH)

    wb = openpyxl.load_workbook(FILE_PATH, data_only=True)
    ws = wb.active

    headers = [
        str(cell.value).strip().lower() if cell.value is not None else ""
        for cell in ws[1]
    ]

    missing = REQUIRED_COLS - set(headers)
    if missing:
        raise ValueError(f"Thiếu cột bắt buộc: {', '.join(sorted(missing))}")

    idx_ten    = headers.index("ten")
    idx_buoc   = headers.index("buoc")
    idx_folder = headers.index("folder") if "folder" in headers else None

    def cell_str(row_idx: int, col_idx: int) -> str:
        v = ws.cell(row_idx, col_idx + 1).value
        return str(v).strip() if v is not None else ""

    rows = []
    for r in range(2, ws.max_row + 1):
        ten    = cell_str(r, idx_ten)
        buoc   = cell_str(r, idx_buoc)
        folder = cell_str(r, idx_folder) if idx_folder is not None else ""

        if not ten and not buoc:
            continue

        rows.append({
            "ten":    ten,
            "buoc":   buoc,
            "folder": folder or "Quy trình",
        })

    wb.close()
    return rows
