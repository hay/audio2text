from whispercpp import Whisper, api

# Not really sure if this should be how things should work
params = api.Params.from_enum(api.SAMPLING_GREEDY)
params = params\
    .with_language("nl")\
    .with_print_progress(True)\
    .with_print_realtime(True)\
    .with_print_timestamps(True)\
    .build()

model = Whisper.from_params("large", params)
text = model.transcribe_from_file("test/nrc-vandaag-small.wav")
print("hoi")
print(text)