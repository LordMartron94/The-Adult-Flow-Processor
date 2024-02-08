import os
from pathlib import Path
from typing import Callable, List, Union

from src.ffmpeg_handling.internal.ffmpeg_command_helper import FFMPEGCommandHelper
from src.ffmpeg_handling.internal.spritesheet_handler import SpritesheetHandler
from src.ffmpeg_handling.internal.video_handler import VideoHandler

class FFMPEGAPI:
	"""
	Custom layer built on top of the FFMPEG CLI to allow for easier interaction in other parts of the software.
	"""

	def __init__(self):
		self._command_helper: FFMPEGCommandHelper = FFMPEGCommandHelper()
		self._spritesheet_handler: SpritesheetHandler = SpritesheetHandler(self._command_helper)
		self._video_handler: VideoHandler = VideoHandler(self._command_helper)

	def merge_videos_together(
			self,
			video_paths_in_sequence: list[str],
			delete_original_files: bool,
			output_file_path: str,
			fail_function: Callable[[List[str], str, str], None],
			model_name: str):
		merge_successful: bool = self._video_handler.merge_stream_segments(video_paths_in_sequence, output_file_path)
		
		if not merge_successful:
			fail_function(video_paths_in_sequence, output_file_path, model_name)
			return

		if delete_original_files:
			for file_path in video_paths_in_sequence:
				if Path(file_path).is_file():
					os.remove(file_path)

	def create_contact_sheet_for_video(
			self, 			
			video_file_path: str, 
			burn_time_stamps_into_sheet: bool,
			output_image_path: str):
		video_duration = self._video_handler.get_video_duration(video_file_path)
		self._spritesheet_handler.create_spritesheet_from_video_file(
			video_file_path, 
			video_duration, 
			burn_time_stamps_into_sheet, 
			output_image_path
		)

	def get_video_duration(self, video_file_path: str) -> Union[float, None]:
		return self._video_handler.get_video_duration(video_file_path)
	
	def video_valid(self, video_file_path: Path, robust_check=False) -> bool:
		"""
		Checks if a video file is valid through ffprobe. Returns true if valid.
		Set robust_check to True if you want a more time consuming but robust video check.
		"""
		return self._video_handler.video_valid(video_file_path, robust_check)
