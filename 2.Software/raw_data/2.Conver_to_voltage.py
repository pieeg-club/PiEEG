#from matplotlib import pyplot as plt

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

with open('C:/Users/irakhmat/Desktop/Python/output.txt', 'r') as file:
    for line in file:
        line = line.strip()
        
        if line:  # Check if the line is not empty
            data = line[1:-1].split(', ')
            output = [int(x) for x in data]
            all_outputs.append(output)

# Print all processed lines
print (all_outputs[3251])
print (all_outputs[3252])
print (all_outputs[3253])

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

print (data_8ch_test[7249])
print (data_8ch_test[3252])
print (data_8ch_test[3253])

#plt.plot(data_1ch_test)
#plt.show()
#plt.plot(data_4ch_test)
#plt.show()
#plt.plot(data_6ch_test)
#plt.show()
#plt.plot(data_7ch_test)
#plt.show()

