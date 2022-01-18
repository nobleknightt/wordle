from dataclasses import dataclass
from random import choice, seed
from string import ascii_uppercase
from time import time_ns
from rich.console import Console
from pyperclip import copy
from pathlib import Path
from os import system, name as os_type

@dataclass(init=False, repr=False, eq=False, order=False)
class Setting:    
    MAX_TRIES  = 6
    WORD_LEN   = 5
    WORD_FILE  = "words.txt"
    TERM_WIDTH = Console().width
    
@dataclass(init=False, repr=False, eq=False, order=False)
class Color:
    BLACK  = "#000000"
    BLUE   = "#82AAFF"
    GRAY   = "#676E95"
    GREEN  = "#62DE84"
    RED    = "#FF5572"
    YELLOW = "#FFCB6B"
    WHITE  = "#FFFEFE"

@dataclass(init=False, repr=False, eq=False, order=False)
class Remark:
    CORRECT = Color.GREEN
    PRESENT = Color.YELLOW
    ABSENT  = Color.RED

@dataclass(init=False, repr=False, eq=False, order=False)
class Cell:
    text = " "
    color = Color.WHITE

TEMPLATE = (
    "+++++++++++++++++++++++++++++++++++++++",
    "+-------------------------------------+",
    "+-+-+-+--+++--++++--++++--+-----+++++-+",
    "+-+-+-+-+---+-+---+-+---+-+-----+-----+",
    "+-+-+-+-+---+-+---+-+---+-+-----++++--+",
    "+-+-+-+-+---+-++++--+---+-+-----+-----+",
    "+--+++---+++--+---+-++++--+++++-+++++-+",
    "+-------------------------------------+",
    "+++++++++++++++++++++++++++++++++++++++"
)

TITLE = "\n".join((
    "",
    *("".join((
        (
            f"[{Color.GRAY} on {Color.GRAY}].[/]" if (
                char == "+"
            ) else f"[{Color.YELLOW} on {Color.YELLOW}].[/]"
        ) for char in line
    )) for line in TEMPLATE),
    "",
    f"[bold]Press Enter to Continue[/]",
    "",
    f"[bold {Color.WHITE}]Reference: [{Color.BLUE} link=https://www.powerlanguage.co.uk/wordle/]www.powerlanguage.co.uk/wordle[/][/]",
))

INSTRUCTIONS = "\n".join((
    "",
    "".join((
        f"[{Color.YELLOW} on {Color.YELLOW}].",
        f"[bold {Color.BLACK}]HOW TO PLAY[/]",
        f".[/]"
    )),
    "",
    "Guess the [bold]WORDLE[/] in 6 tries.",
    "After each guess, the color of the tiles will change to show how close your guess was to the word.",
    "",
    "\u2500" * (Setting.TERM_WIDTH - 2),
    "",
    " ".join((
        (
            f"[{Color.GREEN} on {Color.GREEN}].[{Color.BLACK}]{letter}[/].[/]" if (
                letter == "W"
            ) else f"[{Color.WHITE} on {Color.WHITE}].[{Color.BLACK}]{letter}[/].[/]"
        ) for letter in "WEARY"
    )),
    "",
    "The letter [bold]W[/] is in the word and in the correct spot.",
    "",
    " ".join((
        (
            f"[{Color.YELLOW} on {Color.YELLOW}].[{Color.BLACK}]{letter}[/].[/]" if (
                letter == "L"
            ) else f"[{Color.WHITE} on {Color.WHITE}].[{Color.BLACK}]{letter}[/].[/]"
        ) for letter in "PILOT"
    )),
    "",
    "The letter [bold]L[/] is in the word but in the wrong spot.",
    "",
    " ".join((
        (
            f"[{Color.RED} on {Color.RED}].[{Color.BLACK}]{letter}[/].[/]" if (
                letter == "U"
            ) else f"[{Color.WHITE} on {Color.WHITE}].[{Color.BLACK}]{letter}[/].[/]"
        ) for letter in "VAGUE"
    )),
    "",
    "The letter [bold]U[/] is not in the word in any spot.",
    "",
    "\u2500" * (Setting.TERM_WIDTH - 2),
    "",
    "[bold]Press Enter to Play[/]"
))

keyboard_color = {
    key : (
        Color.BLUE if key == "<" else Color.WHITE
    ) for key in (*ascii_uppercase, "<") 
}

wordle_board = tuple(
    tuple(
       Cell() for j in range(Setting.WORD_LEN)
    ) for i in range(Setting.MAX_TRIES)
)

def keyboard_str():
    return "\n".join((
        "",
        " ".join((
            f"[{keyboard_color[key]} on {keyboard_color[key]}].[{Color.BLACK}]{key}[/].[/]" for key in "QWERTYUIOP"
        )),
        "",
        " ".join((
            f"[{keyboard_color[key]} on {keyboard_color[key]}].[{Color.BLACK}]{key}[/].[/]" for key in "ASDFGHJKL"
        )),
        "",
        " ".join((
            f"[{keyboard_color[key]} on {keyboard_color[key]}].[{Color.BLACK}]{key}[/].[/]" for key in "ZXCVBNM<"
        )),
    ))

def wordle_board_str():
    return "\n".join((
        "",
        "\n\n".join((
            " ".join((
                f"[{cell.color} on {cell.color}].[{Color.BLACK}]{cell.text}[/].[/]" for cell in row
            )) for row in wordle_board
        )),
        ""
    ))

def check(picked_word, entered_word):
    remarks = [Remark.ABSENT for _ in entered_word]
    occurrences = {
        letter: picked_word.count(letter) for letter in picked_word
    }

    for index, letter in enumerate(entered_word):
        if occurrences.get(letter, 0) > 0 and picked_word[index] == letter:
            remarks[index] = Remark.CORRECT
            occurrences[letter] -= 1
    
    for index, letter in enumerate(entered_word):
        if occurrences.get(letter, 0) > 0 and letter in picked_word:
            remarks[index] = Remark.PRESENT
            occurrences[letter] -= 1

    return remarks

def pick_word():
    with (Path(__file__).parent / Setting.WORD_FILE).open("r") as f:
        wordlist = f.read().strip().split("\n")[0].split()

        seed(time_ns())
        picked_word = choice(wordlist)

        return picked_word

def get_wordlist():
    with (Path(__file__).parent / Setting.WORD_FILE).open("r") as f:
        return set(f.read().strip().split("\n")[1].split())

def update(current_try, remarks):
    for index in range(Setting.WORD_LEN):
        wordle_board[current_try][index].color = remarks[index]
        if keyboard_color[
            wordle_board[current_try][index].text
        ] not in (Color.RED, Color.GREEN):
            keyboard_color[
                wordle_board[current_try][index].text
            ] = remarks[index]

def copy_to_clipboard():

    colored_box = {
        Color.GREEN  : "\U0001F7E9",
        Color.RED    : "\U0001F7E5",
        Color.WHITE  : "\U00002B1C",
        Color.YELLOW : "\U0001F7E8"
    }

    tries_required = [
        all(
            cell.text != " " for cell in row
        ) for row in wordle_board
    ].count(True)

    text = (
        f"Wordle {tries_required}/{Setting.MAX_TRIES}",
        "",
        "\n".join((
            "".join((
                f"{colored_box[cell.color]}" for cell in row
            )) for row in wordle_board[:tries_required]
        ))
    )

    try:
        copy("\n".join(text))
        return True

    except:
        return False

def main():
    try:
    
        picked_word  = pick_word()
        wordlist     = get_wordlist()

        console = Console()
        console.clear = (
            lambda: system("cls") if os_type == "nt" else system("clear")
        )
        
        console.show_cursor(False)
        console.clear()

        console.print(TITLE, justify="center")
        console.input(password=True)
        console.clear()

        console.print(INSTRUCTIONS, justify="center")
        console.input(password=True)
        console.clear()

        note = "Use \"<\" then Enter as Back-Space"

        current_try  = 0
        word_guessed = False

        while current_try < Setting.MAX_TRIES and not word_guessed:
            entered_letters = []
            index = 0

            while index < Setting.WORD_LEN:

                console.print(wordle_board_str(), justify="center")

                if note.endswith("is Not in Word List"):
                    console.print(f"[bold {Color.RED}]{note}[/]", justify="center")
                    note = "Use \"<\" then Enter as Back-Space"

                else:
                    console.print(f"[bold {Color.BLUE}]{note}[/]", justify="center")

                console.print(keyboard_str(), justify="center")

                entered_letter = console.input(f"\n[{Color.GRAY}]You have Typed : [/]").strip()[0]

                if entered_letter in (",", "<") and index > 0:
                    entered_letters.pop()
                    wordle_board[current_try][index - 1].text = " "

                    index -= 1

                else:
                    entered_letters.append(entered_letter)
                    wordle_board[current_try][index].text = entered_letter.upper()
                    
                    index += 1

                console.clear()

            entered_word = "".join(entered_letters)
            remarks = check(picked_word, entered_word)

            if all(_ == Remark.CORRECT for _ in remarks):
                update(current_try, remarks)
                word_guessed = True

            elif entered_word not in wordlist:            
                for index in range(Setting.WORD_LEN):
                    wordle_board[current_try][index].text = " "
                
                note = f"\"{entered_word.upper()}\" is Not in Word List"

            else:
                update(current_try, remarks)

                current_try += 1

        console.print(wordle_board_str(), justify="center")
        
        console.print(
            f"[bold {Color.GREEN}]Yay! Guesses Correctly[/]" if (
                word_guessed
            ) else f"[bold {Color.YELLOW}]Word was {picked_word}[/]", 
            justify="center"
        )

        console.print(
            f"[bold {Color.BLUE}]Wordle Copied to Clip-Board[/]" if (
                copy_to_clipboard()
            ) else f"[bold {Color.YELLOW}]Sorry! Unable to Copy Wordle[/]", 
            justify="center"
        )

        console.print(keyboard_str(), justify="center")
        
        console.input(password=True)

        console.show_cursor(True)
    
    except:
        pass

if __name__ == "__main__":

    main()
