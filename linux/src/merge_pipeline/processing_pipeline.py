from common.patterns.pipeline.abstract_pipeline import AbPipeline
from src.merge_pipeline.pipes.raw.filter_raw_segments import FilterRawSegments
from src.merge_pipeline.pipes.raw.process_raw_segments import ProcessRawSegments
from src.merge_pipeline.pipes.raw.get_raw_segments import GatherRawSegments
from src.merge_pipeline.pipes.raw.sort_models_raw import SortModelsRaw
from src.merge_pipeline.pipes.raw.get_model_directories_raw import GetRawModelDirectories
from src.merge_pipeline.pipes.segments.process_segments import ProcessSegments
from src.merge_pipeline.pipes.segments.organize_segments import OrganizeSegments
from src.merge_pipeline.pipes.segments.sort_segments import SortSegments
from src.merge_pipeline.pipes.segments.validate_segments import ValidateSegments
from src.merge_pipeline.pipes.segments.filter_segments import FilterSegments
from src.merge_pipeline.pipes.segments.gather_segments import GatherSegments
from src.merge_pipeline.pipes.models.remove_empty_models import RemoveEmptyModels
from src.merge_pipeline.pipes.models.sort_models import SortModels
from src.merge_pipeline.pipes.models.get_model_directories import GetModelDirectories
from src.merge_pipeline.merge_component_context import MergeComponentContext


class ProcessingPipeline(AbPipeline):
	def __init__(self, merge_context: MergeComponentContext):
		self._merge_context: MergeComponentContext = merge_context
		super().__init__()

	def build_pipeline(self):
		# ==== Raw ====
		self._add_step(GetRawModelDirectories())
		self._add_step(SortModelsRaw(self._merge_context))
		self._add_step(GatherRawSegments(self._merge_context))
		self._add_step(FilterRawSegments(self._merge_context))
		self._add_step(ProcessRawSegments(self._merge_context))

		# ==== Models ====
		self._add_step(GetModelDirectories())
		self._add_step(RemoveEmptyModels(self._merge_context))
		self._add_step(SortModels(self._merge_context))

		# ==== Segments ====
		self._add_step(GatherSegments(self._merge_context))
		self._add_step(FilterSegments(self._merge_context))
		self._add_step(ValidateSegments(self._merge_context))
		self._add_step(SortSegments())
		self._add_step(OrganizeSegments(self._merge_context))
		self._add_step(ProcessSegments(self._merge_context))

		return super().build_pipeline()