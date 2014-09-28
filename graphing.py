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
    print graphArray

dbconnection.commit()
dbconnection.close()

datestamp, value1, value2, value3 = np.loadtxt(graphArray,delimiter=',', unpack=True,
                              converters={0:mdates.strpdate2num('%Y-%m-%d %H:%M:%S')})
print datestamp
print mdates.num2date(datestamp)

fig = plt.figure()
ect = fig.patch
ax1 = fig.add_subplot(1,1,1, axisbg='white')
plt.plot_date(x=datestamp, y=value1/10, fmt='b-', label = 'value', linewidth=2)
plt.plot_date(x=datestamp, y=value2/10, fmt='r-', linewidth=2)
plt.plot_date(x=datestamp, y=value3/10, fmt='g-', linewidth=2)
plt.show()
#plt.savefig('test.png')