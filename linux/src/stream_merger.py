import os
from pathlib import Path
from typing import Callable
from constants import MERGED_VIDEO_EXTENSION
from src.model.stream_model import StreamModel
from src.utility.template_parser import TemplateParser
from src.ffmpeg_handling.ffmpeg_api import FFMPEGAPI

from src.video_handler import VideoHandler


class StreamMerger:
	"""Class responsible for merging model streams together."""
	def __init__(self, 
			  ffmpeg_api: FFMPEGAPI,
			  video_handler: VideoHandler, 
			  template_parser: TemplateParser,
			  move_to_loose_segments: Callable[[list[Path], Path], None],
		) -> None:
		self._api: FFMPEGAPI = ffmpeg_api
		self._video_handler: VideoHandler = video_handler
		self._move_to_loose_segments: Callable[[list[Path], Path, str], None] = move_to_loose_segments
		self._template_parser: TemplateParser = template_parser

	def _get_stream_output_path(self, stream: StreamModel) -> Path:
		output_directory: Path = self._template_parser.get_output_directory_for_video(stream)

		if not output_directory.is_dir():
			os.makedirs(output_directory, exist_ok=True)

		return Path(output_directory, stream.merged_name + MERGED_VIDEO_EXTENSION)

	def _handle_merge_failure(self, segments: list[Path], merge_path: Path, model_name: str):
		for segment in segments:
			self._move_to_loose_segments(segment, merge_path.parent.absolute, model_name)

	def merge_stream(self, stream: StreamModel, make_sprite_sheet: bool, burn_timestamps_in_sheet: bool, delete_original_files: bool):
		final_destination_path = self._get_stream_output_path(stream)

		print(f"Merging from {stream.segments[0].path.name} until {stream.segments[-1].path.name}! -- Going to: {final_destination_path}!")

		segment_paths = [segment.path for segment in stream.segments]

		self._api.merge_videos_together(segment_paths, delete_original_files, final_destination_path, model_name=stream.model_name, fail_function=self._handle_merge_failure)

		if make_sprite_sheet:
			self._api.create_contact_sheet_for_video(
				final_destination_path, 
				burn_timestamps_in_sheet, 
				str(final_destination_path).replace(MERGED_VIDEO_EXTENSION, '.png')
			)

		if delete_original_files:
			for segment in stream.segments:
				self._video_handler.delete_spritesheet_for_video(segment)
