from enum import Enum
import struct


class Alignment(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Widget():
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        if self.parent is not None:
            self.parent.add_children(self)

    def add_children(self, children: "Widget"):
        self.children.append(children)

    def types_to_binary(self, data):
        if type(data) == str:
            return struct.pack('i', len(str(data).encode())) + str(data).encode()
        elif type(data) == float or type(data) == int:
            return struct.pack('i', len(struct.pack('>f', data))) + struct.pack('>f', data)
        elif type(data) == list:
            bvals = b''
            for i in data:
                bv = b''
                if type(i) == int:
                    bv += 'i'.encode()
                elif type(i) == str:
                    bv += 's'.encode()
                bvals += bv + self.types_to_binary(i)
            return struct.pack('i', len(bvals)) + bvals

    def types_from_binary_for_list(self, data, type=""):
        tt = struct.unpack('i', data[:4])[0]
        n = 4
        if type == "":
            elem = []
            while n < tt:
                type = data[n:n + 1].decode()
                tt1 = struct.unpack('i', data[n + 1: n + 5])[0]
                elem.append(self.types_from_binary_for_list(self, data[n + 1: n + 5 + tt1], type))
                n = n + 5 + tt1
            return elem
        elif type == 'i':
            return struct.unpack('>f', data[4: 4 + tt])[0]
        elif type == 's':
            return data[4: 4 + tt].decode()

    def to_binary(self):
        bname = self.class_name.encode()
        bvals = self.types_to_binary(self.get)
        bchildrens = b''
        for i in self.children:
            bchildrens += i.to_binary()
        return struct.pack("i", len(bname)) + bname + bvals + struct.pack("i", len(bchildrens)) + bchildrens

    @classmethod
    def from_binary(self, data, parent=""):

        class_name_length = struct.unpack("i", data[:4])[0]
        class_name = data[4:4 + class_name_length].decode()

        len_value = 4 + class_name_length + struct.unpack("i", data[4 + class_name_length:4 + class_name_length + 4])[0]
        if class_name == "ComboBox":
            value = self.types_from_binary_for_list(self, data[4 + class_name_length:len_value + 4])
        elif class_name == "MainWindow":
            value = self.types_from_binary_for_list(self, data[4 + class_name_length:len_value + 4], "s")
        else:
            value = self.types_from_binary_for_list(self, data[4 + class_name_length:len_value + 4], "i")

        if class_name == 'MainWindow':
            parent = MainWindow(value)
        elif class_name == 'Layout':
            parent = Layout(parent, value)
        elif class_name == 'LineEdit':
            parent = LineEdit(parent, value)
        elif class_name == 'ComboBox':
            parent = ComboBox(parent, value)

        len_childrens = len_value + 4 + struct.unpack("i", data[4 + len_value:4 + len_value + 4])[0]
        cursor = 4 + len_value + 4
        while (cursor < len_childrens):
            children, arr_len = self.from_binary(data[cursor:], parent)
            cursor += arr_len + 4
        return parent, len_childrens

    def to_json(self):
        return {'parent': self.class_name, 'values': self.get, 'children': [i.to_json() for i in self.children]}

    @classmethod
    def from_json(self, json, parent=""):
        if json["parent"] == 'MainWindow':
            parent = MainWindow(json["values"])
        elif json["parent"] == 'Layout':
            parent = Layout(parent, json["values"])
        elif json["parent"] == 'LineEdit':
            parent = LineEdit(parent, json["values"])
        elif json["parent"] == 'ComboBox':
            parent = ComboBox(parent, json["values"])
        children = []
        for i in json["children"]:
            children.append(self.from_json(i, parent))
        return parent

    def __str__(self):
        return f"{self.__class__.__name__}{self.children}"

    def __repr__(self):
        return str(self)


class MainWindow(Widget):
    def __init__(self, title: str):
        super().__init__(None)
        self.title = title

    @property
    def get(self):
        return self.title

    @property
    def class_name(self):
        return "MainWindow"


class Layout(Widget):
    def __init__(self, parent, alignment: Alignment):
        super().__init__(parent)
        self.alignment = alignment

    @property
    def get(self):
        if type(self.alignment) == float:
            return self.alignment
        return self.alignment.value

    @property
    def class_name(self):
        return "Layout"


class LineEdit(Widget):
    def __init__(self, parent, max_length: int = 10):
        super().__init__(parent)
        self.max_length = max_length

    @property
    def get(self):
        return self.max_length

    @property
    def class_name(self):
        return "LineEdit"


class ComboBox(Widget):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items

    @property
    def get(self):
        return self.items

    @property
    def class_name(self):
        return "ComboBox"


app = MainWindow("Application")
layout1 = Layout(app, Alignment.HORIZONTAL)
layout2 = Layout(app, Alignment.VERTICAL)

edit1 = LineEdit(layout1, 20)
edit2 = LineEdit(layout1, 30)

box1 = ComboBox(layout2, [1, 2, 3, 4])
box2 = ComboBox(layout2, ["a", "b", "c"])

bts = app.to_binary()
print(f"Binary data length {len(bts)}")
print(bts)

new_app = MainWindow.from_binary(bts)[0]
print(new_app)

ad = new_app.to_json()
print(ad)

a = MainWindow.from_json(ad)
print(a)

print(a.children[1].children[1].items)
print(new_app.children[1].children[1].items)