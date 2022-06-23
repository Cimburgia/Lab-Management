import pandas as pd
import numpy as np
import os
from circuit import Circuit
from operator import itemgetter
from itertools import groupby

def start_update(circuit):
    IDs = circuit.set_IDs

    # Start Updates
    make_boxmaps(circuit, IDs)

def make_boxmaps(circuit, IDs):
    # Drug_Type_Box#_Date
    files = get_filenames("../../Box Maps")
    circuit_drugs = circuit.drugs.values()
    circuit_types = circuit.types
    existing_maps = []

    filtered = []
    needed = []

    df = pd.DataFrame(columns = ["Box Label",
                                    "Cell",
                                    "Sample ID",
                                    "Date",
                                    "Timepoint"])

    # Filter by drug name and type
    for f in files:
        name = f.split("_")

        if name[0] in circuit_drugs and name[1] in circuit_types:
            filtered.append(f)
            existing_maps.append(tuple((name[0], name[1])))

    # Go through each box
    for type, cirs in groupby(sorted(IDs), key=itemgetter(0)):
        for drug, circuits in groupby(sorted(cirs), key=itemgetter(2,3)):
            for c in circuits:
                

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

def get_num_samples():
    pass

def generate_cells():
    rows = ['A','B','C','D','E','F','G','H','I']
    cols = range(1,10)
    cells = []
    for r in rows:
        for c in cols:
            cells.append(r+str(c))
    return cells

def main():
    test = Circuit("1",
                    "6 hr",
                    {1:"1 min", 2:"5 min", 3:"15 min", 4:"30 min", 5:"1 hr",
                     6:"2 hr", 7:"3 hr", 8:"4 hr", 9:"5 hr", 10:"6 hr"},
                     {"Dx":"Dexmedtomidine", "Cl":"Clindamycin"},
                     "ECMO and CRRT",
                     "True",
                     "2022-6-23")

    make_boxmaps(test, test.set_IDs())
    #print(generate_cells())
if __name__ == "__main__":
    main()
