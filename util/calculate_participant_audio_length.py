import os
import librosa
from tqdm import tqdm

src_folder = "/media/lukas/data/datasets/seniors_dataset/participant_audio_wav/"

participant_counts = {}



for participant_folder in tqdm(os.listdir(src_folder)):
    participant_counts[participant_folder] = 0

    for file in os.listdir(os.path.join(src_folder, participant_folder)):
        fp = os.path.join(src_folder, participant_folder, file)

        y, sr = librosa.load(fp, sr=16000)

        participant_counts[participant_folder] += len(y)/16000

for pid in participant_counts.keys():
    print(pid, ": ", int(participant_counts[pid]//60), " minutes ", int(participant_counts[pid]%60), " seconds")

