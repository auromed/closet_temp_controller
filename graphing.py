__author__ = 'alan'
import sqlite3
import time
import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



dbconnection = sqlite3.connect('temperatures.db')
dbcursor = dbconnection.cursor()
sql = "SELECT * FROM temps"

graphArray = []


for row in dbcursor.execute(sql):
    startingInfo = str(row).replace(')','').replace('(','').replace('u\'','').replace("'","")
    splitInfo = startingInfo.split(',')
    graphArrayAppend = splitInfo[0]+','+splitInfo[1]+','+splitInfo[2]+','+splitInfo[3]
    graphArray.append(graphArrayAppend)

dbconnection.commit()
dbconnection.close()

datestamp, value1, value2, value3 = np.loadtxt(graphArray,delimiter=',', unpack=True,
                              converters={0:mdates.strpdate2num('%Y-%m-%d %H:%M:%S')})

fig = plt.figure()
ect = fig.patch

plt.xlabel("Date - Time")
plt.ylabel("Temp C")
plt.plot_date(x=datestamp, y=value1/10, fmt='b-', label = 'Hot Aisle', linewidth=2)
plt.plot_date(x=datestamp, y=value2/10, fmt='r-', label = 'Server Intake', linewidth=2)
plt.plot_date(x=datestamp, y=value3/10, fmt='g-', label = 'Closet Intake', linewidth=2)
plt.legend(loc=2)
plt.show()
#plt.savefig('test.png')