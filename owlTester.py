from owlready2 import *
onto_path.append(".")
onto = get_ontology("pizzaTutorial.owl")
onto.load()

test_pizza = onto.Pizza("test_pizza_owl_identifier")
test_pizza.has_topping = [ onto.CheeseTopping(), onto.TomatoTopping(), onto.MeatTopping()]
onto.save()