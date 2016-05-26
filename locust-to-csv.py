import os
import re
import csv
import datetime

now = datetime.datetime.now()

#check for this line: "Percentage of the requests completed within given times"
#after matching it, read the 2nd line down (ms results line)
#endpoint, response time

data = {}

def get_file_path():
	dirList = next(os.walk('.'))[1]
	dirList.sort()
	return dirList[-1]

def convert_to_CSV(path):
	errorFlag = 0
	responseFlag = 0
	totalErrors = 0
	totalRequests = 0

	with open(path+"/locust.out") as f:
		for line in f:
			if(re.search('Percentage of the requests.',line)):
				responseFlag = 1
			 
			if(responseFlag == 2 and re.search('-------------------.',line)):
				responseFlag = 3

			if(responseFlag == 1 and re.search('-------------------.',line)):
				responseFlag = 2

			if(responseFlag == 2):
				responseTimes = line.split()
				try:
					if(responseTimes[7].isdigit()):
						data[responseTimes[1]] = responseTimes[7]
				except IndexError:
					print ''

def write_CSV_File(path):
	with open(path+'/responseTime.csv', 'w') as csvfile:
	    fieldnames = ['date', 'endpoint', 'responseTime']
	    writer = csv.writer(csvfile)

	    writer.writerow(fieldnames)
	    for key, value in data.iteritems():
	    	writer.writerow([now.strftime("%Y-%m-%d-%H-%M"), key, value])

path = get_file_path()
convert_to_CSV(path)
write_CSV_File(path)