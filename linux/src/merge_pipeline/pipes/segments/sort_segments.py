from typing import Dict, List
from common.patterns.pipeline.pipe import IPipe
from src.model.video_model import VideoModel
from src.merge_pipeline.merge_component_context import MergeComponentContext


class SortSegments(IPipe):
	"""Sorts segments based on start date in ascending order."""
	def flow(self, models_segments: Dict[str, List[VideoModel]]) -> Dict[str, List[VideoModel]]:
		models_segments_sorted: Dict[str, List[VideoModel]] = {}

		for model_name, model_segments in models_segments.items():
			sorted_segments = sorted(model_segments, key=lambda segment: segment.start_date)
			models_segments_sorted[model_name] = sorted_segments

		return models_segments_sorted
