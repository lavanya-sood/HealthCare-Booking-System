class Centre:
	def __init__ (self,typeof,abn,name,number,location):
		self._typeof = typeof
		self._abn = abn
		self._name = name
		self._number = number
		self._location = location
		self._ratings = []

	def get_typeof(self):
		return self._typeof

	def set_typeof(self):
		self._typeof = typeof

	def get_abn(self):
		return self._abn

	def set_abn(self):
		self._abn = abn

	def get_name(self):
		return self._name

	def set_name(self):
		self._name = name

	def get_number(self):
		return self._number

	def set_number(self):
		self._number = number

	def get_location(self):
		return self._location

	def set_location(self):
		self._location = location

	def set_rating(self,r):
		self._ratings = r

	def get_rating(self):
		return self._ratings


	def __str__(self):
		return self.get_typeof() + self.get_abn() + self.get_name() + self.get_number() + self.get_location() + self.get_rating()