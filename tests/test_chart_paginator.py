import unittest
from pathlib import Path
from unittest.mock import Mock, call
from chart_paginator import ChartPaginator

from PIL import Image
import pyautogui

FIXTURES_DIR = Path(__file__).parent / Path('fixtures')

class TestChartPaginator(unittest.TestCase):

    def setUp(self):
        self._mock_gui_controller()
        self.paginator = ChartPaginator(self.mock_gui_controller)

    def tearDown(self):
        self.day1_screenshot.close()
        self.day2_screenshot.close()
        self.day3_screenshot.close()

    def _mock_gui_controller(self):
        self.mock_gui_controller = Mock(spec=pyautogui)
        self.day1_screenshot = Image.open(FIXTURES_DIR / Path('day1.png'))
        self.day2_screenshot = Image.open(FIXTURES_DIR / Path('day2.png'))
        self.day3_screenshot = Image.open(FIXTURES_DIR / Path('day3.png'))

        self.mock_gui_controller.screenshot.side_effect = [
            self.day1_screenshot,
            self.day2_screenshot,
            self.day3_screenshot
        ]

    def test_instantiates(self):
        self.assertIsInstance(self.paginator, ChartPaginator)

    def test_next_page_clicks_on_date_picker_widget(self):
        self.paginator.next_page()

        self.mock_gui_controller.click.assert_has_calls([call(2320, 58)])

    def test_next_page_clicks_on_expected_day_button(self):
        self.paginator.next_page()