from selenium import webdriver
from selenium.webdriver.common.by import By
from Cocktail import Cocktail
from fraction import Fraction
import difflib
import time
from owlready2 import *
import owlready2
from ast import literal_eval
import re
import types
import string

for i in range(25,35):
	addy = "https://punchdrink.com/recipe-archives/?page="+str(i)
	owlready2.JAVA_EXE = "C:\\Users\\szure\\Downloads\\Protege-5.5.0-win\\Protege-5.5.0\\jre\\bin\\java.exe"
	onto_path.append(".")
	onto = get_ontology("cocktailRefact.owl")
	onto.load()
	#with onto:
		#sync_reasoner_pellet()


	driver = webdriver.Chrome()
	cocktails = []
	missing = ""
	def scrape():
		name = driver.find_element(By.CLASS_NAME, "entry-title.text-center")
		ingredients = driver.find_element(By.CLASS_NAME, "ingredients-list").text
		garnish = driver.find_element(By.CLASS_NAME, "garn-glass").text
		#directions = driver.find_element(By.CLASS_NAME, "recipeInstructions").text.splitlines()
		#preperation = driver.find_element(By.CLASS_NAME, 'recipeInstructions').text.splitlines()
		directions = driver.find_element(By.XPATH, "//ol [@itemprop='recipeInstructions']").text
		cocktails.append(Cocktail(name.text,ingredients, directions, garnish))


	driver.get(addy)
	time.sleep(1)
	items = driver.find_elements(By.CLASS_NAME,'recipe-tease__title')
	main_window = driver.current_window_handle

	for item in items:
		item.click()
		pass
	for child in driver.window_handles:
		if child != main_window:
			driver.switch_to.window(child)
			time.sleep(1)
			scrape()
			driver.close()

	def get_classes():
		classes = list(onto.classes())
		cdict = {}
		for c in classes:
			cdict[re.sub(r"(?<=\w)([A-Z])", r" \1",str(c)[15:]).lower()] = c
		return cdict


	def log(cock):
		onto.contains.python_name = "Contains"
		missing = ""

		for c in cock:
			cocktail_name = string.capwords(c.getName()).replace(" ", "")
			ingredients = c.getIngredients().splitlines()
			with onto:
				mf = False
				found_ing = []
				for ing in ingredients:
					if "ounces" in ing:
						ing = ing[(ing.find("ounces")+6):]
					elif "ounce" in ing:
						ing = ing[(ing.find("ounce")+5):]
					if "(" in ing:
						ing = ing[:ing.find("(")]


					closest_val = difflib.get_close_matches(ing, list(cocktail_dictionary.keys()))
					alt = None
					for potential_ing in list(cocktail_dictionary.keys()):
						if potential_ing in ing.lower():
							alt = potential_ing
							break
					if closest_val != [] and alt == None:
						found_ing.append(closest_val[0])
						#print(match)
					elif closest_val == [] and alt == None:
						#print("COULD NOT FIND MATCH")
						mf = True
						missing += (ing+"\n")
					else:
						found_ing.append(alt)
				if mf == False:
					temp = types.new_class(cocktail_name, (onto.Cocktail,))
					for ingredient in found_ing:
						temp.Contains.append(cocktail_dictionary[ingredient])
					#print(type(c.getIngredients()))
					#print(type(c.getPreperation()))
					#print(type(c.getGarnish()))
					others = [c.getIngredients(), c.getPreperation(), c.getGarnish()]
					temp.comment = others
					#temp.comment.append(c.getPreperation())
					#temp.comment.append(c.getGarnish())

					#temp.contains(cocktail_dictionary[difflib.get_close_matches("ing", list(cocktail_dictionary.keys()))[0]])
		return missing


	cocktail_dictionary = get_classes()
	#print(cocktail_dictionary)
	m = log(cocktails)
	onto.save()
#with open("unknown.txt","w") as f:
#	f.write(m)
	


"""
need to add edge case: if no ingredient found, give alert! 
add this ingredient to temp file that shows the error, let you add what is necessary, 
and then try again!
"""

"""
way to approach:
build scraping program that finds everything not in a class
this will give an idea of how information is formatted
order by number of occurrences
put in those most common first
"""