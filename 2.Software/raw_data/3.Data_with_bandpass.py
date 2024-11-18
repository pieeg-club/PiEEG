from matplotlib import pyplot as plt
#input_data = "[192, 0, 8, 0, 226, 222, 0, 132, 196, 254, 141, 17, 1, 11, 17, 255, 253, 34, 255, 251, 228, 255, 252, 81, 255, 252, 113][192, 0, 8, 0, 226, 185, 0, 132, 157, 254, 140, 228, 1, 10, 227, 255, 253, 36, 255, 251, 233, 255, 252, 83, 255, 252, 119][192, 0, 8, 0, 226, 23, 0, 130, 249, 254, 140, 23, 1, 11, 138, 255, 253, 36, 255, 251, 233, 255, 252, 83, 255, 252, 120][192, 0, 8, 0, 225, 61, 0, 131, 152, 254, 139, 80, 1, 12, 8, 255, 253, 34, 255, 251, 229, 255, 252, 82, 255, 252, 120]"
from scipy.ndimage import gaussian_filter1d
from scipy import signal


with open('data2.txt', 'r') as file:
    # Read the contents of the file
    input_data = file.read()
    
    # Print the contents
   # print(input_data)

# Split the input string into separate lists
lists = input_data.split(']')

# Remove empty strings and strip whitespace
lists = [lst.strip() for lst in lists if lst.strip()]

# Write the formatted lists to a text file
with open('output1.txt', 'w') as f:
    for lst in lists:
        f.write(f"{lst}]\n")



fps = 250
highcut = 8
lowcut = 12


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

with open('output1.txt', 'r') as file:
    for line in file:
        line = line.strip()
        
        if line:  # Check if the line is not empty
            data = line[1:-1].split(', ')
            output = [int(x) for x in data]
            all_outputs.append(output)

# Print all processed lines
#print (all_outputs[3251])
#print (all_outputs[3252])
#print (all_outputs[3253])



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

#print (data_8ch_test[7249])
#print (data_8ch_test[3252])
#print (data_8ch_test[3253])




data_filt_numpy_high_1 = butter_highpass_filter(data_2ch_test, highcut, fps)
data_for_graph_1 = butter_lowpass_filter(data_filt_numpy_high_1, lowcut, fps)


#plt.plot(data_1ch_test)
#plt.show()

plt.plot(data_for_graph_1)
plt.show()

#plt.plot(data_3ch_test)
#plt.show()
#plt.plot(data_4ch_test)
#plt.show()
