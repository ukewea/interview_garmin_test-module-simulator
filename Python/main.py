import datetime as dt
import time
from threading import Thread, Event
from test_modules import AbstractTestModule, AutoTestModule, ManualTestModule
from checker import AbstractChecker, RecentResultChecker, PeriodicResultChecker
from writer import ExcelWriter
from typing import List
import random
import logging


def setup_custom_logger(name):
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def judge_pass_fail(sender: AbstractTestModule, raw_data: str) -> bool:
    """
    Determines a generated data pass or fail.

    Returns:
    bool: True if the result is good, False otherwise.
    """
    return True if random.randint(0, 1) else False
    # return True


logger = setup_custom_logger("root")
logger.setLevel(level=logging.DEBUG)

logger.info("Starting...")

# event to tell test modules to stop
stop_event = Event()

# writer writes test result to Excel spreadsheet
result_writer = ExcelWriter("./test_result.xlsx")

# checker receives result from test modules then do addtional checks before passing text to writer
checker: AbstractChecker = RecentResultChecker(result_writer, stop_event)

# these modules perform test against specific component(s)
test_modules: List[AbstractTestModule] = [
    # auto test module
    AutoTestModule(judge_pass_fail, checker.receive_result, stop_event, 0.5),
    # auto test module extra
    AutoTestModule(judge_pass_fail, checker.receive_result, stop_event, 1.8),
    # manual test module
    ManualTestModule(judge_pass_fail, checker.receive_result, stop_event),
]
logger.debug(f"Initialized {len(test_modules)} test modules")

test_threads = [Thread(target=m.start_testing, daemon=True) for m in test_modules]

try:
    for m in test_modules:
        checker.register_test_module(m)

    checker.start_bg_task()

    # start testing
    for t in test_threads:
        t.start()

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Exiting...")
    stop_event.set()

    for t in test_threads:
        t.join(timeout=5)

    checker.stop_bg_task()

    for m in test_modules:
        checker.unregister_test_module(m)

    logging.info("Exited")
