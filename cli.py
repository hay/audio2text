#!/usr/bin/env python3
from audio2text import AudioToText
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help = "File to parse")
parser.add_argument('-v', '--verbose', action="store_true")
parser.add_argument("-o", "--output")
parser.add_argument("-of", "--output-format",
    choices = ["txt", "vtt", "srt", "csv", "words"],
    default = "srt"
)

args = parser.parse_args()

if not args.file or not args.output:
    parser.print_help()
else:
    a2t = AudioToText(
        model_path = Path("models") / "ggml-large.bin",
        language = "nl",
        output_type = args.output_format
    )

    in_path = Path(args.file)
    out_path = Path(args.output)

    a2t.transcribe(in_path, out_path)