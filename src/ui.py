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
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.parent.configure(background='green')
        label = tk.Label(self, text="Hello World")
        label.pack()

        button = tk.Button(self, text="To Next", command=self.parent.close_login)
        button.pack()

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
