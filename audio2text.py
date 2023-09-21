#!/usr/bin/env python3
from audio2text import WHISPER_OUTPUT_FORMATS, WHISPER_ENGINES, DEFAULT_WHISPER_ENGINE
from audio2text.url import download_tmp_file
from audio2text.whispercpp import WhisperCppEngine
from audio2text.whisperx import WhisperXEngine
from pathlib import Path
import argparse
import logging
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--debug",
    help = "Don't catch errors and halt all processes if errors occur",
    action = "store_true"
)
parser.add_argument("-di", "--diarize",
    help = "Diarize audio (only works for natural stereo audio)",
    action = "store_true"
)
parser.add_argument("-e", "--engine",
    help = "Engine to use",
    choices = WHISPER_ENGINES,
    default = DEFAULT_WHISPER_ENGINE
)
parser.add_argument("-i", "--input",
    help = "Audio file to transcribe, anything that ffmpeg supports will work"
)
parser.add_argument("-l", "--language",
    help = "Language of audio file, if not given Whisper will try to autodetect this"
)
parser.add_argument("-lf", "--log-file",
    help = "Log messages to a logging file with this path, will fail if the directory does not exist (use --od to prevent that)"
)
parser.add_argument("-m", "--model-path",
    help = "Path to model you want to use for transcribing",
    default = Path("models") / "ggml-large.bin"
)
parser.add_argument("-mn", "--model-name",
    help = "Name of model (used when enabling WhisperX)",
    default = "large-v2"
)
parser.add_argument("-o", "--output",
    help = "Path to output file, you don't need to give an extension"
)
parser.add_argument("-od", "--output-directory",
    help = "When giving this argument, a directory will be created before all other commands are run"
)

OF_FORMATS = WHISPER_OUTPUT_FORMATS.copy().append("all")
parser.add_argument("-of", "--output-format",
    choices = OF_FORMATS,
    default = "srt",
    help = "Output format, when giving 'all', all formats will be used"
)

parser.add_argument("-kt", "--keep-temp-files",
    action = "store_true",
    help = "Keep temporary files after transcribing (default is to remove them)"
)

parser.add_argument("-u", "--url",
    help = "Give a URL to an audio file to download (e.g. mp3)"
)
parser.add_argument("-v", "--verbose",
    action = "store_true",
    help = "Print debug information"
)
parser.add_argument("-w", "--whisper-path",
    default = Path("./whispercpp"),
    help = "Path to the Whisper executable (defaults to ./whispercpp)"
)
parser.add_argument("-wa", "--whisper-args",
    help = "Give a string of extra parameters to give to the whisper executable"
)

args = parser.parse_args()
logger = logging.getLogger(__name__)

if (not args.input) and (not args.url):
    parser.print_help()
else:
    loglevel = logging.DEBUG if args.verbose else logging.INFO

    loghandlers = [
        logging.StreamHandler(sys.stdout)
    ]

    if args.output_directory:
        logger.info(f"Creating output direcory: {args.output_directory}")
        Path(args.output_directory).mkdir(parents = True, exist_ok = True)

    if args.log_file:
        print(f"Writing to log file {args.log_file}")
        loghandlers.append( logging.FileHandler(args.log_file, "a") )

    logging.basicConfig(
        format = '[%(asctime)s:%(name)s:%(levelname)s] %(message)s',
        handlers = loghandlers,
        level = loglevel
    )

    logger.debug("")
    logger.debug(f"Command line arguments: {args}")
    logger.debug(f"Logging setup, level ${loglevel}")
    logger.info("📝 Start transcribing")

    if args.engine == "whispercpp":
        logger.info("📝 Using WhisperCPP engine")
        whisper = WhisperCppEngine(
            model_path = args.model_path,
            whisper_path = args.whisper_path,
            diarize = args.diarize,
            language = args.language,
            output_type = args.output_format,
            whisper_args = args.whisper_args,
            keep_tmp_file = args.keep_temp_files
        )
    elif args.engine == "whisperx":
        logger.info("📝 Using WhisperX engine")
        whisper = WhisperXEngine(
            model_name = args.model_name,
            diarize = args.diarize,
            language = args.language,
            output_type = args.output_format,
            whisper_args = args.whisper_args
        )

    if args.url:
        try:
            file_path = download_tmp_file(args.url)
        except Exception as e:
            msg = f"Download exception: {e}"
            logger.error(msg)
            sys.exit(msg)
    else:
        file_path = args.input

    in_path = Path(file_path)

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = False

    try:
        whisper.transcribe(in_path, out_path)
    except Exception as e:
        msg = f"Transcribe exception: {e}"
        logger.error(msg)

        if args.debug:
            raise(e)
        else:
            sys.exit(msg)

    # Delete downloaded file if we've got an URL
    if args.url and not args.keep_temp_files:
        logger.debug(f"Deleting <{file_path}>")
        file_path.unlink()
    else:
        logger.debug(f"Keeping <{file_path}>")

    logger.info("Done")