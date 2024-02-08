import os
from pathlib import Path
from typing import Dict, List
from common.handlers.file_parser import FileParser


class SegmentSorter:
	"""Stream sorter algorithm class."""
	def __init__(self, file_parser: FileParser) -> None:
		self._file_parser: FileParser = file_parser

	def sort_segments(self, segment_directory: Path) -> List[Path]:
		"""
		Organizes segments based on their start datetime in ascending order.
		"""
		segments: Dict[Path, float] = {}  # path : start date time

		for segment_path in os.listdir(Path(segment_directory)):
			segment_path = Path(segment_directory, segment_path).absolute()
			if not self._file_handler.is_mp4_file(segment_path):
				continue

			stream_start = self._file_parser.extract_datetime(segment_path.name)
			segments[segment_path] = stream_start
		
		sorted_segments = sorted(segments.items(), key=lambda item: item[1])
		sorted_paths = [path for path, _ in sorted_segments]
		return sorted_paths