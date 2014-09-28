__author__ = 'alan'
import os
import glob
import time
import sqlite3
from datetime import datetime

# Commenting these out as they will be run at boot time
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#Database Creation and Connection Setup
dbconnection = sqlite3.connect('temperatures.db')
dbcursor = dbconnection.cursor()
dbcursor.execute("CREATE TABLE IF NOT EXISTS temps(date timestamp, device1 int, device2 int, device3 int)")
dbconnection.commit()
dbconnection.close()

# Add temp probe folder names from /esys/bus/w1/devices/
#temp_probe1 = "28-001415ab5aff"
#temp_probe2 = "28-0000054de6d5"
#temp_probe3 = "28-001414c1dcff"

#Values for testing
temp_probe1 = "device1"
temp_probe2 = "device2"
temp_probe3 = "device3"

device_list = [temp_probe1, temp_probe2, temp_probe3 ]

# test values comment out in production
# change base_dir to path for devices folders
base_dir = '/home/alan/Python/closet_temp_controller/sample/'



# production values comment out to test
#base_dir = '/sys/bus/w1/devices/'



#Read a file instead of the modules for testing - Comment out in Production
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
#Store only 3 digits of the temperature by dropping the last 2 digits of the value
            temp_store = int(lines[1][equals_pos + 2:equals_pos + 5])
        else:
            temp_c = 0000
        values[item] = temp_store
    return values

while True:
    current_temps = read_multiple_temp()
    print current_temps
    dbconnection = sqlite3.connect('temperatures.db')
    dbcursor = dbconnection.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dbcursor.execute(
     '''INSERT INTO temps(date,device1, device2, device3) VALUES(?,?,?,?)''', (now, current_temps['device1'],
                                                                        current_temps['device2'],
                                                                        current_temps['device3']))
    dbconnection.commit()
    dbconnection.close()
    time.sleep(60)



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