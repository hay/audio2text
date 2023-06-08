from . import DEFAULT_LANG, DEFAULT_PROCESSOR_COUNT, DEFAULT_OUTPUT_TYPE, WHISPER_OUTPUT_FORMATS
from pathlib import Path
import logging
import time

logger = logging.getLogger(__name__)

class FasterWhisperTranscriber:
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
        logger.info(f"Initializing faster_whisper implementation")

        if self.verbose:
            logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

    def transcribe(self, in_path, out_path):
        logger.info(f"Transcribing {in_path} as {out_path}")
        self.__transcribe_audio(in_path, out_path)

    def __transcribe_audio(self, in_path, out_path = False):
        logger.debug("Loading Faster Whisper module")
        from faster_whisper import WhisperModel

        # FIXME: obviously we need something better than translating
        # model paths into model ids
        if "large" in str(self.model_path):
            model_size = "large-v2"
        else:
            raise Exception(f"Invalid model: {self.model_path}")

        logger.info(f"Loading model '{model_size}'")

        model = WhisperModel(model_size, device = "cpu", compute_type = "int8")
        segments, info = model.transcribe(str(in_path), beam_size = 5)

        lang = info.language
        prob = info.language_probability
        logger.info(f"Detected language '{lang}' with probability {prob}")

        ts = time.time()

        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

        delta = round(time.time() - ts, 3)
        logger.debug(f"Transcription (wall time) took {delta}s")