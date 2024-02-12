from pathlib import Path
from typing import List, Tuple
from common.patterns.pipeline.pipe import IPipe
from src.merge_pipeline.pipes.sort_strategies.sort_strategy import ISortStrategy


class SortAlphabeticalStrategy(ISortStrategy):
	def sort(self, model_directories: List[Path]) -> List[Path]:
		models: List[Tuple[str, Path]] = []

		for model_path in model_directories:
			model_name = model_path.name
			models.append((model_name, model_path))
		
		models.sort(key=lambda x: x[0])

		sorted_paths = [model[1] for model in models]
		
		return sorted_paths
