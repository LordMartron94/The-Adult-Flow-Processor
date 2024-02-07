from src.utils.time_formatters.time_formatter import ABCTimeFormatter


class SFormatter(ABCTimeFormatter):
    """Formats time based on the SS format."""
    def format(self, total_seconds: int, round_digits: int) -> str:
        if round_digits is not None:
            seconds = round(total_seconds, round_digits)
        else:
            seconds = total_seconds
        format_string = "{:0." + str(round_digits) + "f}S"
        return format_string.format(seconds)
