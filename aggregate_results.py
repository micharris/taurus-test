import urllib2
import json
import csv
import sys

apiKey = sys.argv[1]
project = sys.argv[2]
metric = sys.argv[3]
csvRows = []

#metric options: responseTime, error

#get a list 
req = urllib2.Request('https://artifactory.gannettdigital.com/artifactory/api/storage/load-test-results/'+project+'/'+metric+'?list')
req.add_header('x-api-key', apiKey)
resp = urllib2.urlopen(req)
content = resp.read()

d = json.loads(content)
file_list = (d['files'])
#we want the newest files
file_list.sort(reverse=True)

i = 0
for value in file_list: # returns the dictionary as a list of value pairs -- a tuple.
	req = urllib2.Request('https://artifactory.gannettdigital.com/artifactory/load-test-results/'+project+'/'+metric+value['uri'])
	req.add_header('x-api-key', apiKey)
	response = urllib2.urlopen(req)
	content = csv.reader(response)

	j = 0
	for row in content:
		try:
			if(j != 0):
				csvRows.append(row)
				print row
			j += 1
		except:
			pass

	i+=1
	if(i == 20):
		break

#create aggregated CSV file
if metric == "responseTime":
	with open(metric+'-aggregated.csv', 'w') as outcsv:
	    writer = csv.writer(outcsv)
	    writer.writerow(["Date", "endpoint", "responseTime"])
	    for row in csvRows:
	        writer.writerow(row)

if metric == "errorRate":
	with open(metric+'-aggregated.csv', 'w') as outcsv:
	    writer = csv.writer(outcsv)
	    writer.writerow(["Date", "endpoint", "errorRate"])
	    for row in csvRows:
	        writer.writerow(row)