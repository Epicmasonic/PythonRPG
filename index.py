# Just so you know. I asked Gemini (not Google) how to do docstrings :/
# And log.clear is still AI

# AND Gemini told me to use flush=True in log.slow_print :(

print("Loading...")

import menu_input
import commands
import colors
import log

import shop
shop_handler = shop.Shop()
import battle
battle_handler = battle.BattleHandler(shop_handler) # Bit of a hack to let `enemies.py` access `shop` but it wouldn't work as just a `import` so...
from party_members import Groove
battle_handler.player_team.append(Groove())

# Debug stuff
#battle_handler.player_team[0].health = 10
#battle_handler.player_team[0].inspirations["Basic"] = 2

COMMANDS = [
	"Help",
	"Party",
	"Rest",
	"Shop",
	"Fight",
	"Create",
	"Exit"
]

MENU_ITEMS = [
	"Learn more about mechanics.",
	"Check in on my party.",
	f"Take a break. {colors.GRAY}(Save){colors.NORMAL}",
	"Visit the shop.",
	"Get into a fight!",
	"Recruit more fighters.",
	"Get out of here!"
]

log.clear() # For if you run it though the console
log.slow_print(f"{colors.RED}WARNING:{colors.NORMAL}\nThis program will only work properly when run though the terminal.")
log.slow_print("If you're trying to run it though PyCharm's console, it will not work.")
menu_input.eat_input()
menu_input.wait_for_input()
log.clear()

while True:
	log.slow_print(f"{colors.GREEN}Welcome to my little(?) RPG project!{colors.NORMAL}\nWhat do you want to do?\n")
	key = menu_input.get_choice(COMMANDS,MENU_ITEMS)
	log.clear()
	
	match key:
		case "Exit":
			log.slow_print("I hope you had fun! :)")
			menu_input.wait_for_input()
			break
		case "Help":
			commands.command_help()
		case "Party":
			commands.command_party(battle_handler, shop_handler)
		case "Shop":
			commands.command_shop(battle_handler, shop_handler)
		case "Rest":
			commands.command_rest(battle_handler)
		case "Fight":
			commands.command_fight(battle_handler, shop_handler)
		case "Create":
			commands.command_create(battle_handler)
		case _:
			log.slow_print(f"{colors.RED}Whoops!{colors.NORMAL}")
			log.slow_print("I'm not done coding this part yet.")
	
	menu_input.eat_input()
	menu_input.wait_for_input()
	log.clear()

log.clear()