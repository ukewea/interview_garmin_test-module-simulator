from abc import ABC, abstractmethod
from typing import Callable, AnyStr
from threading import Event


class AbstractTestModule(ABC):
    """
    Abstract class for a test module.
    A test module performs test against specific component(s).
    """

    def __init__(
        self,
        judge: Callable[[AnyStr], None],
        receive_result: Callable[[AnyStr], None],
        stop_event: Event,
    ) -> None:
        self.judge = judge
        self.receive_result = receive_result
        self.stop_event = stop_event

    @abstractmethod
    def start_testing(self) -> None:
        pass
