from datetime import timedelta
import os
from pathlib import Path
from typing import Callable
from constants import FINAL_DESTINATION_ROOT, MERGED_VIDEO_EXTENSION
from common.handlers.file_parser import FileParser
from src.ffmpeg_handling.ffmpeg_api import FFMPEGAPI

from src.video_handler import VideoHandler


class StreamMerger:
	"""Class responsible for merging model streams together."""
	def __init__(self, 
			  ffmpeg_api: FFMPEGAPI,
			  video_handler: VideoHandler, 
			  file_parser: FileParser,
			  move_to_loose_segments: Callable[[list[str], str], None],
		) -> None:
		self._file_parser: FileParser = file_parser
		self._api: FFMPEGAPI = ffmpeg_api
		self._video_handler: VideoHandler = video_handler
		self._move_to_loose_segments: Callable[[list[str], str], None] = move_to_loose_segments

	def _get_stream_output_path(self, stream_segments: list[Path], model_name: str) -> str:
		# Set the output directory path
		output_directory = Path(FINAL_DESTINATION_ROOT, model_name, "MERGED")

		# Create the output directory if it doesn't exist
		if not output_directory.is_dir():
			os.makedirs(output_directory, exist_ok=True)

		# Extract start and end datetimes from the stream segments
		start_datetime = self._file_parser.extract_datetime(stream_segments[0].name).strftime('%Y-%m-%d %H:%M:%S')
		end_datetime = (self._file_parser.extract_datetime(stream_segments[-1].name) + timedelta(seconds=self._api.get_video_duration(stream_segments[-1]))).strftime('%Y-%m-%d %H:%M:%S')
		
		# Format the output file name
		output_file_name = f'{model_name}, START {start_datetime}, END {end_datetime}{MERGED_VIDEO_EXTENSION}'.replace(':', '.')

		# Combine the output directory and file name to get the full output path
		return Path(output_directory, output_file_name)


	def _handle_merge_failure(self, segments: list[str], merge_path: str):
		print(f"Error merging: '{merge_path}'! Will move to loose segments folder!")
		for segment in segments:
			self._move_to_loose_segments(segment, Path(merge_path).parent.joinpath("Loose Segments"))

	def merge_stream(self, segments: list[Path], model_name: str, make_sprite_sheet: bool, burn_timestamps_in_sheet: bool, delete_original_files: bool):
		final_destination_path = self._get_stream_output_path(segments, model_name)
		self._api.merge_videos_together(segments, delete_original_files, final_destination_path, fail_function=self._handle_merge_failure)

		if make_sprite_sheet:
			self._api.create_contact_sheet_for_video(
				final_destination_path, 
				burn_timestamps_in_sheet, 
				str(final_destination_path).replace(MERGED_VIDEO_EXTENSION, '.png')
			)
		if delete_original_files:
			for segment in segments:
				self._video_handler.delete_spritesheet_for_video(segment)
