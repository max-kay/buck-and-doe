# Buck and Doe

A CLI version of the pen and paper game.

## Usage
```
Buck and Doe - Usage
buck-and-doe [--count <int>] [--len <int>] [-C] [-L]

    --count   | -c   number of symbols     default: 8
    --len     | -l   length of the secret  default: 5
    -C               disable colors
    -L               disable logging

    --help           print this help
    --explain | -e   print an explantion of the game
    --debug          show the secret
```

To use the script with uv use:
`uv run python main.py`

## The Game
Each turn you can guess the secret.
The input is case insensitive for an empty slot `_` can be used.
Use the arrow keys to get the last input.
