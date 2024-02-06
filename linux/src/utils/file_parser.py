from datetime import datetime

class FileParser:
    """A class for parsing file names and extracting date and time information."""

    def __init__(self):
        """Initialize the FileParser instance."""
        pass

    def extract_datetime_from_filename(self, filename: str) -> str:
        """
        Extract the datetime information from the given filename.

        Args:
            filename (str): The filename from which to extract datetime information.

        Returns:
            str: The extracted datetime information formatted as a string.

        Note:
            The expected filename format is "YYYY-MM-DD_HH-MM-SS_other_parts.ext".
        """
        parts = filename.split('_')
        if len(parts) >= 2:
            date_str, time_str = parts[-3], parts[-2]
            return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H-%M-%S")
        return None

    def extract_timestamp_from_filename(self, filename: str) -> str:
        """
        Extract the Unix timestamp from the given filename.

        Args:
            filename (str): The filename from which to extract the timestamp.

        Returns:
            str: The extracted Unix timestamp.

        Note:
            The expected filename format is "YYYY-MM-DD_HH-MM-SS_other_parts.ext".
        """
        parts = filename.split('_')
        if len(parts) >= 2:
            date_str, time_str = parts[-3], parts[-2]
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H-%M-%S")
            timestamp = (dt - datetime(1970, 1, 1)).total_seconds()  # Calculate seconds since Unix epoch
            return int(timestamp)
        return None
