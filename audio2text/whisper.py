from . import DEFAULT_DEVICE, DEFAULT_COMPUTE_TYPE, DEFAULT_BATCH_SIZE, DEFAULT_LANG, DEFAULT_OUTPUT_TYPE, DEFAULT_WRITER_OPTIONS, DEFAULT_PROCESSOR_COUNT
from pathlib import Path
import logging
import whisperx
import whisper

logger = logging.getLogger(__name__)

class WhisperTranscriber:
    def __init__(self,
        model,
        device = DEFAULT_DEVICE,
        compute_type = DEFAULT_COMPUTE_TYPE,
        language = DEFAULT_LANG,
        output_type = DEFAULT_OUTPUT_TYPE,
        writer_options = DEFAULT_WRITER_OPTIONS,
        processors = DEFAULT_PROCESSOR_COUNT,
        verbose = None,
        diarize = None,
        speed_up = None,
        keep_tmp_file = None,
        whisper_args = None
    ):
        self.model = whisperx.load_model(model, device, compute_type=compute_type)
        self.batch_size = DEFAULT_BATCH_SIZE
        self.language = language or DEFAULT_LANG
        self.output_type = output_type or DEFAULT_OUTPUT_TYPE
        self.processors = processors or DEFAULT_PROCESSOR_COUNT
        self.writer_options = writer_options or DEFAULT_WRITER_OPTIONS
        self.verbose = verbose or False
        self.diarize = diarize or False
        self.speed_up = speed_up or False
        self.whisper_args = whisper_args or False
        self.keep_tmp_file = keep_tmp_file or False
        logger.info(f"Initialized AudioToText")

    def load_file(self, in_path):
        if not Path(in_path).is_file():
            raise FileNotFoundError(f"File not found: {in_path}")

        try :
            audio_file = whisperx.load_audio(in_path)

        except whisperx.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}")

        return audio_file

    def transcribe(self, in_path, out_path):
        logger.info(f"Transcribing {in_path} as {out_path}")
        audio_file = self.load_file(in_path)
        self.transcribe_processed_wav(audio_file, out_path)

        if self.keep_tmp_file:
            logger.info(f"Keeping tmp file {audio_file}")
        else:
            logger.info(f"Removing tmp file {audio_file}")
            audio_file.unlink()

    def transcribe_processed_wav(self, in_path, out_path = False):
               
        if self.language:
            result = whisperx.transcribe(in_path, batch_size=self.batch_size, language=self.language)
        else:
            result = whisperx.transcribe(in_path, batch_size=self.batch_size)

        if out_path:
            # When having the special output type 'all', we're getting all
            # output formats
            writer = whisper.utils.get_writer(self.output_type, out_path)
            writer(result, in_path, self.writer_options)
