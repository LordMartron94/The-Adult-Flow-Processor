from pathlib import Path
import time
from common.handlers.file_parser import FileParser
from src.model_processor import ModelProcessor
from common.handlers.folder_handler import FolderHandler
from common.time_utils import TimeUtils, TimeFormat
from constants import *


class App:
	def __init__(self):
		self._time_utils = TimeUtils()
		self._folder_handler: FolderHandler = FolderHandler()
		self._model_processor: ModelProcessor = ModelProcessor()

	def sort_folders_by_oldest_stream(self, folders):
		"""Sort a list of folders based on the oldest modification date of files."""
		return sorted(folders, key=lambda x: self._folder_handler.find_oldest_modified_date_in_folder(x[0]))


	def run(self):
		# ==== TESTING ====

		# tester = FileParser()
		# results = tester.extract_datetime("aria_petit_2024-01-12_13-47-00_781.ts")

		# print(f"Result: {results}")

		# exit()
		
		# ==== STOP TESTING ====


		directory_path = ORIGINAL_LOCATION_PATH

		start_time = time.time()

		model_directories = []

		for subdirectory in os.listdir(directory_path):
			subdirectory_path = Path(directory_path, subdirectory)
			model_directories.append((subdirectory_path, subdirectory))

		model_directories = self.sort_folders_by_oldest_stream(model_directories)
		num_models = len(model_directories)

		for _, model in model_directories:
			self._model_processor.merge_model_streams(model, SHEET, BURN, DELETE)

		end_time = time.time()
		elapsed_time = end_time - start_time

		time_formatted = self._time_utils.format_time(elapsed_time, TimeFormat.HMS)
		
		if elapsed_time > 0:
			print(f"Avg {self._time_utils.format_time(elapsed_time / num_models, TimeFormat.Dynamic, round_digits=4)} per model!")

		print(" ")
		print(f"It took {time_formatted} to merge all possible segments for every model.")
