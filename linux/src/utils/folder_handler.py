import os
from pathlib import Path

from src.utils.file_handler import FileHandler


class FolderHandler:
	def __init__(self) -> None:
		self._file_handler: FileHandler = FileHandler()

	def find_oldest_modified_date_in_folder(self, folder_path: str) -> float:
		"""Find the oldest modification date of files in the specified folder."""
		if not Path(folder_path).is_dir():
			return None

		mp4_files = [
			self._file_handler.get_file_modified_date(Path(folder_path, item))
			for item in os.listdir(folder_path) if self._file_handler.is_mp4_file(Path(folder_path, item))
		]

		return min(mp4_files, default=float('-inf'))
