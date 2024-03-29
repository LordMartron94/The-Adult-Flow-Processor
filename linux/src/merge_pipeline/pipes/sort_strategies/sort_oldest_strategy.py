from datetime import datetime
from pathlib import Path
from typing import List
from src.model_handler import ModelHandler
from src.merge_pipeline.pipes.sort_strategies.sort_strategy import ISortStrategy



class SortOldestStrategy(ISortStrategy):
	"""Sorts models based on oldest stream segment."""

	def sort(self, model_directories: List[Path]) -> List[Path]:
		model_handler: ModelHandler = self._merge_context.model_handler

		# Filter out directories that have datetime(year=1, month=1, day=1) from find_oldest_segment_in_folder
		valid_model_directories = filter(
			lambda model: model_handler.find_oldest_segment_in_folder(model) != datetime(year=1, month=1, day=1),
			model_directories
		)

		return sorted(valid_model_directories, key=model_handler.find_oldest_segment_in_folder)
