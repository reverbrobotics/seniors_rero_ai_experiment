import os
import csv
from shutil import copyfile

src_dir = "/media/lukas/data/datasets/seniors_dataset/participant_audio_wav/participant"

for i in range(3, 6):
    dst_dir = f"/media/lukas/data/datasets/seniors_dataset/participant_audio_wav/participant{i}"
    csv_path = f"/media/lukas/data/datasets/seniors_dataset/participant_transcripts_final/participant{i}.csv"

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    with open(csv_path, 'r') as rf:
        reader = csv.reader(rf)
        next(reader)

        for row in reader:
            copyfile(os.path.join(src_dir, row[1]), os.path.join(dst_dir, row[1]))