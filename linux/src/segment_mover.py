import os
from pathlib import Path
import shutil

from src.video_handler import VideoHandler


class SegmentMover:
	"""Moves segments (and their sheets) to the desired folder."""
	def __init__(self, video_handler: VideoHandler) -> None:
		self._video_handler: VideoHandler = video_handler

	def move(self, segment: Path, output_directory: Path):
		if not Path(output_directory).is_dir:
			os.makedirs(output_directory, exist_ok=True)

		contact_sheet: Path = self._video_handler.get_accompanying_contact_sheet_path(segment)

		try:
			print(f"Moving '{segment.name}' to 'Couldn't MERGE' directory.")

			shutil.move(segment, Path(output_directory, segment.name))
			shutil.move(contact_sheet, Path(output_directory, contact_sheet.name))

			print(f"Moved '{segment.name}' to 'Couldn't MERGE' directory.")
		except Exception as e:
			print(f"Error while moving file '{segment.name}' to 'Couldn't MERGE' directory: {e}")
			raise e
