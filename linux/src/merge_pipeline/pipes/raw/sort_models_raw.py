from pathlib import Path
from typing import List
from common.patterns.pipeline.pipe import IPipe
from src.merge_pipeline.merge_component_context import MergeComponentContext
from src.merge_pipeline.pipes.sort_strategies.sort_oldest_strategy import SortOldestStrategy


class SortModelsRaw(IPipe):
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._merge_context: MergeComponentContext = merge_context
		super().__init__()

	def flow(self, model_dirs: List[Path]) -> List[Path]:
		strategy: SortOldestStrategy = SortOldestStrategy(self._merge_context)
		return strategy.sort(model_dirs)
