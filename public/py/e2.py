import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取 CSV 文件（修改为你的文件路径）
file_path = "D:/vectionProject/public/Experiment2Data/20250516_135917_fps1_ParticipantName__TrialNumber_1_VelocityOption0.csv"

df = pd.read_csv(file_path)

# 2. 去除列名空格
df.columns = df.columns.str.strip()

# 3. 提取 ResponsePattern=0~4 的最后 StepNumber 对应 V0, A1~A4
param_names = ["V0", "A1", "A2", "A3", "A4"]
params = {}

for pattern in range(5):
    match = df[df["ResponsePattern"] == pattern]
    if not match.empty:
        step = match.iloc[-1]["StepNumber"]
        params[param_names[pattern]] = step
    else:
        params[param_names[pattern]] = 0  # 若未出现则设为0

# 4. 赋值参数
V0 = params["V0"]
A1 = params["A1"]
A2 = params["A2"]
A3 = params["A3"]
A4 = params["A4"]

print(f"V0 = {V0}, A1 = {A1}, A2 = {A2}, A3 = {A3}, A4 = {A4}")

# 5. 设置时间轴和频率
omega = 2 * np.pi  # 1Hz
t = np.linspace(0, 10, 2000)  # 0到10秒，2000个点

# 6. 计算 y(t)
y = V0 + A1 * np.sin(omega * t) + A2 * np.cos(omega * t) + \
    A3 * np.sin(2 * omega * t) + A4 * np.cos(2 * omega * t)

# 7. 绘图
plt.figure(figsize=(12, 5))
plt.plot(t, y, label="y(t)")
plt.title("y(t) = V0 + A1·sin(ωt) + A2·cos(ωt) + A3·sin(2ωt) + A4·cos(2ωt)")
plt.xlabel("Time (s)")
plt.ylabel("y(t)")
plt.ylim(0, 2)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
