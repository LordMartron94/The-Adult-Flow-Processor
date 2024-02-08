from datetime import timedelta
import os
from pathlib import Path
import pprint
import shutil
import time
from typing import Dict, List
from common.collection_extensions import CollectionExtensions

from constants import FINAL_DESTINATION_ROOT, MAX_DIFFERENCE_BETWEEN_SEGMENTS, MERGED_VIDEO_EXTENSION, ORIGINAL_LOCATION_PATH
from common.handlers.file_parser import FileParser
from src.ffmpeg_handling.ffmpeg_api import FFMPEGAPI
from common.handlers.file_handler import FileHandler
from common.time_format import TimeFormat
from common.time_utils import TimeUtils
from src.video_handler import VideoHandler


class ModelProcessor:
	"""
	A class that handles the processing of each model (folder).
	"""

	def __init__(self) -> None:
		self._api: FFMPEGAPI = FFMPEGAPI()
		self._file_handler: FileHandler = FileHandler()
		self._video_handler: VideoHandler = VideoHandler()
		self._time_utils: TimeUtils = TimeUtils()
		self._file_parser: FileParser = FileParser()

	def _sort_streams(self, segment_directory: str) -> List[str]:
		segments: Dict[str, float] = {}  # path : modified time

		for segment_path in os.listdir(Path(segment_directory)):
			segment_path = Path(segment_directory, segment_path).absolute()
			if not self._file_handler.is_mp4_file(segment_path):
				continue

			stream_start = self._file_parser.extract_datetime(segment_path.name)
			segments[segment_path] = stream_start
		
		sorted_segments = sorted(segments.items(), key=lambda item: item[1])
		sorted_paths = [path for path, _ in sorted_segments]
		return sorted_paths
	
	def _split_at_gaps(self, segments: list[str]) -> list:
		def gap_too_large(before, after) -> bool: 
			return self._video_handler.get_time_difference_between_videos(before, after) > MAX_DIFFERENCE_BETWEEN_SEGMENTS

		return list(
			CollectionExtensions.split_between(
				gap_too_large, 
				segments
			)
		)
	
	def _get_stream_output_path(self, stream_segments: list[Path], model_name: str) -> str:
		output_directory = Path(FINAL_DESTINATION_ROOT, model_name, "MERGED")

		if not Path(output_directory).is_dir():
			os.makedirs(output_directory, exist_ok=True)
		
		start_datetime = self._file_parser.extract_datetime(stream_segments[0].name).strftime('%Y-%m-%d %H:%M:%S')
		end_datetime = (self._file_parser.extract_datetime(stream_segments[-1].name) + timedelta(seconds=self._api.get_video_duration(stream_segments[-1]))).strftime('%Y-%m-%d %H:%M:%S')
		output_file_name = f'{model_name}, START {start_datetime}, END {end_datetime}{MERGED_VIDEO_EXTENSION}'.replace(':', '.')

		return Path(output_directory, output_file_name)
	
	def _handle_merge_failure(self, segments: list[str], merge_path: str):
		print(f"Error merging: '{merge_path}'! Will move to loose segments folder!")
		for segment in segments:
			self._move_to_loose_segments(segment, Path(merge_path).parent.joinpath("Loose Segments"))

	def _move_to_loose_segments(self, segments, loose_segment_directory_path):
		if not Path(loose_segment_directory_path).is_dir():
			os.makedirs(loose_segment_directory_path, exist_ok=True)

		for file in segments:
			contact_sheet = self._video_handler.get_accompanying_contact_sheet_path(file)
			try:
				print(f"Moving '{Path(file).name}' to 'Couldn't MERGE' directory.")

				shutil.move(file, Path(loose_segment_directory_path, Path(file).name))
				shutil.move(Path(contact_sheet), Path(loose_segment_directory_path, Path(contact_sheet).name))

				print(f"Moved '{Path(file).name}' to 'Couldn't MERGE' directory.")
			except Exception as e:
				print(f"Error while moving file '{Path(file).name}' to 'Couldn't MERGE' directory: {e}")
				raise e

	def _print_time_passed(self, start_time: float, end_time: float, model_name: str):
		elapsed_time = end_time - start_time
		formatted = self._time_utils.format_time(elapsed_time, TimeFormat.Dynamic)

		print(" ")
		print(f"It took {formatted} to merge all possible segments for model {model_name}.")    
		print(" ")
		print("=====================================")
		print(" ")

	def merge_model_streams(self, model_name: str, make_sprite_sheet: bool, burn_timestamps_in_sheet: bool, delete_original_files: bool):
		start_time = time.time()
		
		segment_directory: str = Path(ORIGINAL_LOCATION_PATH, model_name)
		sorted_segments: List[str] = self._sort_streams(segment_directory)

		if len(sorted_segments) < 1:
			end_time = time.time()
			self._print_time_passed(start_time, end_time, model_name)
			return

		organized_streams: List[List] = self._split_at_gaps(sorted_segments)
		pprint.pp(organized_streams)

		# exit()

		for stream in organized_streams:
			if len(stream) > 1:
				final_destination_path = self._get_stream_output_path(stream, model_name)
				self._api.merge_videos_together(stream, delete_original_files, final_destination_path, fail_function=self._handle_merge_failure)

				if make_sprite_sheet:
					self._api.create_contact_sheet_for_video(final_destination_path, burn_timestamps_in_sheet, str(final_destination_path).replace(MERGED_VIDEO_EXTENSION, '.png'))
				if delete_original_files:
					for segment in stream:
						self._video_handler.delete_spritesheet_for_video(segment)
			else:
				self._move_to_loose_segments(stream, Path(FINAL_DESTINATION_ROOT, model_name, "Loose Segments"))

		end_time = time.time()
		self._print_time_passed(start_time, end_time, model_name)
