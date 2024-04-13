from abc import ABC, abstractmethod
from threading import RLock
from writer.excel_writer import ExcelWriter
from test_modules.abstract_test_module import AbstractTestModule
from datetime import datetime
import threading
import logging

class AbstractChecker(ABC):
    """
    Abstract class for a checker.
    A checker is to check if all test modules output the same result.
    """

    def __init__(self, result_writer: ExcelWriter, stop_event: threading.Event) -> None:
        self.result_writer = result_writer
        self.known_modules = set()
        self.results = {}
        self.results_lock = RLock()
        self.stop_event = stop_event
        self.logger = logging.getLogger('root')


    def register_test_module(self, module: AbstractTestModule):
        """
        讓 checker 認識傳入的 test module，才能在進行檢查時正確判斷
        """
        self.known_modules.add(module)

    def unregister_test_module(self, module: AbstractTestModule):
        """
        當 test module 不再使用時，將其移出名單內
        """
        self.known_modules.remove(module)

    def add_test_result(self, sender: AbstractTestModule, result):
        current_time = datetime.utcnow()
        with self.results_lock:
            self.results[str(sender)] = (current_time, result)

    def is_result_complete_and_identical(self):
        """
        判斷是否已收到來自所有 test module 的測試結果，且結果全部相同。
        若符合以上情況，傳回 True，否則傳回 False
        """
        with self.results_lock:
            return len(self.results) == len(self.known_modules) and (
                all(res[1] == "Pass" for res in self.results.values())
                or all(res[1] == "Fail" for res in self.results.values())
            )

    def start_bg_task(self) -> None:
        pass

    def stop_bg_task(self) -> None:
        pass

    @abstractmethod
    def receive_result(self, sender: AbstractTestModule, result: str) -> None:
        pass
