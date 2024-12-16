from code import InteractiveConsole
import sys

VERSION = "0.0.1"

PYMETH_GREETING = f"""\
Welcome to PyMeth {VERSION}, your python script buddy for combinatorics calculation.
Type "$help" for more information.\
"""

HELP = """\
Type "$switch" to switch to pure python mode without substitutions.\
"""

DEBUG_LEVEL = 3

IMPORTS = """\
from math import *
from itertools import *
"""


def log(debug_level, *args, **kwargs):
    if debug_level > DEBUG_LEVEL:
        return

    match debug_level:
        case 1:
            print("\033[31mError:\033[0m", *args, **kwargs)
        case 2:
            print("\033[33mWarning:\033[0m", *args, **kwargs)
        case 3:
            print("\033[32mInfo:\033[0m", *args, **kwargs)


# Got it from ChatGPT lol
def get_python_header():
    version = sys.version
    platform = sys.platform
    header = (
        f"Python {version} on {platform}\n"
        f'Type "help", "copyright", "credits" or "license" for more information.'
    )
    return header


def to_factorial(prompt: str) -> str:
    log(3, "Entering body to_factorial")
    parentheses = {}
    unmatched_parentheses = []
    factorials = []

    double_quote = False
    single_quote = False
    for i, char in enumerate(prompt):
        if single_quote and char == "'" and prompt[i - 1] != "\\":
            single_quote = False
            continue

        if double_quote and char == '"' and prompt[i - 1] != "\\":
            double_quote = False
            continue

        if single_quote or double_quote:
            continue

        match char:
            case "#":
                break
            case "'":
                single_quote = True
            case '"':
                double_quote = True
            case "(":
                unmatched_parentheses.append(i)
            case ")":
                pair = unmatched_parentheses.pop()
                parentheses[i] = pair
                parentheses[pair] = i
            case "!":
                factorials.append(i)
            case "=" if i > 0 and prompt[i - 1] == "!":
                factorials.pop()

    log(3, f"{prompt=} {parentheses=} {factorials=}")
    processed_prompt = ""
    last_index = 0
    for i in factorials:
        no_parentheses = False
        start = last_index
        end = i

        brackets = 0
        for j in range(i - 1, last_index - 1, -1):
            char = prompt[j]
            match char:
                case "]":
                    brackets += 1
                    no_parentheses = True
                case "[" if brackets > 0:
                    brackets -= 1
                case _ if brackets > 0:
                    pass
                case ")":
                    start = parentheses[j]
                    break
                case _ if char.isalnum() and not no_parentheses:
                    end = j + 1
                    no_parentheses = True
                case _ if no_parentheses and not char.isalnum() and char not in "._":
                    start = j + 1
                    break

        log(3, f"{start=} {end=} {no_parentheses=}")
        processed_prompt += prompt[last_index:start]
        if no_parentheses:
            processed_prompt += "factorial({})".format(prompt[start:end])
            processed_prompt += prompt[end:i]
        else:
            processed_prompt += "factorial" + prompt[start:i]

        last_index = i + 1

    processed_prompt += prompt[last_index:]

    log(3, f"Exiting to_factorial with {processed_prompt=}")
    return processed_prompt


def process(prompt: str) -> str:
    prompt = to_factorial(prompt)
    return prompt


def main():
    print(get_python_header())
    print()
    print(PYMETH_GREETING)
    console = InteractiveConsole()
    console.runsource(IMPORTS, symbol="exec")

    modded = True
    while True:
        try:
            prompt = input(">>> ")
            match prompt:
                case "$help":
                    print(HELP)
                    continue
                case "$switch":
                    modded = not modded
                    continue

            if modded:
                prompt = process(prompt)

            log(3, f"Running python with {prompt=}")

            while console.runsource(prompt):
                prompt += "\n" + input("... ")
                prompt = process(prompt)

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
        except EOFError:
            print()
            exit(0)


if __name__ == "__main__":
    main()
