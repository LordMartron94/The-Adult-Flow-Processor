import os
import shutil
from datetime import timedelta
from file_parser import FileParser
from ffmpeg_api import FfmpegAPI
from constants import *

class VideoUtils:
    """A utility class for handling video-related operations."""

    def __init__(self):
        """Initialize the VideoUtils instance."""
        self._file_parser = FileParser()
        self._api = FfmpegAPI()

    def get_time_difference_between_videos(self, video_one_path: str, video_two_path: str) -> float:
        """
        Calculate the time difference between the end of the first video and the start of the second video.

        Args:
            video_one_path (str): The path to the first video file.
            video_two_path (str): The path to the second video file.

        Returns:
            float: The time difference in seconds between the two videos.
        """
        start_time_file1 = self._file_parser.extract_datetime_from_filename(video_one_path)
        end_time_file1 = start_time_file1 + timedelta(seconds=self.get_video_duration(video_one_path))
        start_time_file2 = self._file_parser.extract_datetime_from_filename(video_two_path)
        
        time_diff = (start_time_file2 - end_time_file1).total_seconds()
        return time_diff

    def get_accompanying_contact_sheet_path(self, video_file_path: str) -> str:
        """
        Get the path to the accompanying contact sheet for a given video file.

        Args:
            video_file_path (str): The path to the video file.

        Returns:
            str: The path to the accompanying contact sheet image.
        """
        _directory_path = os.path.abspath(os.path.dirname(video_file_path))
        file_name = os.path.basename(video_file_path)
        base_name, extension = os.path.splitext(file_name)
        base_name_without_ms = base_name[:-7]  # Correct
        contact_sheet_path = os.path.join(_directory_path, f"{base_name_without_ms}_contactsheet.jpg").replace('\\', '/')
        return contact_sheet_path

    def _create_contact_sheet_for_merged_file(self, merged_file_path: str, burn: bool):
        """
        Create a contact sheet for a merged video file.

        Args:
            merged_file_path (str): The path to the merged video file.
            burn (bool): Whether to burn timestamps onto the contact sheet.
        """
        self._api.create_contact_sheet(merged_file_path, merged_file_path.replace('.mkv', '.jpg'), burn)

    def _concat_segments(self, segments, output_file_path: str):
        with open(DATA_STREAM_PATH, 'w') as tempf:
            for file in segments:
                tempf.write(f"file \'file:{file}\'\n")

        cmd = [
            f'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', temp_file, '-c', 'copy', f"{output_file_path}"
        ]
        print(cmd)
        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode == 0:
            print("Merged video saved successfully.")
            return True
        else:
            print("Merging process failed.")
            print(process.stdout)
            return False

    def merge_stream_segments(self, segments: list, model_name: str, directory_path: str, delete: bool, sheet: bool, burn: bool):
        """
        Merge stream segments into a single video file.

        Args:
            segments (list): List of paths to video segments to be merged.
            model_name (str): The name of the model.
            directory_path (str): The directory path for storing the merged video.
            delete (bool): Whether to delete the original segments after merging.
            sheet (bool): Whether to create an accompanying contact sheet for the merged video.
            burn (bool): Whether to burn timestamps onto the contact sheet.
        """
        start_datetime = self._file_parser.extract_datetime_from_filename(segments[0]).strftime('%Y-%m-%d %H:%M:%S')
        end_datetime = (self._file_parser.extract_datetime_from_filename(segments[-1]) + timedelta(seconds=self.get_video_duration(segments[-1]))).strftime('%Y-%m-%d %H:%M:%S')
        output_file_name = f'{model_name}, START {start_datetime}, END {end_datetime}.mkv'.replace(':', '.')
        os.makedirs(os.path.join(FINAL_DESTINATION_ROOT, model_name, "MERGED"), exist_ok=True)
        output_file_path = os.path.join(FINAL_DESTINATION_ROOT, model_name, "MERGED", output_file_name).replace('\\', '/')
        
        # Check if merging was successful before proceeding with deletion
        if self.concat_segments(segments, output_file_path):
            if delete:
                for f in segments:
                    if os.path.exists(f):
                        os.remove(f)

                for f in segments:
                    contact_sheet_path = self.get_accompanying_contact_sheet_path(f)
                    if os.path.exists(contact_sheet_path):
                        os.remove(contact_sheet_path)

            if sheet:
                self._create_contact_sheet_for_merged_file(output_file_path, burn)