from datetime import datetime
from pathlib import Path
import re
from typing import Union

class FileParser:
    """A class for parsing file names."""        
    def extract_datetime(self, filename: str) -> Union[None, datetime]:
        # Define a list of common datetime patterns to match against
        datetime_patterns = [
            r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})',  # yyyy-mm-dd_HH-mm-ss
            r'(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})',  # yyyyMMdd_HHmm
            r'(\d{2})(\d{2})(\d{4})_(\d{2})(\d{2})',  # ddMMyyyy_HHmm
            r'(\d{4})-(\d{2})-(\d{2})',               # yyyy-mm-dd
            r'(\d{2})-(\d{2})-(\d{4})',               # dd-mm-yyyy
            r'(\d{4})_(\d{2})_(\d{2})',               # yyyy_mm_dd
            r'(\d{2})_(\d{2})_(\d{4})',               # dd_mm_yyyy
            r'(\d{4})(\d{2})(\d{2})',                 # yyyyMMdd
            r'(\d{2})(\d{2})(\d{4})',                 # ddMMyyyy
        ]

        # Try matching each pattern against the filename
        for pattern in datetime_patterns:
            match = re.search(pattern, filename)
            if match:
                groups = match.groups()
                # Try to parse the extracted groups into a datetime object
                try:
                    return datetime(*map(int, groups))
                except ValueError:
                    continue
        # Return None if no datetime information is found
        return None
