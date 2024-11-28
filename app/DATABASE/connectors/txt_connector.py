import os

def read_txt_file(file_path: str) -> str:
    """
    Читает содержимое .txt файла и возвращает его в виде строки.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return content