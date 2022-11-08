from selenium import webdriver
from selenium.webdriver.common.by import By
from Cocktail import Cocktail
from fraction import Fraction
import difflib

with open("classes.txt") as f:
	classes = [c.replace("\n", "") for c in f.readlines()]
driver = webdriver.Chrome()

#driver.get("https://punchdrink.com/recipe-archive")
#items = driver.find_elements(By.CLASS_NAME,'recipe-tease__title')
#for item in items:
#	item.click()
driver.get("https://punchdrink.com/recipes/86-long-island-iced-tea/")

def scrape():
	name = driver.find_element(By.CLASS_NAME, "entry-title.text-center")
	print(name.text)
	ingredients = driver.find_element(By.CLASS_NAME, "ingredients-list").text.splitlines()
	print(ingredients)
	for i in range(len(ingredients)):
		loc = ingredients[i].find("ounce")
		if loc != -1:
			ingredients[i] = ingredients[i][loc+len("ounce"):]
		loc = ingredients[i].find("(")
		if loc != -1:
			ingredients[i] = ingredients[i][:loc]
	for ing in ingredients:
		try:
			print("Class found: " + difflib.get_close_matches(ing, classes)[0]) 
		except:
			print("no matching class found!")
	preperation = driver.find_element(By.XPATH, '//*[@id="recipe-content"]/div[4]/div/div[2]/ol')
	print(preperation.text)
	cocktails = []
	cocktails.append(Cocktail(name.text,ingredients, preperation.text))

#p = driver.current_window_handle
#children = driver.window_handles
#for child in children:
#	if child != p:
#		driver.switch_to.window(child)
#		scrape()

#driver.switch_to.window(p)
scrape()


"""
need to add edge case: if no ingredient found, give alert! 
add this ingredient to temp file that shows the error, let you add what is necessary, 
and then try again!
"""