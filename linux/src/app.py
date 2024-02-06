import shutil
import time
import os
from src.video_utils import VideoUtils
from src.utils.time_utils import TimeUtils, TimeFormat
from src.utils.file_parser import FileParser
from constants import *


class App:
	def __init__(self):
		self._video_utils = VideoUtils()
		self._time_utils = TimeUtils()
		self._file_parser = FileParser()

	def handle_loose_segments(self, segments, loose_segment_directory_path):
		for file in segments:
			if file is None:
				return
			contact_sheet = self._video_utils.get_accompanying_contact_sheet_path(file)
			try:
				print(f"Moving '{os.path.basename(file)}' to 'Couldn't MERGE' directory.")
				shutil.move(file, os.path.join(loose_segment_directory_path, os.path.basename(file)).replace('\\', '/'))
				shutil.move(contact_sheet.replace('\\', '/'), os.path.join(loose_segment_directory_path, os.path.basename(contact_sheet)).replace('\\', '/'))
				print(f"Moved '{os.path.basename(file)}' to 'Couldn't MERGE' directory.")
			except Exception as e:
				print(f"Error while moving file '{os.path.basename(file)}' to 'Couldn't MERGE' directory: {e}")

	def process_current_files(self, current_segments, model_name, directory_path, delete, sheet, burn, loose_segment_directory_path):
		if len(current_segments) >= 2:
			try:
				self._video_utils.merge_stream_segments(current_segments, model_name, directory_path, delete, sheet, burn)
			except Exception as e:
				print(f"Error while merging files: {e}")
				self.handle_loose_segments(current_segments, loose_segment_directory_path)
		else:
			self.handle_loose_segments(current_segments, loose_segment_directory_path)

	def process_segments_for_model(self, video_files, current_files, model_name, directory_path, delete, sheet, burn, loose_segment_directory_path):
		for file in video_files:
			file_path = os.path.join(directory_path, file).replace("\\", "/")

			if not current_files or self._video_utils.get_time_difference_between_videos(current_files[-1], file) > 400:
				self.process_current_files(current_files, model_name, directory_path, delete, sheet, burn, loose_segment_directory_path)
				current_files = []

			current_files.append(file_path)

		self.process_current_files(current_files, model_name, directory_path, delete, sheet, burn, loose_segment_directory_path)

	def process_model(self, directory_path, model_name, sheet=False, 
		burn=False, delete=False):
		_start_time = time.time()
		os.chdir(directory_path)

		video_files = sorted(
			filter(lambda f: f.endswith(('.ts', '.mp4')), os.listdir()),
			key=self._file_parser.extract_timestamp_from_filename
		)

		loose_segment_directory_path = os.path.join(FINAL_DESTINATION_ROOT, model_name, "Loose Segments")
		os.makedirs(loose_segment_directory_path, exist_ok=True)

		current_files = []
		self.process_segments_for_model(video_files, current_files, model_name, directory_path, delete, sheet, burn, loose_segment_directory_path)

		_end_time = time.time()
		_elapsed_time = _end_time - _start_time

		_time_formatted = self._time_utils.format_time(_elapsed_time, TimeFormat.HMS)

		print(" ")
		print(f"It took {_time_formatted} to merge all possible segments for model {model_name}.")    
		print(" ")
		print("=====================================")
		print(" ")


	def is_mp4_file(self, item):
		"""Check if the file has a .mp4 extension."""
		return os.path.isfile(item) and item.lower().endswith('.mp4')

	def get_file_modified_date(self, file_path):
		"""Get the modification time of a file."""
		return os.path.getmtime(file_path)

	def find_oldest_modified_date(self, folder_path):
		"""Find the oldest modification date of .mp4 files in the specified folder."""
		if not os.path.isdir(folder_path):
			return None

		mp4_files = [
			self.get_file_modified_date(os.path.join(folder_path, item))
			for item in os.listdir(folder_path) if self.is_mp4_file(os.path.join(folder_path, item))
		]

		return min(mp4_files, default=float('-inf'))

	def sort_folders_by_oldest_stream(self, folders):
		"""Sort a list of folders based on the oldest modification date of .mp4 files."""
		return sorted(folders, key=lambda x: self.find_oldest_modified_date(x[0]))


	def run(self):
		directory_path = ORIGINAL_LOCATION_PATH

		start_time = time.time()

		model_directories = []

		for subdirectory in os.listdir(directory_path):
			subdirectory_path = os.path.join(directory_path, subdirectory).replace('\\', '/')
			model_directories.append((subdirectory_path, subdirectory))

		model_directories = self.sort_folders_by_oldest_stream(model_directories)
		num_models = len(model_directories)

		for model_directory, model in model_directories:
			print(model, model_directory)
			if os.path.isdir(model_directory):
				self.process_model(model_directory, model, sheet=SHEET, burn=BURN, delete=DELETE)

		end_time = time.time()
		elapsed_time = end_time - start_time

		time_formatted = self._time_utils.format_time(elapsed_time, TimeFormat.HMS)
		
		if elapsed_time > 0:
			print(f"Avg {self._time_utils.format_time(elapsed_time / num_models, TimeFormat.HMS)} per model!")

		print(" ")
		print(f"It took {time_formatted} to merge all possible segments for every model.")
