class ProviderCentre:
	def __init__ (self,name,centre):
		self._name = name
		self._centre = centre

	def get_name(self):
		return self._name

	def set_name(self):
		self._name = name

	def get_centre(self):
		return self._centre

	def set_centre(self):
		self._centre = centre


	def __str__(self):
		return self.get_name() + self.get_centre()