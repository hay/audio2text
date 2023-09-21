from . import ( DEFAULT_BATCH_SIZE, DEFAULT_LANG, DEFAULT_OUTPUT_TYPE )
from pathlib import Path
import logging
import subprocess

logger = logging.getLogger(__name__)

class WhisperXEngine:
    def __init__(self,
        model_name,
        language = DEFAULT_LANG,
        output_type = DEFAULT_OUTPUT_TYPE,
        verbose = None,
        diarize = None,
        whisper_args = None
    ):
        self.model_name = model_name
        self.batch_size = DEFAULT_BATCH_SIZE
        self.language = language or DEFAULT_LANG
        self.output_type = output_type or DEFAULT_OUTPUT_TYPE
        self.verbose = verbose or False
        self.diarize = diarize or False
        self.whisper_args = whisper_args or False
        logger.info(f"Initialized AudioToText")

    def transcribe(self, in_path, out_path):
        logger.info(f"Transcribing {in_path} as {out_path}")

        if not in_path.is_file():
            raise FileNotFoundError(f"File not found: {in_path}")

        cmd = [
            "whisperx",
            in_path.resolve(),
            "--model", self.model_name
        ]

        if self.language:
            cmd.append("--language")
            cmd.append(self.language)

        if self.diarize:
            cmd.append("--diarize")

        if self.batch_size:
            cmd.append("--batch_size")
            cmd.append(self.batch_size)

        if self.verbose:
            cmd.append("--verbose")

        if out_path:
            cmd.append("--output_format")
            cmd.append(self.output_type)
            cmd.append("--output_dir")
            cmd.append(out_path)

        if self.whisper_args:
            cmd.append(self.whisper_args)

        command = " ".join([str(c) for c in cmd])
        logger.debug(f"Executing whisperx command '{command}'")
        subprocess.check_call(command, shell = True)