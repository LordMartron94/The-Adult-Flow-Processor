from dataclasses import dataclass
from datetime import datetime


@dataclass
class VideoModel:
	model_name: str
	start_date: datetime
	end_date: datetime

