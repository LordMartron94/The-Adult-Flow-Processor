from datetime import datetime
import os
from pathlib import Path
from typing import Dict, List
from common.patterns.pipeline.pipe import IPipe
from constants import BURN, ORIGINAL_LOCATION_PATH
from src.model.video_model import VideoModel
from src.segment_mover import SegmentMover
from src.video_handler import VideoHandler
from src.merge_pipeline.merge_component_context import MergeComponentContext


class ProcessRawSegments(IPipe):
	def __init__(self, merge_context: MergeComponentContext) -> None:
		self._merge_context = merge_context
		super().__init__()

	def flow(self, models_raw_segments: Dict[str, List[VideoModel]]) -> None:
		video_handler: VideoHandler = self._merge_context.video_handler
		segment_mover: SegmentMover = self._merge_context.segment_mover

		model_names = [_model_name for _model_name, _ in models_raw_segments.items()]

		for model_name, raw_segments in models_raw_segments.items():
			print(f"Processing raw segments for: {model_name} - {model_names.index(model_name) + 1} of {len(model_names)}")

			for segment in raw_segments:
				print(f"Processing {raw_segments.index(segment) + 1} of {len(raw_segments)} at {datetime.now()}")
				video_handler.remux_video(segment.path)

				output_dir = Path(ORIGINAL_LOCATION_PATH, model_name)
				segment_mover.move_path_based_raw(Path(str(segment.path) + ".mp4"), output_dir, model_name)

				final_path = Path(output_dir, str(segment.path.name) + ".mp4")
				image_path = Path(output_dir, str(segment.path.name[:-7]) + "__contactsheet.jpg")
				video_handler.generate_contact_sheet_for_video(final_path, BURN, image_path)

				os.remove(segment.path.absolute())
			
			print("---------")
