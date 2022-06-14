# Circuit class

class Circuit():

    def __init__(self,
                 length,
                 num_doses,
                 drugs,
                 type,
                 control,
                 date):
        self.length = length
        self.num_doses = num_doses
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
                "Doses: {}\n"
                "Control: {}\n")
        return str.format(self.date,
                        self.type,
                        self.length,
                        self.print_drugs(),
                        self.num_doses,
                        self.control)

    def print_drugs(self):
        s = ""
        tab = ""
        for abrv, drug in self.drugs.items():
            s = s + tab + "{} ({})\n".format(drug, abrv)
            tab = "\t"
        return s

    def get_num_samples(self):
        return len(self.drugs)

    def setID(self):
        # set ID based on circuit #
        pass
