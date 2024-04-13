import time
import random
import threading
import datetime as dt
import pandas as pd
from pathlib import Path
import logging

def setup_custom_logger(name):
    formatter = logging.Formatter(
        fmt="%(levelname)s - %(module)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

logger = setup_custom_logger("root")

class ExcelWriter:
    def __init__(self, file_path: str):
        self.logger = logging.getLogger("root")
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            pd.DataFrame(columns=["Timestamp", "Result"]).to_excel(
                self.file_path, index=False
            )

    def write(self, timestamp, result):
        self.logger.debug(f'received {result}')
        df = pd.read_excel(self.file_path)
        df.loc[len(df)] = {"Timestamp": timestamp, "Result": result}
        df.to_excel(self.file_path, index=False)

results = {
    "auto_test_module": None,
    "auto_test_module_extra": None,
    "manual_test_module": None
}

excel_writer = ExcelWriter("test_results.xlsx")

def receive_result(module_name: str, test_result: str) -> None:
    excel_writer = ExcelWriter("test_results.xlsx")
    if not results:
        raise Exception("Unknown module")

    results[module_name] = test_result
    logger.info(f"{dt.datetime.now()} --> {module_name} Received Result: {test_result}")

    test_result_values = set(results.values)
    if len(test_result_values) == 1 and None not in test_result_values:
        excel_writer.write(dt.datetime.now(), test_result)
        logger.debug(f"Recorded to Excel: {test_result}")


def auto_test_module():
    while True:
        time.sleep(0.5)
        receive_result("auto_test_module", "Pass" if random.randint(0, 1) else "Fail")

def auto_test_module_extra():
    while True:
        time.sleep(1.8)
        receive_result("auto_test_module_extra", "Pass" if random.randint(0, 1) else "Fail")

def manual_test_module():
    while True:
        sleep_time = random.randint(3, 10)
        time.sleep(sleep_time)
        receive_result("manual_test_module", "Pass" if random.randint(0, 1) else "Fail")


try:
    threading.Thread(target=auto_test_module, daemon=True).start()
    threading.Thread(target=auto_test_module_extra, daemon=True).start()
    threading.Thread(target=manual_test_module, daemon=True).start()

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Exiting...")
    logging.info("Exited")
