from pathlib import Path
from typing import List
from common.collection_extensions import CollectionExtensions
from common.handlers.file_parser import FileParser
from constants import MAX_DIFFERENCE_BETWEEN_SEGMENTS
from common.handlers.file_handler import FileHandler
from src.video_handler import VideoHandler
from src.segment_sorter import SegmentSorter


class SegmentOrganizer:
	"""Class responsible for organizing a model's segments."""
	def __init__(self, file_parser: FileParser, video_handler: VideoHandler, file_handler: FileHandler) -> None:
		self._segment_sorter: SegmentSorter = SegmentSorter(file_parser, file_handler)
		self._video_handler: VideoHandler = video_handler

	def _split_at_gaps(self, segments: List[Path]) -> List[List[Path]]:
		def gap_too_large(before, after) -> bool: 
			return self._video_handler.get_time_difference_between_videos(before, after) > MAX_DIFFERENCE_BETWEEN_SEGMENTS

		return list(
			CollectionExtensions.split_between(
				gap_too_large, 
				segments
			)
		)
	
	def organize(self, model_directory: Path) -> List[List[Path]]:
		"""Organizes the model's segments into a list of streams.
		Each stream is a list of segments in order of start datetime.
		"""
		sorted_segments: List[Path] = self._segment_sorter.sort_segments(model_directory)
		return self._split_at_gaps(sorted_segments)


