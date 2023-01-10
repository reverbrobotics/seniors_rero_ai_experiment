import os
import csv

folderA = "/media/lukas/data/datasets/seniors_dataset/participant_whisper_transcripts"
folderB = "/media/lukas/data/datasets/seniors_dataset/participant_transcripts_final"

for file in os.listdir(folderA):

    countA = 0
    countB = 0

    with open(os.path.join(folderA, file), 'r') as rf:
        reader = csv.reader(rf)

        for row in reader:
            countA += 1

    with open(os.path.join(folderB, file), 'r') as rf:
        reader = csv.reader(rf)

        for row in reader:
            countB += 1


    print(file, countA, countB)
