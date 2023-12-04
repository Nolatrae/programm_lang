from typing import Union

class PlocException(Exception):
    pass


class Ploc(dict):

    def __init__(self, d: dict):
        super().__init__()
        self.d = d

    def __getitem__(self, conditions: str):
        buf_conditions = self.parse_conditions(conditions)

        result = "{"

        for k, v in self.d.items():
            item_buf = []
            match k:
                case _ if "(" in k:
                    buf = ""
                    for i in k:
                        if i.isdigit():
                            buf += i
                        elif i == ',':
                            item_buf.append(int(buf))
                            buf = ""
                        elif i == ")":
                            item_buf.append(int(buf))
                case _:
                    if k.isdigit():
                        item_buf.append(int(k))
                    else:
                        item_buf.append(k)



            if len(item_buf) == len(buf_conditions) and not isinstance(item_buf[0], str):
                if len(item_buf) == 1:
                    if self.condition_check(buf_conditions, item_buf[0], 1):
                        result += k + '=' + f"{v}"
                        result += ', '
                elif self.condition_check(buf_conditions, item_buf, len(item_buf)):
                    result += k + '=' + f"{v}"
                    result += ', '

        return "" if len(result) < 2 else result[:-2] + "}"

    def parse_conditions(self, conditions: str):
        result = []
        buf = ""
        op = ""

        for i in conditions:
            if i in "<>=":
                op += i
            elif i.isdigit():
                buf += i
            elif buf and op:
                result.append([op, int(buf)])
                buf = ""
                op = ""

        if buf and op:
            result.append([op, int(buf)])

        return result

    def operation(self, op: str, v1, v2):
        operators = {
            "==": lambda x, y: x == y,
            ">": lambda x, y: x > y,
            "<": lambda x, y: x < y,
            ">=": lambda x, y: x >= y,
            "<=": lambda x, y: x <= y,
            "<>": lambda x, y: x != y,
        }

        return operators[op](v1, v2)

    def condition_check(self, buf_conditions, item, count):
        if count == 1:
            return self.operation(buf_conditions[0][0], item, buf_conditions[0][1])
        return all(self.operation(cond[0], item[i], cond[1]) for i, cond in enumerate(buf_conditions[:count]))



