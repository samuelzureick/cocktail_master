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
            tk.Checkbutton(allergens_frame, bg="#2A3439", text=allergen,font=(("Courier New Bold"), 10), variable=self.allergens[allergen], fg="#E3DAC9").grid(
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
        self.advanced_window.withdraw()

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


        can.create_window((0, 100), window=tframe)
        can.yview_moveto(0)

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

        # Add a label to the advanced query frame
        advl = tk.Label(advanced_frame, text="Advanced Query", font=(("Courier New Bold"), 10), fg="#9F4576")
        advl.place(x=20, y=20)
        # Add a button to return to the main interface
        bb = tk.Button(advanced_frame, text="Back", font=(("Courier New Bold"), 10), command=lambda: self.back_to_main(self.advanced_window), fg="#E3DAC9", bg="#007EA7")
        bb.place(x=20, y=55)

        
        adv_can = tk.Canvas(advanced_frame, width=550, height=450, bg="#2A3439",borderwidth = 0,highlightthickness=0)
        adv_can.place(x=0,y=100)
        subf=tk.Frame(adv_can, width=550, height=450, borderwidth=0, highlightthickness=0,bg="#2A3439")

        def add_filter():
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

            t = ttk.Menubutton(subf, textvariable=contains_v)
            drop = tk.Menu(t, tearoff=False)
            drop.add_radiobutton(label="contains", value="contains", variable=contains_v, command=lambda: contains_v.get())
            drop.add_radiobutton(label="omits", value="omits", variable=contains_v, command=lambda : contains_v.get())
            drop.configure(font=(("Courier New Bold"),10))
            t["menu"] = drop

            ingal = ttk.Menubutton(subf, textvariable=ioa)
            dropioa = tk.Menu(ingal, tearoff=False)
            dropioa.add_radiobutton(label="ingredient", value="ingredient",variable=ioa, command = display_drop)
            dropioa.add_radiobutton(label="allergen", value="allergen", variable=ioa, command = display_drop)
            dropioa.configure(font=(("Courier New Bold"), 10))
            ingal["menu"] = dropioa

            filt = ttk.Menubutton(subf, textvariable=ing)
            almenu = tk.Menu(filt, tearoff=False)
            almenu.configure(font=(("Courier New Bold"), 10))
            for a in list(self.allergens.keys()):
                almenu.add_radiobutton(label=a, value=a, variable=ing, command = ing.get())

            ingmenu = tk.Menu(filt, tearoff=False)
            ingmenu.configure(font=(("Courier New Bold"), 10))
            for i in ing_names:
                ingmenu.add_radiobutton(label=i, value=i, variable=ing, command = ing.get())

            t.place(x=0,y=0+(self.rowc*65))
            ingal.place(x=120, y=0+(self.rowc*65))
            filt.place(x=240, y=0+(self.rowc*65))
            #self.clist.append(t)
            self.rowc += 1
 
        add_filter()

        # add submit button
        sb = tk.Button(advanced_frame, text="search", font=(("Courier New Bold"),10), command=lambda: self.query_results(), fg="#E3DAC9", bg="#007EA7")
        sb.place(x=200, y=55)

        addbut = tk.Button(advanced_frame, text="add filter", font=(("Courier New Bold"), 10),bg="#377771", fg="#E3DAC9", command=lambda : add_filter())

        addbut.place(x=85, y=55)
        adv_can.create_window((300, 250), window=subf, anchor="center")

        self.advanced_window.grab_set()
        self.advanced_window.resizable(False, False)

    def query_results(self):
        # Hide the main window
        self.withdraw()
        self.advanced_window.withdraw()

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

        final = sorted([re.sub(r"(?<=\w)([A-Z])", r" \1",str(cockt)[15:]).lower() for cockt in list(available)])
        print(final)

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
