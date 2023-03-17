#!/usr/bin/env python3
from audio2text import DEFAULT_SRTPARSER_OUTPUT, SRTPARSER_OUTPUT_FORMATS
from audio2text.srt import SrtParser
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help = "File to parse")
parser.add_argument("-o", "--output")
parser.add_argument("-of", "--output-format",
    choices = SRTPARSER_OUTPUT_FORMATS,
    default = DEFAULT_SRTPARSER_OUTPUT
)
parser.add_argument("-tr", "--trim", help = "Trim whitespace in content")
parser.add_argument("-v", "--verbose", action = "store_true")

args = parser.parse_args()

if not args.input:
    parser.print_help()
else:
    parser = SrtParser(
        output_format = args.output_format,
        trim = args.trim,
        verbose = args.verbose
    )

    in_path = Path(args.input)

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = False

    parser.convert(in_path, out_path)