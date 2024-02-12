from typing import Any, Dict, List
from common.patterns.pipeline.pipe import IPipe
from constants import MAX_DIFFERENCE_BETWEEN_SEGMENTS
from common.collection_extensions import CollectionExtensions
from src.model.stream_model import StreamModel
from src.video_handler import VideoHandler
from src.merge_pipeline.merge_component_context import MergeComponentContext
from src.model.video_model import VideoModel


class OrganizeSegments(IPipe):
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._merge_context: MergeComponentContext = merge_context
		super().__init__()

	def _split_at_gaps(self, segments: List[VideoModel]) -> List[List[VideoModel]]:
		video_handler: VideoHandler = self._merge_context.video_handler

		def gap_too_large(before, after) -> bool: 
			time_diff: float = video_handler.get_time_difference_between_videos(before, after)

			return time_diff > MAX_DIFFERENCE_BETWEEN_SEGMENTS

		return list(
			CollectionExtensions.split_between(
				gap_too_large, 
				segments
			)
		)

	def flow(self, models_segments: Dict[str, List[VideoModel]]) -> Dict[str, List[StreamModel]]:
		factory = self._merge_context.stream_factory

		models_streams: Dict[str, List[StreamModel]] = {}

		for model_name, model_segments in models_segments.items():
			organized_segments: List[List[VideoModel]] = self._split_at_gaps(model_segments)

			model_streams: List[StreamModel] = []

			for stream in organized_segments:
				stream_entity: StreamModel = factory.create(model_name, stream)
				model_streams.append(stream_entity)
			
			models_streams[model_name] = model_streams
		
		return models_streams
