from interpreter import Interpreter
import sys


if __name__ == "__main__":
    interp = Interpreter()

    while True:
        print("in> ", end="")
        text = input()
        print(f": {text}")

        if text == "exit" or len(text) < 1:
            break

        try:
            result = interp.eval(text)
            print(f"out> {result}")
        except (SyntaxError, ValueError, TypeError) as e:
            print(f"{type(e).__name__}: {e}", file=sys.stderr)

    print("Done!")
