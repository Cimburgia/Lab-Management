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
        self.timepoints = timpoints
        self.drugs = drugs
        self.type = type
        self.control = control
        # format not working for tkcal
        temps = str(date).split('-')
        up_date = "{}/{}/{}".format(temps[1], temps[2], temps[0])
        self.date = up_date

    def print_circuit(self):
        str = ("{} Circuit Overview:\n"
                "Type: {}\n"
                "Length: {} hours\n"
                "Drugs:  {}"
                "Control: {}\n")
        return str.format(self.date,
                        self.type,
                        self.length,
                        self.print_drugs(),
                        self.control)

    def print_drugs(self):
        s = ""
        tab = ""
        for abrv, drug in self.drugs.items():
            s = s + tab + "{} ({})\n".format(drug, abrv)
            tab = "\t"
        return s

    def set_IDs(self):
        # Generate 1 to n labels
        types = []
        IDs = []
        coad = "CoAd" if len(self.drugs) > 1 else ""


        if self.type == "ECMO":
            types.append("EA")
            if self.control:
                types.append("EC")
        if self.type == "CRRT":
            types.append("CA")
            types.append("CH")
            if self.control:
                types.append("CC")
        if self.type == "ECMO and CRRT":
            types.append("EA")
            types.append("CA")
            types.append("CH")
            if self.control:
                sample_types.append("EC")

        for t in types:
            for d in self.drugs.keys():
                temp_id = t[0] + coad + self.circuit_num + d + t[1]
                IDs.append(temp_id)

        return IDs
