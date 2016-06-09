import sched, time
import requests

apiKey = sys.argv[1]
projectId = sys.argv[2]

i = 0
s = sched.scheduler(time.time, time.sleep)
def poll_artifactory(sc): 
    global i
    i += 1
    
    getResults()

    if(i < 9):
    	sc.enter(5, 1, poll_artifactory, (sc,))

def getResults():
	url = 'http://artifactory.gannettdigital.com/artifactory/load-test-results/'+projectId+'/SLA/'
	payload = json.load(open("request.json"))
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-api-key':apiKey}
	r = requests.get(url, headers=headers)

s.enter(5, 1, poll_artifactory, (s,))
s.run()
