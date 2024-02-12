from pathlib import Path
from typing import List
from common.patterns.pipeline.pipe import IPipe
from common.handlers.file_handler import FileHandler
from src.merge_pipeline.merge_component_context import MergeComponentContext


class RemoveEmptyModels(IPipe):
	"""Removes empty model directories from the processing list to slightly boost performance, but primarily to keep the logs from getting cluttered."""
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._file_handler: FileHandler = merge_context.file_handler
		super().__init__()


	def flow(self, model_directories: List[Path]) -> List[Path]:
		filtered_models: List[Path] = list(model_directories)

		for model_path in model_directories:
			if self._file_handler.get_number_of_files_in_dir(model_path) < 1:
				filtered_models.remove(model_path)

		return filtered_models
