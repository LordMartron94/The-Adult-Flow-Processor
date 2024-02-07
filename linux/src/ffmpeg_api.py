from pathlib import Path
from typing import Union
from constants import *

import os
import subprocess

class FfmpegAPI:
	"""
	Custom layer built on top of the FFMPEG CLI to allow for easier interaction in other parts of the software.
	"""

	def __init__(self):
		self._image_cache_path = f"{CACHE_PATH}/Images"
		self.__pos_init__()

	def __pos_init__(self):
		if not os.path.isdir(self._image_cache_path):
			os.makedirs(self._image_cache_path)

	def _empty_cache(self):
		for file in os.listdir(self._image_cache_path):
			file_path = os.path.join(self._image_cache_path, file)
			if os.path.isfile(file_path):
				os.remove(file_path)

	def get_video_duration(self, video_file: str) -> Union[float, None]:
		duration_process = subprocess.Popen(['ffprobe', "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "-i", video_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		duration_output, duration_error = duration_process.communicate()

		if duration_error:
			print("Error getting video duration:", duration_error)
			return

		return float(duration_output)
	
	def _create_sprites_with_burn(self, duration: float, video_file_path: str):
		for i in range(1, 57):
			interval = int((i - 0.5) * duration / 56)

			ttext = f"{interval // 3600:02d}\:{(interval % 3600) // 60:02d}\:{interval % 60:02d}"

			tmp_image_path = Path(self._image_cache_path, f'image{i:02d}.png')

			if not Path(video_file_path).is_file():
				print("ERROR! Path is not a file or not existen!!!")
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
				f"scale=1920:-1,select='eq(pict_type,I)',drawtext='text={ttext}:fontcolor=white:fontsize=156:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h-10)'",
				"-vframes",
				"1",
				f"{tmp_image_path}"
			]

			if DEBUGGING:
				print(f"Executing: {cmd}")

			result = subprocess.run(cmd, capture_output=True)
			
			if result.returncode != 0:
				print("Something went wrong with creating sprites!")
				print(f"Command: {cmd}")
				error_lines = result.stderr.decode('utf-8').split('\n')
				for line in error_lines:
					print(line)

	def _create_sprites(self, duration: float, video_file_path: str):
		for i in range(1, 57):
			interval = int((i - 0.5) * duration / 56)

			tmp_image_path = Path(self._image_cache_path, f'image{i:02d}.png')
			if not Path(video_file_path).is_file():
				print("ERROR! Path is not a file or not existen!!!")
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
				f"select='eq(pict_type,I)'",
				"-vframes",
				"1",
				f"{tmp_image_path}"
			]

			if DEBUGGING:
				print(f"Executing: {cmd}")

			result = subprocess.run(cmd, capture_output=True)
			
			if result.returncode != 0:
				print("Something went wrong with creating sprites!")
				print(f"Command: {cmd}")
				error_lines = result.stderr.decode('utf-8').split('\n')
				for line in error_lines:
					print(line)

			
	def create_sprites_for_sheet(self, duration: float, video_file_path: str, burn):
		if burn:
			self._create_sprites_with_burn(duration, video_file_path)
		else:
			self._create_sprites(duration, video_file_path)

	def combine_sprites_into_sheet(self, output_image_path: str):
		cmd = [
			"ffmpeg",
			"-y",
			"-i",
			f"{Path(self._image_cache_path)}/image%02d.png",
			"-vf",
			"scale=317:-1,tile=8x7:color=0x333333:margin=2:padding=2,scale=2560:-1",
			"-q:v",
			"3",
			f"{Path(output_image_path)}"
		]

		if DEBUGGING:
			print(f"Executing: {cmd}")

		result = subprocess.run(cmd, capture_output=True)
		
		if result.returncode != 0:
			print("Something went wrong with combining sprites!")
			print(f"Command: {cmd}")
			error_lines = result.stderr.decode('utf-8').split('\n')
			for line in error_lines:
				print(line)

	def create_contact_sheet_for_video(self, video_file_path: str, output_image_path: str, burn=False):
		input_directory = os.path.dirname(video_file_path)

		try:
			duration = self.get_video_duration(video_file_path)
			
			self.create_sprites_for_sheet(duration, video_file_path, burn)
			self.combine_sprites_into_sheet(output_image_path)
		except Exception as e:
			print(f"An error occurred: {e}")
			raise e

		self._empty_cache()

