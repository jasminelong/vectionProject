import matplotlib.pyplot as plt
import numpy as np

# 数据
fps = [5, 10, 30, 60]
distance = [0.8, 0.4,0.133, 0.067]
#fps = [5, 10, 20, 30, 60]
#distance = [0.8, 0.4, 0.2, 0.133, 0.067]
# 将帧率转换为字符串，以便作为类别处理
fps_labels = [str(f) for f in fps]

# 设置图形尺寸
plt.figure(figsize=(10, 6))

# 创建柱状图，使用类别标签确保等距离
bars = plt.bar(fps_labels, distance, color='skyblue', edgecolor='black')

# 添加标题和标签
plt.title('Distance Between Two Frames at Various Frame Rates', fontsize=16)
plt.xlabel('Frame Rate (fps)', fontsize=14)
plt.ylabel('Distance (meters)', fontsize=14)

# 设置y轴刻度
plt.yticks(np.arange(0, 1.0, 0.1), fontsize=12)

# 添加网格线（可选）
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.02, f'{height:.3f}', 
             ha='center', va='bottom', fontsize=12)

# 优化布局
plt.tight_layout()

# 显示图表
plt.show()
