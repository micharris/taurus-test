import re
import os

def response_SLA():
	responseFlag = 0

	with open("stats.log") as f:
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
						if(int(responseTimes[7]) > 1500): #1500 ms is the max 90th percentile response time per Jesiah
							return "SLA response time exceeded for 90th percentile: "+responseTimes[0]+responseTimes[1]+" was "+responseTimes[7]+" ms"
				except IndexError:
					print ''

def write_response(response):
	text_file = open("SLA.txt", "w")
	text_file.write(response)
	text_file.close()

response = response_SLA()
write_response(response)
