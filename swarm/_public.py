"""
_public.py - sunnyqa233

Functions that maybe used in multiple modules.
"""
import time


def colourful_text(colour: str, text: str) -> str:
    """
    Available colours:
      * r --> Red
      * g --> Green
      * b --> Blue
      * y --> Yellow
      * c --> cyan

    :param colour: The char that represents a certain colour.
    :param text: The text that you want to print with colour.
    :return: Text with ANSI escape code.
    """
    colour_table = {
        "r": "\033[91m",
        "b": "\033[94m",
        "g": "\033[92m",
        "y": "\033[93m",
        "c": "\033[96m"
    }
    try:
        return colour_table[colour] + text + "\033[0m"
    except KeyError:
        print(colour_table["y"]+f"Unknown colour '{colour}'." + "\033[0m")
        return text


def sleep(duration: float) -> None:
    """
    To solve the problem that time.sleep() having high error on my pc. This stupid function exists.

    :param duration: How long you would like to block. (Unit: s)(Precision: 0.001s)
    :return: Nothing
    """
    start = time.time()
    while time.time() - start <= duration:
        pass
    return None
