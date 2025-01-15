import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

simulated_data ={
"Dots_forward" :{
    '5 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_050301_Natural_right_luminanceMixture_cameraSpeed4_fps5_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_050122_Natural_right_luminanceMixture_cameraSpeed4_fps5_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_045745_Natural_right_luminanceMixture_cameraSpeed4_fps5_A_trialNumber3.csv',
        
    ],
    '10 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_052116_Natural_right_luminanceMixture_cameraSpeed4_fps10_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250108_190200_Natural_right_luminanceMixture_cameraSpeed4_fps10_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052301_Natural_right_luminanceMixture_cameraSpeed4_fps10_A_trialNumber3.csv',
    ],
    '20 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_124644_Natural_right_luminanceMixture_cameraSpeed4_fps20_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_124815_Natural_right_luminanceMixture_cameraSpeed4_fps20_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_124946_Natural_right_luminanceMixture_cameraSpeed4_fps20_A_trialNumber3.csv',
    ],
    '30 fps':[
        'D:/vectionProject/public/ExperimentData/20250108_192853_Natural_right_luminanceMixture_cameraSpeed4_fps30_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052608_Natural_right_luminanceMixture_cameraSpeed4_fps30_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052438_Natural_right_luminanceMixture_cameraSpeed4_fps30_A_trialNumber3.csv',
    ],   
    '60 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_052750_Natural_right_continuous_cameraSpeed4_fps60_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052920_Natural_right_continuous_cameraSpeed4_fps60_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_053053_Natural_right_continuous_cameraSpeed4_fps60_A_trialNumber3.csv',
    ], 
},
"Dots_right" :{
    '5 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_050301_Natural_right_luminanceMixture_cameraSpeed4_fps5_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_050122_Natural_right_luminanceMixture_cameraSpeed4_fps5_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_045745_Natural_right_luminanceMixture_cameraSpeed4_fps5_A_trialNumber3.csv',
    ],
    '10 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_052116_Natural_right_luminanceMixture_cameraSpeed4_fps10_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250108_190200_Natural_right_luminanceMixture_cameraSpeed4_fps10_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052301_Natural_right_luminanceMixture_cameraSpeed4_fps10_A_trialNumber3.csv',
    ],
    '20 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_124644_Natural_right_luminanceMixture_cameraSpeed4_fps20_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_124815_Natural_right_luminanceMixture_cameraSpeed4_fps20_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_124946_Natural_right_luminanceMixture_cameraSpeed4_fps20_A_trialNumber3.csv',
    ],
    '30 fps':[
        'D:/vectionProject/public/ExperimentData/20250108_192853_Natural_right_luminanceMixture_cameraSpeed4_fps30_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052608_Natural_right_luminanceMixture_cameraSpeed4_fps30_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052438_Natural_right_luminanceMixture_cameraSpeed4_fps30_A_trialNumber3.csv',
    ],   
    '60 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_052750_Natural_right_continuous_cameraSpeed4_fps60_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052920_Natural_right_continuous_cameraSpeed4_fps60_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_053053_Natural_right_continuous_cameraSpeed4_fps60_A_trialNumber3.csv',
    ], 
}, 
"Natural_right" :{
    '5 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_050301_Natural_right_luminanceMixture_cameraSpeed4_fps5_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_050122_Natural_right_luminanceMixture_cameraSpeed4_fps5_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_045745_Natural_right_luminanceMixture_cameraSpeed4_fps5_A_trialNumber3.csv',
    ],
    '10 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_052116_Natural_right_luminanceMixture_cameraSpeed4_fps10_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250108_190200_Natural_right_luminanceMixture_cameraSpeed4_fps10_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052301_Natural_right_luminanceMixture_cameraSpeed4_fps10_A_trialNumber3.csv',
    ],
    '20 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_124644_Natural_right_luminanceMixture_cameraSpeed4_fps20_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_124815_Natural_right_luminanceMixture_cameraSpeed4_fps20_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_124946_Natural_right_luminanceMixture_cameraSpeed4_fps20_A_trialNumber3.csv',
    ],
    '30 fps':[
        'D:/vectionProject/public/ExperimentData/20250108_192853_Natural_right_luminanceMixture_cameraSpeed4_fps30_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052608_Natural_right_luminanceMixture_cameraSpeed4_fps30_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052438_Natural_right_luminanceMixture_cameraSpeed4_fps30_A_trialNumber3.csv',
    ],   
    '60 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_052750_Natural_right_continuous_cameraSpeed4_fps60_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_052920_Natural_right_continuous_cameraSpeed4_fps60_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_053053_Natural_right_continuous_cameraSpeed4_fps60_A_trialNumber3.csv',
    ], 
},
"Natural_forward" :{
    '5 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_045137_Natural_forward_luminanceMixture_cameraSpeed4_fps5_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_045327_Natural_forward_luminanceMixture_cameraSpeed4_fps5_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_045509_Natural_forward_luminanceMixture_cameraSpeed4_fps5_A_trialNumber3.csv',
    ],
    '10 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_054323_Natural_forward_luminanceMixture_cameraSpeed4_fps10_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_054323_Natural_forward_luminanceMixture_cameraSpeed4_fps10_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_054454_Natural_forward_luminanceMixture_cameraSpeed4_fps10_A_trialNumber2.csv',
    ],
    '20 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_124158_Natural_forward_luminanceMixture_cameraSpeed4_fps20_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_124329_Natural_forward_luminanceMixture_cameraSpeed4_fps20_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_124500_Natural_forward_luminanceMixture_cameraSpeed4_fps20_A_trialNumber3.csv',
    ],
    '30 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_053832_Natural_forward_luminanceMixture_cameraSpeed4_fps30_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250109_054001_Natural_forward_luminanceMixture_cameraSpeed4_fps30_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_054139_Natural_forward_luminanceMixture_cameraSpeed4_fps30_A_trialNumber3.csv',
    ],   
    '60 fps':[
        'D:/vectionProject/public/ExperimentData/20250109_053601_Natural_forward_continuous_cameraSpeed4_fps60_A_trialNumber1.csv',
        'D:/vectionProject/public/ExperimentData/20250108_202957_Natural_forward_continuous_cameraSpeed4_fps20_A_trialNumber2.csv',
        'D:/vectionProject/public/ExperimentData/20250109_053429_Natural_forward_continuous_cameraSpeed4_fps60_A_trialNumber3.csv',
    ], 
}
}

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

            # Calculate latent time
            if (vection_response == 1).any():
                first_occurrence_index = vection_response[vection_response == 1].index[0]
                latent_time = time[first_occurrence_index]
            else:
                latent_time = np.nan

            # Calculate duration time
            time_diff = time.diff().fillna(0)
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
fps_values = ['5 fps', '10 fps', '20 fps', '30 fps', '60 fps']

#dots_right= [duration_times['Dots_right'][fps][0] for fps in fps_values]
#dots_forward = [duration_times['Dots_forward'][fps][0] for fps in fps_values]
natural_right = [duration_times['Natural_right'][fps][0] for fps in fps_values]
natural_forward = [duration_times['Natural_forward'][fps][0] for fps in fps_values]

# Plot the data
plt.figure(figsize=(10, 6))
#plt.plot(fps_values, dots_right, marker='o', label='Dots Right')
#plt.plot(fps_values, dots_forward, marker='o', label='Dots Forward')
plt.plot(fps_values, natural_right, marker='o', label='Natural Right')
plt.plot(fps_values, natural_forward, marker='o', label='Natural Forward')

plt.title('Vection Response Time by FPS')
plt.xlabel('')
plt.ylabel('Total Vection Time (s)')
custom_labels = ['LM(5 FPS)', 'LM(10 FPS)', 'LM(20 FPS)', 'LM(30 FPS)', 'No Luminance Mixture\n(60 FPS)']  # Custom labels for x-axis
plt.xticks(ticks=range(len(fps_values)), labels=custom_labels)  # Set custom x-axis tick labels
plt.legend()
plt.grid(True)
plt.show()