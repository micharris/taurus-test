from datadog import initialize, api
import time
import json
import sys
import string
 
#must pass in api key and app key from teamcity
options = {
    'api_key': sys.argv[1],
    'app_key': sys.argv[2]
}

event_type = sys.argv[3]
servers = sys.argv[4]

initialize(**options)
 

#get the hosts names for farm:caproxy,environment:development,farm_role:caproxy-app
start = int(time.time())

query_cpu = 'system.cpu.idle{'+servers+'} by {host}' 
results = api.Metric.query(start=start-100, end=start+100, query=query_cpu)

host_list = []
for row in results["series"]:
	exp_list = row["expression"].split('host:')
	host_list.append(exp_list[1].rstrip('}'))

#loop through host list and post load test event to each host
title = "Load Test"+sys.argv[3]
text = 'Load test '+sys.argv[3]
tags = 'load test'
alert_type = "info"

for host in host_list:
	api.Event.create(title=title, text=text, tags=tags, host=host)
