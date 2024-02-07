from src.utils.time_formatters.time_formatter import ABCTimeFormatter


class MSFormatter(ABCTimeFormatter):
    """Formats time based on the MM:SS format."""
    def format(self, total_seconds: int, round_digits: int) -> str:
        minutes = int(total_seconds / 60)
        if round_digits is not None:
            seconds = round(total_seconds % 60, round_digits)
        else:
            seconds = total_seconds % 60
        format_string = "{:02" + "d}M:{:0." + str(round_digits) + "f}S"
        return format_string.format(minutes, seconds)
