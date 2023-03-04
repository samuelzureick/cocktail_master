import tkinter as tk
from tkinter import *
from owlready2 import *
import owlready2
from ast import literal_eval
import difflib

owlready2.JAVA_EXE = "C:\\Users\\szure\\Documents\\Protege-5.5.0\\jre\\bin\\java.exe"
onto = get_ontology("cocktailRefact.owl")
onto.load()
#with onto:
    #sync_reasoner_pellet()
print("here")
graph = default_world.as_rdflib_graph()
o = "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#"

import tkinter as tk
prev_pos = None

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("400x400+100+100")


        # Create a frame for the search bar
        search_frame = tk.Frame(self)
        search_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Create a label and entry widget for the search bar
        tk.Label(search_frame, text="Search:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", expand=True, fill="x")

        # Create a button to initiate the search
        tk.Button(search_frame, text="Search", command=self.search).pack(side="left", padx=5)

        # Create a frame for the allergen checkboxes
        allergens_frame = tk.Frame(self)
        allergens_frame.pack(padx=10, pady=10)

        # Create the allergen checkboxes
        self.allergens = {
            "Celery": tk.BooleanVar(value=False),
            "Crustaceans": tk.BooleanVar(value=False),
            "Dairy": tk.BooleanVar(value=False),
            "Eggs": tk.BooleanVar(value=False),
            "Fish": tk.BooleanVar(value=False),
            "Gluten": tk.BooleanVar(value=False),
            "Lupin": tk.BooleanVar(value=False),
            "Molluscs": tk.BooleanVar(value=False),
            "Mustard": tk.BooleanVar(value=False),
            "Peanuts": tk.BooleanVar(value=False),
            "Sesame": tk.BooleanVar(value=False),
            "Soybeans": tk.BooleanVar(value=False),
            "Sulphites": tk.BooleanVar(value=False),
            "Tree Nuts": tk.BooleanVar(value=False),
            
        }
        for i, allergen in enumerate(self.allergens):
            tk.Checkbutton(allergens_frame, text=allergen, variable=self.allergens[allergen]).grid(row=i // 2,column=i % 2, sticky="w")
    
        # Create a button to initiate the allergen search
        tk.Button(self, text="Search Allergens", command=self.allergen_search).pack(pady=10)

        # Create a button to switch to the advanced query section
        tk.Button(self, text="Advanced Query", command=self.advanced_query).pack(pady=10)

    def search(self):
        query = self.search_entry.get()
        self.getQuery(query)

    def allergen_search(self):
          # Hide the main window
        self.withdraw()

        # Create a new toplevel window to display the selected allergens
        allergen_window = tk.Toplevel(self)
        x, y = self.winfo_x(), self.winfo_y()
        allergen_window.geometry(f"400x400+{x}+{y}")
        allergen_window.title("Selected Allergens")

        # Create a canvas to hold the allergen frame and scrollbar
        canvas = tk.Canvas(allergen_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar and attach it to the canvas
        scrollbar = tk.Scrollbar(allergen_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame to hold the selected allergens label and back button
        allergen_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=allergen_frame, anchor="nw")
        # Add a label to display the selected allergens
        selected_allergens = [allergen for allergen in self.allergens if self.allergens[allergen].get()]
        allergen_dict = {"Celery" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Celery>",
                        "Crustaceans" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Crustaceans>",
                        "Eggs" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Egg>",
                        "Fish" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Fish>",
                        "Gluten" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Gluten>",
                        "Lupin" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Lupin>",
                        "Dairy" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Dairy>",
                        "Molluscs" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Molluscs>",
                        "Mustard" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Mustard>",
                        "Peanuts" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Peanuts>",
                        "Sesame" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Sesame>",
                        "Soybeans" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Soybeans>",
                        "Sulpher dioxide and sulphites" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Sulphites>",
                        "Tree Nuts" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#TreeNuts>"}
        allergen_str = ", ".join(selected_allergens)
        tk.Label(allergen_frame, text=f"Selected Allergens: {allergen_str}").pack(padx=10, pady=10)
        acceptable = set([inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                    { 
                        ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cocktail> .
                    }""")) for inner in outer])
        for aller in selected_allergens:
            avoid = allergen_dict[aller]
            
            bad = set([inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                { 
                    ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cocktail> .
                    ?x rdfs:subClassOf [a owl:Restriction ; owl:onProperty <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#contains> ; owl:someValuesFrom ?y] .
                    ?y (owl:equivalentClass|^owl:equivalentClass)* """+avoid+""" . 
                }""")) for inner in outer])
            acceptable -= bad
        print(acceptable)
        # Add a back button to return to the main interface
        tk.Button(allergen_frame, text="Back", command=lambda: self.back_to_main(allergen_window)).pack(pady=10)

        # Prevent interaction with the main window while the allergen window is open
        allergen_window.grab_set()


    def getQuery(self, query):
        # Do something with the query here
        print(f"Query: {query}")

    def advanced_query(self):
        # Hide the main window
        self.withdraw()

        # Create a new toplevel window to display the advanced query
        advanced_window = tk.Toplevel(self)
        x, y = self.winfo_x(), self.winfo_y()
        advanced_window.geometry(f"400x400+{x}+{y}")
        advanced_window.title("Advanced Query")

        # Create a new frame to hold the advanced query interface
        advanced_frame = tk.Frame(advanced_window)
        advanced_frame.pack(padx=10, pady=10)

        # Add a label to the advanced query frame
        tk.Label(advanced_frame, text="Advanced Query").pack(padx=10, pady=10)

        # Add a button to return to the main interface
        tk.Button(advanced_frame, text="Back", command=lambda: self.back_to_main(advanced_window)).pack(pady=10)
        advanced_window.grab_set()


    def back_to_main(self, f):
        # Store the position of the advanced query window before it is closed
        #prev_pos = (advanced_frame.winfo_x(), advanced_frame.winfo_y())
        x, y = f.winfo_x(), f.winfo_y()
        self.geometry(f"400x400+{x}+{y}")
        f.destroy()
        
        # Show the main window
        self.deiconify()

        


app = App()
app.mainloop()
