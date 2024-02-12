import os
from pathlib import Path
from typing import Dict, List
from common.patterns.pipeline.pipe import IPipe
from constants import DELETE_CORRUPT_VIDEOS
from src.model.video_model import VideoModel
from src.video_handler import VideoHandler
from src.merge_pipeline.merge_component_context import MergeComponentContext


class ValidateSegments(IPipe):
	"""Removes any segment from the segment list that is corrupt according to ffmpeg."""
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._merge_context: MergeComponentContext = merge_context
		super().__init__()
	
	def flow(self, models_segments: Dict[str, List[VideoModel]]) -> Dict[str, List[VideoModel]]:
		video_handler: VideoHandler = self._merge_context.video_handler
		validated_segments: Dict[str, List[VideoModel]] = {}
		
		for model_name, model_segments in models_segments.items():
			copy_model_segments = list(model_segments)

			for segment in model_segments:
				valid_video_file: bool = video_handler.video_is_valid(segment.path)
				if not valid_video_file:
					copy_model_segments.remove(segment)

					if DELETE_CORRUPT_VIDEOS:
						os.remove(segment.path)

			validated_segments[model_name] = copy_model_segments

		return validated_segments
