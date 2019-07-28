import pytest
from src.HealthCareSystem import HealthCareSystem
from src.client import *

class Test(object):
    
    def setup_method(self):
        from src.AuthenticationManager import DummyAuthenticationManager
        self.system = bootstrap_system(DummyAuthenticationManager())


    def test_book_appointment(self):
        booking = self.system.make_booking()
        #1. test that making a successful appointment and getting a confirmation of the appointment works
        appointments = self.system.bookings
        patient = self.system.login_patient("jack@gmail.com", "cs1531")
        booking = self.system.make_booking(patient, "Toby Weathers", "2:30AM", "2018-10-21", "Sydney Children Hospital", "")
        new_appointments = self.system.bookings
        assert len(new_appointments) > len(appointments)

        #2. test that booking an appointment in the past fails
            #This is handled by the inbuilt features of HTML

        #3. test that booking multiple appointments in the same day/time-slot fails
    def test_book_appointment_past(self)
        appointments = self.system.bookings
        patient = self.system.login_patient("jack@gmail.com", "cs1531")
        asssert len(availableTimes("Toby Weathers","2018-10-21")) == 48
        booking = self.system.make_booking(patient, "Toby Weathers", "2:30AM", "2018-10-21", "Sydney Children Hospital", "")
        new_appointments = self.system.bookings
        asssert len(availableTimes("Toby Weathers","2018-10-21")) == 47
        assert len(new_appointments) > len(appointments)

        #4. test that a provider cannot make an appointment with themselves
            #The booking page is not visible from a provider's perspective so It fails
    
    def test_manage_null_patient_history(self):

        #1. test that when no history/notes exists - the notes are not added to the list
        patient = self.system.get_patient("jack@gmail.com")
        provider = self.system.get_provider("toby@gmail.com")
        booking = self.system.make_booking(patient, provider, "2:00AM", "2018-10-16", "Sydney Children Hospital", "")

        assert(len(self.system.notes) == 0)

    def test_manage_single_patient_history(self):

        #2. test that if notes are added then the notes array has some variables in it 
        patient = self.system.get_patient("jack@gmail.com")
        provider = self.system.get_provider("toby@gmail.com")
        booking = self.system.make_booking(patient, provider, "2:00AM", "2018-10-16", "Sydney Children Hospital", "")
        appointment = self.system.run_appointment(1,"Patient had a mild cold","Mild Anti-biotics")
        assert(len(self.system.notes) != 0)

    def test_manage_single_patient_history_multiple_notes(self):
        #3. test if mutiples notes have been added, they can all be viewed on the same page
        patient = self.system.get_patient("jack@gmail.com")
        provider = self.system.get_provider("toby@gmail.com")
        booking = self.system.make_booking(patient, provider, "2:00AM", "2018-10-16", "Sydney Children Hospital", "")
        appointment = self.system.run_appointment(1,"Patient had a mild cold","Mild Anti-biotics")

        booking2 = self.system.make_booking(patient, provider, "2:30AM", "2018-10-16", "Sydney Children Hospital", "")
        appointment = self.system.run_appointment(1,"Patient had a high cold","Intense Anti-biotics")
        
        booking3 = self.system.make_booking(patient, provider, "3:00AM", "2018-10-16", "Sydney Children Hospital", "")
        appointment = self.system.run_appointment(1,"Patient had a low cold","No Anti-biotics")

        assert(len(self.system.notes) == 3)
        #assert()
    
    def test_view_patient_history_by_doctor_who_made_notes(self):
        #1. check if the consultatncy notes of a patient can be viewed by the doctor who made it
        patient = self.system.get_patient("jack@gmail.com")
        provider = self.system.get_provider("toby@gmail.com")
        booking = self.system.make_booking(patient, provider, "2:00AM", "2018-10-16", "Sydney Children Hospital", "")
        appointment = self.system.run_appointment(1,"Patient had a mild cold","Mild Anti-biotics")
        assert(len(self.system.notes = 1))
        notes = self.system.get_patient_history(patient,provider)
        assert (len(notes) == 1)

    def test_view_patient_history_by_doctor_in_same_centre(self):
        #2. check if the consultatncy notes of a patient can be viewed by the doctor who works at the same centre where the patient previously visited
        patient = self.system.get_patient("jack@gmail.com")
        provider = self.system.get_provider("toby@gmail.com")
        provider2 = self.system.get_provider("anna@gmail.com")
        booking = self.system.make_booking(patient, provider, "2:00AM", "2018-10-16", "Sydney Children Hospital", "")
        appointment = self.system.run_appointment(1,"Patient had a mild cold","Mild Anti-biotics")
        assert(len(self.system.notes = 1))
        notes = self.system.get_patient_history(patient,provider2)
        assert (len(notes) == 1)
        

    def test_view_patient_history_by_doctor_in_different_centre(self):
        #3. check if the consultatncy notes of a patient cannot be viewed by a doctor in a place the patient hasn't previously visited
        patient = self.system.get_patient("jack@gmail.com")
        provider = self.system.get_provider("toby@gmail.com")
        provider2 = self.system.get_provider("helena@gmail.com")
        booking = self.system.make_booking(patient, provider, "2:00AM", "2018-10-16", "Sydney Children Hospital", "")
        appointment = self.system.run_appointment(1,"Patient had a mild cold","Mild Anti-biotics")
        assert(len(self.system.notes = 1))
        notes = self.system.get_patient_history(patient,provider2)
        assert (len(notes) == 0)

    def test_view_multiple_patient_history_by_doctor_in_same_centre(self):
        #4. check if the multiple consultatncy notes of a patient can be viewed by a doctor 
        patient = self.system.get_patient("jack@gmail.com")
        provider = self.system.get_provider("toby@gmail.com")
        booking = self.system.make_booking(patient, provider, "2:00AM", "2018-10-16", "Sydney Children Hospital", "")
        appointment = self.system.run_appointment(1,"Patient had a mild cold","Mild Anti-biotics")
        appointment = self.system.run_appointment(2,"Patient had a Fever","Mild Medicines")
        assert(len(self.system.notes = 2))
        notes = self.system.get_patient_history(patient,provider)
        assert (len(notes) == 2)
