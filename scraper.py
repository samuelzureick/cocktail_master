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

with open("classes.txt") as f:
	classes = [c.replace("\n", "") for c in f.readlines()]
driver = webdriver.Chrome()
cocktails = []
def scrape():
	name = driver.find_element(By.CLASS_NAME, "entry-title.text-center")
	print(name.text)
	ingredients = driver.find_element(By.CLASS_NAME, "ingredients-list").text.splitlines()
	#preperation = driver.find_element(By.CLASS_NAME, 'recipeInstructions').text.splitlines()
	#preperation = driver.find_element(By.XPATH, "//span[contains(@itemprop, 'recipeInstructions')]") 
	preperation="temp"
	cocktails.append(Cocktail(name.text,ingredients, preperation))


driver.get("https://punchdrink.com/recipe-archives/")
time.sleep(1)
items = driver.find_elements(By.CLASS_NAME,'recipe-tease__title')
main_window = driver.current_window_handle

for item in items[:1]:
	item.click()
	pass
for child in driver.window_handles:
	if child != main_window:
		driver.switch_to.window(child)
		time.sleep(1)
		scrape()
		driver.close()

def get_classes():
	owlready2.JAVA_EXE = "C:\\Users\\szure\\Downloads\\Protege-5.5.0-win\\Protege-5.5.0\\jre\\bin\\java.exe"
	onto_path.append(".")
	onto = get_ontology("cocktailRefact.owl")
	onto.load()
	with onto:
		sync_reasoner_pellet()
	print(onto)
	classes = list(onto.classes())
	cdict = {}
	for c in classes:
		cdict[re.sub(r"(?<=\w)([A-Z])", r" \1",str(c)[15:]).lower()] = c
	return cdict


def log(cock):
	for c in cock:
		owlready2.JAVA_EXE = "C:\\Users\\szure\\Downloads\\Protege-5.5.0-win\\Protege-5.5.0\\jre\\bin\\java.exe"
		onto_path.append(".")
		onto = get_ontology("cocktailRefact.owl")
		onto.load()
		with onto:
			sync_reasoner_pellet()
		cocktail_name = string.capwords(c.getName()).replace(" ", "")
		ingredients = c.getIngredients()
		with onto:
			temp = types.new_class(cocktail_name, (Cocktail,))







cocktail_dictionary = get_classes()
log(cocktails)


p = driver.current_window_handle
children = driver.window_handles
for child in children:
	if child != p:
		driver.switch_to.window(child)
		scrape()

driver.switch_to.window(p)
scrape()


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