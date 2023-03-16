#!/usr/bin/env python3
from audio2text import AudioToText
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
parser.add_argument('-v', '--verbose', action="store_true")

args = parser.parse_args()

if not args.input or not args.output:
    parser.print_help()
else:
    a2t = AudioToText(
        diarize = args.diarize,
        model_path = args.model_path,
        language = args.language,
        output_type = args.output_format,
        verbose = args.verbose
    )

    in_path = Path(args.input)
    out_path = Path(args.output)

    a2t.transcribe(in_path, out_path)