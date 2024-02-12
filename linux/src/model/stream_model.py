from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from src.model.video_model import VideoModel


@dataclass
class StreamModel:
	model_name: str
	segments: List[VideoModel]
	start_date: Optional[datetime]
	end_date: Optional[datetime]
	merged_name: Optional[str]
	path: Optional[Path]

	def set_merged_name(self, name: str):
		self.merged_name = name

	def set_path(self, path: Path):
		self.path = path
