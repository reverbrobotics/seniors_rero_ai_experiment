import csv
import os

import whisper
from tqdm import tqdm

participant_folder = "/media/lukas/data/datasets/seniors_dataset/participant_audio_wav"

for src in sorted(os.listdir(participant_folder)):
    print("processing ", src)
    src_folder = os.path.join(participant_folder, src)
    dst_path = f"/media/lukas/data/datasets/seniors_dataset/participant_whisper_tiny_transcripts/{src}.csv"
    out_rows = []

    model = whisper.load_model("tiny.en")

    for file in tqdm(sorted(os.listdir(src_folder))):
        src_file = os.path.join(src_folder, file)
        result = model.transcribe(src_file)

        out_rows.append([src, file, result["text"]])

    with open(dst_path, 'w') as wf:
        writer = csv.writer(wf)

        writer.writerow(["pid", "file", "transcript"])

        writer.writerows(out_rows)

