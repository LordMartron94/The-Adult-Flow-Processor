from pathlib import Path
from typing import List
from common.patterns.pipeline.pipe import IPipe
from src.merge_pipeline.pipes.sort_strategies.sort_strategy import ISortStrategy
from src.merge_pipeline.merge_component_context import MergeComponentContext
from src.merge_pipeline.pipes.sort_strategies.sort_strategy_selector import SortStrategySelector


class SortModels(IPipe):
	"""Sorts models based on the configured strategy."""
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._sort_strategy_selector = SortStrategySelector(merge_context)
		super().__init__()

	def flow(self, model_directories: List[Path]) -> List[Path]:
		sorting_algorithm: ISortStrategy = self._sort_strategy_selector.get_sort_algorithm()
		sorted_models = sorting_algorithm.sort(model_directories)
		return sorted_models
