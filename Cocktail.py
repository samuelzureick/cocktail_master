class Cocktail:
	def __init__(self, name, ingredients, preperation, garnish):
		self.__name = name
		self.__ingredients = ingredients
		self.__preperation = preperation
		self.__garnish = garnish

	def getName(self):
		return self.__name

	def getIngredients(self):
		return self.__ingredients

	def getPreperation(self):
		return self.__preperation

	def getGarnish(self):
		return self.__garnish
