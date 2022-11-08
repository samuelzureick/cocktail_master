from selenium import webdriver
from selenium.webdriver.common.by import By
from Cocktail import Cocktail
from fraction import Fraction

driver = webdriver.Chrome()

driver.get("https://punchdrink.com/recipe-archive")
items = driver.find_elements(By.CLASS_NAME,'recipe-tease__title')
for item in items:
	item.click()

def scrape():
	name = driver.find_element(By.CLASS_NAME, "entry-title.text-center")
	print(name.text)
	ingredients = driver.find_element(By.CLASS_NAME, "ingredients-list")
	print(ingredients.text.splitlines())
	preperation = driver.find_element(By.XPATH, '//*[@id="recipe-content"]/div[4]/div/div[2]/ol')
	print(preperation.text)
	cocktails = []
	cocktails.append(Cocktail(name.text,ingredients.text.splitlines(), preperation.text))

p = driver.current_window_handle
children = driver.window_handles
for child in children:
	if child != p:
		driver.switch_to.window(child)
		scrape()

driver.switch_to.window(p)

#driver.get("https://punchdrink.com/recipes/86-long-island-iced-tea/")

