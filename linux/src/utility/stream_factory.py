from datetime import datetime
from typing import List, Tuple
from src.utility.template_parser import TemplateParser
from src.model.stream_model import StreamModel
from src.model.video_model import VideoModel


class StreamFactory:
	"""Class designed to streamline the process of creating stream models."""
	def __init__(self, template_parser: TemplateParser) -> None:
		self._template_parser: TemplateParser = template_parser

	def _get_start_and_end_dates(self, segments: List[VideoModel]) -> Tuple[datetime, datetime]:
		start_dates = [segment.start_date for segment in segments]
		end_dates = [segment.end_date for segment in segments]

		result = (min(start_dates), max(end_dates))
		return result

	def create(self, model_name: str, segments: List[VideoModel]) -> StreamModel:
		"""Automatically populates the stream dates and the name based on user config."""
		dates = self._get_start_and_end_dates(segments)
		stream: StreamModel = StreamModel(model_name, segments, dates[0], dates[1], None, None)
		merge_name = self._template_parser.get_merge_name(stream)
		stream.set_merged_name(merge_name)
		return stream
