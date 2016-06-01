import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import sys

plt.figure(figsize=(18,8), dpi=100)
plt.xticks(rotation=70)

colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

with open('errorRate-aggregated.csv', 'rU') as infile:
  # read the file as a dictionary for each row ({header : value})
	reader = csv.DictReader(infile)
	data = {}
	for row in reader:
		for header, value in row.items():
			try:
				data[header].append(value)
			except KeyError:
				data[header] = [value]

#get list of unique endpoints for looping through
try:
	endpointList = list(set(data['endpoint']))
	xData = {}
	for value in endpointList:
		xData[value] = [];

	#get rid of duplicate dates
	data['Date'] = list(set(data['Date']))

	#show from oldest test to newest
	data['Date'].reverse()

	with open('errorRate-aggregated.csv', 'rU') as infile:
	  # read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		for row in reader:
			for url in endpointList:
				if row['endpoint'] == url:
					xData[url].append(int(float(row['errorRate'])))

	#get the number of data points - this will be the number of tickpoints on the chart
	x = 0
	num_of_datapoints = []
	while (x < len(xData[endpointList[0]])):
		num_of_datapoints.append(x)
		x += 1

	#set the highest value
	highest = 100

	j = 0
	decrement = 0
	for key, val in xData.items():
		if len(val) > 1:
			x = 0
			num_of_datapoints = []
			for items in val:
				num_of_datapoints.append(x)
				x += 1 

			plt.plot(num_of_datapoints, val, color = colors[j])
			plt.text((len(num_of_datapoints)-1)*1.02, highest - decrement, key, fontsize=14, color=colors[j])
			
			if j == 19:
				j = 0
			else: 
				j += 1
			decrement += highest*.05

	plt.xticks(num_of_datapoints, data['Date'])
	plt.title('Error Rate of Previous builds')
	plt.ylabel('Percentage Error Rate', labelpad=20)
	plt.xlabel('Date: Year-Month-Day-Hour-Second', labelpad=20)
	plt.ylim([-10,110])

	plt.savefig('errorRate.png', bbox_inches='tight')

except:
	print ""