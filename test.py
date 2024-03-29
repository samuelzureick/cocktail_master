import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("400x300")

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
            "Celery": tk.BooleanVar(),
            "Crustaceans": tk.BooleanVar(),
            "Eggs": tk.BooleanVar(),
            "Fish": tk.BooleanVar(),
            "Gluten": tk.BooleanVar(),
            "Lupin": tk.BooleanVar(),
            "Milk": tk.BooleanVar(),
            "Molluscs": tk.BooleanVar(),
            "Mustard": tk.BooleanVar(),
            "Peanuts": tk.BooleanVar(),
            "Sesame": tk.BooleanVar(),
            "Soybeans": tk.BooleanVar(),
            "Sulphur dioxide and sulphites": tk.BooleanVar(),
        }
        for i, allergen in enumerate(self.allergens):
            tk.Checkbutton(allergens_frame, text=allergen, variable=self.allergens[allergen]).grid(row=i//2, column=i%2, sticky="w")

        # Create a button to initiate the allergen search
        tk.Button(self, text="Search Allergens", command=self.allergen_search).pack(pady=10)

    def search(self):
        query = self.search_entry.get()
        self.getQuery(query)

    def allergen_search(self):
        try:
            # Create a new frame to display the selected allergens
            self.allergen_frame = tk.Frame(self)
            self.allergen_frame.pack(padx=10, pady=10)

            # Add a label to display the selected allergens
            selected_allergens = [allergen for allergen in self.allergens if self.allergens[allergen].get()]
            allergen_str = ", ".join(selected_allergens)
            tk.Label(self.allergen_frame, text=f"Selected Allergens: {allergen_str}").pack(padx=10, pady=10)

            # Add a back button to return to the main interface
            tk.Button(self.allergen_frame, text="Back", command=self.back_to_main).pack(pady=10)

            # Hide the main window
            self.withdraw()
        except Exception as e:
            print(e)

    def back_to_main(self):
        # Remove the allergen frame and show the main window
        self.allergen_frame.destroy()
        self.deiconify()

    def getQuery(self, query):
        # Do something with the query here
        print(f"Query: {query}")

app = App()
app.mainloop()
