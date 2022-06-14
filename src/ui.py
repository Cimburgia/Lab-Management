import sys
import tkinter as tk
import pandas as pd
import tkcalendar as tkcal
# program libraries
import server
import circuit

class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Set up window
        self.parent.geometry('600x380')
        self.parent.title('Lab-Manager')
        # Initiate lists
        self.drugs = {}
        # Build label and entry widgets
        self.label = tk.Label(self, text="Please fill out the following information:")
        self.label.place(x=40, y=30)
        # Calendar
        self.date_label = tk.Label(self, text="Circuit Date:")
        self.date_label.place(x=40, y=90)
        self.date_cal = tkcal.DateEntry(self, selectmode='day')
        self.date_cal.place(x=120, y=90)
        # Circuit type
        self.type_label = tk.Label(self, text="Circuit Type:")
        self.type_label.place(x=40, y=120)
        circuits = ['ECMO','CRRT','ECMO and CRRT','Sepcialized Controls']
        variable = tk.StringVar()
        variable.set(circuits[0])
        self.type_drop = tk.OptionMenu(self, variable, *circuits)
        self.type_drop.place(x=120, y=115)
        # Length
        self.length_label = tk.Label(self, text="Experiment Length:\n(hours)",
                                justify=tk.LEFT)
        self.length_label.place(x=40, y=150)
        self.length_entry = tk.Entry(self, width=10)
        self.length_entry.place(x=155, y=155)
        # Doses
        self.num_doses_label = tk.Label(self, text="Number of Doses:")
        self.num_doses_label.place(x=40, y=190)
        num_doses = list(range(1,5))
        variable1 = tk.IntVar()
        variable1.set(num_doses[0])
        self.type_drop = tk.OptionMenu(self, variable1, *num_doses)
        self.type_drop.place(x=145, y=185)
        # Drug Names
        self.drugs_label = tk.Label(self, text="Add Drugs:")
        self.drugs_label.place(x=40, y=220)
        self.drug_name_label1 = tk.Label(self, text="- Full Name:")
        self.drug_name_label1.place(x=40, y=240)
        self.drug_name_label2 = tk.Label(self, text="- Abbreviation:")
        self.drug_name_label2.place(x=40, y=260)
        self.name_entry1 = tk.Entry(self, width=20)
        self.name_entry1.place(x=145, y=240)
        self.name_entry2 = tk.Entry(self, width=10)
        self.name_entry2.place(x=145, y=260)
        self.add_drug_button = tk.Button(self, text="Add", command=self.add_drug,
                                    height=1, width=10)
        self.add_drug_button.place(x=40,y=295)
        # Text box
        self.screen_box = tk.Text(self, height=14, width=35)
        self.screen_box.place(x=300, y=90)
        # Submit button
        self.submit_button = tk.Button(self, text="Run Circuit",
                                        command=self.run_circuit,
                                        height=1, width=20, bg='green')
        self.submit_button.place(x=360, y=330)

    # Adds drugs to dictionary and
    def add_drug(self):
        drug_name = self.name_entry1.get()
        drug_abbreviation = self.name_entry2.get()
        self.drugs[drug_abbreviation] = drug_name
        self.name_entry1.delete(0, 'end')
        self.name_entry2.delete(0, 'end')
        self.screen_box.delete(1.0, "end-1c")
        for abrv, drug in self.drugs.items():
            self.screen_box.insert("end-1c", "{} ({})\n".format(drug, abrv))

    def run_circuit(self):
        print("Hi Travis!")

def main():
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
