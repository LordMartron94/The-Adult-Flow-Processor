from src.utils.time_format import TimeFormat
from src.utils.time_formatters.hms_formatter import HMSFormatter
from src.utils.time_formatters.ms_formatter import MSFormatter
from src.utils.time_formatters.s_formatter import SFormatter
from src.utils.time_formatters.time_formatter import ABCTimeFormatter


class TimeFormatterFactory:
    def create_time_formatter(self, format: TimeFormat) -> ABCTimeFormatter:
        if format == TimeFormat.HMS:
            return HMSFormatter()
        if format == TimeFormat.MS:
            return MSFormatter()
        if format == TimeFormat.S:
            return SFormatter()
        
        raise Exception(f"Format: '{format}' not yet implemented!")
