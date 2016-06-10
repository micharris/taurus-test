import sched, time
import requests
import sys
import urllib2

apiKey = sys.argv[1]
projectId = sys.argv[2]
file_list = []
list_count = 0

i = 0
s = sched.scheduler(time.time, time.sleep)
def poll_artifactory(sc): 
    global i
    i += 1
    
    getResults(i)

    if(i < 12):
    	sc.enter(60, 1, poll_artifactory, (sc,))

def getResults(i):
	global list_count

	#get a list 
	req = urllib2.Request('https://artifactory.gannettdigital.com/artifactory/api/storage/load-test-results/'+projectId+'/sla?list')
	req.add_header('x-api-key', apiKey)
	resp = urllib2.urlopen(req)
	content = resp.read()

	d = json.loads(content)
	file_list = (d['files'])
	num_files = len(file_list)

	#on first run get the total number of files
	if i == 1:
		list_count = num_files

	#when a new file is added - that is the latest SLA result file
	if i != 1:
		if num_files > list_count:
			file_list.sort(reverse=True)
			file_url = file_list[-1]
			getSLA(file_url)

def getSLA(file_url):
	req = urllib2.Request('https://artifactory.gannettdigital.com/artifactory/load-test-results/'+projectId+'/sla/'+file_url)
	req.add_header('x-api-key', apiKey)
	response = urllib2.urlopen(req)
	content = csv.reader(response)
	print content


s.enter(60, 1, poll_artifactory, (s,))
s.run()
