class Cocktail:
	def __init__(self, name, ingredients, preperation):
		self.__name = name
		self.__ingredients = ingredients
		self.__preperation = preperation

	def getName(self):
		return self.__name

	def getIngredients(self):
		return self.__ingredients

	def getPreperation(self):
		return self.__preperation
