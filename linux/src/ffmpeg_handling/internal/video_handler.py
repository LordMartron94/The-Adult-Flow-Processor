import os
from pathlib import Path
from subprocess import CompletedProcess
from typing import Union
from constants import DATA_STREAM_PATH, SHOW_MERGE_COMMANDS

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
        try:
            return float(output.stdout)
        except ValueError: # Invalid output, corrupt video!            
            return None

    
    def merge_stream_segments(self, segments: list[str], output_file_path: str) -> bool:
        with open(DATA_STREAM_PATH, 'w+') as data_stream_file:
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

        results: CompletedProcess = self._command_helper.execute_command(cmd, output_override=SHOW_MERGE_COMMANDS)
        return results.returncode == 0
    
    def video_valid(self, video_file_path: Path, robust_check=False) -> bool:
        if not robust_check:
            cmd = [
                'ffprobe',
                video_file_path
            ]
        else:
            cmd = [
                'ffmpeg',
                '-i',
                video_file_path,
                '-f',
                'null'
            ]

        results: CompletedProcess = self._command_helper.execute_command(cmd)
        return results.returncode == 0 
    
    def remux_video(self, input_video_path: Path, output_extension: str=".mp4"):
        remux_command = [
            "ffmpeg",
            "-i",
            str(input_video_path),
            "-c:v",
            "copy",
            "-movflags",
            "faststart",
            "-y",
            "-f",
            "mp4",
            str(input_video_path) + output_extension
        ]

        results: CompletedProcess = self._command_helper.execute_command(remux_command)
        return results.returncode == 0
