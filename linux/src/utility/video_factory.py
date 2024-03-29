from datetime import timedelta
from pathlib import Path
from common.handlers.file_parser import FileParser
from src.ffmpeg_handling.ffmpeg_api import FFMPEGAPI
from src.model.video_model import VideoModel


class VideoFactory:
    """Class designed to streamline the process of creating video models."""

    def __init__(self, file_parser: FileParser, ffmpeg_api: FFMPEGAPI) -> None:
        self._file_parser: FileParser = file_parser
        self._api: FFMPEGAPI = ffmpeg_api

    def create(self, model_name: str, video_path: Path) -> VideoModel:
        start_date = self._file_parser.extract_datetime(video_path.name)
        video_duration = self._api.get_video_duration(video_path)

        if video_duration is not None:
            end_date = start_date + timedelta(seconds=video_duration)
        else:
            end_date = start_date

        video: VideoModel = VideoModel(model_name, start_date, end_date, video_path)
        return video

# def create_stream(self, model_name: str, video_one_path: Path, video_two_path: Path) -> VideoModel:
# 		start_date = self._file_parser.extract_datetime(video_one_path.name)

# 		start_vid_two = self._file_parser.extract_datetime(video_two_path.name)
# 		end_date = start_vid_two + timedelta(seconds=self._api.get_video_duration(video_two_path))

# 		video: VideoModel = VideoModel(model_name, start_date, end_date)
# 		return video
