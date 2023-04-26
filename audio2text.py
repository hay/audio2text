#!/usr/bin/env python3
from audio2text import WHISPER_OUTPUT_FORMATS
from audio2text.url import download_tmp_file
from audio2text.whisper import WhisperTranscriber
from pathlib import Path
import argparse
import logging
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-di", "--diarize",
    help = "Diarize audio (only works for natural stereo audio)",
    action = "store_true"
)
parser.add_argument("-i", "--input", help = "File to parse")
parser.add_argument("-l", "--language")
parser.add_argument("-lf", "--log-file",
    help = "Path to a logging file"
)
parser.add_argument("-m", "--model-path",
    help = "Path to model",
    default = Path("models") / "ggml-large.bin"
)
parser.add_argument("-o", "--output")
parser.add_argument("-od", "--output-directory",
    help = "When giving this argument, a directory will be created before all other commands are run"
)

OF_FORMATS = WHISPER_OUTPUT_FORMATS.copy().append("all")
parser.add_argument("-of", "--output-format",
    choices = OF_FORMATS,
    default = "srt",
    help = "Output format, when giving 'all', all formats will be used"
)

parser.add_argument("-su", "--speed-up", action = "store_true")
parser.add_argument("-u", "--url",
    help = "Give a URL to an audio file to download (e.g. mp3)"
)
parser.add_argument("-v", "--verbose", action = "store_true")
parser.add_argument("-w", "--whisper-path",
    default = Path("./whispercpp")
)
parser.add_argument("-wa", "--whisper-args",
    help = "Give a string of extra parameters to give to the whisper executable"
)

args = parser.parse_args()

if (not args.input) and (not args.url):
    parser.print_help()
else:
    loglevel = logging.DEBUG if args.verbose else logging.WARNING

    loghandlers = [
        logging.StreamHandler(sys.stdout)
    ]

    if args.output_directory:
        logging.info(f"Creating output direcory: {args.output_directory}")
        Path(args.output_directory).mkdir(parents = True, exist_ok = True)

    if args.log_file:
        loghandlers.append( logging.FileHandler(args.log_file, "a") )

    logging.basicConfig(
        datefmt = '%H:%M:%S',
        format = '%(asctime)s,%(msecs)d:%(name)s:%(levelname)s %(message)s',
        handlers = loghandlers,
        level = loglevel
    )

    logging.info("")
    logging.info(f"Logging setup, level ${loglevel}")
    logging.info("*** STARTING WHISPER TRANSCRIBER ***")

    whisper = WhisperTranscriber(
        model_path = args.model_path,
        whisper_path = args.whisper_path,
        diarize = args.diarize,
        language = args.language,
        output_type = args.output_format,
        speed_up = args.speed_up,
        whisper_args = args.whisper_args
    )

    if args.url:
        file_path = download_tmp_file(args.url)
    else:
        file_path = args.input

    in_path = Path(file_path)

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = False

    whisper.transcribe(in_path, out_path)