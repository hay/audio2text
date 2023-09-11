import os

DEFAULT_DOWNLOAD_TIMEOUT = 60 # Seconds
DEFAULT_LANG = None # Auto detect
DEFAULT_BATCH_SIZE = 16
DEFAULT_DEVICE = "cuda"
DEFAULT_COMPUTE_TYPE = "float16"
DEFAULT_OUTPUT_TYPE = "all"
DEFAULT_PROCESSOR_COUNT = 1
DEFAULT_WRITER_OPTIONS = {"max_line_width":None,
                          "max_line_count":None,
                          "highlight_words":None}
DEFAULT_SRTPARSER_OUTPUT = "csv"
SRTPARSER_OUTPUT_FORMATS = ["csv", "json", "txt"]
TMP_FILE_FOLDER = os.environ['TMPDIR']
WHISPER_OUTPUT_FORMATS = ["txt", "vtt", "srt", "words", "csv"]