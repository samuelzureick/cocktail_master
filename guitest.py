import difflib
import tkinter as tk
from ast import literal_eval
from tkinter import *
from tkinter import font, ttk

import owlready2
import PIL
from owlready2 import *
from PIL import Image, ImageShow, ImageTk

ImageShow.WindowsViewer.format = "PNG"


owlready2.JAVA_EXE = "C:\\Users\\szure\\Documents\\Protege-5.5.0\\jre\\bin\\java.exe"
onto = get_ontology("cocktailRefact.owl")
onto.load()

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
        self.rowc=0
        self.flist = []
        self.slist = []
        self.tlist = []


        # Create a frame for the search bar
        search_frame = tk.Frame(self, borderwidth = 0)
        search_frame.pack(side="top", fill="x", padx=10, pady=10)
        search_frame.configure(bg="#2A3439")

        
        # Create a label and entry widget for the search bar
        titleText = ImageTk.PhotoImage(Image.open("finalb.PNG"))
        l1 = tk.Label(search_frame, image=titleText,borderwidth = 0)
        l1.image = titleText
        l1.pack(side="top", anchor="nw")

        #add label to explain the allergen search thing 
        tk.Label(self, text="Filter for cocktails omitting: ", font=(("Courier New Bold"),10 ),fg="#9F4576", bg="#2A3439").place(x=10,y=165)
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

        self.allergen_dict = {"Celery" : "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Celery>",
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

        for i, allergen in enumerate(self.allergens):
            tk.Checkbutton(allergens_frame, selectcolor="#304C53", bg="#2A3439", text=allergen,font=(("Courier New Bold"), 10), variable=self.allergens[allergen], fg="#E3DAC9").grid(
                row=i // 2, column=i % 2, sticky="w")


        # Create a button to initiate the allergen search
        tk.Button(allergens_frame, text="search allergens", command=self.allergen_search, bg="#377771", fg="#E3DAC9", font=(("Courier New Bold"), 10)).grid(row=8, column=0)


        # Create a button to switch to the advanced query section
        tk.Button(allergens_frame, text="advanced query", font=(("Courier New Bold"), 10), command=self.advanced_query, bg="#377771", fg="#E3DAC9").grid(row=8, column=1, padx=5)

        # create custom menu button
        tk.Button(self, text="menu generator", font=(("Courier New Bold"), 10), command=self.menugen, bg="#377771", fg="#E3DAC9").place(x=10, y=420)


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
        self.cocktail_listbox.config(yscrollcommand=scrollbar.set, width=50,bg="#2A3439", font=(("Courier New Bold"), 10),fg="#E3DAC9")
        scrollbar.config(command=self.cocktail_listbox.yview)
        self.cocktail_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)


        # Load data into the listbox
        self.load_cocktails()

        # Create a filter label and entry widget for the listbox
        tk.Label(filter_frame, text="filter cocktails:", font=(("Courier New Bold"), 10)).pack(side="left")
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
        
    def menugen(self):
        # Hide the main window
        self.withdraw()
        self.advanced_window.withdraw

        acceptable_spirits = [
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Mezcal>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Tequila>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Calvados>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#AppleJack>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Armagnac>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cognac>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Grappa>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Pisco>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Genever>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#LondonDryGin>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#OldTomGin>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Baijiu>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cachaca>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#BataviaArrack>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Rum>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#OverproofRum>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#DarkRum>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Dairy>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#BlackStrapRum>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#DemeraraRum>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#RhumAgricole>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Vodka>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Bourbon>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#rye>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#IrishWhiskey>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Scotch>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#IslayScotch>",
                            "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#BlendedScotch>"]
        available = set([inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                    { 
                        ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cocktail> .
                    }""")) for inner in outer])

        for i in range(len(self.flist)):
            print(self.ing_dict[self.tlist[i].get()])
            results = set([inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                { 
                    ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cocktail> .
                    ?x rdfs:subClassOf [a owl:Restriction ; owl:onProperty <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#contains> ; owl:someValuesFrom ?y] .
                    ?y (owl:equivalentClass|^owl:equivalentClass)* """+self.ing_dict[self.tlist[i].get()]+""" . 
                }""")) for inner in outer])
            if self.flist[i].get() == "contains":
                available = available & results
            elif self.flist[i].get() == "omits":
                available = available - results


        # Create a new toplevel window to display the advanced query
        self.q_window = tk.Toplevel(self)
        x, y = self.winfo_x(), self.winfo_y()
        self.q_window.geometry(f"600x500+{x}+{y}")
        self.q_window.title("Advanced Query")


        # Create a new frame to hold the advanced query interface
        q_frame = tk.Frame(self.q_window, bg="#2A3439", width="550", height="450")
        q_frame.pack(padx=10, pady=10, fill="both", expand=True)


        # Add a label to the advanced query frame
        ql = tk.Label(q_frame, text="Advanced Query", font=(("Courier New Bold"), 10), fg="#9F4576")
        ql.place(x=20, y=20)
        # Add a button to return to the main interface
        bb = tk.Button(q_frame, text="Back", font=(("Courier New Bold"), 10), command=lambda: self.advanced_query(), fg="#E3DAC9", bg="#007EA7")
        bb.place(x=20, y=55)

        
        q_can = tk.Canvas(q_frame, width=550, height=450, bg="#2A3439",borderwidth = 0,highlightthickness=0)
        q_can.place(x=0,y=100)
        subf=tk.Frame(q_can, width=550, height=450, borderwidth=0, highlightthickness=0,bg="#2A3439")


        q_can.create_window((300, 250), window=subf, anchor="center")

        self.q_window.grab_set()
        self.q_window.resizable(False, False)


    def allergen_search(self):
          # Hide the main window
        self.withdraw()

        def findDrinks():            
            acceptable = set([inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                    { 
                        ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cocktail> .
                    }""")) for inner in outer])

            for aller in selected_allergens:
                avoid = self.allergen_dict[aller]
                
                bad = set([inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                    { 
                        ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cocktail> .
                        ?x rdfs:subClassOf [a owl:Restriction ; owl:onProperty <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#contains> ; owl:someValuesFrom ?y] .
                        ?y (owl:equivalentClass|^owl:equivalentClass)* """+avoid+""" . 
                    }""")) for inner in outer])

                acceptable -= bad
            
            if list(acceptable) == []:
                tk.Label(tframe, text="No matching cocktails found...", font=(("Courier New Bold"), 10,), wraplength=420, justify="center", bg="#2A3439",fg="#E3DAC9").pack(pady=10)
            for cock in acceptable:
                name = re.sub(r"(?<=\w)([A-Z])", r" \1",str(cock)[15:]).lower()

                ingredients = cock.comment[0]
                preperation = cock.comment[1]
                garnish = cock.comment[2]

                tk.Label(tframe, text=name, font=(("Courier New Bold"), 13), wraplength=220, justify="center", anchor="w").pack(pady=10)

                tk.Label(tframe, text=ingredients, font=(("Courier New Bold"), 10), wraplength=420, justify="center", anchor="w", bg="#2A3439",fg="#E3DAC9").pack(pady=10)

                tk.Label(tframe, text=preperation, font=(("Courier New Bold"), 10), wraplength=420, justify="center", anchor="w", bg="#2A3439",fg="#E3DAC9").pack(pady=10)

                tk.Label(tframe, text=garnish, font=(("Courier New Bold"), 10), wraplength=420, justify="center", anchor="w",bg="#2A3439",fg="#E3DAC9").pack(pady=10)

                ttk.Separator(tframe, orient="horizontal").pack(fill="x",pady=10)

            sb = tk.Scrollbar(allergen_frame, orient="vertical")
            sb.configure(command=can.yview)

            sb.pack(side="right", fill="y")
            can.configure(scrollregion=can.bbox("all"))
            can.configure(yscrollcommand=sb.set)
            can.bind('<Configure>', lambda x: can.configure(scrollregion=can.bbox("all")))
            allergen_frame.bind("<Configure>", lambda event: can.configure(scrollregion=allergen_frame.bbox("all")))

            can.create_window((250, 300), window=tframe, anchor="n")
            x, y = self.winfo_x(), self.winfo_y()
            allergen_window.geometry(f"600x501+{x}+{y}")
            ldl.place_forget()
            can.yview_moveto(0)

            

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


        tframe = tk.Frame(can,bg="#2A3439")
        ldl = tk.Label(allergen_frame, text="Loading Query Results...", font=(("Courier New Bold"), 10), fg="#9F4576")
        ldl.place(x=200,y=250)

        self.after(1000, findDrinks)

        # Prevent interaction with the main window while the allergen window is open
        allergen_window.grab_set()

    def advanced_query(self):
        # Hide the main window
        x, y = self.winfo_x(), self.winfo_y()
        self.withdraw()
        try:
            self.q_window.withdraw()
        except:
            pass
        self.flist = []
        self.slist = []
        self.tlist = []
        self.rowc = 0
        ing_list = [inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                    { 
                        ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Ingredient> .
                    }""")) for inner in outer]
        self.ing_dict = {}
        for i in ing_list:
            self.ing_dict[re.sub(r"(?<=\w)([A-Z])", r" \1",str(i)[15:]).lower()] = "<http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#"+(str(i)[15:])+">"

        ing_names = sorted([re.sub(r"(?<=\w)([A-Z])", r" \1",str(cock)[15:]).lower() for cock in ing_list])

        allergen_list = list(self.allergens.keys())

        # Create a new toplevel window to display the advanced query
        self.advanced_window = tk.Toplevel(self)
        
        self.advanced_window.geometry(f"600x500+{x}+{y}")
        self.advanced_window.title("Advanced Query")

        # Create a new frame to hold the advanced query interface
        advanced_frame = tk.Frame(self.advanced_window, bg="#2A3439", width="550", height="450")
        advanced_frame.pack(padx=10, pady=10, fill="both", expand=True)

        
        adv_can = tk.Canvas(advanced_frame, width=550, height=450, bg="#2A3439",borderwidth = 0,highlightthickness=0)
        adv_can.place(x=0,y=0)
        subf=tk.Frame(adv_can, borderwidth=0, highlightthickness=0,bg="#2A3439")
        adv_can.create_window((230, 100), window=subf, anchor="n")

        # need to modify this to add frames to canvas subframe so that i can scroll and pack these elements!!!!!
        def add_filter():
            self.advanced_window.grab_set()
            if self.rowc>=7:
                addbut.config(bg="grey")
                return
            ssf = tk.Frame(subf, borderwidth=0, highlightthickness=0, height=30, width=400, bg="#2A3439")

            adv_can.configure(scrollregion=subf.bbox("all"))
            adv_can.bind('<Configure>', lambda x: adv_can.configure(scrollregion=subf.bbox("all")))

            adv_can.config(yscrollcommand=self.scroll.set)
            self.scroll.config(command=adv_can.yview)

            contains_v = tk.StringVar()
            contains_v.set("contains/omits")
            ioa = tk.StringVar()
            ioa.set("select an option")
            ing = tk.StringVar()
            ing.set("")
            self.flist.append(contains_v)
            self.slist.append(ioa)
            self.tlist.append(ing)


            def display_drop():
                if ioa.get() == "ingredient":
                    ing.set("select an ingredient")
                    filt["menu"] = ingmenu
                    return ioa.get()
                elif ioa.get() == "allergen":
                    ing.set("select an allergen")
                    filt["menu"] = almenu

            t = ttk.Menubutton(ssf, textvariable=contains_v)
            drop = tk.Menu(t, tearoff=False)
            drop.add_radiobutton(label="contains", value="contains", variable=contains_v, command=lambda: contains_v.get())
            drop.add_radiobutton(label="omits", value="omits", variable=contains_v, command=lambda : contains_v.get())
            drop.configure(font=(("Courier New Bold"),10))
            t["menu"] = drop

            ingal = ttk.Menubutton(ssf, textvariable=ioa)
            dropioa = tk.Menu(ingal, tearoff=False)
            dropioa.add_radiobutton(label="ingredient", value="ingredient",variable=ioa, command = display_drop)
            dropioa.add_radiobutton(label="allergen", value="allergen", variable=ioa, command = display_drop)
            dropioa.configure(font=(("Courier New Bold"), 10))
            ingal["menu"] = dropioa

            filt = ttk.Menubutton(ssf, textvariable=ing)
            almenu = tk.Menu(filt, tearoff=False)
            almenu.configure(font=(("Courier New Bold"), 10))
            for a in list(self.allergens.keys()):
                almenu.add_radiobutton(label=a, value=a, variable=ing, command = ing.get())

            ingmenu = tk.Menu(filt, tearoff=False)
            ingmenu.configure(font=(("Courier New Bold"), 10))
            for i in ing_names:
                ingmenu.add_radiobutton(label=i, value=i, variable=ing, command = ing.get())

            t.place(x=0,y=0)
            ingal.place(x=120, y=0)
            filt.place(x=240, y=0)
            #self.clist.append(t)
            ssf.pack(pady=10)
            self.rowc += 1
            adv_can.configure(yscrollcommand=self.scroll.set)
            adv_can.bind('<Configure>', lambda x: adv_can.configure(scrollregion=adv_can.bbox("all")))
            subf.bind('<Configure>', lambda x: adv_can.configure(scrollregion=adv_can.bbox("all")))

            self.scroll.configure(command=adv_can.yview)
            adv_can.yview_moveto(0)

        
        self.scroll = tk.Scrollbar(advanced_frame)
        self.scroll.pack(side="right", fill="y")
        adv_can.config(yscrollcommand=self.scroll.set)
        adv_can.bind('<Configure>', lambda x: adv_can.configure(scrollregion=adv_can.bbox("all")))
        advanced_frame.bind('<Configure>', lambda x: adv_can.configure(scrollregion=advanced_frame.bbox("all")))

        self.scroll.config(command=adv_can.yview)
        adv_can.yview_moveto(0)

        add_filter()
        
        def validate_query():
            if len(["" for t in self.tlist if t.get() == ""]) > 0:
                errorWindow = tk.Toplevel(self, bg="#2A3439")
                errorWindow.title("Query Error")
                errorWindow.geometry("350x120")
                errorWindow.resizable(False,False)
                tk.Label(errorWindow, text="search error:\nmissing ingredient/ allergen selection", font=(("Courier New Bold"), 10), bg="#2A3439", fg="#E3DAC9").pack(pady=10)
                tk.Button(errorWindow, text="Dismiss", command= lambda: errorWindow.destroy(), font=(("Courier New Bold"), 10), bg="#377771", fg="#E3DAC9").pack(pady=10)
                errorWindow.grab_set()
            elif len(["" for f in self.flist if f.get() == "contains/omits"]) > 0:
                errorWindow = tk.Toplevel(self, bg="#2A3439")
                errorWindow.title("Query Error")
                errorWindow.geometry("350x120")
                errorWindow.resizable(False,False)
                tk.Label(errorWindow, text="Search error:\ncontain/omit selection not complete", font=(("Courier New Bold"), 10), bg="#2A3439", fg="#E3DAC9").pack(pady=10)
                tk.Button(errorWindow, text="Dismiss", command= lambda: errorWindow.destroy()).pack(pady=10)
                errorWindow.grab_set()
            else:
                self.query_results()

        # add submit button
        sb = tk.Button(advanced_frame, text="search", font=(("Courier New Bold"),10), command=lambda: validate_query(), fg="#E3DAC9", bg="#377771")
        sb.place(x=200, y=55)

        addbut = tk.Button(advanced_frame, text="add filter", font=(("Courier New Bold"), 10),bg="#377771", fg="#E3DAC9", command=lambda : add_filter())
        # Add a label to the advanced query frame
        advl = tk.Label(advanced_frame, text="Advanced Query", font=(("Courier New Bold"), 10), fg="#9F4576")
        advl.place(x=20, y=20)
        # Add a button to return to the main interface
        bb = tk.Button(advanced_frame, text="Back", font=(("Courier New Bold"), 10), command=lambda: self.back_to_main(self.advanced_window), fg="#E3DAC9", bg="#007EA7")
        bb.place(x=20, y=55)

        addbut.place(x=85, y=55)

        self.advanced_window.grab_set()
        self.advanced_window.resizable(False, False)
    

    def query_results(self):
        def display_results():
            scrollbar = tk.Scrollbar(q_frame, orient="vertical")
            scrollbar.pack(side="right", fill="y")
            q_can.configure(scrollregion=q_can.bbox("all"))
            q_can.configure(yscrollcommand=scrollbar.set)
            scrollbar.configure(command=q_can.yview)
            q_can.bind('<Configure>', lambda x: q_can.configure(scrollregion=q_can.bbox("all")))
            q_frame.bind("<Configure>", lambda event: q_can.configure(scrollregion=q_can.bbox("all")))
                
            q_can.create_window((300, 250), window=subf, anchor="n")

            x, y = self.winfo_x(), self.winfo_y()
            self.q_window.geometry(f"600x501+{x}+{y}")
            if self.final==[]:
                tk.Label(subf, text="No matching cocktails found...", font=(("Courier New Bold"), 10,), wraplength=420, justify="center", bg="#2A3439",fg="#E3DAC9").pack(pady=10)
            else:
                for cock in self.final:
                    name = re.sub(r"(?<=\w)([A-Z])", r" \1",str(cock)[15:]).lower()

                    ingredients = cock.comment[0]
                    preperation = cock.comment[1]
                    garnish = cock.comment[2]

                    tk.Label(subf, text=name, font=(("Courier New Bold"), 13), wraplength=220, justify="center", anchor="w").pack(pady=10)

                    tk.Label(subf, text=ingredients, font=(("Courier New Bold"), 10), wraplength=420, justify="center", anchor="w", bg="#2A3439",fg="#E3DAC9").pack(pady=10)

                    tk.Label(subf, text=preperation, font=(("Courier New Bold"), 10), wraplength=420, justify="center", anchor="w", bg="#2A3439",fg="#E3DAC9").pack(pady=10)

                    tk.Label(subf, text=garnish, font=(("Courier New Bold"), 10), wraplength=420, justify="center", anchor="w",bg="#2A3439",fg="#E3DAC9").pack(pady=10)

                    ttk.Separator(subf, orient="horizontal").pack(fill="x",pady=10)



            


        def get_results():
            available = set([inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                        { 
                            ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cocktail> .
                        }""")) for inner in outer])

            for i in range(len(self.flist)):
                if self.slist[i].get() == "ingredient":
                    v = self.ing_dict[self.tlist[i].get()]
                elif self.slist[i].get() == "allergen":
                    v = self.allergen_dict[self.tlist[i].get()]
                results = set([inner for outer in list(graph.query_owlready("""SELECT ?x WHERE 
                    { 
                        ?x rdfs:subClassOf+ <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#Cocktail> .
                        ?x rdfs:subClassOf [a owl:Restriction ; owl:onProperty <http://www.semanticweb.org/szure/ontologies/2023/1/untitled-ontology-3#contains> ; owl:someValuesFrom ?y] .
                        ?y (owl:equivalentClass|^owl:equivalentClass)* """+v+""" . 
                    }""")) for inner in outer])
                if self.flist[i].get() == "contains":
                    available = available & results
                elif self.flist[i].get() == "omits":
                    available = available - results

            self.final = list(available)
            print(self.final)
            display_results()
            q_can.yview_moveto(0.0)



        # Hide the main window
        self.withdraw()
        self.advanced_window.withdraw()
        self.final = []

        # Create a new toplevel window to display the advanced query
        self.q_window = tk.Toplevel(self)
        x, y = self.winfo_x(), self.winfo_y()
        self.q_window.geometry(f"600x500+{x}+{y}")
        self.q_window.title("Advanced Query Results")


        # Create a new frame to hold the advanced query interface
        q_frame = tk.Frame(self.q_window, bg="#2A3439")
        q_frame.pack(padx=10, pady=10, fill="both", expand=True)


        # Add a label to the advanced query frame
        ql = tk.Label(q_frame, text="Advanced Query Results", font=(("Courier New Bold"), 10), fg="#9F4576")
        ql.place(x=20, y=20)
        # Add a button to return to the main interface
        bb = tk.Button(q_frame, text="Back", font=(("Courier New Bold"), 10), command=lambda: self.advanced_query(), fg="#E3DAC9", bg="#007EA7")
        bb.place(x=20, y=55)

        
        q_can = tk.Canvas(q_frame, width=550, height=350, bg="#2A3439",borderwidth = 0,highlightthickness=0)
        subf=tk.Frame(q_can, borderwidth=0, highlightthickness=0, bg="#2A3439")
        q_can.place(x=0,y=100)


        #ld = tk.Label(subf, text="LOADING QUERY RESULTS...", font=(("Courier New Bold"), 10), fg="#2A3439").pack()
        self.q_window.grab_set()
        self.q_window.resizable(False, False)
        self.after(100,lambda: get_results())

        
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
