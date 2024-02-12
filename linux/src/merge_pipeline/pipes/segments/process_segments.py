from datetime import datetime
import pprint
import time
from typing import Dict, List
from common.patterns.pipeline.pipe import IPipe
from common.time_utils import TimeUtils
from common.time_format import TimeFormat
from src.utility.template_parser import TemplateParser
from src.stream_merger import StreamMerger
from src.segment_mover import SegmentMover
from src.merge_pipeline.merge_component_context import MergeComponentContext
from src.model.stream_model import StreamModel
from constants import BURN, DEBUGGING, DELETE, SHEET

class ProcessSegments(IPipe):
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._merge_context: MergeComponentContext = merge_context
		super().__init__()

	def _print_time_passed_model(self, start_time: float, end_time: float, model_name: str):
		time_utils: TimeUtils = self._merge_context.time_utils
		elapsed_time = end_time - start_time
		formatted = time_utils.format_time(elapsed_time, TimeFormat.Dynamic)

		print(" ")
		print(f"It took {formatted} to merge all possible segments for model {model_name}.")    
		print(" ")
		print("=====================================")
		print(" ")

	def _print_time_passed_global(self, start_time: float, end_time: float, num_models: int):
		time_utils: TimeUtils = self._merge_context.time_utils
		elapsed_time = end_time - start_time

		time_formatted = time_utils.format_time(elapsed_time, TimeFormat.HMS)
		
		if elapsed_time > 0:
			print(f"Avg {time_utils.format_time(elapsed_time / num_models, TimeFormat.Dynamic, round_digits=4)} per model!")

		print(" ")
		print(f"It took {time_formatted} to merge all possible segments for every model.")


	def flow(self, models_streams: Dict[str, List[StreamModel]]) -> None:
		segment_mover: SegmentMover = self._merge_context.segment_mover
		segment_merger: StreamMerger = self._merge_context.stream_merger
		template_parser: TemplateParser = self._merge_context.template_parser

		start_time_global = time.time()

		model_names = [_model_name for _model_name, _ in models_streams.items()]

		for model_name, streams in models_streams.items():
			print(f"Processing: '{model_name}'  - {model_names.index(model_name) + 1} of {len(model_names)}")

			start_time_model = time.time()

			if DEBUGGING:
				pprint.pp(streams)

			for stream in streams:
				print(f"Processing {streams.index(stream) + 1} of {len(streams)} at {datetime.now()}")
				if len(stream.segments) > 1:
					segment_merger.merge_stream(stream, SHEET, BURN, DELETE)
				else:
					destination_dir = template_parser.get_output_directory_for_video(stream)
					stream.set_path(stream.segments[0].path)
					segment_mover.move(stream, destination_dir)

			end_time_model = time.time()
			self._print_time_passed_model(start_time_model, end_time_model, model_name)

		end_time_global = time.time()
		self._print_time_passed_global(start_time_global, end_time_global, len(models_streams.keys()))