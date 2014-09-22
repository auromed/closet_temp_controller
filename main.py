__author__ = 'alan'
import os
import glob
import time

#Commenting these out as they will be run at boot time
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

temp_probe1 = "28-001415ab5aff"
temp_probe2 = "28-0000054de6d5"
temp_probe3 = "28-001414c1dcff"

base_dir = '/sys/bus/w1/devices/'
device_list = [temp_probe1, temp_probe2, temp_probe3 ]

for item in device_list:
   device_file = base_dir + item + '/w1_slave'
   print device_file





 def read_temp_raw():
     f = open(device_file, 'r')
     lines = f.readlines()
     f.close()
     return lines

 def read_temp():
     lines = read_temp_raw()
     while lines[0].strip()[-3:] != 'YES':
         time.sleep(0.2)
         lines = read_temp_raw()
     equals_pos = lines[1].find('t=')
     if equals_pos != -1:
         temp_string = lines[1][equals_pos+2:]
         temp_c = float(temp_string) / 1000.0
         temp_f = temp_c * 9.0 / 5.0 + 32.0
         return temp_c, temp_f

 while True:
 	print(read_temp())
 	time.sleep(1)


