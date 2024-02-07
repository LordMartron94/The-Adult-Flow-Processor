from pathlib import Path
from subprocess import CompletedProcess
from typing import Union
from constants import DATA_STREAM_PATH

from src.ffmpeg_handling.internal.ffmpeg_command_helper import FFMPEGCommandHelper


class VideoHandler:
    """
    Class to make working with videos through FFMPEG easier.
    """
    def __init__(self, command_helper: FFMPEGCommandHelper) -> None:
        self._command_helper: FFMPEGCommandHelper = FFMPEGCommandHelper()

    def get_video_duration(self, video_file_path: str) -> Union[float, None]:
        command = [
            'ffprobe',
            "-v", 
            "error", 
            "-show_entries", 
            "format=duration", 
            "-of", 
            "default=noprint_wrappers=1:nokey=1", 
            "-i", 
            Path(video_file_path)
        ]

        output = self._command_helper.execute_command(command)
        return float(output.stdout)
    
    def merge_stream_segments(self, segments: list[str], output_file_path: str) -> bool:
        with open(DATA_STREAM_PATH, 'w') as data_stream_file:
            for file_path in segments:
                data_stream_file.write(f"file \'file:{Path(file_path)}\'\n")

        cmd = [
            'ffmpeg', 
            '-y', 
            '-f', 
            'concat', 
            '-safe', 
            '0', 
            '-i', 
            DATA_STREAM_PATH, 
            '-c', 
            'copy', 
            f"{output_file_path}"
        ]

        results: CompletedProcess = self._command_helper.execute_command(cmd)
        return results.returncode == 0
