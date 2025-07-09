import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 文件路径列表
file_paths = [
    ("D:/vectionProject/public/BrightnessLinearData/20250709_143549_Fps1_CameraSpeed1_ExperimentPattern_FunctionMix_ParticipantName_KK_TrialNumber_1.csv", "Trial 1"),
    ("D:/vectionProject/public/BrightnessLinearData/20250709_143949_Fps1_CameraSpeed1_ExperimentPattern_FunctionMix_ParticipantName_KK_TrialNumber_2.csv", "Trial 2"),
    ("D:/vectionProject/public/BrightnessLinearData/20250709_144327_Fps1_CameraSpeed1_ExperimentPattern_FunctionMix_ParticipantName_KK_TrialNumber_3.csv", "Trial 3")
]

# 定义基础函数
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

# 横轴
x_vals = np.linspace(0, 1, 500)

# 收集三次函数值
dyn_curves = []

# 绘制每次实验图
for path, label in file_paths:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    ratio = df["FunctionRatio"].dropna().iloc[-1]
    dyn_vals = dynamic_blend(x_vals, ratio)
    dyn_curves.append(dyn_vals)

"""     plt.figure()
    plt.plot(x_vals, cosine_blend(x_vals), linestyle="--", label="Cosine")
    plt.plot(x_vals, linear_blend(x_vals), linestyle="--", label="Linear")
    plt.plot(x_vals, acos_blend(x_vals), linestyle="--", label="Acos")
    plt.plot(x_vals, dyn_vals, linewidth=2, label=f"{label} (FunctionRatio={ratio:.3f})")
    plt.title(f"{label} - 动态混合函数")
    plt.xlabel("Normalized Time (x)")
    plt.ylabel("Blend Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show() """

# 绘制三次试验的平均曲线图
avg_curve = np.mean(dyn_curves, axis=0)
plt.figure()
plt.plot(x_vals, cosine_blend(x_vals), linestyle="--", label="Cosine")
plt.plot(x_vals, linear_blend(x_vals), linestyle="--", label="Linear")
plt.plot(x_vals, acos_blend(x_vals), linestyle="--", label="Acos")
plt.plot(x_vals, avg_curve, linewidth=2, label="Average Curve")
plt.title("Average dynamic mixing curve of three experiments")
plt.xlabel("Normalized Time (x)")
plt.ylabel("Blend Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
