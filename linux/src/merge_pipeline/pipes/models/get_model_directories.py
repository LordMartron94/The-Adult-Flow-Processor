import os
from pathlib import Path
from typing import Any, List
from common.patterns.pipeline.pipe import IPipe
from constants import ORIGINAL_LOCATION_PATH


class GetModelDirectories(IPipe):
	def flow(self, data: None) -> List[Path]:
		model_directories = []

		for subdirectory in os.listdir(ORIGINAL_LOCATION_PATH):
			model_path = Path(ORIGINAL_LOCATION_PATH, subdirectory)
			model_directories.append(model_path)

		return model_directories
