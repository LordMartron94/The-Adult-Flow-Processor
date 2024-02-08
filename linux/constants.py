import os

DEBUGGING: bool = True
PROJECT_ROOT: str = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH: str = os.path.join(PROJECT_ROOT, "CACHE")

# ===== CONFIG =====

# ---- PATHS ----
DATA_STREAM_PATH: str = "/mnt/nas/5TB WD External/Media Library/Porn/Porn Utilities/Stream Segment Merger/linux/CACHE/data_stream.txt"
ORIGINAL_LOCATION_PATH: str = "/media/mr-hoorn/Seagate External (HDD) [3.7TB]/Porn Streaming Cache/2. Recordings Triage"
FINAL_DESTINATION_ROOT: str = "/mnt/nas/5TB WD External/Media Library/Porn/Utility Tests/"

FINAL_DIRECTORY_STRUCTURE: str = "Streaming (Cam4, Stripchat, etc.)/${model_name}/${year}/${month}/${day}"
MERGE_NAME_TEMPLATE: str = "${model_name}, START ${start_date}, END ${end_date}"

# ---- VIDEO HANDLING ----
MERGED_VIDEO_EXTENSION: str = ".mp4"
MAX_DIFFERENCE_BETWEEN_SEGMENTS = 400  # Difference between segments in seconds before a segment is decided to be a loose segment (a stream on its own).

SHEET = True  # Whether to create a contact sheet for merged files.
BURN = True  # Whether to burn the timestamps into the contact sheet.
DELETE = True  # Whether to delete the original segments after merging the file.

DELETE_CORRUPT_VIDEOS = True  # Whether to delete videos that are deemed corrupt by ffmpeg.
