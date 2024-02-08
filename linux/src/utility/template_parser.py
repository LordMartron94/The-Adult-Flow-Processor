from pathlib import Path
from typing import Any, Dict
from constants import FINAL_DESTINATION_ROOT, FINAL_DIRECTORY_STRUCTURE, MERGE_NAME_TEMPLATE
from src.model.video_model import VideoModel


class TemplateParser:
	"""A class designed to parse the directory template set in constants.py"""
	def _formulate_possibilities(self, video: VideoModel) -> Dict[str, Any]:
		possibilities = {
			"${model_name}": video.model_name,
			"${year}": "{:04d}".format(video.start_date.year),
			"${month}": "{:02d}".format(video.start_date.month),
			"${day}": "{:02d}".format(video.start_date.day),
			"${start_date}": video.start_date.strftime('%Y-%m-%d %H:%M:%S').replace(":", "."),
			"${end_date}": video.end_date.strftime('%Y-%m-%d %H:%M:%S').replace(":", "."),
		}

		return possibilities

	def get_output_directory_for_video(self, video: VideoModel) -> Path:
		"""Returns the designated output path for the stream based on the user template."""
		# Replace variables in the template with their corresponding values
		possibilities = self._formulate_possibilities(video)

		populated_template = FINAL_DIRECTORY_STRUCTURE
		for variable, data in possibilities.items():
			populated_template = populated_template.replace(variable, str(data))
		return Path(FINAL_DESTINATION_ROOT, populated_template)
	
	def get_merge_name(self, stream: VideoModel) -> str:
		"""Returns the final merge name based on the user provided template."""
		possibilities = self._formulate_possibilities(stream)

		populated_template = MERGE_NAME_TEMPLATE
		for variable, data in possibilities.items():
			populated_template = populated_template.replace(variable, str(data))
		return populated_template
