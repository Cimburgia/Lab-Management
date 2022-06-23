import pandas as pd
import numpy as np
import os
from circuit import Circuit

def start_update(circuit):
    IDs = circuit.set_IDs

    # Start Updates
    make_boxmaps(circuit, IDs)

def make_boxmaps(circuit, IDs):
    files = get_filenames("../../Box Maps")

    

def build_file_names(circuit, extension, other=""):
    file_names = []
    drugs = circuit.drugs.keys()
    date = circuit.date.replace("/","")

    for d in drugs:
        for t in circuit.type:
            name = "{}_{}_{}{}.{}".format(d,t,date,other,extension)
            file_names.append(name)

    return file_names

def get_filenames(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return files

def main():
    test = Circuit("1",
                    "6 hr",
                    {1:"1 min", 2:"5 min", 3:"15 min", 4:"30 min", 5:"1 hr",
                     6:"2 hr", 7:"3 hr", 8:"4 hr", 9:"5 hr", 10:"6 hr"},
                     {"Dx":"Dexmedtomidine", "Cl":"Clindamycin"},
                     "ECMO and CRRT",
                     "True",
                     "2022-6-23")
    make_boxmaps(test, "csv")

if __name__ == "__main__":
    main()
