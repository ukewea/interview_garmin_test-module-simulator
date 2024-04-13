from .abstract_checker import AbstractChecker
from writer.excel_writer import ExcelWriter
from test_modules.abstract_test_module import AbstractTestModule
from datetime import datetime


class RecentResultChecker(AbstractChecker):
    """
    Checks if latest test result from all test modules have the same result.
    """

    def receive_result(self, sender: AbstractTestModule, result: str) -> None:
        if self.stop_event.is_set():
            self.logger.warn("receive_result() called while stop_event is set")
            return

        if sender not in self.known_modules:
            raise Exception("test result sent from an unknown test module")

        self.logger.debug(f"{datetime.now()} --> Received Result: {result}; from {sender}")

        with self.results_lock:
            self.add_test_result(sender, result)
            if self.is_result_complete_and_identical():
                self.logger.info(f"all test results are `{result}`, output to writer")
                times = [r[0] for r in self.results.values()]
                self.result_writer.write(max(times), result)
