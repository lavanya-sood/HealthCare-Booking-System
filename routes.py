#from server import app, valid_time, auth_manager

from server import *

from flask import request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, UserMixin, login_user, logout_user, login_required
from src.client import *
from src.HealthCareSystem import *
from src.booking import *
import datetime

#very first page
@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('start.html')

#welcome page
@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome_page():
	name = current_user.name
	return render_template('welcome.html',name=name)

#error page
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404

#patient login
@app.route('/login', methods=['GET', 'POST'])
def login():
	messagePatient = ''
	if request.method == "POST":
		username = request.form['name']
		password = request.form['password']

		if system.login_patient(username,password):
			return redirect(url_for('welcome_page'))
		else:
			messagePatient = 'Wrong username or password. Please try again.'
				
	return render_template("login.html", messagePatient = messagePatient,messageProvider = '')

#admin login
@app.route('/login_provider', methods=['GET', 'POST'])
def login_provider():
	messageProvider = ''
	if request.method == "POST":
		username = request.form['name']
		password = request.form['password']

		if system.login_provider(username,password):
			return redirect(url_for('welcome_page'))
		else:
			messageProvider = 'Wrong username or password. Please try again.'
				
	return render_template("login.html",messageProvider=messageProvider,messagePatient = '')


#search page
@app.route('/search', methods=['GET', 'POST'])
#@auth_manager.patient_required
@login_required
@auth_manager.patient_required
def search_page():
	
	message = ''
	
	locations = ['--Please select a location--'] + system.all_locations()
	specialities = ['--Please select a speciality--'] + system.all_specialities()

	if request.method == 'POST':
		type_search = request.form['select']

		if type_search == 'search_center':
			center_search = request.form['center']
			lcoation_search = request.form['loc']
			message = f"Searching by Center name - {center_search}"

			
			correct_results = system.centre_search(center_search,lcoation_search,1)
			length = len(correct_results)
			numres = "Results: {} search results.".format(length)

			return render_template('search.html',message=message,locations=locations, specialities=specialities,correct_results=correct_results,length=length,numres=numres,provider_search=False,centre_search=True)

		elif type_search == 'search_location':
			center_search = request.form['center']
			lcoation_search = request.form['loc']
			message = f"Searching by Location name - {lcoation_search}"

			correct_results = system.centre_search(center_search,lcoation_search,2)
			length = len(correct_results)
			numres = "Results: {} search results.".format(length)
			return render_template('search.html',message=message,locations=locations, specialities=specialities,correct_results=correct_results,length=length,numres=numres,provider_search=False,centre_search=True)

		elif type_search == 'search_speciality':
			provider_search = request.form['provider']
			speciality_search = request.form['sp']
			message = f"Searching by Provider Speciality - {speciality_search}"

			correct_results2 = system.provider_search(provider_search,speciality_search,2)
			length = len(correct_results2)
			numres = "Results: {} search results.".format(length)
			return render_template('search.html',message=message,locations=locations, specialities=specialities,correct_results2=correct_results2,length=length,numres=numres,provider_search=True,centre_search=False)
		
		else:
			provider_search = request.form['provider']
			speciality_search = request.form['sp']
			message = f"Searching by Provider name - {provider_search}"

			correct_results2 = system.provider_search(provider_search,speciality_search,1)
			length = len(correct_results2)
			numres = "Results: {} search results.".format(length)
			return render_template('search.html',message=message,locations=locations, specialities=specialities,correct_results2=correct_results2,length=length,numres=numres,provider_search=True,centre_search=False)

	correct_results = system.centre_search('','',3)
	message = "All results"
	length = len(correct_results)
	numres = "Results: {} search results.".format(length)

	return render_template('search.html',message=message,locations=locations, specialities=specialities,correct_results=correct_results,length=length,numres=numres,centre_search=False, provider_search=False)

#making an appointment 
@app.route('/book_part1', methods=['POST', 'GET'])
@auth_manager.patient_required
def book_page():

	if request.method == 'POST':
		center_chosen = request.form["healthcare_centres"]
		now = datetime.datetime.now()
		current_day_plus1 = int(now.day) + 1
		current_date = f"{now.year}-{now.month}-{current_day_plus1}"
		return render_template('booking_part2.html', centre_chosen=center_chosen,current_date=current_date,providerCentres=system.get_providerForCentre(center_chosen))
	
	return render_template('booking.html',centre_names=system.centre_list())


@app.route('/book_part2', methods=['POST', 'GET'])
@auth_manager.patient_required
def book_page_part2():

	if request.method == 'POST':
		date_chosen = request.form["date_slot"]
		center_chosen = request.form["healthcare_centres"]
		provider_chosen = request.form['providerBasedOnCentre']
		return render_template('booking_part3.html', centre_chosen=center_chosen,date_chosen=date_chosen,provider_chosen=provider_chosen,availableTimes=system.availableTimes(provider_chosen,date_chosen))
	
	abort(404)


@app.route('/book_part3', methods=['POST', 'GET'])
@auth_manager.patient_required
def book_page_part3():

	if request.method == 'POST':

		time_slot = request.form["time_slot"]
		date_slot = request.form["date_slot"]
		comment = request.form["comments"]
		patient = current_user.name
		provider = request.form['providerBasedOnCentre']
		centre_chosen = request.form['healthcare_centres']

		booking = system.make_booking(patient, provider, time_slot, date_slot, centre_chosen, comment)
		return render_template('success_booking.html')
	
	abort(404)



#viewing profiles of patient  = COMPLETED, works fine dont edit
@app.route('/view_patient/<name>',methods=['GET','POST'])
@auth_manager.patient_required
def view_patient_profile(name):
	patient =  system.get_patient(current_user.username)
	return render_template('patient_profile.html',patient=patient)

@app.route('/view_patient_adminview/<name>',methods=['GET','POST'])
@auth_manager.provider_required
def view_patient_profile_admin(name):

	patient = system.get_patient_admin(name)
	return render_template('patient_profile.html',patient=patient)


#log out
@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    auth_manager.logout()
    return redirect(url_for("index"))

#view all apointments - PATIENT
@app.route('/appointments',methods=['GET','POST'])
@auth_manager.patient_required
def appointments_page():
	return render_template('appointment.html',name=current_user.name,book=system.patient_relevant_booking(system.bookings,current_user.name))


#view current apointments - PATIENT
@app.route('/patient_appointments_current',methods=['GET','POST'])
@auth_manager.patient_required
def patient_appointments_currentpage():
	return render_template('appointment.html',book=system.patient_relevant_bookingcurr(system.bookings,current_user.name),name=current_user.name)


#view past apointments - PATIENT
@app.route('/patient_appointments_past',methods=['GET','POST'])
@auth_manager.patient_required
def patient_appointments_pastpage():
	return render_template('appointment.html',book=system.patient_relevant_bookingpast(system.bookings,current_user.name),name=current_user.name)


#view all apointments - ADMIN
@app.route('/provider_appointments',methods=['GET','POST'])
@auth_manager.provider_required
def admin_appointments_page():
	return render_template('appointment.html',book=system.provider_relevant_booking(system.bookings,current_user.name),name=current_user.name)


#view current apointments - ADMIN
@app.route('/provider_appointments_current',methods=['GET','POST'])
@auth_manager.provider_required
def admin_appointments_currentpage():
	return render_template('appointment.html',currstat=True,book=system.provider_relevant_bookingcurr(system.bookings,current_user.name),name=current_user.name)


#view past apointments - ADMIN
@app.route('/provider_appointments_past',methods=['GET','POST'])
@auth_manager.provider_required
def admin_appointments_pastpage():
	return render_template('appointment.html',currstat=False,book=system.provider_relevant_bookingpast(system.bookings,current_user.name),name=current_user.name)


@app.route('/consultation,<idno>',methods=['GET','POST'])
@login_required
@auth_manager.provider_required
def consultation_page(idno):
	if request.method == 'POST':
		comments = request.form["comments"]
		perscription = request.form["perscription"]
		system.run_appointment(idno,comments,perscription)
		return render_template('consultation.html',idno=idno,donestatus=True)

	return render_template('consultation.html',idno=idno,donestatus=False)

#history of patient
@app.route('/history/<name>',methods=['GET','POST'])
@login_required
@auth_manager.provider_required
def patient_history(name):
	history = system.get_patient_history(name,current_user.name)
	return render_template('notes.html',name=name,history=history)

#viewing profiles of providers
@app.route('/view_provider/<name>')
@login_required
def view_profile_provider(name):
	provider = system.get_provider(name)
	current_rating = system.provider_relevant_rating(name, current_user.name)
	len_of_ratings = system.length_provider_relevant_rating(name,current_user.name)
	workingCentres = system.get_centreForProvider(provider.username)
	return render_template('provider_profile.html', provider=provider,workingCentres=workingCentres,current_rating=current_rating,len_of_ratings=len_of_ratings)


#view centre profile = COMPLETED,
@app.route('/view_centre/<name>')
@auth_manager.patient_required
def view_profile(name):
	centre = system.get_centre(name)
	current_rating = system.provider_relevant_rating(name, current_user.name)
	len_of_ratings = system.length_provider_relevant_rating(name, current_user.name)
	workingProviders = system.get_providerForCentre(name)
	return render_template('centre_profile.html',centre=centre,workingProviders=workingProviders,current_rating=current_rating,len_of_ratings=len_of_ratings)

@app.route('/adminview_centre/<name>')
@auth_manager.provider_required
def view_profile_admin(name):
	centre = system.get_centre(name)
	workingProviders = system.get_providerForCentre(name)
	return render_template('centre_profile.html',centre=centre,workingProviders=workingProviders)

@app.route('/give_rating_provider/<name>',methods=["POST", "GET"])
@auth_manager.patient_required
def give_rating_provider(name):
	message = ""

	if request.method == "POST":

		rating = int(request.form["rating"])
		system.add_rating(name,current_user.name,rating)
		message = "Thank you for rating."
		return render_template('give_rate_provider.html',name=name,message=message)

	return render_template('give_rate_provider.html',name=name,message=message)


@app.route('/give_rating_centre/<name>',methods=["POST", "GET"])
@auth_manager.patient_required
def give_rating_centre(name):
	message = ""

	if request.method == "POST":

		rating = int(request.form["rating"])
		system.add_rating(name,current_user.name,rating)
		message = "Thank you for rating."
		return render_template('give_rate_centre.html',name=name,message=message)

	return render_template('give_rate_centre.html',name=name,message=message)


#edit patient profile
@app.route('/edit_patient_profile/<name>',methods=['GET','POST'])
@auth_manager.patient_required
def edit_profile(name):
	
	#patient =  system.get_patient(current_user.username)
	patient = system.get_patient_admin(name)
	if request.method == "POST":
		new_username = request.form["new_username"]
		new_number = request.form["new_number"]
		new_medicare = request.form["new_medicare"]
		system.edit_patient(name,new_username,new_number,new_medicare)
		return render_template('edit_patient_profile.html', patient=patient,donestatus=True,message="Changes are saved!")
	
	return render_template('edit_patient_profile.html', patient=patient,donestatus=False)


#edit provider profile
@app.route('/edit_provider_profile/<name>',methods=['GET','POST'])
@auth_manager.provider_required
def edit_profile_provider(name):
	
	#patient =  system.get_patient(current_user.username)
	provider = system.get_provider(name)
	if request.method == "POST":
		new_username = request.form["new_username"]
		new_number = request.form["new_number"]
		idnumber = request.form["new_id"]
		system.edit_provider(name,new_username,new_number,idnumber)
		return render_template('edit_provider_profile.html', provider=provider,donestatus=True,message="Changes are saved!")
	
	return render_template('edit_provider_profile.html', provider=provider,donestatus=False)		
