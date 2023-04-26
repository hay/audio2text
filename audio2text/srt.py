from . import DEFAULT_SRTPARSER_OUTPUT, SRTPARSER_OUTPUT_FORMATS
from dataknead import Knead
from pathlib import Path
import logging
import srt

logger = logging.getLogger(__name__)

# Be nice for CSV users
CSV_FIELDNAMES = ["index", "start", "end", "content", "proprietary"]

class SrtParser:
    def __init__(self,
        output_format = None,
        trim = None,
        verbose = None
    ):
        if output_format not in SRTPARSER_OUTPUT_FORMATS:
            raise Exception(f"Invalid output_format: {output_format}")

        self.output_format = output_format or DEFAULT_SRTPARSER_OUTPUT
        self.trim = trim or True
        self.verbose = verbose or False
        logger.debug(f"Initialized SrtParser")
        logger.debug(f"output_format: {self.output_format}")

    def convert(self, in_path, out_path = None):
        with open(in_path) as f:
            generator = srt.parse(f.read())

        data = []

        for line in generator:
            if self.trim:
                content = line.content.strip()
            else:
                content = line.content

            data.append({
                "index" : line.index,
                "start" : str(line.start),
                "end" : str(line.end),
                "content" : content,
                "proprietary" : line.proprietary
            })

        # Convert to correct format
        if self.output_format == "txt":
            output = [i["content"] for i in data]
        else:
            output = data

        if not out_path:
            # Just print to stdout
            print(Knead(output))
        else:
            if self.output_format == "csv":
                Knead(output).write(out_path, fieldnames = CSV_FIELDNAMES)
            else:
                Knead(output).write(out_path)