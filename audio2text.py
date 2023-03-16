from pathlib import Path
import ffmpeg
from shortuuid import uuid
import subprocess

class AudioToText:
    def __init__(self,
        model_path,
        language = "en",
        output_type = "vtt",
        processors = 1,
        verbose = False,
        diarize = False
    ):
        self.model_path = model_path
        self.language = language
        self.output_type = output_type
        self.processors = processors
        self.verbose = verbose
        self.diarize = diarize
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

    def transcribe_processed_wav(self, in_path, out_path):
        cmd = [
            "./whispercpp",
            "-m", str(self.model_path.resolve()),
            "--file", str(in_path.resolve()),
            "-l", self.language,
            f"--output-{self.output_type}",
            "-of", str(out_path.resolve()),
            "-p", str(self.processors)
        ]

        if self.diarize:
            cmd.append("--diarize 1")

        command = " ".join(cmd)
        self._log(f"Executing whisper command '{command}'")
        subprocess.check_call(command, shell = True)