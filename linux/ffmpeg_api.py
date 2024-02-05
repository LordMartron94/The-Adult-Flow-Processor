from constants import *

import os
import subprocess

class FfmpegAPI:
	"""
	Custom layer built on top of the FFMPEG CLI to allow for easier interaction in other parts of the software.
	"""

	def __init__(self):
		...

    def _empty_cache(self):
        for file in os.listdir(CACHE):
            file_path = os.path.join(CACHE, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

	def get_video_duration(self, video_file: str) -> Union[str, None]:
		duration_process = subprocess.Popen(['ffprobe', "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "-i", video_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    	duration_output, duration_error = duration_process.communicate()

	    if duration_error:
	        print("Error getting video duration:", duration_error)
	        return

	    return duration_output


	def create_sprites_for_sheet(self, duration: str, video_file_path: str, burn):
        for i in range(1, 57):
            interval = int((i - 0.5) * duration / 56)

            if burn:
                ttext = f"{interval // 3600:02d}\:{(interval % 3600) // 60:02d}\:{interval % 60:02d}"

                tmp_image_path = os.path.join(CACHE, f'image{i:02d}.png').replace("\\", '/')
                command = f"ffmpeg -y -skip_frame nokey -ss {interval} -i \"{video_file_path}\" -vf scale=-1:720,select='eq(pict_type,I)',drawtext='text={ttext}:fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h-10)' -vframes 1 \"{tmp_image_path}\""
            else:
                tmp_image_path = os.path.join(CACHE, f'image{i:02d}.png').replace("\\", '/')
                command = f"ffmepg -y -skip_frame nokey -ss {interval} -i \"{video_file_path}\" -vf select='eq(pict_type,I)' -vframes 1 \"{tmp_image_path}\""

            # print(command)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output, ffmpeg_error = process.communicate()

            if process.returncode == 0:
                ...
            else:
                print(command)
                print("Something went wrong with executing!")
                error_lines = ffmpeg_error.decode('utf-8').split('\n')
                for line in error_lines:
                    print(line)

    def combine_sprites_into_sheet(self, output_image_path: str):
        command = f"ffmpeg -y -i \"{CACHE}/image%02d.png\" -vf \"scale=317:-1,tile=8x7:color=0x333333:margin=2:padding=2,scale=2560:-1\" -q:v 3 \"{output_image_path}\""
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpeg_output, ffmpeg_error = process.communicate()

        if process.returncode == 0:
            print("Successfully executed!")
        else:
            print("Something went wrong with executing!")
            error_lines = ffmpeg_error.decode('utf-8').split('\n')
            for line in error_lines:
                print(line)

	def create_contact_sheet_for_video(video_file_path: str, output_image_path: str, burn=False):
		input_directory = os.path.dirname(video_file_path)

        try:
            duration = self.get_video_duration(video_file_path)
            self.create_sprites_for_sheet(duration, video_file_path, burn)
            self.combine_sprites_into_sheet(output_image_path)
        except Exception as e:
            print(f"An error occurred: {e}")

        self._empty_cache()

