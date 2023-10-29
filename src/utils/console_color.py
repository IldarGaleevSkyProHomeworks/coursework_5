# ANSI Escape Sequences
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
ESC_FG = '\x1B[38;5;{}m'
FG_RED = ESC_FG.format(1)
FG_GREEN = ESC_FG.format(2)
FG_YELLOW = ESC_FG.format(3)
FG_MAGENTA = ESC_FG.format(5)
FG_RESET = '\x1B[0m'
