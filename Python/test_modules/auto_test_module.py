import time
from .abstract_test_module import AbstractTestModule
from typing import Callable, AnyStr, Union
from threading import Event


class AutoTestModule(AbstractTestModule):
    """
    A test module that performs test automatically.
    """

    def __init__(
        self,
        judge: Callable[[AnyStr], None],
        receive_result: Callable[[AnyStr], None],
        stop_event: Event,
        test_interval: Union[int, float],
    ) -> None:
        super().__init__(judge, receive_result, stop_event)
        self.test_interval = test_interval

    def start_testing(self) -> None:
        """
        Simulates an automatic test, thus it spit outs a result regularly.
        """
        while not self.stop_event.is_set():
            time.sleep(self.test_interval)
            self.receive_result(self, "Pass" if self.judge(self, "") else "Fail")

    def __str__(self):
        return f"{self.__class__.__name__} with {self.test_interval}s interval"
