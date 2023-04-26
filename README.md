# audio2text
> Python command line utility wrappers for Whispercpp and other speech-to-text utilities

## Introduction
This is mainly a set of useful scripts to automate Whispercpp processing, including:
* Automatic conversion of any video or audio format `ffmpeg` supports to the WAV format Whispercpp needs.
* Conversion of the transcripts to CSV, SRT, TXT, VTT and WTS (karaoke subtitles).

## Install
1. You need to have a working executable version of [whisper.cpp](https://github.com/ggerganov/whisper.cpp),
   you can either place that in the root of this repo as `whispercpp` or give the
   path using the `-w` flag
2. Place your models in the `models` folder. By default `audio2text.py` will
   look for `ggml-large.bin` in the models folder. You can also use the `-m` flag to give a path to the model.
3. `ffmpeg` is required and should be somewhere in your `$PATH`
4. You might want to make a virtual environment and then install the `requirements.txt`, e.g.

```bash
python -m venv .env
source .env/bin/activate
pip install -U pip
pip install -r requirements.txt
./audio2text.py
```

## Usage

### `audio2text.py`
To convert the given `berliner.ogg` file in the test directory to a CSV file (note that you don't need to give an extension)
```bash
./audio2text.py -i test/berliner.ogg -o test/berliner -of csv
```

If you want multiple output formats you can separate them by comma
```bash
./audio2text.py -i test/berliner.ogg -o test/berliner -of srt,txt
```

When giving the argument `all` to the `-of/--output-format` flag all Whisper-supported formats will be written
```bash
./audio2text.py -i test/berliner.ogg -o test/berliner -of all
```

To prevent duplication of all possible command line options for `whisper.cpp` you can use the `-wa` / `--whisper-args` flag to pass extra command line options to the whisper.cpp executable:

```bash
./audio2text.py -i test/berliner.ogg -o test/berliner -of csv -wa="--threads 8"
```

You can also use the `-u/--url` flag to give an URL to a MP3 file (or any other audio format `ffmpeg` supports). This will be downloaded to the `tmp` directory.

```bash
./audio2text.py -u https://www.bykr.org/test/berliner.mp3
```

To enable logging to a file use the `-lf/--log-file` flag, optionally combined with the `-v/--verbose` flag:

```bash
./audio2text.py -u https://www.bykr.org/test/berliner.mp3 -v -lf log.txt
```

To write all files and the log file to a non-existing directory you can use the `-od/--output-directory` flag:

```bash
./audio2text.py -u https://www.bykr.org/test/berliner.mp3 -of all -o out/text -v -lf out/log.log -od out
```

### `srtparse.py`
Converts SRT files to JSON, CSV and TXT using [dataknead](github.com/hay/dataknead).
```bash
./srtparse.py -i test/berliner.srt -o test/berliner.csv
```

## Troubleshooting
If you add the `-v` (verbose) flag `audio2text` will give much more debug information.

## All options
You'll get this when doing `audio2text.py -h`

```
usage: audio2text.py [-h] [-di] [-i INPUT] [-l LANGUAGE] [-lf LOG_FILE]
                     [-m MODEL_PATH] [-o OUTPUT] [-od OUTPUT_DIRECTORY]
                     [-of OUTPUT_FORMAT] [-kt] [-u URL] [-v] [-w WHISPER_PATH]
                     [-wa WHISPER_ARGS]

options:
  -h, --help            show this help message and exit
  -di, --diarize        Diarize audio (only works for natural stereo audio)
  -i INPUT, --input INPUT
                        Audio file to transcribe, anything that ffmpeg
                        supports will work
  -l LANGUAGE, --language LANGUAGE
                        Language of audio file, if not given Whisper will try
                        to autodetect this
  -lf LOG_FILE, --log-file LOG_FILE
                        Log messages to a logging file with this path, will
                        fail if the directory does not exist (use --od to
                        prevent that)
  -m MODEL_PATH, --model-path MODEL_PATH
                        Path to model you want to use for transcribing
  -o OUTPUT, --output OUTPUT
                        Path to output file, you don't need to give an
                        extension
  -od OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        When giving this argument, a directory will be created
                        before all other commands are run
  -of OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                        Output format, when giving 'all', all formats will be
                        used
  -kt, --keep-temp-files
                        Keep temporary files after transcribing (default is to
                        remove them)
  -u URL, --url URL     Give a URL to an audio file to download (e.g. mp3)
  -v, --verbose         Print debug information
  -w WHISPER_PATH, --whisper-path WHISPER_PATH
                        Path to the Whisper executable (defaults to
                        ./whispercpp)
  -wa WHISPER_ARGS, --whisper-args WHISPER_ARGS
                        Give a string of extra parameters to give to the
                        whisper executable
 ```

## License
MIT &copy; [Hay Kranen](http://www.haykranen.nl)