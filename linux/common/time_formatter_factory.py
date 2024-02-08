from common.time_format import TimeFormat
from common.time_formatters.hms_formatter import HMSFormatter
from common.time_formatters.ms_formatter import MSFormatter
from common.time_formatters.s_formatter import SFormatter
from common.time_formatters.time_formatter import ABCTimeFormatter


class TimeFormatterFactory:
    def create_time_formatter(self, format: TimeFormat) -> ABCTimeFormatter:
        if format == TimeFormat.HMS:
            return HMSFormatter()
        if format == TimeFormat.MS:
            return MSFormatter()
        if format == TimeFormat.S:
            return SFormatter()
        
        raise Exception(f"Format: '{format}' not yet implemented!")
