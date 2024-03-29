import os
from pathlib import Path
import shutil
from constants import BURN, LOOSE_SEGMENT_TEMPLATE, REGEN_SHEETS
from src.ffmpeg_handling.ffmpeg_api import FFMPEGAPI
from src.utility.video_factory import VideoFactory
from src.model.video_model import VideoModel
from src.utility.template_parser import TemplateParser

from src.video_handler import VideoHandler


class SegmentMover:
	"""Moves segments (and their sheets) to the desired folder."""
	def __init__(self, video_handler: VideoHandler, template_parser: TemplateParser, video_factory: VideoFactory, ffmpeg_api: FFMPEGAPI) -> None:
		self._video_handler: VideoHandler = video_handler
		self._template_parser: TemplateParser = template_parser
		self._video_factory: VideoFactory = video_factory
		self._api: FFMPEGAPI = ffmpeg_api

	def _rename(self, segment: Path, model_name: str) -> str:
		"""Returns the segment's new name based on the provided template."""
		if LOOSE_SEGMENT_TEMPLATE is None or LOOSE_SEGMENT_TEMPLATE == "":
			return segment.name
		else:
			video: VideoModel = self._video_factory.create(model_name, segment)
			return self._template_parser.get_video_name(video) + ".mp4"

	def move(self, segment: VideoModel, output_directory: Path):
		if not Path(output_directory).is_dir():
			os.makedirs(output_directory, exist_ok=True)

		contact_sheet: Path = self._video_handler.get_accompanying_contact_sheet_path(segment)

		try:
			print(f"Moving '{segment.path.name}' to '{output_directory}' directory.")

			segment_name: str = self._rename(segment.path, segment.model_name)
			segment_path: Path = Path(output_directory, segment_name)
			shutil.move(segment.path, segment_path)

			if not REGEN_SHEETS:
				if Path(contact_sheet).exists() and Path(contact_sheet).is_file():
					shutil.move(contact_sheet, Path(output_directory, contact_sheet.name))
			else:
				if Path(contact_sheet).exists() and Path(contact_sheet).is_file():
					os.remove(contact_sheet)
				self._api.create_contact_sheet_for_video(segment_path, BURN, str(segment_path).replace('.mp4', '.png'))

			print(f"Moved '{segment.path.name}' to '{output_directory}' directory.")
		except Exception as e:
			print(f"Error while moving file '{segment.path.name}' to '{output_directory}' directory: {e}")
			raise e
		
	def move_raw(self, segment: VideoModel, output_directory: Path):
		if not Path(output_directory).is_dir():
			os.makedirs(output_directory, exist_ok=True)

		if not Path(segment.path).is_file():
			print("File does not exist: " + segment.path.name)
			return

		try:
			print(f"Moving '{segment.path.name}' to '{output_directory}' directory.")

			shutil.move(segment.path, Path(output_directory, segment.path.name))

			print(f"Moved '{segment.path.name}' to '{output_directory}' directory.")
		except Exception as e:
			print(f"Error while moving file '{segment.path.name}' to '{output_directory}' directory: {e}")
			raise e
		
	def move_path_based(self, segment_path: Path, output_dir: Path, model_name: str):
		"""Moves the segment based on paths instead of models. Useful for adapting to other APIs."""
		video: VideoModel = self._video_factory.create(model_name, segment_path)
		self.move(video, output_dir)

	def move_path_based_raw(self, segment_path: Path, output_dir: Path, model_name: str):
		"""Moves the segment based on paths instead of models. Useful for adapting to other APIs."""
		video: VideoModel = self._video_factory.create(model_name, segment_path)
		self.move_raw(video, output_dir)
