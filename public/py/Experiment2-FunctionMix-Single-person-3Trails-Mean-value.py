import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re
from collections import defaultdict

# ========== 设置路径和读取文件 ==========
root_dir = "D:/vectionProject/public/BrightnessFunctionMixAndPhaseData"  # ChatGPT环境路径
pattern = re.compile(r"ExperimentPattern_Phase_ParticipantName_(\w+)_TrialNumber_.*?_BrightnessBlendMode_(\w+)\.csv")

participant_files = defaultdict(lambda: defaultdict(list))
for fname in os.listdir(root_dir):
    if fname.endswith(".csv") and "Test" not in fname:
        match = pattern.search(fname)
        if match:
            participant, mode = match.groups()
            full_path = os.path.join(root_dir, fname)
            participant_files[participant][mode].append(full_path)

# ========== 设置参与者和模式 ==========
selected_participant = "O"
selected_mode = "FunctionMix"
selected_files = participant_files[selected_participant][selected_mode][:9]
file_paths = [(path, f"Trial {i+1}") for i, path in enumerate(selected_files)]

# ========== 定义函数 ==========
def cosine_blend(x):
    return 0.5 * (1 - np.cos(np.pi * x))

def linear_blend(x):
    return x

def acos_blend(x):
    return np.arccos(-2 * x + 1) / np.pi

def dynamic_blend(x, knob_value):
    if knob_value <= 0.1 or knob_value >= 1.9:
        return cosine_blend(x)
    k = knob_value - 0.1
    if k <= 0.6:
        t = k / 0.6
        return (1 - t) * cosine_blend(x) + t * linear_blend(x)
    elif k <= 1.2:
        t = (k - 0.6) / 0.6
        return (1 - t) * linear_blend(x) + t * acos_blend(x)
    else:
        t = (k - 1.2) / 0.6
        return (1 - t) * acos_blend(x) + t * cosine_blend(x)

# ========== 定义区间 ==========
intervals = [(0, 0.1), (0.1, 0.7), (0.7, 1.3), (1.3, 1.9), (1.9, 2.0)]
interval_labels = ["区间0", "区间1", "区间2", "区间3", "区间4"]
values_per_trial = {label: [] for label in interval_labels}

# ========== 读取实际 ratio 并归类 ==========
for path, label in file_paths:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    ratio = df["FunctionRatio"].dropna().iloc[-1]
    for i, (start, end) in enumerate(intervals):
        if start <= ratio < end:
            val = dynamic_blend(0.5, ratio)
            values_per_trial[interval_labels[i]].append(val)
            break

# ========== 画图 ==========
plt.figure(figsize=(12, 7))
data = [values_per_trial[label] for label in interval_labels]
plt.boxplot(data, labels=interval_labels, showmeans=True)

for i, vals in enumerate(data):
    plt.scatter([i+1]*len(vals), vals, color='red', zorder=3, label='实验值' if i==0 else "")

plt.ylabel("Blend Value")
plt.title("9次实验在五个区间的分布")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
