from common.time_format import TimeFormat
from common.time_formatter_factory import TimeFormatterFactory
from common.time_formatters.time_formatter import ABCTimeFormatter

class TimeUtils:
	"""
	A utility class for formatting time.
	"""

	def __init__(self):
		self._formatter_factory: TimeFormatterFactory = TimeFormatterFactory()

	def format_time(self, total_seconds: int, time_format: TimeFormat=TimeFormat.HMS, round_digits=4) -> str:
		"""
		Formats the given total seconds into hours, minutes, and seconds based on the selected format.

		Args:
			total_seconds (int): The total number of seconds.
			time_format (TimeFormat): The format type to use. Default is TimeFormat.HMS.
			round_digits (int): The amount of digits to round seconds to. Defaults to 4.

		Returns:
			str: A string representing the formatted time.

		Raises:
			ValueError: If the specified format type is invalid.
		"""
		if time_format == TimeFormat.Dynamic:
			return self._format_dynamic(total_seconds, round_digits)

		formatter: ABCTimeFormatter = self._formatter_factory.create_time_formatter(time_format)
		return formatter.format(total_seconds, round_digits)


	def _format_dynamic(self, total_seconds: int, round_digits: int) -> str:
		if total_seconds >= 3600:
			return self._formatter_factory.create_time_formatter(TimeFormat.HMS).format(total_seconds, round_digits)
		if total_seconds >= 60:
			return self._formatter_factory.create_time_formatter(TimeFormat.MS).format(total_seconds, round_digits)
		return self._formatter_factory.create_time_formatter(TimeFormat.S).format(total_seconds, round_digits)
