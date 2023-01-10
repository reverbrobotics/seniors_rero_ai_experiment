import os
import csv

from wer.wer_utils import convert_text, wer

src_dir = "/media/lukas/data/datasets/seniors_dataset/participant_data"
dst_file = "/media/lukas/data/datasets/seniors_dataset/results/wer/poem_wer.csv"

out_rows = [["pid", "poem_line", "recognized_text", "reference_text", "wer"]]

for folder in os.listdir(src_dir):
    src_file = os.path.join(src_dir, folder, "poem_data.csv")

    if not os.path.exists(src_file):
        continue

    with open(src_file, 'r') as rf:
        reader = csv.reader(rf)
        next(reader)

        for row in reader:
            src_transcript = convert_text(row[4])
            ref_transcript = convert_text(row[3])

            wer_res = wer(src_transcript, ref_transcript)

            out_rows.append([folder, row[1], src_transcript, ref_transcript, wer_res])

with open(dst_file, 'w') as wf:
    writer = csv.writer(wf)

    writer.writerows(out_rows)
