from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy import signal
import pandas as pd


#Band pass filter settings 
fps = 250
highcut = 8
lowcut = 12

#convert data from PiEEG app 
with open('eeg_data_2.txt', 'r') as file:
    # Read the contents of the file
    input_data = file.read()
    
lists = input_data.split(']')
# Remove empty strings and strip whitespace
lists = [lst.strip() for lst in lists if lst.strip()]
# Write the formatted lists to a text file
with open('output2.txt', 'w') as f:
    for lst in lists:
        f.write(f"{lst}]\n")


data_test= 0x7FFFFF
data_check=0xFFFFFF
result=[0]*27
data_1ch_test = []
data_2ch_test = []
data_3ch_test = []
data_4ch_test = []
data_5ch_test = []
data_6ch_test = []
data_7ch_test = []
data_8ch_test = []


all_outputs = []

with open('output2.txt', 'r') as file:
    for line in file:
        line = line.strip()
        
        if line:  # Check if the line is not empty
            data = line[1:-1].split(', ')
            output = [int(x) for x in data]
            all_outputs.append(output)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y
def butter_highpass(cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

for i, output in enumerate(all_outputs, 1): 
    for a in range (3,25,3):
        voltage_1=(output[a]<<8)| output[a+1]
        voltage_1=(voltage_1<<8)| output[a+2]
        convert_voktage=voltage_1|data_test
        if convert_voktage==data_check:
            voltage_1_after_convert=(voltage_1-16777214)
        else:
           voltage_1_after_convert=voltage_1
        channel_num =  (a/3)

        result[int(channel_num)]=round(1000000*4.5*(voltage_1_after_convert/16777215),2)
        #print ("result", result[int(channel_num)])

    data_1ch_test.append(result[1])
    data_2ch_test.append(result[2])
    data_3ch_test.append(result[3])
    data_4ch_test.append(result[4])
    data_5ch_test.append(result[5])
    data_6ch_test.append(result[6])
    data_7ch_test.append(result[7])
    data_8ch_test.append(result[8])

data_filt_numpy_high_1 = butter_highpass_filter(data_1ch_test, highcut, fps)
data_for_graph_1 = butter_lowpass_filter(data_filt_numpy_high_1, lowcut, fps)

data_filt_numpy_high_2 = butter_highpass_filter(data_2ch_test, highcut, fps)
data_for_graph_2 = butter_lowpass_filter(data_filt_numpy_high_2, lowcut, fps)

data_filt_numpy_high_3 = butter_highpass_filter(data_3ch_test, highcut, fps)
data_for_graph_3 = butter_lowpass_filter(data_filt_numpy_high_3, lowcut, fps)

data_filt_numpy_high_4 = butter_highpass_filter(data_4ch_test, highcut, fps)
data_for_graph_4 = butter_lowpass_filter(data_filt_numpy_high_4, lowcut, fps)

data_filt_numpy_high_5 = butter_highpass_filter(data_5ch_test, highcut, fps)
data_for_graph_5 = butter_lowpass_filter(data_filt_numpy_high_5, lowcut, fps)

data_filt_numpy_high_6 = butter_highpass_filter(data_6ch_test, highcut, fps)
data_for_graph_6 = butter_lowpass_filter(data_filt_numpy_high_6, lowcut, fps)

data_filt_numpy_high_7 = butter_highpass_filter(data_7ch_test, highcut, fps)
data_for_graph_7 = butter_lowpass_filter(data_filt_numpy_high_7, lowcut, fps)

data_filt_numpy_high_8 = butter_highpass_filter(data_8ch_test, highcut, fps)
data_for_graph_8 = butter_lowpass_filter(data_filt_numpy_high_8, lowcut, fps)

fig, axs = plt.subplots(4, 2, figsize=(15, 20))
fig.suptitle('Filtered Data for 8 Channels', fontsize=16)

# Flatten the axs array for easier indexing
axs = axs.flatten()
# List of data to plot
data_list = [data_for_graph_1, data_for_graph_2, data_for_graph_3, data_for_graph_4,
             data_for_graph_5, data_for_graph_6, data_for_graph_7, data_for_graph_8]

print (data_for_graph_1)
# Plot each dataset in its own subplot
for i, data in enumerate(data_list):
    axs[i].plot(data)
    axs[i].set_title(f'Channel {i+1}')
    axs[i].set_xlabel('Sample')
    axs[i].set_ylabel('Amplitude')

# Adjust the layout and display the plot
plt.tight_layout()
plt.show()

dataset = pd.DataFrame({'Ch1': data_for_graph_1, 'Ch2': data_for_graph_2, 'Ch3': data_for_graph_3, 'Ch4': data_for_graph_4, 'Ch5': data_for_graph_5, 'Ch6': data_for_graph_6, 'Ch7': data_for_graph_7, 'Ch8': data_for_graph_8})
print (dataset)


dataset.to_csv('dataset.csv', index=False)

