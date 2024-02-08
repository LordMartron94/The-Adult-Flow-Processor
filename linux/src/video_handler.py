import os
from datetime import timedelta
from pathlib import Path
from typing import Union
from common.handlers.file_parser import FileParser
from src.ffmpeg_handling.ffmpeg_api import FFMPEGAPI
from constants import *

class VideoHandler:
    """A utility class for handling video-related operations."""

    def __init__(self):
        """Initialize the VideoUtils instance."""
        self._file_parser: FileParser = FileParser()
        self._api: FFMPEGAPI = FFMPEGAPI()

    def get_time_difference_between_videos(self, video_one_path: Path, video_two_path: Path) -> float:
        """
        Calculate the time difference between the end of the first video and the start of the second video.

        Args:
            video_one_path (Path): The path to the first video file.
            video_two_path (Path): The path to the second video file.

        Returns:
            float: The time difference in seconds between the two videos.
            None: The video file is corrupt and thus cannot be used.
        """
        start_time_file1 = self._file_parser.extract_datetime(video_one_path.name)
        duration_video_one = self._api.get_video_duration(video_one_path)

        end_time_file1 = start_time_file1 + timedelta(seconds=duration_video_one)

        start_time_file2 = self._file_parser.extract_datetime(video_two_path.name)
        
        time_diff = (start_time_file2 - end_time_file1).total_seconds()

        if DEBUGGING:
            print(f"Files: {video_one_path.name}, {video_two_path.name}\nTime difference: {time_diff}")

        return time_diff

    def get_accompanying_contact_sheet_path(self, video_file_path: str) -> str:
        """
        Get the path to the accompanying contact sheet for a given video file.

        Args:
            video_file_path (str): The path to the video file.

        Returns:
            str: The path to the accompanying contact sheet image.
        """
        _directory_path = Path(video_file_path).parent.absolute()
        
        file_name = os.path.basename(video_file_path)
        base_name, _ = os.path.splitext(file_name)
        base_name_without_ms = base_name[:-7]

        contact_sheet_path = Path(_directory_path, f"{base_name_without_ms}_contactsheet.jpg")
        return contact_sheet_path
    
    def delete_spritesheet_for_video(self, video_file_path: str):
        sheet_path = self.get_accompanying_contact_sheet_path(video_file_path)
        if Path(sheet_path).is_file():
            os.remove(sheet_path)
