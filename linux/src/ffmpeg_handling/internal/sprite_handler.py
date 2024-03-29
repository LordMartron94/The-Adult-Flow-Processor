import os
from pathlib import Path
from constants import CACHE_PATH
from src.ffmpeg_handling.internal.ffmpeg_command_helper import FFMPEGCommandHelper


class SpriteHandler:
	"""
	A class to handle the creation of sprites from videos.
	"""

	def __init__(self, command_helper: FFMPEGCommandHelper) -> None:
		self._command_helper: FFMPEGCommandHelper = FFMPEGCommandHelper()
		self._image_cache_path: Path = Path(CACHE_PATH, "Images")
		self.__pos_init__()

	def __pos_init__(self):
		if not Path(self._image_cache_path).is_dir():
			os.makedirs(self._image_cache_path)
		
		self._empty_image_cache()

	def _empty_image_cache(self):
		for file in os.listdir(self._image_cache_path):
			file_path = Path(self._image_cache_path, file)
			if file_path.is_file():
				os.remove(file_path)

	def _create_sprites_without_burn(self, video_file_path: str, video_duration: int):
		for i in range(1, 57):
			interval = int((i - 0.5) * video_duration / 56)

			tmp_image_path = Path(self._image_cache_path, f'image{i:02d}.png')

			cmd = [
				"ffmpeg",
				"-y",
				"-skip_frame",
				"nokey",
				"-ss",
				f"{interval}",
				"-i",
				f"{Path(video_file_path)}",
				"-vf",
				f"select='eq(pict_type,I)'",
				"-vframes",
				"1",
				f"{tmp_image_path}"
			]

			self._command_helper.execute_command(cmd)

	def _create_sprites_with_burn(self, video_file_path: str, video_duration: int):
		if video_duration is None:
			print("Error with spritesheet creation, skipping!")
			return

		for i in range(1, 57):
			interval = int((i - 0.5) * video_duration / 56)

			ttext = f"{interval // 3600:02d}\:{(interval % 3600) // 60:02d}\:{interval % 60:02d}"

			tmp_image_path = Path(self._image_cache_path, f'image{i:02d}.png')

			if not Path(video_file_path).is_file():
				print("ERROR! Path is not a file or not existent!!!")
				return

			cmd = [
				"ffmpeg",
				"-y",
				"-skip_frame",
				"nokey",
				"-ss",
				f"{interval}",
				"-i",
				f"{Path(video_file_path)}",
				"-vf",
				f"scale=1920:-1,select='eq(pict_type,I)',drawtext='text={ttext}:fontcolor=white:fontsize=156"
				f":fontfile=C\\:/Windows/Fonts/arial.ttf:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h-10)'",
				"-vframes",
				"1",
				f"{tmp_image_path}"
			]

			self._command_helper.execute_command(cmd)

	def create_sprites_from_video_file(self, video_file_path: str, video_duration: int, burn: bool):
		if burn:
			self._create_sprites_with_burn(video_file_path, video_duration)
		else:
			self._create_sprites_without_burn(video_file_path, video_duration)
