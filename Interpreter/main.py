from interpreter import Interpreter
import sys

if __name__ == "__main__":
    interp = Interpreter()
    print("in> ", end="")
    text=""
    while True:

        code_text = input()
        text += code_text + " "
        print(f": {text}")

        if code_text == "END.":
            break

        try:
            interp.eval(text)
            print(f"out> {interp.variable}")
        except (SyntaxError, ValueError, TypeError) as e:
            print(f"{type(e).__name__}: {e}", file=sys.stderr)

    print("Done!")
