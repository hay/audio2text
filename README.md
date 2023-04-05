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
To convert the given `berliner.ogg` file in the test directory to a CSV file
```bash
./audio2text.py -i test/berliner.ogg -o test/berliner -of csv
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

```bash
usage: audio2text.py [-h] [-di] [-i INPUT] [-l LANGUAGE] [-m MODEL_PATH] [-o OUTPUT] [-of {txt,vtt,srt,csv,words}] [-su] [-v]
                     [-w WHISPER_PATH]

options:
  -h, --help            show this help message and exit
  -di, --diarize        Diarize audio (only works for natural stereo audio)
  -i INPUT, --input INPUT
                        File to parse
  -l LANGUAGE, --language LANGUAGE
  -m MODEL_PATH, --model-path MODEL_PATH
                        Path to model
  -o OUTPUT, --output OUTPUT
  -of {txt,vtt,srt,csv,words}, --output-format {txt,vtt,srt,csv,words}
  -su, --speed-up
  -v, --verbose
  -w WHISPER_PATH, --whisper-path WHISPER_PATH
 ```

## License
MIT &copy; [Hay Kranen](http://www.haykranen.nl)
