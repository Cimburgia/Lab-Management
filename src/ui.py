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
        self.parent.geometry('720x420')
        self.parent.title('Lab-Manager')
        # Initiate lists
        self.drugs = {}
        # Build label and entry widgets
        self.label = tk.Label(self, text="Please fill out the following information:")
        self.label.place(x=40, y=30)
        # Calendar
        self.date_label = tk.Label(self, text="Circuit Date:")
        self.date_label.place(x=40, y=60)
        self.date_cal = tkcal.DateEntry(self, selectmode='day')
        self.date_cal.place(x=120, y=60)
        # Circuit Number
        self.number_label = tk.Label(self, text="Circuit Number:")
        self.number_label.place(x=40, y=90)
        self.circuit_num_var = tk.StringVar()
        self.circuit_num_var.set("1")
        self.number_entry = tk.Entry(self,
                                    textvariable=self.circuit_num_var, width=10)
        self.number_entry.place(x=135, y=90)
        # Circuit type
        self.type_label = tk.Label(self, text="Circuit Type:")
        self.type_label.place(x=40, y=120)
        circuits = ['ECMO','CRRT']
        self.type_var = tk.StringVar()
        self.type_var.set(circuits[0])
        self.type_drop = tk.OptionMenu(self, self.type_var, *circuits)
        self.type_drop.place(x=120, y=115)
        # Length
        self.length_label = tk.Label(self, text="Experiment Length:\n(hours)",
                                justify=tk.LEFT)
        self.length_label.place(x=40, y=150)
        self.length_var = tk.StringVar()
        self.length_var.set("6")
        self.length_entry = tk.Entry(self, textvariable=self.length_var, width=10)
        self.length_entry.place(x=155, y=155)
        # Sample time points
        self.timepoints_label = tk.Label(self, text="Timepoints:")
        self.timepoints_label.place(x=40, y=190)
        self.timepoints_button = tk.Button(self, text="Check", width=10,
                                            command=self.check_timepoints)
        self.timepoints_button.place(x=115, y=190)
        self.timepoints_dict = self.get_timepoints()
        # Control
        self.label_control = tk.Label(self, text="Control:")
        self.label_control.place(x=40, y=230)
        t_f = ["Yes", "No"]
        self.control_var = tk.StringVar()
        self.control_var.set(t_f[0])
        self.control_drop = tk.OptionMenu(self, self.control_var, *t_f)
        self.control_drop.place(x=100, y=220)
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
        self.screen_box = tk.Text(self, height=21, width=50)
        self.screen_box.place(x=300, y=60)
        # Submit button
        self.submit_button = tk.Button(self, text="Run Circuit",
                                        command=self.run_circuit,
                                        height=1, width=20, bg='green')
        self.submit_button.place(x=40, y=375)

    # Populate, check timepoints
    def get_timepoints(self):
        timepoints = {1:"1 min", 2:"5 min", 3:"15 min", 4:"30 min", 5:"1 hr",
                        6:"2 hr", 7:"3 hr", 8:"4 hr", 9:"5 hr",
                        10:"6 hr"}
        end = self.length_var.get()

        if end == "8":
            timepoints.update({11:"8 hr"})
        elif end == "10":
            timepoints.update({11:"8 hr",12:"10 hr"})
        elif end == "24":
            timepoints.update({11:"8 hr", 12:"24 hr"})

        return timepoints


    def check_timepoints(self):
        print_to_screen(self.screen_box, "Please edit and confirm timepoints:\n",
                        delete=True)
        self.timepoints_button.config(text="Confirm")
        self.timepoints_dict = self.get_timepoints()
        self.timepoints_button.config(command=self.add_timepoints)
        tps = print_dict(self.timepoints_dict)
        print_to_screen(self.screen_box, tps)

    def add_timepoints(self):
        tps = self.screen_box.get("1.0",'end-1c')
        tps = tps.split("\n")

        try:
            for t in tps[1:]:
                if t:
                    temp = t.split(':')
                    self.timepoints_dict[int(temp[0])] = temp[1]
        except:
            show_message("Must maintain sample#:timepoint format")
        else:
            print_to_screen(self.screen_box, "Timepoints confirmed!", delete=True)
            self.timepoints_button.config(text="Check")
            self.timepoints_button.config(command=self.check_timepoints)

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
        length = self.length_var.get()
        circuit_num = self.circuit_num_var.get()
        timepoints = self.timepoints_dict
        compounds = self.drugs
        type = self.type_var.get()
        control = True if self.control_var.get() == "Yes" else False
        date = self.date_cal.get_date()

        # Check entries
        print_to_screen(self.screen_box, "Checking entries...", delete=True)
        if not length.isnumeric():
            show_message('Circuit length must be numeric.')
            return
        if not circuit_num.isnumeric():
            show_message('Circuit number must be numeric.')
            return
        if not compounds or '' in compounds:
            compounds.pop('', None)
            show_message('No drugs added.')
            return
        else:
            print_to_screen(self.screen_box, "passed.\n")

        # User check
        new_circuit = circuit.Circuit(circuit_num, length, timepoints, compounds,
                                        type, control, date)
        print_to_screen(self.screen_box, new_circuit.print_circuit(), delete=True)
        user_check = show_message("Please review circuit. Do you wish to \
                                    continue?", type='question')
        if user_check == 'No':
            message = "Please re-add drugs and check circuit parameters."
            print_to_screen(self.screen_box, message, delete=True)
            return

        message = "Circuit created!\nCircuit IDs:\n"
        print_to_screen(self.screen_box, message, delete=True)
        ids = new_circuit.set_IDs()
        for i in ids:
            print_to_screen(self.screen_box, i + "\n")
        end = server.start_update(new_circuit)
        print_to_screen(self.screen_box, end, delete=True)

def show_message(message, type='error'):
    if type == 'question':
        return tk.messagebox.askquestion('User Check', message)
    else:
        tk.messagebox.showerror('Error', message)
    return

def print_to_screen(screen, message, delete=False):
    if delete:
        screen.delete(1.0, 'end-1c')
    screen.insert('end-1c', message)

def print_dict(dict):
    str = ""
    for key, val in dict.items():
        str = str + "{}:{}\n".format(key, val)

    return str

def main():
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
