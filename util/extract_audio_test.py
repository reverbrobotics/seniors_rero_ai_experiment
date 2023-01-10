import os

import librosa
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from tqdm import tqdm

src_file = "/media/lukas/data/datasets/seniors_dataset/participant_audio/participant6/recording_1668489275557.raw"
data, samplerate = sf.read(src_file, channels=1, samplerate=16000, subtype='PCM_16', endian='LITTLE')

inds = np.array(range(len(data)))/16000.0

peakind = len(data)
for i in range(len(data)):
    if data[i] > 0.1 or data[i] < -0.1:
        peakind = i
        break

peakind -= 10

plt.plot(data)
plt.axvline(x = peakind, color = 'b', label = 'peak')
plt.show()
