import time
import random
from .abstract_test_module import AbstractTestModule


class ManualTestModule(AbstractTestModule):
    """
    A test module that performs test manually.
    """

    def start_testing(self) -> None:
        """
        此項為模擬人手動測試的情況，因此隨機等待 3~10 秒後才會執行
        """
        while not self.stop_event.is_set():
            time.sleep(random.randint(3, 10))
            self.receive_result(self, "Pass" if self.judge(self, "") else "Fail")

    def __str__(self):
        return f"{self.__class__.__name__}"
