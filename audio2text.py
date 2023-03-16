import subprocess

class AudioToText:
    def __init__(self, model_path,
        language = "en",
        output_type = "vtt",
        processors = 1
    ):
        self.model_path = model_path
        self.language = language
        self.output_type = output_type
        self.processors = processors

    def transcribe(self, in_path, out_path):
        cmd = [
            "./whispercpp",
            "-m", str(self.model_path.resolve()),
            "--file", str(in_path.resolve()),
            "-l", self.language,
            f"--output-{self.output_type}",
            "-of", str(out_path.resolve()),
            "-p", str(self.processors)
        ]

        command = " ".join(cmd)
        print(command)
        subprocess.check_call(command, shell = True)