import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import json
import sys
import urllib2
import numbers

apiKey = sys.argv[1]
project = sys.argv[2]
metric = sys.argv[3]

plt.figure(figsize=(18,8), dpi=100)
plt.xticks(rotation=70)

colors = ['#000000', '#1f77b4', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

#sometimes we get a null value from datadog
#need to set it to a value or matplot will error
#we set it to an average value
def setNullValues(y_list):
	total = 0
	i = 0
	for val in y_list:
		if val != 'null':
			total += val
			i += 1
	avg = total / i
	
	for key, val in enumerate(y_list):
	    if val == 'null':
	        y_list[key] = avg

	return y_list

def drawGraph(x_list, y_list, count):
	if count == 0:
		plt.plot(x_list, y_list, color = colors[count], linewidth = 5)
	else:	
		plt.plot(x_list, y_list, color = colors[count])


def getFileList():
	req = urllib2.Request('https://artifactory.gannettdigital.com/artifactory/api/storage/load-test-results/'+project+'/'+metric+'?list')
	req.add_header('x-api-key', apiKey)
	resp = urllib2.urlopen(req)
	content = resp.read()

	d = json.loads(content)
	file_list = (d['files'])
	#we want the newest files
	file_list.sort(reverse=True)
	return file_list

def getFileValues(file_list):
	i = 0
	date_list = []
	min_val = 0
	max_val = 0

	for value in file_list: # returns the dictionary as a list of value pairs -- a tuple.
		req = urllib2.Request('https://artifactory.gannettdigital.com/artifactory/load-test-results/'+project+'/'+metric+value['uri'])
		req.add_header('x-api-key', apiKey)
		response = urllib2.urlopen(req)
		content = csv.reader(response)
		x_list = []
		y_list = []

		j = 0
		for row in content:
			try:
				if(j == 0):
					date_list.append(row[1][5:])
				else:
					if row[1] == "":
						y_list.append('null')
					else:
						y_list.append(float(row[1]))
						if float(row[1]) > max_val:
							max_val = float(row[1])
						if(i == 0):
							min_val = float(row[1])
						if float(row[1]) < min_val:
							min_val = float(row[1])

					x_list.append(int(row[0]))

				j += 1
			except:
				pass

		i+=1
		if(i == 20):
			break

		y_list = setNullValues(y_list)
		drawGraph(x_list, y_list, i-1)
	
	return [date_list, min_val, max_val]


def drawLegend(legend_values):		
	#show the dates below graph
	global metric
	i = 0
	j = 0
	col = 0

	delta = float(legend_values[2]) - float(legend_values[1])
	y_val = float(legend_values[1]) - delta * .35

	for date in legend_values[0]:
		plt.text(col, float(y_val-(delta*j)), date, fontsize=14, color=colors[i])
		i += 1
		j += .06
		
		if i > 6 and i < 14:
			col = 75
		elif i >= 14:
			col = 150
		
		if i == 7:
			j = 0
		if i == 14:
			j = 0
	
	if(metric == 'cpu'):
		x_label = 'Idle CPU'

	if(metric == 'memory'):
		x_label = 'Memory Gigabytes'
	
	plt.title('DataDog metric: '+x_label+' for '+project)
	plt.ylabel(x_label, labelpad=20)
	plt.xlabel('Runtime of the tests', labelpad=20)
	plt.savefig(metric+'.png', bbox_inches='tight')

file_list = getFileList()
legend_values = getFileValues(file_list)
drawLegend(legend_values)


