import random
import readline
from os import get_terminal_size

MARGIN = "    "

GREEN = "\033[0;32m"
GRAY = "\033[0;61m"
YELLOW = "\033[0;33m"
WHITE = "\033[0;37m"


def clear() -> None:
    print("\033[2J\033[H", end="")


def print_centered(s: str) -> None:
    term_width = get_terminal_size().columns
    for line in s.splitlines():
        margin = (term_width - len(line)) // 2
        print(" " * margin + line)


TITLE = r"""  ___         _                  _   ___
 | _ )_  _ __| |__  __ _ _ _  __| | |   \ ___  ___
 | _ \ || / _| / / / _` | ' \/ _` | | |) / _ \/ -_)
 |___/\_,_\__|_\_\ \__,_|_||_\__,_| |___/\___/\___|

"""

TITLE_WIDTH = max(len(line) for line in TITLE.splitlines())

WIN_MSG = r"""                                  .''.
      .''.      .        *''*    :_\/_:     .
     :_\/_:   _\|/_  .:.*_\/_*   : /\ :  .'.:.'.
 .''.: /\ :   ./|\   ':'* /\ * :  '..'.  -=:o:=-
:_\/_:'.:::.    ' *''*    * '.\'/.' _\|/_'.':'.'
: /\ : :::::     *_\/_*     -= o =-  /|\    '  *
 '..'  ':::'     * /\ *     .'/.\'.   '
     *            *..*         :
       *
       *
"""

WIN_MSG_WIDTH = max(len(line) for line in WIN_MSG.splitlines())


class Game:
    def __init__(
        self,
        num_symbols: int | None,
        len_secret: int | None,
        debug: bool,
        log: bool,
    ):
        readline.set_auto_history(False)
        if not num_symbols:
            self.num_symbols: int = 8
        else:
            self.num_symbols: int = num_symbols

        if not len_secret:
            self.len_secret: int = 5
        else:
            self.len_secret: int = len_secret
        self.valid_symbols: list[str] = [
            chr(i + ord("A")) for i in range(self.num_symbols)
        ]
        self.status: str = ""
        self.guesses: list[list[str]] = []
        self.secret = [
            random.choice(self.valid_symbols) for _i in range(self.len_secret)
        ]
        self.secret_count = {c: 0 for c in self.valid_symbols}
        for c in self.secret:
            self.secret_count[c] += 1
        self.debug = debug
        self.log_enabeled = log
        self.last_input_valid = True

    def print_state(self, in_game: bool = True) -> None:
        term_width = get_terminal_size().columns
        margin = (term_width - TITLE_WIDTH) // 2
        print(YELLOW, end="")
        for line in TITLE.splitlines():
            print(" " * margin + line)
        print(WHITE, end="")

        print()

        template = "{number: >2})" + MARGIN + "{guess}" + MARGIN + "{check}"
        example = template.format(
            number=0,
            guess=" ".join(["A"] * self.len_secret),
            check=self.check_guess(["A"] * self.len_secret, use_colors=False),
        )

        line_len = len(example)
        left_margin = (term_width - line_len) // 2

        first_symbol = example.find("A")

        if in_game:
            symbols = "symbols:" + MARGIN
            print(
                " " * (left_margin + first_symbol - len(symbols))
                + symbols
                + " ".join(self.valid_symbols)
            )
            print()

            secret = "secret:" + MARGIN
            if not self.debug:
                print(
                    " " * (left_margin + first_symbol - len(secret))
                    + secret
                    + " ".join(["_"] * self.len_secret)
                    + MARGIN
                    + f"({self.len_secret})"
                )
            else:
                print(
                    " " * (left_margin + first_symbol - len(secret))
                    + secret
                    + " ".join(self.secret)
                    + MARGIN
                    + f"({self.len_secret})"
                )
            print()

        for i, guess in enumerate(self.guesses):
            print(
                " " * left_margin
                + template.format(
                    number=i + 1,
                    guess=" ".join(guess),
                    check=self.check_guess(guess),
                )
            )
        if in_game:
            print()
            print(" " * left_margin + self.status, end="")
        return first_symbol + left_margin

    def check_guess(self, guess: list[str], use_colors=True) -> str:
        count = {c: 0 for c in self.valid_symbols}
        for c in guess:
            if c != "_":
                count[c] += 1
        correct_sym = 0
        for c in self.valid_symbols:
            correct_sym += min(count[c], self.secret_count[c])
        correct_pos = 0
        for a, b in zip(self.secret, guess):
            if a == b:
                correct_pos += 1
        return (
            (GREEN if use_colors else "")
            + "+" * correct_pos
            + (YELLOW if use_colors else "")
            + "-" * (correct_sym - correct_pos)
            + (GRAY if use_colors else "")
            + "." * (self.len_secret - correct_sym)
            + (WHITE if use_colors else "")
        )

    def parse_line(self, s: str) -> None:
        guess = []
        for c in s:
            if c == " " or c == "\n":
                continue
            upper = c.upper()
            if upper in self.valid_symbols or upper == "_":
                guess.append(upper)
            else:
                readline.add_history(s)
                self.status = f"invalid symbol {upper}\n"
                return

        readline.add_history(" ".join(guess))

        if len(guess) < self.len_secret:
            self.status = f"not enough symbols in {' '.join(guess)}\n"
            return
        if len(guess) > self.len_secret:
            self.status = f"too many symbols in {' '.join(guess)}\n"
            return
        self.guesses.append(guess)
        self.status = ""

    def end_success(self) -> None:
        self.log()
        clear()
        self.print_state(in_game=False)
        print()
        if len(self.guesses) == 1:
            print_centered("You guessed correctely in only one guess!")
        else:
            print_centered(f"You guessed correctely in {len(self.guesses)} guesses!")
        print()
        margin = (get_terminal_size().columns - WIN_MSG_WIDTH) // 2
        for line in WIN_MSG.splitlines():
            print(" " * margin + line)

        exit()

    def end_defeat(self) -> None:
        clear()
        first_symbol = self.print_state(in_game=False)
        print()
        msg = "secret was:" + MARGIN
        print(" " * (first_symbol - len(msg)) + msg + " ".join(self.secret))
        print()
        print_centered("You gave up!")
        exit()

    def round(self) -> None:
        clear()
        margin = self.print_state()
        try:
            text = input(" " * margin)
            self.parse_line(text)
            if self.guesses and self.guesses[-1] == self.secret:
                self.end_success()
        except EOFError:
            self.end_defeat()

    def serialize(self) -> str:
        import json

        as_dict = {
            "count": len(self.valid_symbols),
            "len": self.len_secret,
            "secret": " ".join(self.secret),
            "guesses": [" ".join(g) for g in self.guesses],
        }
        return json.dumps(as_dict, indent=2)

    def log(self):
        if not self.log_enabeled:
            return
        import datetime

        with open(
            f"logs/{datetime.datetime.today().isoformat()}.json", mode="w"
        ) as file:
            print(self.serialize(), file=file, end="")


def print_usage():
    print("Buck and Doe - Usage")
    print("buck-and-doe [--count <int>] [--len <int>] [-C] [-L]")
    print()
    print("    --count   | -c   number of symbols     default: 8")
    print("    --len     | -l   length of the secret  default: 5")
    print("    -C               disable colors")
    print("    -L               enable logging")
    print()
    print("    --help           print this help")
    print("    --explain | -e   print an explantion of the game")
    print("    --debug          show the secret")


def print_explainer():
    print("Buck and Doe")
    print()
    print("The goal of the game is to guess the secret.")
    print("Each turn you can make one guess.")
    print("The guess is checked and for each correct symbol a + is given")
    print("and for each symbol which is in the secret but at the wrong")
    print("position a - is given.")
    print()
    print("e.g. if the secret is A B C D and you guessed B B E C")
    print("The result will be +-..")
    print("the + for the correct guess of B")
    print("and the - for the correct guess of C which is not at its correct position")
    print()
    print("The game ends when you guess the secret correctly.")
    print()
    print("Your input is treated case insensitively and spaces are ignored.")
    print("You can use `_` as a placeholder")


def parse_argv() -> Game:
    import sys

    for s in sys.argv:
        if s in ["help", "--help", "-help", "-h"]:
            print_usage()
            exit()
    for s in sys.argv:
        if s in ["--explain", "-e"]:
            print_explainer()
            exit()
    argiter = iter(sys.argv)
    num_symbols = None
    len_secret = None
    debug = False
    log = False
    try:
        while True:
            flag = next(argiter)
            if flag in ["--count", "-c"]:
                try:
                    num = int(next(argiter))
                    if not 1 <= num <= 26:
                        print("num symbols must be between 1 and 26")
                    num_symbols = num
                except ValueError:
                    print("invalid count argument")
            elif flag in ["--len", "-l"]:
                try:
                    num = int(next(argiter))
                    if num < 1:
                        print("the length of the secret must at least be 1")
                    len_secret = num
                except ValueError:
                    print("invalid count argument")
            elif flag == "-C":
                global WHITE, YELLOW, GREEN, GRAY
                WHITE = ""
                YELLOW = ""
                GREEN = ""
                GRAY = ""
            elif flag == "-L":
                log = True
            elif flag == "--debug":
                debug = True
            else:
                print(f"flag `{flag}` not recognized")
                print_usage()
    except StopIteration:
        pass
    return Game(num_symbols, len_secret, debug, log)


if __name__ == "__main__":
    game = parse_argv()
    while True:
        game.round()
