import subprocess

from constants import DEBUGGING


class FFMPEGCommandHelper:
	"""
	Helper class meant to streamline the execution and formatting of a ffmpeg command. Enjoy.
	"""
	def execute_command(self, command: list, display_output: bool=True) -> subprocess.CompletedProcess:
		"""
		Executes a given ffmpeg command.
		Prints errors regardless.
		"""
		if DEBUGGING:
			print(f"Executing command: {command}")

		result = subprocess.run(command, capture_output=display_output)
		if result.returncode != 0:
			print("Error executing command:")
			print(f"Command: {' '.join(command)}")
			error_lines = result.stderr.decode('utf-8').split('\n')
			for line in error_lines:
				print(line)
		return result
