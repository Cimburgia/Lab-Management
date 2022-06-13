import sys
import tkinter as tk
import pandas as pd

# program libraries
import server
import circuit

class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        label = tk.Label(self, text="Hello Other World")
        label.pack()

class LoginFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=600, height=600)
        self.parent = parent

        # Build frame widgets
        label = tk.Label(self, text="Please log in to access Box.")
        label.place(x=40, y=30)
        user_name = tk.Label(self, text="uNID:").place(x=40, y=60)
        password = tk.Label(self, text="Password:").place(x=40, y=100)
        user_name_input = tk.Entry(self, width=40).place(x=110, y=60)
        password_input = tk.Entry(self, width=40).place(x=110, y=100)

        submit = tk.Button(self, text="Login", command=self.login)
        submit.place(x=40, y=130)

        def login(self):
            #TODO: Interface with server, log in to box
            parent.close_login()
            
class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('600x600')
        self.title('Box Login')

        self.login = LoginFrame(self)
        self.mainframe = MainFrame(self)

        self.login.pack()

    def close_login(self):
        self.login.pack_forget()
        self.mainframe.pack()


def main():

    root = MainApplication()
    root.mainloop()

if __name__ == "__main__":
    main()
