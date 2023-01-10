import os
import csv

from tqdm import tqdm

from wer_utils import convert_text, wer

src_dir = "/media/lukas/data/datasets/seniors_dataset/participant_vosk_transcripts"
ref_dir = "/media/lukas/data/datasets/seniors_dataset/participant_final_transcripts"
dst_file = "/media/lukas/data/datasets/seniors_dataset/results/wer/vosk_max_wer.csv"

out_rows = [["pid", "file", "transcript", "ref_transcript", "wer"]]


for file in tqdm(sorted(os.listdir(src_dir))):
    src_file = os.path.join(src_dir, file)
    ref_file = os.path.join(ref_dir, file)

    assert(os.path.exists(src_file))
    assert(os.path.exists(ref_file))

    src_rows = []
    ref_rows = []

    with open(src_file, 'r') as rf:
        reader = csv.reader(rf)
        next(reader)

        for row in reader:
            src_rows.append(row)

    with open(ref_file, 'r') as rf:
        reader = csv.reader(rf)
        next(reader)

        for row in reader:
            ref_rows.append(row)

    assert(len(src_rows) == len(ref_rows))

    for i in range(len(src_rows)):
        src_transcript = convert_text(src_rows[i][2])
        ref_transcript = convert_text(ref_rows[i][2])

        if len(ref_transcript) == 0:
            continue

        wer_res = wer(src_transcript, ref_transcript)

        if wer_res > 1:
            wer_res = 1

        out_rows.append([src_rows[i][0], src_rows[i][1], src_transcript, ref_transcript, wer_res])

with open(dst_file, 'w') as wf:
    writer = csv.writer(wf)

    writer.writerows(out_rows)
