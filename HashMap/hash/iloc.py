class IlocException(Exception):
    pass

class Iloc(dict):
    def __init__(self, d: dict):
        self.d = d

    def __getitem__(self, index):
        sorted_items = sorted(self.d.items(), key=lambda x: str(x[0]))
        sorted_dict = dict(sorted_items)

        values = list(sorted_dict.values())

        if 0 <= index < len(values):
            return values[index]

        raise IlocException("Invalid index")