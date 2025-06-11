import cv2
import numpy as np
import os
import csv

# 视频路径
video_path = 'D:/444/Gamma.mp4'
cap = cv2.VideoCapture(video_path)

# ROI 区域位置
x, y, w, h = 420, 446, 40, 40  # 感兴趣区域

# 视频信息
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 输出路径准备
output_dir = 'D:/444'
os.makedirs(output_dir, exist_ok=True)

# 使用时间戳自动命名输出文件
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_path = os.path.join(output_dir, f'video_with_rgb_waveform_{timestamp}.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# 波形图高度
plot_height = 150
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height + plot_height))

# 保存 RGB 历史值
r_values, g_values, b_values = [], [], []
max_history = width  # 匹配画面宽度，显示完整波形

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # 提取 ROI 区域
    roi = frame[y:y+h, x:x+w]
    b_avg = int(np.mean(roi[:, :, 0]))
    g_avg = int(np.mean(roi[:, :, 1]))
    r_avg = int(np.mean(roi[:, :, 2]))

    print(f"Frame {frame_count} - R: {r_avg}, G: {g_avg}, B: {b_avg}")

    # 保存 RGB
    r_values.append(r_avg)
    g_values.append(g_avg)
    b_values.append(b_avg)

    if len(r_values) > max_history:
        r_values.pop(0)
        g_values.pop(0)
        b_values.pop(0)

    # 在视频帧上画红框
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    text = f'R:{r_avg} G:{g_avg} B:{b_avg}'
    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # 创建 RGB 波形图图像
    plot = np.ones((plot_height, width, 3), dtype=np.uint8) * 255

    # 归一化 RGB 值到 0~plot_height
    def normalize(vals):
        return [plot_height - int(v / 255 * plot_height) for v in vals]

    rr = normalize(r_values)
    gg = normalize(g_values)
    bb = normalize(b_values)

    print(f"rr[-5:]: {rr[-5:]}, gg[-5:]: {gg[-5:]}, bb[-5:]: {bb[-5:]}")

    # 画网格线 + 数值刻度
    for val in [0, 64, 128, 192, 255]:
        y_val = plot_height - int(val / 255 * plot_height)
        cv2.line(plot, (0, y_val), (width, y_val), (220, 220, 220), 1)
        cv2.putText(plot, str(val), (5, y_val - 5), cv2.FONT_HERSHEY_PLAIN, 1, (100, 100, 100), 1)

    # 画 RGB 折线
    for i in range(1, len(rr)):
        x1, x2 = i-1, i
        if x2 >= width: break  # 画面宽度限制
        if abs(rr[i] - rr[i-1]) > 0:
            cv2.line(plot, (x1, rr[i-1]), (x2, rr[i]), (0, 0, 255), 1)
        if abs(gg[i] - gg[i-1]) > 0:
            cv2.line(plot, (x1, gg[i-1]), (x2, gg[i]), (0, 255, 0), 1)
        if abs(bb[i] - bb[i-1]) > 0:
            cv2.line(plot, (x1, bb[i-1]), (x2, bb[i]), (255, 0, 0), 1)

    # 图例
    cv2.putText(plot, 'R', (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(plot, 'G', (40, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(plot, 'B', (70, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # 拼接原始帧 + 波形图
    combined = np.vstack((frame, plot))

    # 写入新视频
    out.write(combined)

    # （可选）显示
    cv2.imshow('Live RGB Waveform', combined)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
