import os
from datetime import timedelta
from pathlib import Path
from typing import Union
from common.handlers.file_parser import FileParser
from src.model.stream_model import StreamModel
from src.model.video_model import VideoModel
from src.ffmpeg_handling.ffmpeg_api import FFMPEGAPI
from constants import *

class VideoHandler:
    """A utility class for handling video-related operations."""

    def __init__(self):
        """Initialize the VideoUtils instance."""
        self._file_parser: FileParser = FileParser()
        self._api: FFMPEGAPI = FFMPEGAPI()

    def get_time_difference_between_videos(self, video_one: VideoModel, video_two: VideoModel) -> float:
        """
        Calculate the time difference between the end of the first video and the start of the second video.

        Args:
            video_one_path (VideoModel): The first video entity.
            video_two_path (VideoModel): The second video entity.

        Returns:
            float: The time difference in seconds between the two videos.
            None: The video file is corrupt and thus cannot be used.
        """        
        time_diff = (video_two.start_date - video_one.end_date).total_seconds()

        if DEBUGGING:
            print(f"Files: {video_one.path.name}, {video_two.path.name}\nTime difference: {time_diff}")

        return time_diff

    def get_accompanying_contact_sheet_path(self, video_model: Union[VideoModel, StreamModel]) -> str:
        """
        Get the path to the accompanying contact sheet for a given video file.

        Args:
            video_file_path (str): The path to the video file.

        Returns:
            str: The path to the accompanying contact sheet image.
        """
        _directory_path = video_model.path.parent.absolute()
        
        file_name = os.path.basename(video_model.path)
        base_name, _ = os.path.splitext(file_name)
        base_name_without_ms = base_name[:-7]

        contact_sheet_path = Path(_directory_path, f"{base_name_without_ms}_contactsheet.jpg")
        return contact_sheet_path
    
    def delete_spritesheet_for_video(self, video_model: Union[VideoModel, StreamModel]):
        sheet_path = self.get_accompanying_contact_sheet_path(video_model)
        if Path(sheet_path).is_file():
            os.remove(sheet_path)

    def video_is_valid(self, video_file_path: Path) -> bool:
        return self._api.video_valid(video_file_path)

    def remux_video(self, input_video_path: Path) -> bool:
        return self._api.remux_video(input_video_path)

    def generate_contact_sheet_for_video(self, input_video_path: Path, burn_timestamps: bool, output_image_path: Path) -> None:
        return self._api.create_contact_sheet_for_video(input_video_path, burn_timestamps, output_image_path)
