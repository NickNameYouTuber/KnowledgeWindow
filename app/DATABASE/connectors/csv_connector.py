import pandas as pd

def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Читает содержимое .csv файла и возвращает его в виде DataFrame.
    """
    return pd.read_csv(file_path)