import os

DEFAULT_BATCH_SIZE = 16
DEFAULT_DOWNLOAD_TIMEOUT = 60 # Seconds
DEFAULT_LANG = None # Auto detect
DEFAULT_OUTPUT_TYPE = "all"
DEFAULT_PROCESSOR_COUNT = 1
DEFAULT_WHISPER_ENGINE = "whispercpp"
DEFAULT_SRTPARSER_OUTPUT = "csv"
SRTPARSER_OUTPUT_FORMATS = ["csv", "json", "txt"]
TMP_FILE_FOLDER = os.environ['TMPDIR']
WHISPER_ENGINES = ["whispercpp", "whisperx"]
WHISPER_OUTPUT_FORMATS = ["txt", "vtt", "srt", "words", "csv"]