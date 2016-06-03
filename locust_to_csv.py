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
	startFlag = 0

	with open(path+"/locust.out") as f:
		for line in f:
			#get median response times for each endpoint
			if(responseFlag == 0 and re.search('Median',line)):
				responseFlag = 2

			if(responseFlag == 3):
				if(re.search('-------------------.',line)):
					responseFlag = 0
				else:	
					responseTimes = line.split()
					try:
						if(responseTimes[8].isdigit()):
							data[responseTimes[1]] = responseTimes[8]

					except IndexError:
						print ''

			if(responseFlag == 2 and re.search('-------------------.',line)):
				responseFlag = 3

			#get error percentages for each endpoint
			if(re.search('Percentage of the requests.',line)):
				startFlag = 1

			if(startFlag == 1 and re.search('Name',line)):
				errorFlag = 1

			if(errorFlag == 2 and re.search('-------------------.',line)):
				errorFlag = 3

			if(errorFlag == 1 and re.search('-------------------.',line)):
				errorFlag = 2

			if(re.search('Total',line)):
				errorFlag = 0

			if(errorFlag == 2):
				errorData = line.split()
				try:
					if(errorData[2].isdigit()):
						err = errorData[3]
						err = err.split('(')
						err = err[1].split('%')
						errors[errorData[1]] = err[0]
				except IndexError:
					print ''

def write_CSV_File():
	with open('responseTime.csv', 'w') as csvfile:
	    fieldnames = ['date', 'endpoint', 'responseTime']
	    writer = csv.writer(csvfile)

	    writer.writerow(fieldnames)
	    for key, value in data.iteritems():
	    	writer.writerow([now.strftime("%Y-%m-%d-%H-%M"), key, value])

def write_error_file():
	with open('errorRate.csv', 'w') as csvfile:
	    fieldnames = ['date', 'endpoint', 'errorRate']
	    writer = csv.writer(csvfile)

	    writer.writerow(fieldnames)
	    for key, value in errors.iteritems():
	    	writer.writerow([now.strftime("%Y-%m-%d-%H-%M"), key, value])

path = get_file_path()
convert_to_CSV(path)
write_CSV_File()
write_error_file()
