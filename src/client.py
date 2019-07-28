from src.centre import *
from src.user import *
from src.providerCentre import *
from src.HealthCareSystem import HealthCareSystem
from src.AdminSystem import *
import csv

def bootstrap_system(auth_manager):

	admin_system = AdminSystem(auth_manager)
	system = HealthCareSystem(admin_system, auth_manager)

	#add centres to system
	with open('src/health_centres.csv') as f:
		csv_reader = csv.reader(f, delimiter=',')
		next(csv_reader)
		for row in csv_reader:
			system.add_centre(Centre(row[0], row[1], row[2], row[3], row[4]))


	#add providers to system
	with open('src/provider.csv') as f:
		reader = csv.reader(f, delimiter=',')
		next(reader)
		for row in reader:
			system.add_provider(Provider(row[0], row[1], row[2],row[3],row[4],row[5]))


	#add patients to system
	with open('src/patient.csv') as f:
		reader = csv.reader(f, delimiter=',')
		next(reader)
		for row in reader:
			system.add_patient(Patient(row[0], row[1], row[2],row[3],row[4]))

	#add centre providers to system
	with open('src/provider_health_centre.csv') as f:
		reader = csv.reader(f, delimiter=',')
		next(reader)
		for row in reader:
			system.add_providerCentre(ProviderCentre(row[0], row[1]))

	return system

