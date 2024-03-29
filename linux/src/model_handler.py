from datetime import datetime
import os
from pathlib import Path
from typing import List

from common.handlers.file_handler import FileHandler
from common.handlers.file_parser import FileParser


class ModelHandler:
	def __init__(self, file_parser: FileParser, file_handler: FileHandler) -> None:
		self._file_parser: FileParser = file_parser
		self._file_handler: FileHandler = file_handler
	
	def find_oldest_segment_in_folder(self, folder_path: str) -> datetime:
		"""Finds the oldest stream segment in the model folder based on the start dates of each video."""
		if not Path(folder_path).is_dir():
			raise Exception(f"This folder path does not exist!: {folder_path}")
		
		try:
			segments = [
				self._file_parser.extract_datetime(item) 
				for item in os.listdir(folder_path) 
				if self._file_handler.is_mp4_file(Path(folder_path, item)) or self._file_handler.is_ts_file(Path(folder_path, item))
			]
		except Exception as e:
			print("Error with folder: ", e)
			return datetime(year=1, month=1, day=1)
			

		if len(segments) < 1:
			return datetime(year=1, month=1, day=1)

		return min(segments)

	def get_segment_paths(self, model_path: str, file_extension: str=".mp4") -> List[Path]:
		return self._file_handler.get_children_paths(model_path, file_extension)


