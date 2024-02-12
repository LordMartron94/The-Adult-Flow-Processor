from constants import MODEL_SORTING_ALGORITHM
from src.exceptions.config_error import ConfigurationError
from src.merge_pipeline.pipes.sort_strategies.sort_alphabetical_reverse_strategy import SortAlphabeticalReverseStrategy
from src.merge_pipeline.pipes.sort_strategies.sort_alphabetical_strategy import SortAlphabeticalStrategy
from src.merge_pipeline.merge_component_context import MergeComponentContext
from src.merge_pipeline.pipes.sort_strategies.sort_oldest_strategy import SortOldestStrategy
from src.merge_pipeline.pipes.sort_strategies.sort_strategy import ISortStrategy


class SortStrategySelector:
	"""Strategy pattern. Choose strategy based on input."""
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._options = {
			"${oldest}": SortOldestStrategy(merge_context),
			"${alphabetical}": SortAlphabeticalStrategy(merge_context),
			"${alphabetical_reversed}": SortAlphabeticalReverseStrategy(merge_context)
		}

	def get_sort_algorithm(self) -> ISortStrategy:
		configured_algorithm = MODEL_SORTING_ALGORITHM
		for option, strategy in self._options.items():
			if configured_algorithm == option:
				return strategy
		
		raise ConfigurationError(f"Unknown sort_algorithm option: '{configured_algorithm}'")
