import tkinter as tk
import pandas as pd

# program libraries
import server
import circuit


top = tk.Tk()

c = circuit.Circuit(10, 1, ["Ak"], "CRRT", False, "05/05/2022")
w = tk.Label(top, text = c.type)
w.pack()

top.mainloop()
