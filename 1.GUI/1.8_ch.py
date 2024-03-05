import spidev
import time
from RPi import GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
from gpiozero import LED,Button
from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy import signal
import gpiod
button_pin = 26
chip = gpiod.Chip("gpiochip4")

button_line = chip.get_line(button_pin)
button_line.request(consumer = "Button", type = gpiod.LINE_REQ_DIR_IN)

from time import sleep
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=600000

#spi.max_speed_hz=25000
spi.lsbfirst=False
#spi.cshigh=False
#spi.cslow=True

spi.mode=0b01
spi.bits_per_word = 8

who_i_am=0x00
config1=0x01
config2=0X02
config3=0X03

reset=0x06
stop=0x0A
start=0x08
sdatac=0x11
rdatac=0x10
wakeup=0x02
rdata = 0x12

ch1set=0x05
ch2set=0x06
ch3set=0x07
ch4set=0x08
ch5set=0x09
ch6set=0x0A
ch7set=0x0B
ch8set=0x0C

data_test= 0x7FFFFF
data_check=0xFFFFFF

def read_byte(register):
 write=0x20
 register_write=write|register
 data = [register_write,0x00,register]
 read_reg=spi.xfer(data)
 print ("data", read_reg)
 
def send_command(command):
 send_data = [command]
 com_reg=spi.xfer(send_data)
 
def write_byte(register,data):
 write=0x40
 register_write=write|register
 data = [register_write,0x00,data]
 print (data)
 spi.xfer(data)

send_command (wakeup)
send_command (stop)
send_command (reset)
send_command (sdatac)

write_byte (config1, 0x96)
write_byte (config2, 0xD4)
write_byte (config3, 0xFF)
write_byte (0x04, 0x00)
write_byte (0x0D, 0x00)
write_byte (0x0E, 0x00)
write_byte (0x0F, 0x00)
write_byte (0x10, 0x00)
write_byte (0x11, 0x00)
write_byte (0x15, 0x20)
#
write_byte (0x17, 0x00)
write_byte (ch1set, 0x00)
write_byte (ch2set, 0x00)
write_byte (ch3set, 0x00)
write_byte (ch4set, 0x00)
write_byte (ch5set, 0x00)
write_byte (ch6set, 0x00)
write_byte (ch7set, 0x00)
write_byte (ch8set, 0x00)

send_command (rdatac)
send_command (start)
DRDY=1

result=[0]*27
data_1ch_test = []
data_2ch_test = []
data_3ch_test = []
data_4ch_test = []
data_5ch_test = []
data_6ch_test = []
data_7ch_test = []
data_8ch_test = []

figure, axis = plt.subplots(8, 1)
plt.subplots_adjust(hspace=1) 

axis_x=0
y_minus_graph=250
y_plus_graph=250
x_minux_graph=5000
x_plus_graph=250
sample_len = 250

axis = [0,1,2,3,4,5,6,7]
for ax in axis:
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title('Data after pass filter')

test_DRDY = 5 

#1.2 Band-pass filter
data_before = []
data_after =  []
just_one_time = 0
data_lenght_for_Filter = 2     # how much we read data for filter, all lenght  [_____] + [_____] + [_____]
read_data_lenght_one_time = 1   # for one time how much read  [_____]
sample_len = 250
sample_lens = 250
fps = 250
highcut = 1
lowcut = 10
data_before_1 = data_before_2 = data_before_3 = data_before_4 = data_before_5 = data_before_6 = data_before_7 = data_before_8 = [0]*250

print (data_lenght_for_Filter*read_data_lenght_one_time-read_data_lenght_one_time)

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

while 1:
    # print("before")
    button_state = button_line.get_value()
    # print("after")
    if button_state == 1:
       # print ("button_state 1")
        test_DRDY = 10
    if test_DRDY == 10 and button_state == 0:
        test_DRDY = 0 

        output=spi.readbytes(27)
        for a in range (3,25,3):
            voltage_1=(output[a]<<8)| output[a+1]
            voltage_1=(voltage_1<<8)| output[a+2]
            convert_voktage=voltage_1|data_test
            if convert_voktage==data_check:
                voltage_1_after_convert=(voltage_1-16777214)
            else:
               voltage_1_after_convert=voltage_1
            channel_num =  (a/3)

            result[int (channel_num)]=round(1000000*4.5*(voltage_1_after_convert/16777215),2)

        data_1ch_test.append(result[1])
        data_2ch_test.append(result[2])
        data_3ch_test.append(result[3])
        data_4ch_test.append(result[4])
        data_5ch_test.append(result[5])
        data_6ch_test.append(result[6])
        data_7ch_test.append(result[7])
        data_8ch_test.append(result[8])
        datasets = [data_1ch_test, data_2ch_test, data_3ch_test, data_4ch_test, data_5ch_test, data_6ch_test, data_7ch_test, data_8ch_test]
        if len(data_2ch_test)==sample_len:


            for i, data_after in enumerate(datasets):
                 dataset = data_before[i] + data_after
                 data_before[i] = dataset[250:]
                 data_for_graph = dataset
             
                 data_filt_numpy_high = butter_highpass_filter(data_for_graph, highcut, fps)
                 data_for_graph = butter_lowpass_filter(data_filt_numpy_high, lowcut, fps)
             
                 axis[i].plot(range(axis_x, axis_x + sample_lens, 1), data_for_graph[250:], color='#0a0b0c')
                 axis[i].axis([axis_x - x_minux_graph, axis_x + x_plus_graph, data_for_graph[50] - y_minus_graph, data_for_graph[150] + y_plus_graph])




            plt.pause(0.000001)
            
            axis_x=axis_x+sample_lens 
            data_1ch_test = []
            data_2ch_test = []
            data_3ch_test = []
            data_4ch_test = []
            data_5ch_test = []
            data_6ch_test = []
            data_7ch_test = []
            data_8ch_test = []
spi.close()
