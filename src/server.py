import pandas as pd
import numpy as np
import os
import docx
from docx.enum.section import WD_ORIENT
from docx.enum.section import WD_SECTION
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
    circuit_type = circuit.type
    existing_maps = []
    filtered = []
    needed = []

    # Go through each box
    for type, cirs in groupby(sorted(IDs), key=itemgetter(0)):
        for drug, circuits in groupby(sorted(cirs), lambda x : x[2:4]):
            df = pd.DataFrame(columns = ["Box Label",
                                            "Cell",
                                            "Sample ID",
                                            "Date",
                                            "Timepoint"])
            cur_type = 'ECMO' if type == 'E' else 'CRRT'
            cur_drug = circuit.drugs[drug]
            cand_box = None
            box_num = 1
            num_samples = circuit.get_samples_per_drug()
            file_date = circuit.date.replace('/','')
            tube_date = circuit.date.replace('/','.')
            cir_names = list(circuits)
            cells = generate_cells()
            start = 0
            new = True

            # look up room in current boxes
            # Get last used box
            for f in files:
                name = f.split("_")
                if name[0] == cur_drug and name[1] == cur_type:
                    if box_num <= int(name[2][3:]):
                        box_num = int(name[2][3:])
                        cand_box = f

            # Check candidate box for room or make new box
            if cand_box:
                box = pd.read_csv("../../Box Maps/" + cand_box)
                box = box[box['Sample ID'] != 'Empty']
                room = 81 - len(box)
                if room >= num_samples:
                    start = 81 - room
                    label = cand_box[:-4]
                    new = False
                else:
                    box_num = box_num + 1
            # Check if new box needs to be made
            if new:
                cand_box = "{}_{}_Box{}_{}.csv".format(cur_drug,
                                                    cur_type,
                                                    box_num,
                                                    file_date)
                label = "{} - {} Box {}, Watt {}".format(cur_drug,
                                                    cur_type,
                                                    box_num,
                                                    file_date[-4:])
            # Build dataframe
            time = 0
            count = range(start, 81)
            fill = True
            mod = len(cir_names)
            for idx, x in enumerate(count):
                if idx%mod == 0 and fill:
                    time = time + 1
                _type = cir_names[idx%mod]
                if idx >= num_samples:
                    sample_id = "Empty"
                    tube_date = ""
                    timepoint = ""
                    fill = False
                else:
                     sample_id = _type + str(time)
                     timepoint = circuit.timepoints[time]
                df.loc[len(df)] = [label,
                                    cells[x],
                                    sample_id,
                                    tube_date,
                                    timepoint]
            if not new:
                df = pd.concat([box, df])

            df.to_csv("../../Box Maps/" + cand_box, index=False)

def build_labs_crf(circuit):
    doc = docx.Document()
    sections = doc.sections
    for s in sections:
        s.orientation = WD_ORIENT.LANDSCAPE
        new_width, new_height = s.page_height, s.page_width
        s.page_width = new_width
        s.page_height = new_height

    # Header
    section = doc.sections[0]
    header = section.header
    h_para = header.paragraphs[0]
    h_para.text = "Date:__________________" + \
                    "\t\t\tPage_______ of ______\n" + \
                    "Circuit #:__________________\n" + \
                    "Drug:__________________"

    table = doc.add_table(rows=12, cols=14, style = 'Table Grid')
    head = table.rows[0].cells
    cols = ["Mode", "Circuit", "Drug", "Date", "Time", "Sample", "ph", "CO2",
            "O2", "HCO3", "Na", "K", "Hgb", "Hct"]
    for idx, c in enumerate(cols):
        run = head[idx].paragraphs[0].add_run(c)
        run.bold = True


    doc.save("test.docx")


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

def generate_cells():
    rows = ['A','B','C','D','E','F','G','H','I']
    cols = range(1,10)
    cells = []
    for r in rows:
        for c in cols:
            cells.append(r+str(c))
    return cells

def main():
    test = Circuit("2",
                    "6 hr",
                    {1:"1 min", 2:"5 min", 3:"15 min", 4:"30 min", 5:"1 hr",
                     6:"2 hr", 7:"3 hr", 8:"4 hr", 9:"5 hr", 10:"6 hr", 11:"8 hr"},
                     {"Dx":"Dexmedtomidine", "Cl":"Clindamycin"},
                     "CRRT",
                     "True",
                     "2022-6-23")

    build_labs_crf(test)

if __name__ == "__main__":
    main()
