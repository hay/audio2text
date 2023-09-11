import os

DEFAULT_DOWNLOAD_TIMEOUT = 60 # Seconds
DEFAULT_LANG = "auto" # Auto detect
DEFAULT_OUTPUT_TYPE = "srt"
DEFAULT_PROCESSOR_COUNT = 1
DEFAULT_SRTPARSER_OUTPUT = "csv"
SRTPARSER_OUTPUT_FORMATS = ["csv", "json", "txt"]
TMP_FILE_FOLDER = os.environ['TMPDIR']
WHISPER_OUTPUT_FORMATS = ["txt", "vtt", "srt", "words", "csv"]