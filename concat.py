import os
import subprocess
import tempfile
import time
import shutil
from pathlib import Path
from datetime import datetime, timedelta

ffmpeg_path = "D:/CTBrec/ctbrec/lib/ffmpeg/ffmpeg.exe"
ffprobe_path = "C:/Program Files/Wondershare/Wondershare Repairit/ffprobe.exe"
ffont = "C:/Windows/fonts/arial.ttf"
temp_file = "Y:/Media Library/Porn/temp_stream.txt"
final_destination_root = "Y:/Media Library/Porn/VIDEO/Autorecordings/2. Recordings Triage"

def format_time(total_seconds):
	hours = int(total_seconds / 3600)
	remaining_seconds = total_seconds % 3600
	minutes = int(remaining_seconds / 60)
	seconds = int(remaining_seconds % 60)
	
	return f"{hours:02d}H:{minutes:02d}M:{seconds:02d}S"

def create_contact_sheet(infile, output_image, burn=False):
	input_dir = os.path.dirname(infile)
	tmpdir = os.path.join(input_dir, os.urandom(6).hex())
	tmpdir = tmpdir.replace('\\', '/')
	os.makedirs(tmpdir, exist_ok=True)

	duration_process = subprocess.Popen([ffprobe_path, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "-i", infile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	duration_output, duration_error = duration_process.communicate()

	if duration_error:
		print("Error getting video duration:", duration_error)
		return

	try:
		duration = float(duration_output)

		for i in range(1, 57):
			interval = int((i - 0.5) * duration / 56)
			ttext = f"{interval // 3600:02d}\:{(interval % 3600) // 60:02d}\:{interval % 60:02d}"

			if burn:
				tmp_image_path = os.path.join(tmpdir, f'image{i:02d}.png').replace("\\", '/')
				ffcmd = f"{ffmpeg_path} -y -skip_frame nokey -ss {interval} -i \"{infile}\" -vf scale=-1:720,select='eq(pict_type,I)',drawtext='text={ttext}:fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h-10)' -vframes 1 \"{tmp_image_path}\""
			else:
				tmp_image_path = os.path.join(tmpdir, f'image{i:02d}.png').replace("\\", '/')
				ffcmd = f"{ffmpeg_path} -y -skip_frame nokey -ss {interval} -i \"{infile}\" -vf select='eq(pict_type,I)' -vframes 1 \"{tmp_image_path}\""

			print(ffcmd)
			process = subprocess.Popen(ffcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			ffmpeg_output, ffmpeg_error = process.communicate()

			if process.returncode == 0:
				# print("Successfully executed!")
				...
			else:
				print(ffcmd)
				print("Something went wrong with executing!")
				error_lines = ffmpeg_error.decode('utf-8').split('\n')
				for line in error_lines:
					print(line)
			# exit()

		# Modify the command to use wildcard pattern for input
		ffcmd = f"{ffmpeg_path} -y -i \"{tmpdir}/image%02d.png\" -vf \"scale=317:-1,tile=8x7:color=0x333333:margin=2:padding=2,scale=2560:-1\" -q:v 3 \"{output_image}\""

		print(ffcmd)
		process = subprocess.Popen(ffcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		ffmpeg_output, ffmpeg_error = process.communicate()

		if process.returncode == 0:
			print("Successfully executed!")
		else:
			print("Something went wrong with executing!")
			error_lines = ffmpeg_error.decode('utf-8').split('\n')
			for line in error_lines:
				print(line)

	except Exception as e:
		print(f"An error occurred: {e}")

	for file in os.listdir(tmpdir):
		file_path = os.path.join(tmpdir, file)
		if os.path.isfile(file_path):
			os.remove(file_path)

	os.rmdir(tmpdir)

def get_video_duration(infile):
	if os.path.exists(infile):
		try:
			info = subprocess.check_output([ffprobe_path, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'format=duration', '-of', 'csv=p=0', infile], text=True)
			duration = float(info.strip())
			return duration
		except subprocess.CalledProcessError as e:
			print(f"Error while getting duration for {infile}: {e}")
			return 0.0
	else:
		return 0.0

def concat_files(files, output_path):
	with open(temp_file, 'w') as tempf:
		for file in files:
			tempf.write(f"file \'file:{file}\'\n")

	# exit()
	cmd = [
		f'{ffmpeg_path}', '-y', '-f', 'concat', '-safe', '0', '-i', temp_file, '-c', 'copy', f"{output_path}"
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

def extract_datetime_from_filename(filename):
	parts = filename.split('_')
	# print(parts)
	if len(parts) >= 2:
		date_str, time_str = parts[-3], parts[-2]
		return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H-%M-%S")
	return None

def extract_timestamp_from_filename(filename):
	parts = filename.split('_')
	if len(parts) >= 2:
		date_str, time_str = parts[-3], parts[-2]
		dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H-%M-%S")
		timestamp = (dt - datetime(1970, 1, 1)).total_seconds()  # Calculate seconds since Unix epoch
		return int(timestamp)
	return None

def time_difference(file1, file2):
	start_time_file1 = extract_datetime_from_filename(file1)
	end_time_file1 = start_time_file1 + timedelta(seconds=get_video_duration(file1))
	start_time_file2 = extract_datetime_from_filename(file2)
	
	time_diff = (start_time_file2 - end_time_file1).total_seconds()
	return time_diff

def get_contact_sheetpath(f):
	_directory_path = os.path.abspath(os.path.dirname(f))
	file_name = os.path.basename(f)
	base_name, extension = os.path.splitext(file_name)
	base_name_without_ms = base_name[:-7]  # Correct
	contact_sheet_path = os.path.join(_directory_path, f"{base_name_without_ms}_contactsheet.jpg").replace('\\', '/')
	return contact_sheet_path

def merge_and_delete_files(files, model_name, directory_path, delete, sheet, burn):
	start_datetime = extract_datetime_from_filename(files[0]).strftime('%Y-%m-%d %H:%M:%S')
	end_datetime = (extract_datetime_from_filename(files[-1]) + timedelta(seconds=get_video_duration(files[-1]))).strftime('%Y-%m-%d %H:%M:%S')
	output_file_name = f'{model_name}, START {start_datetime}, END {end_datetime}.mkv'.replace(':', '.')
	os.makedirs(os.path.join(final_destination_root, model_name, "MERGED"), exist_ok=True)
	output_file_path = os.path.join(final_destination_root, model_name, "MERGED", output_file_name).replace('\\', '/')
	
	# Check if merging was successful before proceeding with deletion
	if concat_files(files, output_file_path):
		if delete:
			for f in files:
				if os.path.exists(f):
					os.remove(f)

			# Add code to delete associated contact sheets
			for f in files:
				contact_sheet_path = get_contact_sheetpath(f)
				if os.path.exists(contact_sheet_path):
					os.remove(contact_sheet_path)

		if sheet:
			create_contact_sheet(output_file_path, output_file_path.replace('.mkv', '.jpg'), burn)

def move_to_couldn_merge_directory(files, couldn_merge_directory):
	for file in files:
		if file is None:
			return
		contact_sheet = get_contact_sheetpath(file)
		try:
			print(f"Moving '{os.path.basename(file)}' to 'Couldn't MERGE' directory.")
			shutil.move(file, os.path.join(couldn_merge_directory, os.path.basename(file)).replace('\\', '/'))
			shutil.move(contact_sheet.replace('\\', '/'), os.path.join(couldn_merge_directory, os.path.basename(contact_sheet)).replace('\\', '/'))
			print(f"Moved '{os.path.basename(file)}' to 'Couldn't MERGE' directory.")
		except Exception as e:
			print(f"Error while moving file '{os.path.basename(file)}' to 'Couldn't MERGE' directory: {e}")

def process_current_files(current_files, model_name, directory_path, delete, sheet, burn, couldn_merge_directory):
	if len(current_files) >= 2:
		try:
			merge_and_delete_files(current_files, model_name, directory_path, delete, sheet, burn)
		except Exception as e:
			print(f"Error while merging files: {e}")
			move_to_couldn_merge_directory(current_files, couldn_merge_directory)
	else:
		move_to_couldn_merge_directory(current_files, couldn_merge_directory)

def process_files(video_files, current_files, model_name, directory_path, delete, sheet, burn, couldn_merge_directory):
	for file in video_files:
		file_path = os.path.join(directory_path, file).replace("\\", "/")

		if not current_files or time_difference(current_files[-1], file) > 400:
			process_current_files(current_files, model_name, directory_path, delete, sheet, burn, couldn_merge_directory)
			current_files = []

		current_files.append(file_path)

	process_current_files(current_files, model_name, directory_path, delete, sheet, burn, couldn_merge_directory)

def main(directory_path, model_name, sheet=False, burn=False, delete=False):
	_start_time = time.time()
	os.chdir(directory_path)

	video_files = sorted(
		filter(lambda f: f.endswith(('.ts', '.mp4')), os.listdir()),
		key=extract_timestamp_from_filename
	)

	couldn_merge_directory = os.path.join(final_destination_root, model_name, "Couldn't MERGE")
	os.makedirs(couldn_merge_directory, exist_ok=True)

	current_files = []
	process_files(video_files, current_files, model_name, directory_path, delete, sheet, burn, couldn_merge_directory)

	_end_time = time.time()
	_elapsed_time = _end_time - _start_time

	_time_formatted = format_time(_elapsed_time)

	print(" ")
	print(f"It took {_time_formatted} to merge all possible segments for model {model_name}.")    
	print(" ")
	print("=====================================")
	print(" ")

def is_mp4_file(item):
	"""Check if the file has a .mp4 extension."""
	return os.path.isfile(item) and item.lower().endswith('.mp4')

def get_file_modified_date(file_path):
	"""Get the modification time of a file."""
	return os.path.getmtime(file_path)

def find_oldest_modified_date(folder_path):
	"""Find the oldest modification date of .mp4 files in the specified folder."""
	if not os.path.isdir(folder_path):
		return None

	mp4_files = [
		get_file_modified_date(os.path.join(folder_path, item))
		for item in os.listdir(folder_path) if is_mp4_file(os.path.join(folder_path, item))
	]

	return min(mp4_files, default=float('-inf'))

def sort_folders_by_oldest_stream(folders):
	"""Sort a list of folders based on the oldest modification date of .mp4 files."""
	return sorted(folders, key=lambda x: find_oldest_modified_date(x[0]))

if __name__ == '__main__':
	directory_path = "H:/Porn Streaming Cache/2. Recordings Triage"
	sheet = True  # Set this to True if you want to create a contact sheet
	burn = True  # Set this to True if you want to burn timestamps
	delete = True  # Set this to True if you want to delete temporary images

	start_time = time.time()

	model_directories = []

	for subdirectory in os.listdir(directory_path):
		subdirectory_path = os.path.join(directory_path, subdirectory).replace('\\', '/')
		model_directories.append((subdirectory_path, subdirectory))

	model_directories = sort_folders_by_oldest_stream(model_directories)
	num_models = len(model_directories)

	for model_directory, model in model_directories:
		print(model, model_directory)
		if os.path.isdir(model_directory):
			main(model_directory, model, sheet=sheet, burn=burn, delete=delete)

	end_time = time.time()
	elapsed_time = end_time - start_time

	time_formatted = format_time(elapsed_time)
	
	if elapsed_time > 0:
		print(f"Avg {format_time(elapsed_time / num_models)} per model!")

	print(" ")
	print(f"It took {time_formatted} to merge all possible segments for every model.")   
