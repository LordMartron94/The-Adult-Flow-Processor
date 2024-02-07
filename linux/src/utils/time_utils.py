from enum import Enum

class TimeFormat(Enum):
	Dynamic = 'Dynamic'
	HMS = 'HMS'
	MS = 'MS'
	S = 'S'

class TimeFormatter:
    """
    A class responsible for formatting time strings based on the specified format and digits.
    """

    @staticmethod
    def format_hours_minutes_seconds(total_seconds, hour_digits=2, minute_digits=2, second_digits=2, round_digits=None):
        hours = int(total_seconds / 3600)
        remaining_seconds = total_seconds % 3600
        minutes = int(remaining_seconds / 60)
        if round_digits is not None:
            seconds = round(remaining_seconds % 60, round_digits)
        else:
            seconds = remaining_seconds % 60
        format_string = "{:0" + str(hour_digits) + "d}H:{:0" + str(minute_digits) + "d}M:{:0." + str(round_digits) + "f}S"
        return format_string.format(hours, minutes, seconds)

    @staticmethod
    def format_minutes_seconds(total_seconds, minute_digits=2, second_digits=2, round_digits=None):
        minutes = int(total_seconds / 60)
        if round_digits is not None:
            seconds = round(total_seconds % 60, round_digits)
        else:
            seconds = total_seconds % 60
        format_string = "{:0" + str(minute_digits) + "d}M:{:0." + str(round_digits) + "f}S"
        return format_string.format(minutes, seconds)

    @staticmethod
    def format_seconds(total_seconds, second_digits=2, round_digits=None):
        if round_digits is not None:
            seconds = round(total_seconds, round_digits)
        else:
            seconds = total_seconds
        format_string = "{:0." + str(round_digits) + "f}S"
        return format_string.format(seconds)

class TimeUtils:
	"""
	A utility class for formatting time.
	"""

	def __init__(self):
		self._formatters = {
			TimeFormat.Dynamic: self._format_dynamic,
			TimeFormat.HMS: TimeFormatter.format_hours_minutes_seconds,
			TimeFormat.MS: TimeFormatter.format_minutes_seconds,
			TimeFormat.S: TimeFormatter.format_seconds
		}

	def format_time(self, total_seconds: int, time_format: TimeFormat=TimeFormat.HMS, **kwargs):
		"""
		Formats the given total seconds into hours, minutes, and seconds based on the selected format.

		Args:
			total_seconds (int): The total number of seconds.
			time_format (TimeFormat): The format type to use. Default is TimeFormat.HMS.
			**kwargs: Additional keyword arguments for specifying digits. (defaults to 2 for each)
				- hour_digits (int, optional): Number of digits for hours.
				- minute_digits (int, optional): Number of digits for minutes.
				- second_digits (int, optional): Number of digits for seconds.
				- round_digits (int, optional): Number of digits to round seconds to.

		Returns:
			str: A string representing the formatted time.

		Raises:
			ValueError: If the specified format type is invalid.

		Example:
			>>> time_utils = TimeUtils()
			>>> formatted_time = time_utils.format_time(3665, TimeFormat.HMS, hour_digits=1, minute_digits=1, second_digits=1)
			'1H:1M:5S'
		"""
		formatter = self._formatters.get(time_format)
		if formatter is None:
			raise ValueError(f"Invalid format type. Available options: {', '.join(f.value for f in TimeFormat)}")

		return formatter(total_seconds, **kwargs)


	def _format_dynamic(self, total_seconds, **kwargs):
		if total_seconds >= 3600:
			return TimeFormatter.format_hours_minutes_seconds(total_seconds, **kwargs)
		if total_seconds >= 60:
			return TimeFormatter.format_minutes_seconds(total_seconds, **kwargs)
		return TimeFormatter.format_seconds(total_seconds, **kwargs)
