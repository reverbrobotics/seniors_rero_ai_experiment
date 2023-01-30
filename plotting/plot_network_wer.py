import csv
import json
import math

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


sns.set_theme(style="whitegrid")
sns.set(font_scale=1.5)

labels = ["vosk", "vosk_max", "whisper_digitrep", "whisper_max", "whisper_tiny", "whisper_tiny_max"]
disp_labels = ["Vosk", "Vosk (Max 1.0)", "Whisper","Whisper (Max 1.0)", "Tiny Whisper","Tiny Whisper (Max 1.0)"]


fp = "/media/lukas/data/datasets/seniors_dataset/results/wer/{}_wer.csv"

data = []


for i, label in enumerate(labels):
    with open(fp.format(label), 'r') as rf:
        reader = csv.reader(rf)
        header = next(reader)

        for row in reader:
            data.append((label, disp_labels[i], float(row[4])))



df = pd.DataFrame(data)
df.columns = ["label", "Speech Recognition Networks", "WER (%)"]
print(df)

df["WER (%)"] *= 100

stats = df.groupby(['Speech Recognition Networks'])['WER (%)'].agg(['mean', 'count', 'std'])

ci95 = []

for i in stats.index:
    m, c, s = stats.loc[i]
    ci95.append(1.96*s/math.sqrt(c))


stats['ci95'] = ci95
print(stats)

plt.figure(figsize=(12,8))
ax = sns.barplot(x="Speech Recognition Networks", y="WER (%)", data=df, ci=95, capsize=0.25)
plt.title("Word Error Rate (WER) Results on Seniors Speech Dataset")

plt.show()