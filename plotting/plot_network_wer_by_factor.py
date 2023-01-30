import csv
import json
import math

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.display.width = 0

sns.set_theme(style="whitegrid")
sns.set(font_scale=1.5)

factor = 'Age'

labels = ["vosk", "vosk_max", "whisper_digitrep", "whisper_max", "whisper_tiny", "whisper_tiny_max", "poem"]
disp_labels = ["ReRo AI", "Vosk (Max 1.0)", "Whisper","Whisper (Max 1.0)", "Tiny Whisper","Tiny Whisper (Max 1.0)", "Poem"]

data_ind = 6

fp = f"/media/lukas/data/datasets/seniors_dataset/results/wer/{labels[data_ind]}_wer.csv"
demographics_fp = "/media/lukas/data/datasets/seniors_dataset/results/demographic_data.csv"

wer_df = pd.read_csv(fp)
demo_df = pd.read_csv(demographics_fp)
combined_df = wer_df.join(demo_df.set_index('ParticipantID'), on='pid')
combined_df.rename(columns={"wer":"WER (%)"}, inplace=True)
print(combined_df.keys())

combined_df["WER (%)"] *= 100
#
# stats = df.groupby(['Speech Recognition Networks'])['WER (%)'].agg(['mean', 'count', 'std'])
#
# ci95 = []
#
# for i in stats.index:
#     m, c, s = stats.loc[i]
#     ci95.append(1.96*s/math.sqrt(c))
#
#
# stats['ci95'] = ci95
# print(stats)
#
plt.figure(figsize=(12,8))
ax = sns.barplot(x=factor, y="WER (%)", data=combined_df, ci=95, capsize=0.25)
plt.title(f"{disp_labels[data_ind]} Word Error Rate (WER) Results by {factor} on Seniors Speech Dataset")

plt.show()