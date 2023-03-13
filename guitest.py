import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import ttk
from owlready2 import *
import owlready2
from ast import literal_eval
import difflib
import PIL
from PIL import ImageTk, Image, ImageShow 
ImageShow.WindowsViewer.format = "PNG"


owlready2.JAVA_EXE = "C:\\Users\\szure\\Documents\\Protege-5.5.0\\jre\\bin\\java.exe"
onto = get_ontology("cocktailRefact.owl")
onto.load()
#with onto:
    #sync_reasoner_pellet()
graph = default_world.as_rdflib_graph()
o = "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#"

import tkinter as tk
cocktails = set([inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                    { 
                        ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cocktail> .
                    }""")) for inner in outer])
cocktails = [re.sub(r"(?<=\w)([A-Z])", r" \1",str(cock)[15:]).lower() for cock in cocktails]



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Booze Muse")
        self.geometry("600x500+100+100")
        self.configure(bg="#2A3439")


        # Create a frame for the search bar
        search_frame = tk.Frame(self, borderwidth = 0)
        search_frame.pack(side="top", fill="x", padx=10, pady=10)
        search_frame.configure(bg="#2A3439")

        
        # Create a label and entry widget for the search bar
        titleText = ImageTk.PhotoImage(Image.open("finalb.PNG"))
        l1 = tk.Label(search_frame, image=titleText,borderwidth = 0)
        l1.image = titleText
        l1.pack(side="top", anchor="nw")


        # Create a frame for the allergen checkboxes
        allergens_frame = tk.Frame(self, borderwidth = 0)
        allergens_frame.pack(side="left", padx=10, pady=10)
        allergens_frame.configure(bg="#2A3439")


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
            tk.Checkbutton(allergens_frame, bg="#2A3439", text=allergen,font=(("Courier New Bold"), 10), variable=self.allergens[allergen], fg="#E3DAC9").grid(
                row=i // 2, column=i % 2, sticky="w")


        # Create a button to initiate the allergen search
        tk.Button(allergens_frame, text="Search Allergens", command=self.allergen_search, bg="#377771", fg="#E3DAC9").grid(row=8, column=0)


        # Create a button to switch to the advanced query section
        tk.Button(allergens_frame, text="Advanced Query", font=(("Courier New Bold"), 10), command=self.advanced_query, bg="#377771", fg="#E3DAC9").grid(row=8, column=1)


        # Create a frame for the cocktail listbox and filter box
        cocktail_frame = tk.Frame(self, borderwidth = 0)
        cocktail_frame.pack(side="right", fill="both", padx=10, pady=10)
        cocktail_frame.configure(bg="#2A3439")


        # Create a filter box and add it to the cocktail frame
        filter_frame = tk.Frame(cocktail_frame, borderwidth = 0)
        filter_frame.pack(side="top", fill="x", padx=10, pady=10)
        filter_frame.configure(bg="#2A3439")

        
        # Create a listbox for displaying the cocktails
        self.cocktail_listbox = tk.Listbox(cocktail_frame, selectmode=tk.SINGLE, width=50)

        # Create a scrollbar for the cocktail listbox
        scrollbar = tk.Scrollbar(cocktail_frame)
        scrollbar.pack(side="right", fill="y")
        self.cocktail_listbox.config(yscrollcommand=scrollbar.set, width=50,bg="#2A3439")
        scrollbar.config(command=self.cocktail_listbox.yview)
        self.cocktail_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)


        # Load data into the listbox
        self.load_cocktails()

        # Create a filter label and entry widget for the listbox
        tk.Label(filter_frame, text="Filter Cocktails:", font=(("Courier New Bold"), 10)).pack(side="left")
        self.filter_entry = tk.Entry(filter_frame)
        self.filter_entry.pack(side="left", expand=True, fill="x")
        self.filter_entry.bind("<KeyRelease>", self.filter_cocktails)


    def load_cocktails(self):
        # Add cocktails to the listbox
        for cocktail in cocktails:
            self.cocktail_listbox.insert(tk.END, cocktail)

    def filter_cocktails(self, event):
        # Clear the listbox
        self.cocktail_listbox.delete(0, tk.END)

        # Filter the cocktails based on the filter text
        filter_text = self.filter_entry.get().lower()
        for cocktail in cocktails:
            if filter_text in cocktail.lower():
                self.cocktail_listbox.insert(tk.END, cocktail)
        


    def search(self):
        query = self.search_entry.get()
        self.getQuery(query)


    def allergen_search(self):
          # Hide the main window
        self.withdraw()

        # Create a new toplevel window to display the selected allergens
        allergen_window = tk.Toplevel(self)
        x, y = self.winfo_x(), self.winfo_y()

        allergen_window.geometry(f"600x500+{x}+{y}")
        allergen_window.title("Selected Allergens")
        allergen_window.resizable(False,False)
        allergen_window.configure(bg="#2A3439")
        

        # Create a frame to hold the selected allergens label and back button
        allergen_frame = tk.Frame(allergen_window, borderwidth = 0)
        allergen_frame.configure(bg="#2A3439")
        allergen_frame.pack() 

        selected_allergens = [allergen for allergen in self.allergens if self.allergens[allergen].get()]
        allergen_str = ", ".join(selected_allergens)

        tk.Label(allergen_frame, font=(("Courier New Bold"), 10), text=f"Cocktails without: {allergen_str}", fg="#9F4576").place(x=10,y=10)

        tk.Button(allergen_frame, text="Back", font=(("Courier New Bold"), 10), command=lambda: self.back_to_main(allergen_window), fg="#E3DAC9", bg="#007EA7").place(x=10,y=50)

        can = tk.Canvas(allergen_frame, width=550, height=450, bg="#2A3439",borderwidth = 0,highlightthickness=0)
        can.pack(side="left", expand=1, fill = "both",pady=90)

        sb = tk.Scrollbar(allergen_frame, orient=tk.VERTICAL, command=can.yview,bg="#2A3439",borderwidth = 0)
        sb.pack(side="right", fill=tk.Y)

        can.configure(yscrollcommand=sb.set)
        can.yview_moveto(0)
        can.bind('<Configure>', lambda x: can.configure(scrollregion=can.bbox("all")))

        tframe = tk.Frame(can, width=550, height=450,borderwidth = 0)
        tframe.configure(bg="#2A3439")
        
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
                        "Sulphites" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Sulphites>",
                        "Tree Nuts" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#TreeNuts>"}

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
        

        for cock in acceptable:
            name = re.sub(r"(?<=\w)([A-Z])", r" \1",str(cock)[15:]).lower()

            ingredients = cock.comment[0]
            preperation = cock.comment[1]
            garnish = cock.comment[2]


            tk.Label(tframe, text=name, font=(("Courier New Bold"), 13), wraplength=220, justify="center", anchor="w").pack(pady=10)

            tk.Label(tframe, text=ingredients, font=(("Courier New Bold"), 10), wraplength=420, justify="center", anchor="w", bg="#2A3439").pack(pady=10)

            tk.Label(tframe, text=preperation, font=(("Courier New Bold"), 10), wraplength=420, justify="center", anchor="w", bg="#2A3439").pack(pady=10)

            tk.Label(tframe, text=garnish, font=(("Courier New Bold"), 10), wraplength=420, justify="center", anchor="w",bg="#2A3439").pack(pady=10)

            ttk.Separator(tframe, orient="horizontal").pack(fill="x",pady=10)


        can.create_window((0, 100), window=tframe)
        can.yview_moveto(50)

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
        advanced_window.geometry(f"600x500+{x}+{y}")
        advanced_window.title("Advanced Query")


        # Create a new frame to hold the advanced query interface
        advanced_frame = tk.Frame(advanced_window)
        advanced_frame.pack(padx=10, pady=10)


        # Add a label to the advanced query frame
        tk.Label(advanced_frame, text="Advanced Query", font=(("Courier New Bold"), 10), fg="#E3DAC9").pack(padx=10, pady=10)


        # Add a button to return to the main interface
        tk.Button(advanced_frame, text="Back", font=(("Courier New Bold"), 10), command=lambda: self.back_to_main(advanced_window), fg="#E3DAC9", bg="#007EA7").pack(pady=10)
        advanced_window.grab_set()


    def back_to_main(self, f):
        # Store the position of the advanced query window before it is closed
        x, y = f.winfo_x(), f.winfo_y()
        self.geometry(f"600x500+{x}+{y}")
        f.destroy()
        
        # Show the main window
        self.deiconify()


app = App()
app.resizable(False, False) 
app.mainloop()
