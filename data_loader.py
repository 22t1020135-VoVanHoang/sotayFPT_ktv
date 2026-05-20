"""
data_loader.py
Load và parse SO_TAY_KTV.xlsx bằng openpyxl.
"""

import os
import openpyxl

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_SEARCH_PATHS = (
    os.path.join(_BASE_DIR, "SO_TAY_KTV.xlsx"),
    os.path.join(_BASE_DIR, "tailieu", "SO_TAY_KTV.xlsx"),
)
REQUIRED_COLS = frozenset({"ten", "buoc"})
DEFAULT_FOLDER = "Quy trình"


def _find_file() -> str:
    for path in _SEARCH_PATHS:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(f"Không tìm thấy SO_TAY_KTV.xlsx trong: {_SEARCH_PATHS}")


def load_data() -> list[dict]:
    """
    Đọc SO_TAY_KTV.xlsx, trả về list[dict] với keys: 'ten', 'buoc', 'folder'.
    Raise FileNotFoundError / ValueError nếu có lỗi.
    """
    file_path = _find_file()
    wb = openpyxl.load_workbook(file_path, data_only=True, read_only=True)
    ws = wb.active

    headers = [
        str(c).strip().lower() if (c := cell.value) is not None else ""
        for cell in next(ws.iter_rows(max_row=1))
    ]

    missing = REQUIRED_COLS - set(headers)
    if missing:
        wb.close()
        raise ValueError(f"Thiếu cột bắt buộc: {', '.join(sorted(missing))}")

    idx = {name: headers.index(name) for name in ("ten", "buoc")}
    idx_folder = headers.index("folder") if "folder" in headers else None

    def _val(row, col_idx: int) -> str:
        v = row[col_idx].value
        return str(v).strip() if v is not None else ""

    rows = []
    for row in ws.iter_rows(min_row=2):
        ten  = _val(row, idx["ten"])
        buoc = _val(row, idx["buoc"])
        if not ten and not buoc:
            continue
        folder = (_val(row, idx_folder) if idx_folder is not None else "") or DEFAULT_FOLDER
        rows.append({"ten": ten, "buoc": buoc, "folder": folder})

    wb.close()
    return rows
