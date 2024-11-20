from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy import signal
import pandas as pd

#convert data from PiEEG app 
with open('eeg_data_3.txt', 'r') as file:
    # Read the contents of the file
    input_data = file.read()
    
lists = input_data.split(']')
# Remove empty strings and strip whitespace
lists = [lst.strip() for lst in lists if lst.strip()]
# Write the formatted lists to a text file
with open('output3.txt', 'w') as f:
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

with open('output3.txt', 'r') as file:
    for line in file:
        line = line.strip()
        
        if line:  # Check if the line is not empty
            data = line[1:-1].split(', ')
            output = [int(x) for x in data]
            all_outputs.append(output)

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

    data_1ch_test.append(result[1])
    data_2ch_test.append(result[2])
    data_3ch_test.append(result[3])
    data_4ch_test.append(result[4])
    data_5ch_test.append(result[5])
    data_6ch_test.append(result[6])
    data_7ch_test.append(result[7])
    data_8ch_test.append(result[8])

# Adjust the layout and display the plot

dataset = pd.DataFrame({'Ch1': data_1ch_test, 'Ch2': data_2ch_test, 'Ch3': data_3ch_test, 'Ch4': data_4ch_test, 'Ch5': data_5ch_test, 'Ch6': data_6ch_test, 'Ch7': data_7ch_test, 'Ch8': data_8ch_test})
print (dataset)
dataset.to_csv('dataset1.csv', index=False)

