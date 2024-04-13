import pandas as pd
from pathlib import Path
import logging


class ExcelWriter:
    """
    Writes test result to an excel file.
    """

    def __init__(self, file_path: str):
        self.logger = logging.getLogger("root")
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            # Create an empty DataFrame and save it if the file does not exist
            pd.DataFrame(columns=["Timestamp", "Result"]).to_excel(
                self.file_path, index=False
            )

    def write(self, timestamp, result):
        self.logger.debug(f'received {result}')
        df = pd.read_excel(self.file_path)
        df.loc[len(df)] = {"Timestamp": timestamp, "Result": result}
        df.to_excel(self.file_path, index=False)
