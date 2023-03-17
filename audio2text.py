#!/usr/bin/env python3
from audio2text.whisper import WhisperTranscriber
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-di", "--diarize",
    help = "Diarize audio (only works for natural stereo audio)",
    action = "store_true"
)
parser.add_argument("-i", "--input", help = "File to parse")
parser.add_argument("-l", "--language")
parser.add_argument("-m", "--model-path",
    help = "Path to model",
    default = Path("models") / "ggml-large.bin"
)
parser.add_argument("-o", "--output")
parser.add_argument("-of", "--output-format",
    choices = ["txt", "vtt", "srt", "csv", "words"],
    default = "srt"
)
parser.add_argument("-su", "--speed-up", action = "store_true")
parser.add_argument("-v", "--verbose", action = "store_true")
parser.add_argument("-w", "--whisper-path",
    default = Path("./whispercpp")
)

args = parser.parse_args()

if not args.input:
    parser.print_help()
else:
    whisper = WhisperTranscriber(
        model_path = args.model_path,
        whisper_path = args.whisper_path,
        diarize = args.diarize,
        language = args.language,
        output_type = args.output_format,
        speed_up = args.speed_up,
        verbose = args.verbose
    )

    in_path = Path(args.input)

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = False

    whisper.transcribe(in_path, out_path)