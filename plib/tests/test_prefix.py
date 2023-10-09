import pytest
from plib import base


def test_is_operator():
    assert base.is_operator("+") == True
    assert base.is_operator("-") == True
    assert base.is_operator("*") == True
    assert base.is_operator("/") == True
    assert base.is_operator("5") == False
    assert base.is_operator("a") == False
    assert base.is_operator(" ") == False


def test_is_operand():
    assert base.is_operand("5") == True
    assert base.is_operand("-5") == True
    assert base.is_operand("0") == True
    assert base.is_operand("-0") == True
    assert base.is_operand("a") == False
    assert base.is_operand("+") == False


def test_precedence():
    assert base.precedence("+") == 1
    assert base.precedence("-") == 1
    assert base.precedence("*") == 2
    assert base.precedence("/") == 2
    assert base.precedence("a") == 0
    assert base.precedence("5") == 0


def test_prefix_to_infix():
    assert base.prefix_to_infix("+ - 13 4 55") == "((13 - 4) + 55)"
    assert base.prefix_to_infix("+ 2 * 2 - 2 1") == "(2 + (2 * (2 - 1)))"
    assert base.prefix_to_infix("+ + 10 20 30") == "((10 + 20) + 30)"
    with pytest.raises(ValueError):
        base.prefix_to_infix("- - 1 2")
    assert base.prefix_to_infix(
        "/ + 3 10 * + 2 3 - 3 5") == "((3 + 10) / ((2 + 3) * (3 - 5)))"
