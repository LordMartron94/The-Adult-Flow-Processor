import os
from pathlib import Path
from typing import Callable
from constants import MERGED_VIDEO_EXTENSION
from src.utility.video_factory import VideoFactory
from src.model.video_model import VideoModel
from src.utility.template_parser import TemplateParser
from src.ffmpeg_handling.ffmpeg_api import FFMPEGAPI

from src.video_handler import VideoHandler


class StreamMerger:
	"""Class responsible for merging model streams together."""
	def __init__(self, 
			  ffmpeg_api: FFMPEGAPI,
			  video_handler: VideoHandler, 
			  video_factory: VideoFactory,
			  template_parser: TemplateParser,
			  move_to_loose_segments: Callable[[list[str], str], None],
		) -> None:
		self._api: FFMPEGAPI = ffmpeg_api
		self._video_handler: VideoHandler = video_handler
		self._move_to_loose_segments: Callable[[list[str], str, str], None] = move_to_loose_segments
		self._template_parser: TemplateParser = template_parser
		self._video_factory: VideoFactory = video_factory

	def _get_stream_output_path(self, stream_segments: list[Path], model_name: str) -> Path:
		# Set the output directory path
		stream: VideoModel = self._video_factory.create_stream(model_name, stream_segments[0], stream_segments[1])

		output_directory: Path = self._template_parser.get_output_directory_for_video(stream)
		output_name: str = self._template_parser.get_merge_name(stream)

		# Create the output directory if it doesn't exist
		if not output_directory.is_dir():
			os.makedirs(output_directory, exist_ok=True)

		# Combine the output directory and file name to get the full output path
		return Path(output_directory, output_name + MERGED_VIDEO_EXTENSION)

	def _handle_merge_failure(self, segments: list[str], merge_path: str, model_name: str):
		print(f"Error merging: '{merge_path}'! Will move to loose segments folder!")
		for segment in segments:
			self._move_to_loose_segments(segment, merge_path, model_name)

	def merge_stream(self, segments: list[Path], model_name: str, make_sprite_sheet: bool, burn_timestamps_in_sheet: bool, delete_original_files: bool):
		final_destination_path = self._get_stream_output_path(segments, model_name)

		print(f"Merging from {segments[0].name} until {segments[-1].name}! -- Going to: {final_destination_path}!")

		self._api.merge_videos_together(segments, delete_original_files, final_destination_path, model_name=model_name, fail_function=self._handle_merge_failure)

		if make_sprite_sheet:
			self._api.create_contact_sheet_for_video(
				final_destination_path, 
				burn_timestamps_in_sheet, 
				str(final_destination_path).replace(MERGED_VIDEO_EXTENSION, '.png')
			)
		if delete_original_files:
			for segment in segments:
				self._video_handler.delete_spritesheet_for_video(segment)
