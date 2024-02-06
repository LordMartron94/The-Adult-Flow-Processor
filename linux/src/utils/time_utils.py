from enum import Enum

class TimeFormat(Enum):
    """
    - Dynamic: formats in the smallest possible way.
    - HMS: formats as HH:MM:SS
    - MS: formats as MM:SS
    - S: formats as SS
    """
    Dynamic = 'Dynamic'
    HMS = 'HMS'
    MS = 'MS'
    S = 'S'

class TimeUtils:
    """
    A utility class for formatting time.
    """

    def __init__(self):
        self._formatters = {
            TimeFormat.Dynamic: self._format_dynamic,
            TimeFormat.HMS: self._format_hours_minutes_seconds,
            TimeFormat.MS: self._format_minutes_seconds,
            TimeFormat.S: self._format_seconds
        }

    def format_time(self, total_seconds: int, time_format: TimeFormat=TimeFormat.HMS):
        """
        Formats the given total seconds into hours, minutes, and seconds based on the selected format.

        Args:
            total_seconds (int): The total number of seconds.
            time_format (str): The format type to use. Default is 'HMS'.

        Returns:
            str: A string representing the formatted time.
        """
        formatter = self._formatters.get(time_format)
        if formatter is None:
            raise ValueError(f"Invalid format type. Available options: {', '.join(f.value for f in TimeFormat)}")
        
        return formatter(total_seconds)
    
    def _format_dynamic(self, total_seconds):
        if total_seconds >= 3600:
            return self._format_hours_minutes_seconds(total_seconds)
        if total_seconds >= 60:
            return self._format_minutes_seconds(total_seconds)
        return self._format_seconds(total_seconds)

    def _format_hours_minutes_seconds(self, total_seconds):
        hours = int(total_seconds / 3600)
        remaining_seconds = total_seconds % 3600
        minutes = int(remaining_seconds / 60)
        seconds = int(remaining_seconds % 60)
        return f"{hours:02d}H:{minutes:02d}M:{seconds:02d}S"

    def _format_minutes_seconds(self, total_seconds):
        minutes = int(total_seconds / 60)
        seconds = int(total_seconds % 60)
        return f"{minutes:02d}M:{seconds:02d}S"

    def _format_seconds(self, total_seconds):
        return f"{total_seconds}S"
