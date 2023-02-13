from owlready2 import *
import owlready2
owlready2.JAVA_EXE = "C:\\Users\\szure\\Downloads\\Protege-5.5.0-win\\Protege-5.5.0\\jre\\bin\\java.exe"
onto_path.append(".")
onto = get_ontology("cocktailmaster.owl")
onto.load()
with onto:
	sync_reasoner_pellet()
cocktails = onto.get_children_of(onto.cocktail)
allergens = onto.get_children_of(onto.major_allergen)
for c in cocktails:
	s = str(c.is_a)
	for a in allergens:
		if str(a) in s:
			print("allergen found!")
			print("cocktail: " +str(c))
			print("allergen: " +str(a))
