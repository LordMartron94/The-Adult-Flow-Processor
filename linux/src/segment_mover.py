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

	def move(self, segment: Path, output_directory: Path, model_name: str):
		if not Path(output_directory).is_dir():
			os.makedirs(output_directory, exist_ok=True)

		contact_sheet: Path = self._video_handler.get_accompanying_contact_sheet_path(segment)

		try:
			print(f"Moving '{segment.name}' to 'Couldn't MERGE' directory.")

			segment_name: str = self._rename(segment, model_name)
			segment_path: Path = Path(output_directory, segment_name)
			shutil.move(segment, segment_path)

			if not REGEN_SHEETS:
				if Path(contact_sheet).exists() and Path(contact_sheet).is_file():
					shutil.move(contact_sheet, Path(output_directory, contact_sheet.name))
			else:
				if Path(contact_sheet).exists() and Path(contact_sheet).is_file():
					os.remove(contact_sheet)
				self._api.create_contact_sheet_for_video(segment_path, BURN, str(segment_path).replace('.mp4', '.png'))

			print(f"Moved '{segment.name}' to 'Couldn't MERGE' directory.")
		except Exception as e:
			print(f"Error while moving file '{segment.name}' to 'Couldn't MERGE' directory: {e}")
			raise e
