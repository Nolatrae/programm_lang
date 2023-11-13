import pytest
from interpreter import Interpreter, BinOp, UnOp, Number, NodeVisitor, Var, Empty, Semi, Assigment
from interpreter import Token, TokenType, Parser


@pytest.fixture(scope="function")
def interpreter():
    return Interpreter()


@pytest.fixture(scope="function")
def parser():
    return Parser()


class TestInterpreter:

    interpreter = Interpreter()

    def test_add(self, interpreter):
        assert interpreter.eval("2+2") == 4

    def test_sub(self, interpreter):
        assert interpreter.eval("2-2") == 0

    def test_mul(self, interpreter):
        assert interpreter.eval("25*25") == 625

    assert interpreter.eval("22+2*2") == 26

    def test_div(self, interpreter):
        assert interpreter.eval("2/2") == 1

    def test_brackets(self, interpreter):
        assert interpreter.eval("2*(2+2)") == 8

    assert interpreter.eval("2*((2+2)+(3*2))") == 20

    def test_un_plus(self, interpreter):
        assert interpreter.eval("++11") == 11

    assert interpreter.eval("+1++2") == 3

    def test_un_minus(self, interpreter):
        assert interpreter.eval("-11") == -11

    assert interpreter.eval("+1+-(-2)") == 3

    def test_invalid_factor(self, interpreter):
        with pytest.raises(SyntaxError):
            assert interpreter.eval("11++")

    def test_binop_invalid_operator(self, interpreter):
        with pytest.raises(ValueError):
            assert interpreter.visit_binop(BinOp(Number(Token(TokenType.NUMBER, "2")), Token(TokenType.OPERATOR, "&"), Number(Token(TokenType.NUMBER, "2"))))

    def test_unop_invalid_operator(self, interpreter):
        with pytest.raises(ValueError):
            assert interpreter.visit_unop(UnOp(Token(TokenType.OPERATOR, "&"), Number(Token(TokenType.NUMBER, "2"))))

    def test_ast_binop_str(self):
        assert BinOp(Number(Token(TokenType.NUMBER, "2")), Token(TokenType.OPERATOR, "+"),
                     Number(Token(TokenType.NUMBER, "2"))).__str__() == f"BinOp+ (Number (Token(TokenType.NUMBER, 2)), Number (Token(TokenType.NUMBER, 2)))"

    def test_ast_unop_str(self):
        assert UnOp(Token(TokenType.OPERATOR, "+"), Number(Token(TokenType.NUMBER, "2"))).__str__() == f"UnOp+ (Number (Token(TokenType.NUMBER, 2)))"

    def test_nodeVisutor(self):
        assert NodeVisitor().visit() is None

    def test_add_with_spaces(self, interpreter):
        assert interpreter.eval("2+ 2") == 4

    def test_expr_break(self, interpreter):
        assert interpreter.eval("2+2*2/2") == 6

    def test_expr_continue(self, interpreter):
        assert interpreter.eval("2+2*2/2+2") == 6

    def test_invalid_expr(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("2+a")

        with pytest.raises(SyntaxError):
            interpreter.eval("t+a")

    def test_invalid_token_order(self, parser):
        parser._current_token = Token(TokenType.NUMBER, "2")
        with pytest.raises(SyntaxError):
            parser.check_token(TokenType.OPERATOR)


    def test_add_with_letter(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("2+a")
        with pytest.raises(SyntaxError):
            interpreter.eval("t+2")

    def test_wrong_operator(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("2&3")

    @pytest.mark.parametrize(
        "interpreter, code", [(interpreter, "2 + 2"),
                              (interpreter, "2 +2 "),
                              (interpreter, " 2+2")]
    )
    def test_add_spaces(self, interpreter, code):
        assert interpreter.eval(code) == 4

    def test_empty(self, interpreter):
        assert interpreter.eval("BEGIN END.") == {}

    def test_variable(self, interpreter):
        assert interpreter.eval("BEGIN x:= 2 + 3 * (2 + 3); END.") == {'x': 17.0}

    def test_NodeVisitor(self):
        assert NodeVisitor().visit() is None

    def test_uninitialized_variable(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.eval("BEGIN b := -10 + +a + 10 * y / 4; END.")

    def test_bad_token(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_ASSIGN(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a== 2 + 3 * (2 + 3); END.")

    def test_bad_token_SEMI(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_DOT(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_END(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_ID(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_LPAREN(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_RPAREN(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_invalid_token_order(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a = 2 + 3 * (2 + 3); END.")

    def test_Invalid_statement(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a = 2 + 3 * (2 + 3); END.")

    def test_Invalid_statement_assign(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a = 2 + 3 * (2 + 3); END.")

    def test_ast_Assigment_num(self):
        assert Assigment(Var(Token(TokenType.ID, "h")), Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"Assigment Variable (Token(TokenType.ID, h)) (Number (Token(TokenType.NUMBER, 2)))"

    def test_ast_Assigment_str(self):
        assert Assigment(Var(Token(TokenType.ID, "h")), Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"Assigment Variable (Token(TokenType.ID, h)) (Number (Token(TokenType.NUMBER, 2)))"

    def test_ast_Empty(self):
        assert Empty(Token(TokenType.END, "END.")).__str__() == "Empty (Token(TokenType.END, END.))"

    def test_ast_BinOp_str(self):
        assert BinOp(Number(Token(TokenType.NUMBER, "2")), Token(TokenType.OPERATOR, "+"),
                     Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"BinOp+ (Number (Token(TokenType.NUMBER, 2)), Number (Token(TokenType.NUMBER, 2)))"

    def test_BinOp_invalid_operator(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.visit_binop(BinOp(Number(Token(TokenType.NUMBER, "2")), Token(TokenType.OPERATOR, "&"),
                                          Number(Token(TokenType.NUMBER, "2"))))

    def test_unop_invalid_operator(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.visit_unop(UnOp(Token(TokenType.OPERATOR, "&"), Number(Token(TokenType.NUMBER, "2"))))

    def test_ast_UnOp_str(self):
        assert UnOp(Token(TokenType.OPERATOR, "+"), Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"UnOp+ (Number (Token(TokenType.NUMBER, 2)))"

    def test_ast_Number_str(self):
        assert Number(Token(TokenType.NUMBER, "2")).__str__() == "Number (Token(TokenType.NUMBER, 2))"

    def test_ast_Variable_str(self):
        assert Var(Token(TokenType.ID, "h")).__str__() == "Variable (Token(TokenType.ID, h))"

    def test_ast_Assigment_str(self):
        assert Assigment(Var(Token(TokenType.ID, "h")), Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"Assigment Variable (Token(TokenType.ID, h)) (Number (Token(TokenType.NUMBER, 2)))"


