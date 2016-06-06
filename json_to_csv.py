import os, sys
import json
import csv
import datetime

fileName = sys.argv[1]

rows = []
legend = []
i = 1
increment = 4 #time increment is approx evey 4 seconds for a 10 minute test (150 data points per datadog request)

with open(fileName+'.json') as data_file:    
    data = json.load(data_file)

for row in data["series"][0]["pointlist"]:
	rows.append(row[1])

time_stamp = data["series"][0]["start"]
t = datetime.datetime.fromtimestamp(int(time_stamp/1000)).strftime('date_%m_%d_%H_%M')

header = ['time_stamp', t]
with open(fileName+'.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for row in rows:
    	writer.writerow([i*increment,row]) 
    	i+=1
