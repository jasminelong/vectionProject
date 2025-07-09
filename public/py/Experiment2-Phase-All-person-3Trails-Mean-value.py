import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import defaultdict
from statistics import mean

# 设置根目录
root_dir = "D:/vectionProject/public/BrightnessData"

# 用正则匹配文件名中的模式
pattern = re.compile(r"ExperimentPattern_Phase_ParticipantName_(\w+)_.*?_BrightnessBlendMode_(\w+)\.csv")

# 按实验者和模式收集文件路径（排除Test文件）
participant_files = defaultdict(lambda: defaultdict(list))
for fname in os.listdir(root_dir):
    if fname.endswith(".csv") and "Test" not in fname:
        match = pattern.search(fname)
        if match:
            participant, mode = match.groups()
            full_path = os.path.join(root_dir, fname)
            participant_files[participant][mode].append(full_path)

# 计算 v(t)
def v_curve(par, t):
    V0, A1, φ1, A2, φ2 = par
    ω = 2 * np.pi
    return V0 + A1 * np.sin(ω * t + φ1 + np.pi) + A2 * np.sin(2 * ω * t + φ2 + np.pi)

# 遍历每位实验者绘图
for participant, mode_files in participant_files.items():
    fig, axs = plt.subplots(2, 3, figsize=(15, 8))
    plt.suptitle(f"Participant {participant}: Brightness & v(t) Average", fontsize=16)
    t = np.linspace(0, 10, 2000)

    for i, mode in enumerate(["CosineOnly", "LinearOnly", "AcosOnly"]):
        files = mode_files.get(mode, [])
        params_list = []
        luminance_data = []

        for path in files:
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip()

            v0_series = df[df["StepNumber"] == 0]["Velocity"]
            V0 = v0_series.iloc[-1] if not v0_series.empty else 0
            A1 = df[df["StepNumber"] == 1]["Amplitude"].iloc[-1] if not df[df["StepNumber"] == 1].empty else 0
            φ1 = df[df["StepNumber"] == 2]["Amplitude"].iloc[-1] if not df[df["StepNumber"] == 2].empty else 0
            A2 = df[df["StepNumber"] == 3]["Amplitude"].iloc[-1] if not df[df["StepNumber"] == 3].empty else 0
            φ2 = df[df["StepNumber"] == 4]["Amplitude"].iloc[-1] if not df[df["StepNumber"] == 4].empty else 0

            params_list.append([V0, A1, φ1, A2, φ2])

            time = df["Time"] / 1000
            mask = (time <= 10) & (df["BackFrameNum"] % 2 != 0)
            df.loc[mask, ["BackFrameNum", "FrondFrameNum"]] = df.loc[mask, ["FrondFrameNum", "BackFrameNum"]].to_numpy()
            df.loc[mask, ["BackFrameLuminance", "FrondFrameLuminance"]] = df.loc[mask, ["FrondFrameLuminance", "BackFrameLuminance"]].to_numpy()
            luminance_data.append((time, df["FrondFrameLuminance"], df["BackFrameLuminance"]))

        ax1 = axs[0, i]
        for time, front, back in luminance_data:
            ax1.plot(time, front, label="Front", alpha=0.7)
            ax1.plot(time, back, label="Back", alpha=0.7)
        ax1.set_title(f"Luminance - {mode}")
        ax1.set_xlim(0, 10)
        ax1.set_ylabel("Luminance")
        ax1.grid(True)

        ax2 = axs[1, i]
        if params_list:
            avg_params = np.mean(params_list, axis=0)
            v_vals = v_curve(avg_params, t)
            ax2.plot(t, v_vals, label="v(t)", color="tab:blue")
            param_text = "\n".join([f"{n}={v:.2f}" for n, v in zip(["V0", "A1", "φ1", "A2", "φ2"], avg_params)])
            ax2.text(0.02, 0.95, param_text, transform=ax2.transAxes, fontsize=10,
                     verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))
            ax2.set_title(f"v(t) - {mode}")
            ax2.set_xlim(0, 5)
            ax2.set_ylim(-2, 4)
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Velocity")
            ax2.grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
