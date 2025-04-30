import re
from datetime import datetime, timezone

import pytesseract

from log import logger


class OHLCVParser:

    # Sample input: 'UVIX 30 D 15m | D: 6/16/22, 11:15 AM | O: 1071 | H: 1084.5 | L: 1069 | C: 1078 | R: 15.5 | ¥: 783.77 | FPL: $5,199.50 | Volume | 2,426 | SimpleMovingAvg (CLOSE, 15, 0, no) | 1073.03'

    TOKEN_REGEXES = {
        'mm/dd/yy': r'.*D:\s*(\d+)/(\d+)/(\d+)',
        'hh[:;]mm ampm': r'.*D:.*,\s*(\d+)[:;i](\d+)\s*(AM|PM)',
        'open': r'.*[:;i]\s*(.*)',
        'high': r'.*[:;i]\s*(.*)',
        'low': r'.*[:;i]\s*(.*)',
        'close': r'.*[:;i]\s*(.*)',
        'volume': r'(.*)'
    }

    def __init__(self, image):
        text = pytesseract.image_to_string(image, lang='eng').strip()
        logger.info(f'Parsing OHLCV: {text}')
        self._tokenize(text)

    def _tokenize(self, text):
        text = text.replace('{', '|')
        text = text.replace('}', '|')
        text = text.replace(']', '|')
        text = text.replace('[', '|')
        text = text.replace('[|', '|')
        text = text.replace(']|', '|')
        text = text.replace('|[', '|')
        text = text.replace('|]', '|')
        self._tokens = [t.strip() for t in text.split('|')]

    def get_month(self):
        m = re.match(self.TOKEN_REGEXES['mm/dd/yy'], self._tokens[1])
        month = int(self._replace_misread_characters(m.group(1)))

        return month

    def get_day(self):
        m = re.match(self.TOKEN_REGEXES['mm/dd/yy'], self._tokens[1])
        day = int(self._replace_misread_characters(m.group(2)))

        return day

    def get_year(self):
        m = re.match(self.TOKEN_REGEXES['mm/dd/yy'], self._tokens[1])
        year = int(self._replace_misread_characters(m.group(3)))

        return year

    def get_hour(self):
        m = re.match(self.TOKEN_REGEXES['hh[:;]mm ampm'], self._tokens[1])
        hour = int(self._replace_misread_characters(m.group(1)))

        return hour

    def get_minute(self):
        m = re.match(self.TOKEN_REGEXES['hh[:;]mm ampm'], self._tokens[1])
        minute = int(self._replace_misread_characters(m.group(2)))

        return minute

    def get_second(self):
        return 0

    def get_ampm(self):
        m = re.match(self.TOKEN_REGEXES['hh[:;]mm ampm'], self._tokens[1])
        ampm = m.group(3)

        return ampm

    def get_open(self):
        m = re.match(self.TOKEN_REGEXES['open'], self._tokens[2])
        open = float(self._replace_misread_characters(m.group(1)))

        return open

    def get_high(self):
        m = re.match(self.TOKEN_REGEXES['high'], self._tokens[3])
        high = float(self._replace_misread_characters(m.group(1)))

        return high

    def get_low(self):
        m = re.match(self.TOKEN_REGEXES['low'], self._tokens[4])
        low = float(self._replace_misread_characters(m.group(1)))

        return low

    def get_close(self):
        m = re.match(self.TOKEN_REGEXES['close'], self._tokens[5])
        close = float(self._replace_misread_characters(m.group(1)))

        return close

    def get_volume(self):
        m = re.match(self.TOKEN_REGEXES['volume'], self._tokens[10])
        volume = int(self._replace_misread_characters(m.group(1).replace(',', '')))

        return volume

    def get_timestamp(self):
        timestamp = self._datetime_to_utc_timestamp(
            self.get_month(), self.get_day(), self.get_year(),
            self.get_hour(), self.get_minute(), self.get_second(),
            self.get_ampm()
        )

        timestamp_ms = int(timestamp * 1000)

        return timestamp_ms

    def is_past_last_ohlcv(self):
        return self._tokens[3] == 'Volume'

    def _datetime_to_utc_timestamp(self, month, day, year,
                                   hour, minute, second, am_pm):
        dt = datetime.strptime(
            f'{month:02} {day:02} {year:02} '
            f'{hour:02} {minute:02} {second:02} {am_pm}',
            '%m %d %y %I %M %S %p'
        )

        dt_utc = dt.replace(tzinfo=timezone.utc)
        timestamp = dt_utc.timestamp()

        return timestamp

    def _replace_misread_characters(self, text):
        text = text.replace('&', '8')
        text = text.replace('i', '1')
        text = text.replace('I', '1')
        text = text.replace(',', '.')

        return text

class RSIParser:

    # Sample input: '47.2149'
    PATTERN = r'[^\d]*(\d+[\.,]\d+)'

    def __init__(self, image):
        self.text = pytesseract.image_to_string(image, lang='eng').strip()
        logger.info(f'Parsing RSI: {self.text}')

    def get_rsi(self):
        m = re.match(self.PATTERN, self.text)

        if m is None:
            return

        g = m.groups()

        return float(g[0].replace(',', '.'))

class BufferingStatusParser:

    PATTERN = r'(.*)'

    def __init__(self, image):
        self.text = pytesseract.image_to_string(image, lang='eng').strip()

    def get_buffering_status(self):
        m = re.match(self.PATTERN, self.text)

        if m is None:
            return

        g = m.groups()

        return g[0]
