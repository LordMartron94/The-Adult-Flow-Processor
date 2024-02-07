from src.utils.time_formatters.time_formatter import ABCTimeFormatter


class HMSFormatter(ABCTimeFormatter):
    """Formats time based on the HH:MM:SS format."""
    def format(self, total_seconds: int, round_digits: int) -> str:
        hours = int(total_seconds / 3600)
        remaining_seconds = total_seconds % 3600
        minutes = int(remaining_seconds / 60)
        if round_digits is not None:
            seconds = round(remaining_seconds % 60, round_digits)
        else:
            seconds = remaining_seconds % 60
        format_string = "{:02" + "d}H:{:02" + "d}M:{:0." + str(round_digits) + "f}S"
        return format_string.format(hours, minutes, seconds)
