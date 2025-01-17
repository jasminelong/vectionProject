import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path

with open('/Users/jasmine/Documents/GitHub/vectionProject/public/data/A.json', 'r', encoding='utf-8') as file:
    simulated_data = json.load(file)

latent_times = {}
duration_times = {}
for condition, data in simulated_data.items():
    luminance_latent_times = {}
    luminance_duration_times = {}
    for xcondition, paths in data.items():
        participant_latent_times = {}
        participant_duration_times = {}
        for file_path in paths:
            participant_name = file_path.split('_')[-2]  # Extract participant identifier
            if participant_name not in participant_latent_times:
                participant_latent_times[participant_name] = []
                participant_duration_times[participant_name] = []

            # Load the data
            df = pd.read_csv(file_path)
            time = df['Time'] / 1000
            vection_response = df['Vection Response']

            mask = (time >= 0) & (time <= 60000)

                # 应用掩码筛选数据
            filtered_vection = vection_response[mask]
            filtered_time = time[mask]
            # Calculate latent time
            if (vection_response == 1).any():
                first_occurrence_index = filtered_vection[vection_response == 1].index[0]
                latent_time = filtered_time[first_occurrence_index]
            else:
                latent_time = np.nan

            # Calculate duration time
            time_diff = filtered_time.diff().fillna(0)
            duration_time = time_diff[vection_response == 1].sum() if latent_time is not np.nan else 0

            participant_latent_times[participant_name].append(latent_time)
            participant_duration_times[participant_name].append(duration_time)
        
        # Store average values for each condition
        luminance_latent_times[xcondition] = [
            np.nanmean(participant_latent_times[p]) for p in participant_latent_times
        ]
        luminance_duration_times[xcondition] = [
            np.mean(participant_duration_times[p]) for p in participant_duration_times
        ]

    latent_times[condition] = luminance_latent_times
    duration_times[condition] = luminance_duration_times

print(duration_times)

# Prepare data for plotting
fps_values = ['5 fps', '10 fps', '30 fps', '60 fps']

dots_right= [latent_times['Dots_right'][fps][0] for fps in fps_values]
dots_forward = [latent_times['Dots_forward'][fps][0] for fps in fps_values]
natural_right = [latent_times['Natural_right'][fps][0] for fps in fps_values]
natural_forward = [latent_times['Natural_forward'][fps][0] for fps in fps_values]
#dots_right= [duration_times['Dots_right'][fps][0] for fps in fps_values]
#dots_forward = [duration_times['Dots_forward'][fps][0] for fps in fps_values]
#natural_right = [duration_times['Natural_right'][fps][0] for fps in fps_values]
#natural_forward = [duration_times['Natural_forward'][fps][0] for fps in fps_values]

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(fps_values, dots_right, marker='o', label='Dots Right')
plt.plot(fps_values, dots_forward, marker='o', label='Dots Forward')
plt.plot(fps_values, natural_right, marker='o', label='Natural Right')
plt.plot(fps_values, natural_forward, marker='o', label='Natural Forward')

plt.title('Vection Onset Latency Time by FPS')
plt.ylabel('Vection Onset Latency Time (s)')
#plt.title('Vection Duration Time by FPS')
#plt.ylabel('Vection Duration Time (s)')
plt.xlabel('')

custom_labels = ['LM(5 FPS)', 'LM(10 FPS)', 'LM(30 FPS)', 'No Luminance Mixture\n(60 FPS)']  # Custom labels for x-axis
plt.xticks(ticks=range(len(fps_values)), labels=custom_labels)  # Set custom x-axis tick labels
plt.legend()
plt.grid(True)
plt.show()