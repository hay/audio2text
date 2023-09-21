from . import DEFAULT_LANG, DEFAULT_PROCESSOR_COUNT, DEFAULT_OUTPUT_TYPE, WHISPER_OUTPUT_FORMATS
from .file import get_tmp_file_path
from pathlib import Path
import ffmpeg
import logging
import subprocess

logger = logging.getLogger(__name__)

class WhisperTranscriber:
    def __init__(self,
        whisper_path,
        model_path,
        language = DEFAULT_LANG,
        output_type = DEFAULT_OUTPUT_TYPE,
        processors = DEFAULT_PROCESSOR_COUNT,
        verbose = None,
        diarize = None,
        speed_up = None,
        keep_tmp_file = None,
        whisper_args = None
    ):
        self.whisper_path = Path(whisper_path)
        self.model_path = Path(model_path)
        self.language = language or DEFAULT_LANG
        self.output_type = output_type or DEFAULT_OUTPUT_TYPE
        self.processors = processors or DEFAULT_PROCESSOR_COUNT
        self.verbose = verbose or False
        self.diarize = diarize or False
        self.speed_up = speed_up or False
        self.whisper_args = whisper_args or False
        self.keep_tmp_file = keep_tmp_file or False
        logger.info(f"Initialized AudioToText")

    def convert(self, in_path):
        if not Path(in_path).is_file():
            raise FileNotFoundError(f"File not found: {in_path}")

        tmp_file_path = get_tmp_file_path(suffix = ".wav")

        logger.info(f"Converting {in_path} to {tmp_file_path}")

        try :
            (
                ffmpeg.input(in_path)
                .output(
                    str(tmp_file_path.resolve()),
                    acodec = "pcm_s16le",
                    ac = 2,
                    ar = 16000
                ).run(quiet = True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}")

        return tmp_file_path

    def transcribe(self, in_path, out_path):
        logger.info(f"Transcribing {in_path} as {out_path}")
        tmp_file = self.convert(in_path)
        self.transcribe_processed_wav(tmp_file, out_path)

        if self.keep_tmp_file:
            logger.info(f"Keeping tmp file {tmp_file}")
        else:
            logger.info(f"Removing tmp file {tmp_file}")
            tmp_file.unlink()

    def transcribe_processed_wav(self, in_path, out_path = False):
        cmd = [
            str(self.whisper_path.resolve()),
            "--model", str(self.model_path.resolve()),
            "--file", str(in_path.resolve()),
            "--language", self.language
        ]

        if self.diarize:
            cmd.append("--diarize 1")

        if self.whisper_args:
            cmd.append(self.whisper_args)

        if out_path:
            # When having the special output type 'all', we're getting all
            # output formats
            if self.output_type == "all":
                logger.debug("Outputting to all output formats")

                for fmt in WHISPER_OUTPUT_FORMATS:
                    cmd.append(f"--output-{fmt}")
            else:
                # Split by comma to make multiple formats work
                for fmt in self.output_type.split(","):
                    cmd.append(f"--output-{fmt}")

            cmd.append(f"-of {out_path.resolve()}")

        command = " ".join(cmd)
        logger.debug(f"Executing whisper command '{command}'")
        subprocess.check_call(command, shell = True)