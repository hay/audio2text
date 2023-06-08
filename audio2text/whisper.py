from . import WHISPER_IMPLEMENTATION_CPP
from .whispercpp import CppTranscriber

class Transcriber:
    def __init__(self, implementation, **kwargs):
        if implementation == WHISPER_IMPLEMENTATION_CPP:
            self.__transcriber = CppTranscriber(**kwargs)
        else:
            raise Exception(f"Unsupported implementation: {implementation}")

    def transcribe(self, **kwargs):
        print(kwargs)
        self.__transcriber.transcribe(**kwargs)