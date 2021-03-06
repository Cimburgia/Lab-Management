# Circuit class

class Circuit():

    def __init__(self,
                 circuit_num,
                 length,
                 timepoints,
                 drugs,
                 type,
                 control,
                 date):
        self.length = length
        self.circuit_num = circuit_num
        self.timepoints = timepoints
        self.drugs = drugs
        self.type = type
        self.control = control
        # format not working for tkcal
        temps = str(date).split('-')
        self.date = "{}/{}/{}".format(temps[1], temps[2], temps[0])
        self.tube_date = "{}.{}.{}".format(temps[1], temps[2], temps[0])
        self.file_date = "{}{}{}".format(temps[1], temps[2], temps[0])
        self.samples_per_type = list(timepoints)[-1]

    def print_circuit(self):
        str = ("{} Circuit Overview:\n"
                "Number: {}\n"
                "Type: {}\n"
                "Length: {} hours\n"
                "Drugs:  {}"
                "Control: {}\n"
                "Timepoints: {}")
        return str.format(self.circuit_num,
                        self.date,
                        self.type,
                        self.length,
                        self.print_dicts(self.drugs),
                        self.control,
                        self.print_dicts(self.timepoints))

    def print_dicts(self, dict):
        s = ""
        tab = ""
        for value, key in dict.items():
            s = s + tab + "{} ({})\n".format(value, key)
            tab = '\t'
        return s

    def get_sample_types(self):
        types = ["A"]
        if self.control:
            types.append("C")
        if self.type == "CRRT":
            types.append("H")
        return types

    def set_IDs(self, drug=None):
        if drug is None:
            drug = self.drugs
        # Generate 1 to n labels
        types = []
        IDs = []

        if self.type == "ECMO":
            types.append("EA")
            if self.control:
                types.append("EC")
        if self.type == "CRRT":
            types.append("CA")
            types.append("CH")
            if self.control:
                types.append("CC")

        for t in types:
            for d in drug:
                temp_id = t[0] + self.circuit_num + d + t[1]
                IDs.append(temp_id)
        self.IDs = IDs

        return IDs

    def get_samples_per_drug(self):
        add_ctrl = 1 if self.control else 0
        add_hf = 1 if self.type == 'CRRT' else 0
        return len(self.timepoints) * (1 + add_ctrl + add_hf)
