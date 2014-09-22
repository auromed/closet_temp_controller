__author__ = 'alan'
import os
import glob
import time

#Commenting these out as they will be run at boot time
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')


# Add temp probe folder names from /esys/bus/w1/devices/
temp_probe1 = "28-001415ab5aff"
temp_probe2 = "28-0000054de6d5"
temp_probe3 = "28-001414c1dcff"

# test values comment out in production
# change base_dir to path for devices folders
base_dir = '/home/alan/Python/closet_temp_controller/sample/'
device_list = ['device1', 'device2', 'device3']


# production values comment out to test
#base_dir = '/sys/bus/w1/devices/'
#device_list = [temp_probe1, temp_probe2, temp_probe3 ]



def read_temp_raw(current_file):
    f = open(current_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#Read all of the temperature files specified in the device_list
def read_multiple_temp():
#Create Dictionary to store current temp readings
    values = {}
#Iterate through the temperature probes
    for item in device_list:
        device_file = base_dir + item + '/w1_slave'
        lines = read_temp_raw(device_file)
#Check for valid output from hardware probe when reading by checking CRC
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string=lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
        else:
            temp_c = 0.000
        values[item]=temp_c
    return values









while True:
    current_temps =  read_multiple_temp()
    print current_temps
    time.sleep(1)






# def read_temp():
#     lines = read_temp_raw()
#     while lines.strip()[-3:] != 'YES':
#         time.sleep(0.2)
#         lines = read_temp_raw()
#     equals_pos = lines[1].find('t=')
#     if equals_pos != -1:
#         temp_string = lines[1][equals_pos+2:]
#         temp_c = float(temp_string) / 1000.0
#         temp_f = temp_c * 9.0 / 5.0 + 32.0
#         return temp_c, temp_f