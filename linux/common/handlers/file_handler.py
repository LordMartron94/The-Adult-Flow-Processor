import os
from pathlib import Path


class FileHandler:
	"""
	Class made to make working with the files created by CTBREC easier.
	"""

	def is_mp4_file(self, file):
		"""Check if the file has a .mp4 extension."""
		return Path(file).is_file() and str(file).lower().endswith('.mp4')

	def get_file_modified_date(self, file_path: str) -> float:
		"""Get the modification time of a file."""
		return os.path.getmtime(file_path)
