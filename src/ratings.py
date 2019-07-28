class Rating(object):

    def __init__(self, provider, patient, rating):
        self._providers = provider
        self._patients  = patient
        self._ratings   = rating

    @property
    def provider(self):
        return self._providers

    @property
    def patient(self):
        return self._patients

    @property
    def rating(self):
        return self._ratings


    def __str__(self):
        return self._providers + self._patients + self._ratings