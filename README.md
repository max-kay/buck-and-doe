# Buck and Doe

A CLI version of the pen and paper game.

## Usage
```
python main.py [--count <int>] [--len <int>] [-C] [-L] [--debug]

    --count | -c     number of symbols     default: 8
    --len   | -l     length of the secret  default: 5
    -C               disable colors
    -L               enable logging
    --debug          print the secret on each turn
```

To use the script with uv use:
`uv run python main.py`

## The Game
Each turn you can guess the secret.
The input is case insensitive for an empty slot `_` can be used.
Use the arrow keys to get the last input.
