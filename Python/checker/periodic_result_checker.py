from threading import Timer
from .abstract_checker import AbstractChecker
from writer.excel_writer import ExcelWriter
from test_modules.abstract_test_module import AbstractTestModule


class PeriodicResultChecker(AbstractChecker):
    """
    Periodically checks if all test modules have the same result.
    """

    def __init__(self, result_writer: ExcelWriter):
        """
        Args:
        result_writer (ExcelWriter): The writer to write the result to.
        """
        super().__init__(result_writer)

        self.timer = None

        # interval is in seconds
        self.check_interval = 1.0

    def start_bg_task(self) -> None:
        """
        Starts the background task to perform periodically check.
        """
        self.timer = Timer(self.check_interval, self.check_and_record)
        self.timer.start()

    def stop_bg_task(self) -> None:
        """
        Stops the background task.
        """
        if self.timer:
            self.timer.cancel()

    def receive_result(self, sender: AbstractTestModule, result: str) -> None:
        """
        Saves the result from a test module for later comparison.
        """
        self.add_test_result(sender, result)

    def check_and_record(self):
        """
        Checks if all test modules have the same result, and record the result if conditions are met.
        """
        with self.results_lock:
            if self.is_result_complete_and_identical():
                times = [r[0] for r in self.results.values()]
                for sender, result in self.results.items():
                    self.result_writer.write(max(times), result)
        self.start_periodic_check()
