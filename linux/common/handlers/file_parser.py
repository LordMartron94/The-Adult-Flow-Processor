from datetime import datetime
from pathlib import Path
import re
from typing import Union

class FileParser:
    """A class for parsing file names."""
    def _validate_range(self, day: int, month: int) -> bool:
        return 1 <= day <= 31 and 1 <= month <= 12
    
    def _look_for_match(self, filename: str) -> Union[str, None]:
        datetime_patterns = [
            r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})_(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<second>\d{2})',  # yyyy-mm-dd_HH-mm-ss
            r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_(?P<hour>\d{2})(?P<minute>\d{2})',  # yyyyMMdd_HHmm
            r'(?P<day>\d{2})(?P<month>\d{2})(?P<year>\d{4})_(?P<hour>\d{2})(?P<minute>\d{2})',  # ddMMyyyy_HHmm
            r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})',               # yyyy-mm-dd
            r'(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})',               # dd-mm-yyyy
            r'(?P<year>\d{4})_(?P<month>\d{2})_(?P<day>\d{2})',               # yyyy_mm_dd
            r'(?P<day>\d{2})_(?P<month>\d{2})_(?P<year>\d{4})',               # dd_mm_yyyy
            r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})',                 # yyyyMMdd
            r'(?P<day>\d{2})(?P<month>\d{2})(?P<year>\d{4})',                 # ddMMyyyy
        ]
        
        for pattern in datetime_patterns:
            match = re.search(pattern, filename)
            if match: return match

        return None

    def _process_match(self, match: str) -> datetime:
            groups = match.groupdict()
            year, month, day = int(groups['year']), int(groups['month']), int(groups['day'])
            hour, minute, second = 0, 0, 0
            if 'hour' in groups:
                hour = int(groups['hour'])
            if 'minute' in groups:
                minute = int(groups['minute'])
            if 'second' in groups:
                second = int(groups['second'])

            if self._validate_range(day, month):
                try:
                    return datetime(year, month, day, hour, minute, second)
                except ValueError as ve:
                    raise Exception(f"Something went wrong while processing the filename!\n{ve}")

    def extract_datetime(self, filename: str) -> Union[None, datetime]:
        pattern_match: Union[str, None] = self._look_for_match(filename)

        if pattern_match:
            return self._process_match(pattern_match)

        return None
