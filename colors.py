import menu_input

NORMAL = '\033[0m'

BOLD = '\033[1m'
ITALIC = '\033[3m'
UNDER = '\033[4m'
STRIKE = '\033[9m'
INVERT = '\033[7m'
BLINK = '\033[5m' # WHY IS THIS A THING?
#ALSO_BLINK = '\033[6m' # WHY ARE THERE TWO!?

GRAY = '\033[2m'

RED = '\033[38;5;9m'
ORANGE = '\033[38;5;214m'
YELLOW = '\033[38;5;11m'
GREEN = '\033[38;5;10m'
BLUE = '\033[38;5;12m'
PURPLE = '\033[38;5;5m'
BLACK = '\033[38;5;240m'

BASIC = f"{GRAY}{ORANGE}●{NORMAL}" # That circle should be brown?
FIRE = f"{RED}●{NORMAL}"
ROCK = f"{ORANGE}●{NORMAL}"
ZAP = f"{YELLOW}●{NORMAL}"
LIFE = f"{GREEN}●{NORMAL}"
WATER = f"{BLUE}●{NORMAL}"
POISON = f"{PURPLE}●{NORMAL}"
TRUTH = f"●"
LIE = f"{GRAY}●{NORMAL}"

ALL = [
	NORMAL,
	BOLD,
	ITALIC,
	UNDER,
	STRIKE,
	INVERT,
	BLINK,
	GRAY,
	RED,
	ORANGE,
	YELLOW,
	GREEN,
	BLUE,
	PURPLE,
	BLACK
]

#print(RED + "Red" + NORMAL)
#print(ORANGE + "Orange" + NORMAL)
#print(YELLOW + "Yellow" + NORMAL)
#print(GREEN + "Green" + NORMAL)
#print(BLUE + "Blue" + NORMAL)
#print(PURPLE + "Purple" + NORMAL)
#print("White")
#print(BLACK + "Black" + NORMAL)
#
#menu_input.wait_for_input()