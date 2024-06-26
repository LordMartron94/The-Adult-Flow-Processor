import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from common.patterns.pipeline.pipe import IPipe
from constants import DEBUGGING, MIN_SEGMENT_AGE_FOR_POST_PROCESS, DELETE_CORRUPT_VIDEOS
from src.model.video_model import VideoModel
from src.merge_pipeline.merge_component_context import MergeComponentContext


class FilterRawSegments(IPipe):
	"""Filters segments based on minimum age."""
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._merge_context: MergeComponentContext = merge_context
		super().__init__()
	
	def flow(self, models_segments: Dict[str, List[Path]]) -> Dict[str, List[VideoModel]]:
		if MIN_SEGMENT_AGE_FOR_POST_PROCESS == 0:
			return models_segments

		video_factory = self._merge_context.video_factory
		filtered_segments: Dict[str, List[VideoModel]] = {}
		
		for model_name, model_segments in models_segments.items():
			model_segments_new: List[VideoModel] = []

			for segment in model_segments:
				segment_entity: VideoModel = video_factory.create(model_name, segment)

				if segment_entity.start_date == segment_entity.end_date:
					if DELETE_CORRUPT_VIDEOS:
						os.remove(segment_entity.path)

				time_diff = datetime.now() - segment_entity.start_date

				if time_diff > timedelta(hours=MIN_SEGMENT_AGE_FOR_POST_PROCESS):
					model_segments_new.append(segment_entity)
				else:
					if DEBUGGING:
						print(f"Video {segment.name} too young!")

			filtered_segments[model_name] = model_segments_new

		return filtered_segments
