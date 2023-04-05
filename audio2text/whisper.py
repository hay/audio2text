from pathlib import Path
from shortuuid import uuid
from . import DEFAULT_LANG, DEFAULT_PROCESSOR_COUNT, DEFAULT_OUTPUT_TYPE
import ffmpeg
import subprocess

class WhisperTranscriber:
    def __init__(self,
        whisper_path,
        model_path,
        language = DEFAULT_LANG,
        output_type = DEFAULT_OUTPUT_TYPE,
        processors = DEFAULT_PROCESSOR_COUNT,
        verbose = None,
        diarize = None,
        speed_up = None
    ):
        self.whisper_path = Path(whisper_path)
        self.model_path = Path(model_path)
        self.language = language or DEFAULT_LANG
        self.output_type = output_type or DEFAULT_OUTPUT_TYPE
        self.processors = processors or DEFAULT_PROCESSOR_COUNT
        self.verbose = verbose or False
        self.diarize = diarize or False
        self.speed_up = speed_up or False
        self._log(f"Initialized AudioToText")

    def _log(self, msg):
        if self.verbose:
            print(msg)

    def convert(self, in_path):
        tmp_file = Path("tmp") / f"{uuid()}.wav"

        self._log(f"Converting {in_path} to {tmp_file}")

        try :
            (
                ffmpeg.input(in_path)
                .output(
                    str(tmp_file.resolve()),
                    acodec = "pcm_s16le",
                    ac = 2,
                    ar = 16000
                ).run(quiet = True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}")

        return tmp_file

    def transcribe(self, in_path, out_path):
        self._log(f"Transcribing {in_path} as {out_path}")
        tmp_file = self.convert(in_path)
        self.transcribe_processed_wav(tmp_file, out_path)
        self._log(f"Removing tmp file {tmp_file}")
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

        if self.speed_up:
            cmd.append("--speed-up 1")

        if out_path:
            cmd.append(f"--output-{self.output_type}")
            cmd.append(f"-of {out_path.resolve()}")

        print(cmd)

        command = " ".join(cmd)
        self._log(f"Executing whisper command '{command}'")
        subprocess.check_call(command, shell = True)