from pathlib import Path
from typing import Dict, List
from common.patterns.pipeline.pipe import IPipe
from src.model_handler import ModelHandler
from src.merge_pipeline.merge_component_context import MergeComponentContext


class GatherRawSegments(IPipe):
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._merge_context: MergeComponentContext = merge_context
		super().__init__()

	def flow(self, model_directories: List[Path]) -> Dict[str, List[Path]]:
		model_handler: ModelHandler = self._merge_context.model_handler

		segments: Dict[str, List[Path]] = {}

		for model_path in model_directories:
			model_name: str = model_path.name
			model_segments = model_handler.get_segment_paths(model_path, ".ts")
			segments[model_name] = model_segments
		
		return segments
