import unittest
import unittest.mock as mock
from .recent_result_checker import RecentResultChecker
from test_modules.abstract_test_module import AbstractTestModule
from writer.excel_writer import ExcelWriter
import threading

class TestRecentResultChecker(unittest.TestCase):
    def setUp(self):
        stop_event = threading.Event()
        self.mock_writer = mock.create_autospec(spec=ExcelWriter)
        self.checker = RecentResultChecker(self.mock_writer, stop_event)

    def test_receive_result_with_unregistered_module(self):
        mock_sender1 = mock.create_autospec(spec=AbstractTestModule)
        mock_sender2 = mock.create_autospec(spec=AbstractTestModule)
        self.checker.register_test_module(mock_sender1)

        self.checker.receive_result(mock_sender1, "Fail")

        def add_result_from_unknown_sender():
            self.checker.receive_result(mock_sender2, "Fail")

        self.assertRaises(Exception, add_result_from_unknown_sender)

    def test_receive_result_with_incomplete_results(self):
        mock_sender1 = mock.create_autospec(spec=AbstractTestModule)
        mock_sender2 = mock.create_autospec(spec=AbstractTestModule)
        self.checker.register_test_module(mock_sender1)
        self.checker.register_test_module(mock_sender2)

        self.checker.receive_result(mock_sender1, "Fail")

        self.assertFalse(self.checker.is_result_complete_and_identical())

    def test_receive_result_with_complete_but_different_results(self):
        mock_sender1 = mock.create_autospec(spec=AbstractTestModule)
        mock_sender2 = mock.create_autospec(spec=AbstractTestModule)
        self.checker.register_test_module(mock_sender1)
        self.checker.register_test_module(mock_sender2)

        self.checker.receive_result(mock_sender1, "Pass")
        self.checker.receive_result(mock_sender2, "Fail")

        self.assertFalse(self.checker.is_result_complete_and_identical())
        self.mock_writer.write.assert_not_called()

    def test_receive_result_with_complete_and_same_results(self):
        mock_sender1 = mock.create_autospec(spec=AbstractTestModule)
        mock_sender2 = mock.create_autospec(spec=AbstractTestModule)
        self.checker.register_test_module(mock_sender1)
        self.checker.register_test_module(mock_sender2)

        self.checker.receive_result(mock_sender1, "Pass")
        self.checker.receive_result(mock_sender2, "Pass")

        self.assertTrue(self.checker.is_result_complete_and_identical())
        self.mock_writer.write.assert_called()
