from src.centre import Centre
from src.user import Patient,Provider
from flask_login import current_user
from flask import render_template, request, redirect, url_for, abort
from src.booking import *
from src.notes import *
from src.ratings import *
from server import *
import copy


class HealthCareSystem:
	def __init__(self,admin_system,auth_manager):
		self._centres = []
		self._providers = []
		self._patients = []
		self._bookings = []
		self._ratings = []
		self._notes = []
		self._providerCentre = []
		self._idnumbers = [0000]
		self._pastbook = []
		self._admin_system = admin_system
		self._auth_manager = auth_manager

	#Search by centre values
	def centre_search(self, name=None, location=None, type=1):
		centre_res=[]
		if type == 1:
			for i in self._centres:
				if name.lower() in i.get_name().lower():
					centre_res.append(i)
		elif type == 2:
			for i in self._centres:
				if location == i.get_location():
					centre_res.append(i)
		elif type == 3:
			for i in self._centres:
				centre_res.append(i)
		
		return centre_res	

	#accessing total centre list
	def centre_list(self):
		centre_list = []
		for i in self._centres:
			centre_list.append(i.get_name())

		return centre_list
	
	#Search by centre values
	def provider_search(self, name=None, speciality=None,type=1):
		provider_res =[]
		if type == 1:
			for i in self._providers:
				if name.lower() in i.get_name().lower():
					provider_res.append(i)
		elif type == 2:
			for i in self._providers:
				print(i.get_speciality())
				if speciality == i.get_speciality():
					provider_res.append(i)

		return provider_res	


#Login services

	def login_patient(self, username, password):
		for patient in self._patients:
			if self._auth_manager.login(patient, username, password):
				return True
		return False

	def login_provider(self, username,password):
		for provider in self._providers:
			if self._auth_manager.login(provider, username, password):
				return True
		return False

#Search services

	#getting values for search = location
	def all_locations(self):
		locations = []
		for i in self._centres:
			if i not in locations:
				locations.append(i.get_location())
		return locations

	#getting values for search - specialities
	def all_specialities(self):
		specialities = []
		for i in self._providers:
			if i.get_speciality() not in specialities:
				specialities.append(i.get_speciality())

		return specialities

	#change name of function
	def store_provider_centre(self,name,centre):
		for i in self._providers:
			if i.username == name:
				i.centres.append(centre)
	#add values to the arrays
	def add_centre(self,centre):
		self._centres.append(centre)

	def add_provider(self,provider):
		self._providers.append(provider)

	def add_patient(self,patient):
		self._patients.append(patient)

	def add_providerCentre(self,providerCentre):
		self._providerCentre.append(providerCentre)

	def get_user_by_id(self, user_id):
		for p in self._patients:
			if p.get_id() == user_id:
				return p

		for provider in self._providers:
			if provider.get_id() == user_id:
				return provider
                
		return self._admin_system.get_user_by_id(user_id)


	#Patient Profile editing
	def edit_patient(self, name, username, number, medicare):
	 	#edit_profile(patient,patient.username,new_number,patient.medicare)
		for i in self._patients:
			if i.get_name() == name:
				if username != "":
					i.set_username(username)
				if number != "":
					i.set_number(number)
				if medicare != "":
					i.set_medicare(medicare)
	
	#Provider Profile editing
	def edit_provider(self, name, username, number, idnumber):
	 	#edit_profile(patient,patient.username,new_number,patient.medicare)
		for i in self._providers:
			if i.get_name() == name:
				if username != "":
					i.set_username(username)
				if number != "":
					i.set_number(number)
				if idnumber != "":
					i.set_idno(idnumber)
	


	#retrieving info for html display

	def get_centre(self,name):
		for c in self._centres:
			if c.get_name() == name:
				return c
		return None
	
	def get_patient(self,username):
		for c in self._patients:
			if c.username == current_user.username:
				return c
		return None

	def get_patient_admin(self,name):
		for c in self._patients:
			if c.get_name() == name:
				return c
		return None

	def get_provider(self,name):
		for c in self._providers:
			if c.get_name() == name:
				return c
		return None

	def get_current_user_admin(self,name):
		for c in self._providers:
			if c.username == current.username:
				return c.get_name()
		return None



	@property
	def notes(self):
		return self._notes

	def get_providerForCentre(self,providerCentre):
		working_providers = []

		all_emails = []
		for c in self._providerCentre:
			if c.get_centre() == providerCentre:
				email = c.get_name()
				all_emails.append(email)


		for i in range(len(all_emails)):
			for c in self._providers:
				if c.username == all_emails[i]:
					working_providers.append(c)

		return working_providers


	def get_centreForProvider(self,email):
		all_centres = []

		for c in self._providerCentre:
			if c.get_name() == email:
				centre = c.get_centre()
				all_centres.append(centre)

		return all_centres


#make booking service

	def make_booking(self, patient, provider, time, date, centre, comment):
		id_number = self._idnumbers[-1] + 1;
		self._idnumbers.append(id_number)
		new_booking = Booking(patient, provider, time, date, centre, comment,id_number)
		self._bookings.append(new_booking)
		return new_booking

	@property
	def bookings(self):
		return self._bookings

	def provider_relevant_booking(self,booking,provider):
		relevant_bookings = []
		for c in self._bookings:
			if c.book_provider == provider:
				relevant_bookings.append(c)

		return relevant_bookings

	def provider_relevant_bookingpast(self,booking,provider):
		relevant_bookings = []
		for c in self._pastbook:
			if c.book_provider == provider:
				relevant_bookings.append(c)
		return relevant_bookings

	def provider_relevant_bookingcurr(self,booking,provider):
		relevant_bookings = []
		for c in self._bookings:
			if c.book_provider == provider and c not in self._pastbook:
				relevant_bookings.append(c)

		return relevant_bookings

	def patient_relevant_booking(self,booking,patient):
		relevant_bookings = []
		for c in self._bookings:
			if c.book_patient == patient:
				relevant_bookings.append(c)

		return relevant_bookings

	def patient_relevant_bookingpast(self,booking,patient):
		relevant_bookings = []
		for c in self._pastbook:
			if c.book_patient == patient:
				relevant_bookings.append(c)
		return relevant_bookings

	def patient_relevant_bookingcurr(self,booking,patient):
		relevant_bookings = []
		for c in self._bookings:
			if c.book_patient == patient and c not in self._pastbook:
				relevant_bookings.append(c)

		return relevant_bookings
	
	def availableTimes(self,provider,date):

		list_allTimes = ["12:00AM","12:30AM","1:00AM","1:30AM","2:00AM","2:30AM","3:00AM","3:30AM",
						"4:00AM","4:30AM","5:00AM","5:30AM","6:00AM","6:30AM","7:00AM","7:30AM",
						"8:00AM","8:30AM","9:00AM","9:30AM","10:00AM","10:30AM","11:00AM","11:30AM",
						"12:00PM","12:30PM","1:00PM","1:30PM","2:00PM","2:30PM","3:00PM","3:30PM",
						"4:00PM","4:30PM","5:00PM","5:30PM","6:00PM","6:30PM","7:00PM","7:30PM",
						"8:00PM","8:30PM","9:00PM","9:30PM","10:00PM","10:30PM","11:00PM","11:30PM"]

		for i in self._bookings:
			if (i.book_provider == provider) and (i.book_date == date):
				
				list_allTimes.remove(i.book_time)

		return list_allTimes

#running the appointment
	def run_appointment(self,idno,note,prescription):
		for i in self._bookings:
			if int(i.book_id) == int(idno):
				self._pastbook.append(i)
				for m in self._patients:
					if i.book_patient == m.name:
						self._notes.append(Notes(i.book_provider,i.book_patient,note,prescription,i.book_date,i.book_centre))
		return None
 	

#rating services
	@property
	def ratings(self):
		return self._ratings


	def add_rating(self,provider,patient,rating):
		new_rating = Rating(provider, patient,rating)

		for i in self._ratings:
			if i.provider == provider and i.patient == patient:
				self._ratings.remove(i)

		self._ratings.append(new_rating)
		return new_rating


	def provider_relevant_rating(self,provider,patient):

		relevant_ratings = []
		for i in self._ratings:
			if i.provider == provider:
				rating_given = i.rating
				relevant_ratings.append(rating_given)

		default_rating = 3
		if len(relevant_ratings) == 0:
			return default_rating
		else:
			total_sum = sum(relevant_ratings)
			length = len(relevant_ratings)
			final_rating = total_sum/length
			return round(final_rating,2)

 		 
	def length_provider_relevant_rating(self,provider,patient):

		relevant_ratings = []
		for i in self._ratings:
			if i.provider == provider:
				rating_given = i.rating
				relevant_ratings.append(rating_given)

		return len(relevant_ratings)


	#get the patients history
	def get_patient_history(self,patient,provider):
		patient_notes =[]
		for h in self._notes:
			if patient == h.get_patient():
				for p in self._providers:
					if provider == p.name:
						all_centres = []

						for c in self._providerCentre:
							if c.get_name() == p.username:
								centre = c.get_centre()
								all_centres.append(centre)

						if h.get_centre() in all_centres:
							patient_notes.append(h)

		return patient_notes



 