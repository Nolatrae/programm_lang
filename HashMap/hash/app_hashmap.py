
from hash.iloc import Iloc
from hash.ploc import Ploc


class HashDictionary(dict):
    def __init__(self):
        self.keys = {}
        self.iloc = Iloc(self)
        self.ploc = Ploc(self)

