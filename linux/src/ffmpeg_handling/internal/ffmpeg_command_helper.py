import subprocess

from constants import DEBUGGING


class FFMPEGCommandHelper:
	"""
	Helper class meant to streamline the execution and formatting of a ffmpeg command. Enjoy.
	"""
	def execute_command(self, command: list, output_override: bool = False) -> subprocess.CompletedProcess:
		"""
		Executes a given ffmpeg command.
		Prints errors regardless.
		"""
		if DEBUGGING or output_override:
			print(f"Executing command: {command}")

		result = subprocess.run(command, capture_output=True)
		if result.returncode != 0:
			print("Error executing command:")

			if not DEBUGGING:
				print(f"Command: {command}")
				
			error_lines = result.stderr.decode('utf-8').split('\n')
			for line in error_lines:
				print(line)
		return result
