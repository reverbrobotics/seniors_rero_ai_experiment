import os

import librosa
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from tqdm import tqdm

src_folder = "/media/lukas/data/datasets/seniors_dataset/participant_audio/"
dst_folder = "/media/lukas/data/datasets/seniors_dataset/participant_audio_raw/"
for participant_folder in tqdm(os.listdir(src_folder)):

    for file in tqdm(os.listdir(os.path.join(src_folder, participant_folder))):
        src_file = os.path.join(src_folder, participant_folder, file)
        data, samplerate = sf.read(src_file, channels=1, samplerate=16000, subtype='PCM_16', endian='LITTLE')

        inds = np.array(range(len(data)))/16000.0

        peakind = len(data)
        for i in range(len(data)):
            if data[i] > 0.1 or data[i] < -0.1:
                peakind = i
                break

        peakind -= 10

        data = data[:peakind]
        data = np.concatenate((data, np.zeros(shape=(64000), dtype=np.int16)))
        # plt.plot(data)
        # plt.axvline(x = peakind, color = 'b', label = 'peak')
        # plt.show()
        if not os.path.exists(os.path.join(dst_folder, participant_folder)):
            os.makedirs(os.path.join(dst_folder, participant_folder))

        dst_file = os.path.join(dst_folder, participant_folder, file)
        sf.write(dst_file, data, samplerate=16000, subtype='PCM_16', endian='LITTLE')