import os
from pathlib import Path
from typing import List
from common.patterns.pipeline.pipe import IPipe
from constants import ORIGINAL_LOCATION_PATH_RAW


class GetRawModelDirectories(IPipe):
	def flow(self, data: None) -> List[Path]:
		model_directories = []

		for subdirectory in os.listdir(ORIGINAL_LOCATION_PATH_RAW):
			model_path = Path(ORIGINAL_LOCATION_PATH_RAW, subdirectory)
			model_directories.append(model_path)

		return model_directories
