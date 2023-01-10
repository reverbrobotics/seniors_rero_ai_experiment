import csv
import json
import os
import sys
import wave

from vosk import Model, KaldiRecognizer, SetLogLevel
from tqdm import tqdm

participant_folder = "/media/lukas/data/datasets/seniors_dataset/participant_audio_wav"

model = Model(lang="en-us")



for src in sorted(os.listdir(participant_folder)):
    print("processing ", src)
    src_folder = os.path.join(participant_folder, src)
    dst_path = f"/media/lukas/data/datasets/seniors_dataset/participant_vosk_transcripts/{src}.csv"
    out_rows = []



    for file in tqdm(sorted(os.listdir(src_folder))):
        src_file = os.path.join(src_folder, file)


        with wave.open(src_file, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                print("Audio file must be WAV format mono PCM.")
                sys.exit(1)

            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)
            rec.SetPartialWords(True)

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                rec.AcceptWaveform(data)

        sr_res = json.loads(rec.FinalResult())

        out_rows.append([src, file, sr_res["text"]])

    with open(dst_path, 'w') as wf:
        writer = csv.writer(wf)

        writer.writerow(["pid", "file", "transcript"])

        writer.writerows(out_rows)

