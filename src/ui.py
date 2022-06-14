import sys
import tkinter as tk
import tkcalendar as tkcal
import tkinter.messagebox
# program libraries
import server
import circuit

class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Set up window
        self.parent.geometry('700x380')
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
        self.variable = tk.StringVar()
        self.variable.set(circuits[0])
        self.type_drop = tk.OptionMenu(self, self.variable, *circuits)
        self.type_drop.place(x=120, y=115)
        # Length
        self.length_label = tk.Label(self, text="Experiment Length:\n(hours)",
                                justify=tk.LEFT)
        self.length_label.place(x=40, y=150)
        self.val = tk.StringVar()
        self.val.set("6")
        self.length_entry = tk.Entry(self, textvariable=self.val, width=10)
        self.length_entry.place(x=155, y=155)
        # Control
        self.label_control = tk.Label(self, text="Control:")
        self.label_control.place(x=40, y=200)
        t_f = ["Yes", "No"]
        self.variable2 = tk.StringVar()
        self.variable2.set(t_f[0])
        self.control_drop = tk.OptionMenu(self, self.variable2, *t_f)
        self.control_drop.place(x=145, y=190)
        # Doses
        self.num_doses_label = tk.Label(self, text="Number of Doses:")
        self.num_doses_label.place(x=40, y=230)
        num_doses = list(range(1,5))
        self.variable1 = tk.IntVar()
        self.variable1.set(num_doses[0])
        self.type_drop = tk.OptionMenu(self, self.variable1, *num_doses)
        self.type_drop.place(x=145, y=220)
        # Drug Names
        self.drugs_label = tk.Label(self, text="Add Drugs:")
        self.drugs_label.place(x=40, y=255)
        self.drug_name_label1 = tk.Label(self, text="- Full Name:")
        self.drug_name_label1.place(x=40, y=275)
        self.drug_name_label2 = tk.Label(self, text="- Abbreviation:")
        self.drug_name_label2.place(x=40, y=295)
        self.name_entry1 = tk.Entry(self, width=20)
        self.name_entry1.place(x=145, y=275)
        self.name_entry2 = tk.Entry(self, width=10)
        self.name_entry2.place(x=145, y=295)
        self.add_drug_button = tk.Button(self, text="Add", command=self.add_drug,
                                    height=1, width=10)
        self.add_drug_button.place(x=40,y=330)
        # Text box
        self.screen_box = tk.Text(self, height=14, width=45)
        self.screen_box.place(x=300, y=90)
        # Submit button
        self.submit_button = tk.Button(self, text="Run Circuit",
                                        command=self.run_circuit,
                                        height=1, width=20, bg='green')
        self.submit_button.place(x=395, y=330)

    # Adds drugs to dictionary and print to screen
    def add_drug(self):
        drug_name = self.name_entry1.get()
        drug_abbreviation = self.name_entry2.get()
        self.drugs[drug_abbreviation] = drug_name
        self.name_entry1.delete(0, 'end')
        self.name_entry2.delete(0, 'end')
        self.screen_box.delete(1.0, "end-1c")
        for abrv, drug in self.drugs.items():
            print_to_screen(self.screen_box, "Added {} ({})\n".format(drug, abrv))

    def run_circuit(self):
        # Get fields
        length = self.val.get()
        num_doses = self.variable1.get()
        compounds = self.drugs
        type = self.variable.get()
        control = True if self.variable2.get() == "Yes" else False
        date = self.date_cal.get_date()

        # Check entries
        print_to_screen(self.screen_box, "Checking entries...", delete=True)
        if not length.isnumeric():
            show_message('Circuit length must be numeric.')
            return
        if not compounds or '' in compounds:
            compounds.pop('', None)
            show_message('No drugs added.')
            return
        else:
            print_to_screen(self.screen_box, "passed.\n")

        # User check
        user_check = show_message("Please double check circuit. Do you wish to \
                                    continue?", type='question')
        if user_check == 'yes':
            new_circuit = circuit.Circuit(length, num_doses, compounds, type,
                                            control, date)
            message = "Creating new {} circuit...\n".format(new_circuit.type)
            print_to_screen(self.screen_box, message)
            print_to_screen(self.screen_box, new_circuit.print_circuit())
        else:
            return

def show_message(message, type='error'):
    if type == 'question':
        return tk.messagebox.askquestion('', message)
    else:
        tk.messagebox.showerror('Error', message)
    return

def print_to_screen(screen, message, delete=False):
    if delete:
        screen.delete(1.0, 'end-1c')
    screen.insert('end-1c', message)

def main():
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
