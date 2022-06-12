# Circuit class

class Circuit():

    def __init__(self,
                 length,
                 num_doses,
                 compounds,
                 type,
                 control,
                 date):
        self.length = length
        self.num_doses = num_doses
        self.compounds = compounds
        self.type = type
        self.control = control
        self.date = date

    def get_num_samples(self):
        # returns number of samples based on dose number and circuit length
        pass

    def setID(self):
        # set ID based on circuit #
        pass
        
