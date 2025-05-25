from typing import Literal


def color_text(text, color: Literal["red", "green", "yellow", "blue", "magenta", "cyan", "white"]):
    code = {
        "red": 91,
        "green": 92,
        "yellow": 93,
        "blue": 94,
        "magenta": 95,
        "cyan": 96,
        "white": 97,
    }


    return f"\033[{code[color]}m{text}\033[0m"