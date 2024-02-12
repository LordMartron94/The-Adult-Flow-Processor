import os
from pathlib import Path
from constants import CACHE_PATH
from src.ffmpeg_handling.internal.ffmpeg_command_helper import FFMPEGCommandHelper
from src.ffmpeg_handling.internal.sprite_handler import SpriteHandler


class SpritesheetHandler:
	"""
	A class designed to handle the creation of spritesheets from videos.
	"""

	def __init__(self, command_helper: FFMPEGCommandHelper) -> None:
		self._command_helper: FFMPEGCommandHelper = FFMPEGCommandHelper()
		self._sprite_handler: SpriteHandler = SpriteHandler(command_helper)
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


	def create_spritesheet_from_video_file(self, video_file_path: Path, video_duration: int, burn_timestamps: bool, output_image_path: Path):
		self._sprite_handler.create_sprites_from_video_file(video_file_path, video_duration, burn_timestamps)

		cmd = [
			"ffmpeg",
			"-y",
			"-i",
			f"{self._image_cache_path}/image%02d.png",
			"-vf",
			"scale=317:-1,tile=8x7:color=0x333333:margin=2:padding=2,scale=2560:-1",
			"-q:v",
			"3",
			f"{output_image_path}"
		]

		self._command_helper.execute_command(cmd)
		self._empty_image_cache()
