import pytest
from prefix.prefix import is_operator, is_operand, precedence, prefix_to_infix


def test_is_operator():
    assert is_operator("+") == True
    assert is_operator("-") == True
    assert is_operator("*") == True
    assert is_operator("/") == True
    assert is_operator("5") == False
    assert is_operator("a") == False
    assert is_operator(" ") == False


def test_is_operand():
    assert is_operand("5") == True
    assert is_operand("-5") == True
    assert is_operand("0") == True
    assert is_operand("-0") == True
    assert is_operand("a") == False
    assert is_operand("+") == False


def test_precedence():
    assert precedence("+") == 1
    assert precedence("-") == 1
    assert precedence("*") == 2
    assert precedence("/") == 2
    assert precedence("a") == 0
    assert precedence("5") == 0


def test_prefix_to_infix():
    assert prefix_to_infix("+ - 13 4 55") == "((13 - 4) + 55)"
    assert prefix_to_infix("+ 2 * 2 - 2 1") == "(2 + (2 * (2 - 1)))"
    assert prefix_to_infix("+ + 10 20 30") == "((10 + 20) + 30)"
    assert prefix_to_infix("- - 1 2") == "Invalid expression"
    assert prefix_to_infix(
        "/ + 3 10 * + 2 3 - 3 5") == "((3 + 10) / ((2 + 3) * (3 - 5)))"


if __name__ == '__main__':
    pytest.main()
