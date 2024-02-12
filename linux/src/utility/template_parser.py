from pathlib import Path
from typing import Any, Dict, Union
from constants import FINAL_DESTINATION_ROOT, FINAL_DIRECTORY_STRUCTURE, LOOSE_SEGMENT_TEMPLATE, MERGE_NAME_TEMPLATE, ORIGINAL_LOCATION_PATH
from src.model.stream_model import StreamModel
from src.model.video_model import VideoModel


class TemplateParser:
	"""A class designed to parse the directory template set in constants.py"""
	def _formulate_possibilities(self, video: Union[VideoModel, StreamModel]) -> Dict[str, Any]:
		possibilities = {
			"${model_name}": video.model_name,
			"${year}": "{:04d}".format(video.start_date.year),
			"${month}": "{:02d}".format(video.start_date.month),
			"${day}": "{:02d}".format(video.start_date.day),
			"${start_date}": video.start_date.strftime('%Y-%m-%d %H:%M:%S').replace(":", "."),
			"${end_date}": video.end_date.strftime('%Y-%m-%d %H:%M:%S').replace(":", "."),
		}

		return possibilities

	def get_output_directory_for_video(self, video: Union[VideoModel, StreamModel]) -> Path:
		"""Returns the designated output path for the stream based on the user template."""
		# Replace variables in the template with their corresponding values
		possibilities = self._formulate_possibilities(video)

		populated_template = FINAL_DIRECTORY_STRUCTURE
		for variable, data in possibilities.items():
			populated_template = populated_template.replace(variable, str(data))
		return Path(FINAL_DESTINATION_ROOT, populated_template)
	
	def get_output_directory_for_video_raw(self, video: Union[VideoModel, StreamModel]) -> Path:
		"""Returns the designated output path for the stream based on the user template."""
		# Replace variables in the template with their corresponding values
		possibilities = self._formulate_possibilities(video)

		populated_template = FINAL_DIRECTORY_STRUCTURE
		for variable, data in possibilities.items():
			populated_template = populated_template.replace(variable, str(data))
		return Path(ORIGINAL_LOCATION_PATH, populated_template)
	
	def get_merge_name(self, stream: StreamModel) -> str:
		"""Returns the final merge name based on the user provided template."""
		possibilities = self._formulate_possibilities(stream)

		populated_template = MERGE_NAME_TEMPLATE
		for variable, data in possibilities.items():
			populated_template = populated_template.replace(variable, str(data))
		return populated_template

	def get_video_name(self, video: VideoModel) -> str:
		"""Returns the video name based on the user provided template."""
		possibilities = self._formulate_possibilities(video)

		populated_template = LOOSE_SEGMENT_TEMPLATE
		for variable, data in possibilities.items():
			populated_template = populated_template.replace(variable, str(data))
		return populated_template
