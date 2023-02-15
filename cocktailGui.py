import tkinter as tk
from tkinter import *
from owlready2 import *
import owlready2
from ast import literal_eval
import difflib


owlready2.JAVA_EXE = "C:\\Users\\szure\\Downloads\\Protege-5.5.0-win\\Protege-5.5.0\\jre\\bin\\java.exe"
onto_path.append(".")
onto = get_ontology("cocktailmaster.owl")
onto.load()
with onto:
	sync_reasoner_pellet()

cocktails = onto.get_children_of(onto.cocktail)
allergens = onto.get_children_of(onto.major_allergen)

cocktail_names = [str(cock)[15:] for cock in cocktails]
allergen_names = [str(aller)[15:] for aller in allergens]

print(cocktail_names)
print(allergen_names)

class mainApp(tk.Tk):
    tk.Tk.__init__(self, *args, **kwargs)

    self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

    # the container is where we'll stack a bunch of frames
    # on top of each other, then the one we want visible
    # will be raised above the others
    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.frames = {}
    for F in (MainPage, SearchResults, PageTwo):
        page_name = F.__name__
        frame = F(parent=container, controller=self)
        self.frames[page_name] = frame

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Main")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def getQuery():
            term = entry.get()
            if term == "":
                res["text"] = "No input given!"
                res["fg"] = "black"
                res["bg"] = "red",
            else:
                found = difflib.get_close_matches(term, cocktail_names)
                print(found)
                if found:
                    res["text"] = "Found: " +" ".join(found)
                    res["fg"] = "black"
                    res["bg"] = "green"

                else:
                    res["text"] = ("Search term: " +term + " not found")
                    res["bg"] = "red"

        def allergenQuery():
            allergen_query = {
               "celery" : celery.get() == 1,
                "dairy" : dairy.get() == 1,
                "eggs" : eggs.get() == 1,
                "gluten" : gluten.get() == 1,
                "peanuts" : peanuts.get() == 1,
                "sulphites" : sulphites.get() == 1,
                "tree_nuts" : tree_nuts.get() == 1
            }
            contains = []
            for k in allergen_query.keys():
                if allergen_query[k]:
                    contains.append(k)
            allergen_containing_cocktails = []
            q ="""SELECT ?cocktail ?y
                    WHERE { ?cocktail rdfs:subClassOf ?? .
                            ?y rdfs:subClassOf ?? .
                    }"""
            
            p = [onto.cocktail, onto.allergen]
            print(list(default_world.sparql(q, p)))



        title = tk.Label(
            text="Cocktail Master", 
            fg="red",
            width=50,
            height=5)
        title.grid(row=0, column=0, sticky=W, pady=1)

        aller = tk.Label(
            text="search by allergen",
            fg="blue",
            width=50,
            height=5
        )
        aller.grid(row=0, column=1, sticky=W, pady=1)

        entry = tk.Entry(fg="yellow", bg="blue", width=50)
        entry.grid(row=1, column=0, sticky=W, pady=2)

        button = tk.Button(
            text="search for ingredient",
            width=50,
            height=3,
            bg="green",
            fg="black",
            command=getQuery
        )
        button.grid(row=2, column = 0, sticky = W, pady=2)

        res = tk.Label(text="",height=5, width=50)
        res.grid(row=3, column = 0, sticky = N, pady=2)

        allergenFrame = Frame(window)
        allergenFrame.grid(row=2, column=1)
        celery = IntVar()
        Checkbutton(allergenFrame ,text="Celery", variable=celery).grid(row=0, sticky=W)
        dairy = IntVar()
        Checkbutton(allergenFrame ,text="dairy", variable=dairy).grid(row=1, sticky=W)
        eggs = IntVar()
        Checkbutton(allergenFrame ,text="eggs", variable=eggs).grid(row=2, sticky=W)
        gluten = IntVar()
        Checkbutton(allergenFrame ,text="gluten", variable=gluten).grid(row=3, sticky=W)
        peanuts = IntVar()
        Checkbutton(allergenFrame ,text="peanuts", variable=peanuts).grid(row=4, sticky=W)
        sulphites = IntVar()
        Checkbutton(allergenFrame ,text="sulphites", variable=sulphites).grid(row=5, sticky=W)
        tree_nuts = IntVar()
        Checkbutton(allergenFrame ,text="tree nuts", variable=tree_nuts).grid(row=6, sticky=W)
        Button(allergenFrame, text="Find", command=allergenQuery).grid(row=7, sticky=W)
