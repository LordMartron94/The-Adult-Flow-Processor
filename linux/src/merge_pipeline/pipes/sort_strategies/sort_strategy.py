from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from src.merge_pipeline.merge_component_context import MergeComponentContext


class ISortStrategy(ABC):
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._merge_context: MergeComponentContext = merge_context	

	@abstractmethod
	def sort(self, model_directories: List[Path]) -> List[Path]:
		"""Sorts model directories based on the specific algorithm."""
		...
