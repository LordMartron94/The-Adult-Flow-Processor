from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class VideoModel:
	model_name: str
	start_date: datetime
	end_date: datetime
	path: Path
