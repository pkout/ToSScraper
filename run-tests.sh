#!/bin/bash

DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

coverage run -m unittest discover --verbose -s tests
# coverage run -m unittest tests.test_candle_scraper.TestCandleScraper
# python -m unittest tests.test_candle_scraper.TestCandleScraper
coverage report -m