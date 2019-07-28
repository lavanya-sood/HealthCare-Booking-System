class Notes(object):

    def __init__(self, provider, patient, notes,prescription,date,centre):
        self._provider = provider
        self._patient  = patient
        self._notes     = notes
        self._prescription = prescription
        self._date      = date
        self._centre     = centre

    def get_provider(self):
        return self._provider

    def set_provider(self,provider):
        self._provider = provider

    
    def get_patient(self):
        return self._patient

    def set_patient(self,patient):
        self._patient = patient

    def get_notes(self):
        return self._notes

    def set_notes(self,notes):
        self._notes = notes

    def get_prescription(self):
        return self._prescription

    def set_prescription(self,prescription):
        self._prescription = prescription

    def get_date(self):
        return self._date

    def set_date(self,date):
        self._date = date

    def get_centre(self):
        return self._centre

    def set_centre(self,centre):
        self._centre = centre

    def __str__(self):
        return get_provider(self) + get_patient(self) + get_notes(self) + get_prescription(self) + get_prescription(self)  + get_centre(self)



