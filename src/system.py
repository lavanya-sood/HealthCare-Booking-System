import csv

centre_list = []
with open('health_centres.csv') as f:
	csv_reader = csv.reader(f, delimiter=',')
	next(csv_reader)
	for row in csv_reader:
		centre_list.append(Centre(row[0], row[1], row[2], row[3], row[4]))

