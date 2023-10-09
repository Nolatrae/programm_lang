def is_operator(token):
    return token in "+-*/"


def is_operand(token):
    return token.isdigit() or (token[0] == '-' and token[1:].isdigit())


def precedence(operator):
    if operator in "+-":
        return 1
    if operator in "*/":
        return 2
    return 0


def prefix_to_infix(expression):
    tokens = expression.split()
    stack = []

    for token in reversed(tokens):
        if is_operand(token):
            stack.append(token)
        elif is_operator(token):
            if len(stack) < 2:
                raise ValueError("Неверное выражение")
            operand1 = stack.pop()
            operand2 = stack.pop()
            infix_expression = f"({operand1} {token} {operand2})"
            stack.append(infix_expression)

    if len(stack) == 1:
        return stack[0]
    else:
        raise ValueError("Неверное выражение")


def main():
    prefix_expression = input("Введите префиксное выражение: ")

    try:
        infix_expression = prefix_to_infix(prefix_expression)
        print(f"Инфиксная запись: {infix_expression}")
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
