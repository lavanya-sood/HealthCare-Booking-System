class Booking(object):

    def __init__(self, patient, provider, time, date, centre, comment,idno):
        self._patient   = patient
        self._provider  = provider
        self._time      = time
        self._date      = date
        self._centre    = centre
        self._comment   = comment
        self._id        = idno
        self._status    = False
    @property
    def book_centre(self):
        return self._centre

    @property
    def book_patient(self):
        return self._patient

    @property
    def book_provider(self):
        return self._provider

    @property
    def book_time(self):
        return self._time

    @property
    def book_date(self):
        return self._date

    @property
    def book_comments(self):
        return self._comment

    @property
    def book_id(self):
        return self._id

    @property
    def book_status(self):
        return self._status

    def set_bookstatus(self,status):
        self._status = status

    def __str__(self):
        return self.book_centre + self.book_patient + self.book_provider + self.book_time + self.book_date + self.book_comments + self.book_id