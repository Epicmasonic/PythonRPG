import colors
import log
import menu_input
import skills
from log import slow_print
from party_members import PartyMember

def command_help():
	PAGES = [
		"Skip Text",
		"Stats",
		"Float Stats",
		"Inspiration Colors"
	]
	
	TITLES = [
		"Is there a way to have text load faster?",
		"What do all the stats do?",
		"Why do some stats have decimal points?",
		"What kinds of Inspirations are there?"
	]
	
	log.slow_print(f"What would you like to learn about?")
	page = menu_input.get_choice(PAGES, TITLES)
	log.clear()
	
	match page:
		case "Skip Text":
			log.slow_print("There is!\nYou can hit any button while I'm writing for me to spit it all out at once.")
			log.slow_print("How about you try it out now? I'll keep writing and you can press something to skip it!")
			log.slow_print("\nWhat do I write though...")
			menu_input.cancelable_sleep(1)
			log.slow_print("\nHmm...")
			menu_input.cancelable_sleep(1)
			log.slow_print("\nUh...")
			menu_input.cancelable_sleep(1)
			log.slow_print("\nYeah, I've got nothing.")
			log.slow_print("Sorry about that! :P")
		
		case "Stats":
			log.slow_print("Here's the basics on each of the stats you'll see when checking on your party")
			log.slow_print(f"\n{colors.BLUE}Will{colors.NORMAL}")
			log.slow_print("Goes down when taking damage.\nIf it hits 0 you'll give up fighting.")
			log.slow_print(f"\n{colors.BLUE}Inspiration{colors.NORMAL}")
			log.slow_print("Needed to use skills.")
			log.slow_print(f"\n{colors.BLUE}Willpower{colors.NORMAL}")
			log.slow_print("The maximum amount of Will you can have at once.")
			log.slow_print(f"\n{colors.BLUE}Creative{colors.NORMAL}")
			log.slow_print("The maximum amount of Inspirations you can have at once.")
			log.slow_print(f"\n{colors.BLUE}Attack{colors.NORMAL}")
			log.slow_print("Increases physical damage dealt.")
			log.slow_print(f"\n{colors.BLUE}Defence{colors.NORMAL}")
			log.slow_print("Decreases physical damage received.")
			log.slow_print(f"\n{colors.BLUE}Charisma{colors.NORMAL}")
			log.slow_print("Increases mental damage dealt.")
			log.slow_print(f"\n{colors.BLUE}Resolve{colors.NORMAL}")
			log.slow_print("Decreases mental damage received.")
		
		case "Float Stats":
			log.slow_print("The defensive stats (Defence and Resolve) have access to the tenth place.")
			log.slow_print("Fractional defence provides a chance to block an additional point of damage.")
			log.slow_print("\nSo, if you have 1.2 Defence, you'll normally block 1 physical damage with a 20% chance to block 2 instead!")
			log.slow_print("Likewise, 3.6 Resolve will normally block 3 mental damage with a 60% chance to block 4 instead.")
		
		case "Inspiration Colors":
			log.slow_print("There are 9 different flavors of Inspiration out there.\n")
			log.slow_print(f"- {colors.GRAY + colors.ORANGE}Basic{colors.NORMAL}")
			log.slow_print(f"- {colors.RED}Fire{colors.NORMAL}")
			log.slow_print(f"- {colors.ORANGE}Rock{colors.NORMAL}")
			log.slow_print(f"- {colors.YELLOW}Zap{colors.NORMAL}")
			log.slow_print(f"- {colors.GREEN}Life{colors.NORMAL}")
			log.slow_print(f"- {colors.BLUE}Water{colors.NORMAL}")
			log.slow_print(f"- {colors.PURPLE}Poison{colors.NORMAL}")
			log.slow_print(f"- Truth")
			log.slow_print(f"- {colors.GRAY}Lie{colors.NORMAL}")
			log.slow_print("\n(Sorry if you're colorblind. :/)")
		
		case _:
			log.slow_print("Huh? How did you even do that?")
			log.slow_print("You must have somehow picked an option that doesn't exist.")
			log.slow_print("Maybe I just haven't gotten around to writing it?")

def command_party(battle_handler, shop_handler):
	party_names = []
	for party_member in battle_handler.player_team:
		party_names.append(party_member.name)
	
	slow_print("Who are you interested in?\n")
	chosen_party_member = menu_input.get_choice(battle_handler.player_team, party_names)
	log.clear()
	
	PAGES = [
		"Stats",
		#"Traits",
		"Known Skills",
		"Equipped Skills",
		"Equip Skills"
	]
	
	TITLES = [
		"Check their stats.",
		#f"What are they like? {colors.GRAY}(Traits){colors.NORMAL}",
		"See what skills do they know.",
		"See what are they planing to do.",
		"Change their plans."
	]
	
	slow_print(f"What do you want to do with {chosen_party_member.name}?\n")
	page = menu_input.get_choice(PAGES, TITLES)
	log.clear()
	
	match page:
		case "Stats":
			dashCount = len(chosen_party_member.name) + 10
			log.slow_print(colors.GREEN + "-" * dashCount)
			log.slow_print(f" {str.upper(chosen_party_member.name)}'S STATS")
			log.slow_print("-" * dashCount + f"{colors.NORMAL}\n")
			
			log.slow_print(
				f"Will:\n[{chosen_party_member.stringify_health()}] {chosen_party_member.health}/{chosen_party_member.max_health}\n")
			log.slow_print(
				f"Inspirations:\n[{chosen_party_member.stringify_inspirations()}] {chosen_party_member.get_total_inspirations()}/{chosen_party_member.creativity}\n")
			
			log.slow_print(f" Willpower: {chosen_party_member.max_health}")
			log.slow_print(f"Creativity: {chosen_party_member.creativity}")
			log.slow_print(f"    Attack: {chosen_party_member.attack}")
			log.slow_print(f"   Defense: {chosen_party_member.defense}")
			log.slow_print(f"  Charisma: {chosen_party_member.charisma}")
			log.slow_print(f"   Resolve: {chosen_party_member.resolve}\n")
			log.slow_print(f"  Collected Bits: {colors.BLUE}✦{colors.NORMAL} {shop_handler.gold}")
			log.slow_print(f"Collected Pollen: {colors.YELLOW}✿{colors.NORMAL} {chosen_party_member.experience}")
		
		#case "Traits":
		#	log.slow_print("I still haven't coded the trait system. :/")
		
		case "Known Skills":
			dashCount = len(chosen_party_member.name) + 17
			log.slow_print(colors.GREEN + "-" * dashCount)
			log.slow_print(f" {str.upper(chosen_party_member.name)}'S KNOWN SKILLS")
			log.slow_print("-" * dashCount + f"{colors.NORMAL}")
			
			for skill in chosen_party_member.known_skills:
				log.slow_print("\n" + str(skill))
		
		case "Equipped Skills":
			show_plan(chosen_party_member)
		
		case "Equip Skills":
			edit_plan(chosen_party_member)
			log.clear()
			show_plan(chosen_party_member)
		
		case _:
			log.slow_print("Huh? How did you even do that?")
			log.slow_print("You must have somehow picked an option that doesn't exist.")
			log.slow_print("Maybe I just haven't gotten around to writing it?")

def show_plan(party_member):
	dashCount = len(party_member.name) + 15
	log.slow_print(colors.GREEN + "-" * dashCount)
	log.slow_print(f" {party_member.name.upper()}'S PRIORITIES")
	log.slow_print("-" * dashCount + f"{colors.NORMAL}\n")
	
	if len(party_member.equipped_skills) <= 0:
		log.slow_print("None :(")
	else:
		i = 1
		for skill in party_member.equipped_skills:
			log.slow_print(f"{i}: {colors.BLUE}{skill.name}{colors.NORMAL}")
			i += 1

def edit_plan(party_member):
	skill_names = [skill.name for skill in party_member.known_skills]
	
	log.slow_print("What skill do you want to change?\n")
	selected_skill = menu_input.get_choice(party_member.known_skills, skill_names)
	log.clear()
	
	skill_ids = []
	skill_names = []
	index = 0
	for skill in party_member.equipped_skills:
		if skill == selected_skill:
			skill_ids.append(-1)
			skill_names.append(f"{colors.GRAY}(Unequip){colors.NORMAL}")
		else:
			skill_ids.append(index)
			skill_names.append(skill.name)
			index += 1
	skill_ids.append(-2)
	skill_names.append(f"{colors.GRAY}(Add){colors.NORMAL}")
	
	log.slow_print(f"Where do you want to add {selected_skill.name}?")
	target = menu_input.get_choice(skill_ids, skill_names)
	
	party_member.edit_skill(selected_skill, target)

def command_shop(battle_handler, shop_handler):
	log.slow_print(f"Your balance: {colors.BLUE}✦{colors.NORMAL} {shop_handler.gold} bits\n")
	
	log.slow_print("I haven't coded the shop yet. :/")

def command_rest(battle_handler):
	battle_handler.reset_battle()
	
	for party_member in battle_handler.player_team:
		party_member.health = party_member.max_health
	
	for party_member in battle_handler.player_team:
		for key in party_member.inspirations:
			party_member.inspirations[key] = 0
	
	log.slow_print("Everyone was fully healed!")

def command_fight(battle_handler, shop_handler):
	PAGES = [
		"Single",
		"Semi Auto",
		"Auto",
		#"Full Auto"
	]
	
	TITLES = [
		"Just run a single turn.",
		"Run though turns until someone wins.",
		"Run though turns automatically until someone wins.",
		#"Automatically run as many battles as we can."
	]
	
	slow_print(f"How much fighting do you want to do?\n")
	speed = menu_input.get_choice(PAGES, TITLES)
	log.clear()
	
	if speed == "Single":
		battle_handler.run_turn()
		return
	
	input_needed = False
	delay = 0
	
	if speed == "Semi Auto":
		input_needed = True
	else:
		while True:
			delay = input("How many seconds do you want to wait?\n\n> ")
			try:
				delay = float(delay)
				break
			except ValueError:
				print("\nPlease enter a number")
				menu_input.cancelable_sleep(1)
				log.clear()
		log.clear()
	
	
	extra_loop = False
	first_loop = True
	while True:
		battle_handler.run_turn(not first_loop, not input_needed)
		
		if battle_handler.check_for_win() or battle_handler.check_for_loss():
			if extra_loop or first_loop:
				break
			extra_loop = True
		
		if input_needed:
			menu_input.eat_input()
			menu_input.wait_for_input()
		else:
			menu_input.eat_input()
			menu_input.cancelable_sleep(delay)
		log.clear()
		
		first_loop = False

def command_create(battle_handler):
	temp = PartyMember("Unnamed",15,5)
	temp.known_skills = [skills.Prepare(), skills.Attack()]
	
	delay = None
	while True:
		print(end=colors.GRAY)
		log.slow_print(f"Name: {temp.name}\n", delay)
		
		log.slow_print(f" Willpower: {temp.max_health}", delay)
		log.slow_print(f"Creativity: {temp.creativity}", delay)
		log.slow_print(f"    Attack: {temp.attack}", delay)
		log.slow_print(f"   Defense: {temp.defense}", delay)
		log.slow_print(f"  Charisma: {temp.charisma}", delay)
		log.slow_print(f"   Resolve: {temp.resolve}\n", delay)
		print(end=colors.NORMAL)
		
		log.slow_print("What do you want to edit?\n")
		
		options = [
			"Name",
			"Stats",
			#"Traits",
			"Save",
			"Exit"
		]
		labels = [
			"Change their name.",
			"Reassign stats.",
			#"Pick traits.",
			"I'm done!",
			"Nevermind..."
		]
		
		field = menu_input.get_choice(options, labels)
		log.undo_line(len(options) + 4)
		
		match field:
			case "Name":
				log.slow_print("What do you want them to be called?\n")
				temp.name = input(f"{colors.GRAY}>{colors.NORMAL} ")
			
			case "Stats":
				log.slow_print("Pick a stat to edit.\n")
				stat_type = menu_input.get_choice([
					"Willpower",
					"Creativity",
					"Attack",
					"Defense",
					"Charisma",
					"Resolve"
				])
				
				log.undo_line(10)
				log.slow_print(f"What do you want to set their {stat_type.lower()} to?\n")
				log.slow_print("(I would have added something of stat buy system but I wasn't sure how to balance it so...\nPlease don't make your characters too overpowered?)\n")
				
				#stat_amount = None
				while True:
					stat_amount = input(f"{colors.GRAY}>{colors.NORMAL} ")
					try:
						stat_amount = float(stat_amount)
						break
					except ValueError:
						print("\nPlease enter a number")
						menu_input.cancelable_sleep(1)
						log.undo_line(3)
				
				if not (stat_type == "Defense" or stat_type == "Resolve"):
					stat_amount = round(stat_amount)
				
				if stat_type == "Willpower":
					temp.health = stat_amount
					temp.max_health = stat_amount
				else:
					exec(f"temp.{stat_type.lower()} = {stat_amount}")
			
			case "Save":
				name_used = False
				for party_member in battle_handler.player_team:
					if party_member.name.lower() == temp.name.lower():
						name_used = True
						break
				
				if name_used:
					log.slow_print(f"{colors.RED}Whoops!{colors.NORMAL}")
					log.slow_print("That name is already in use.\nPlease change it")
				else:
					log.slow_print(f"{temp.name} was added to your party!")
					battle_handler.player_team.append(temp)
					break
			
			case "Exit":
				log.slow_print(f"{temp.name} was left behind...")
				break
			
			case _:
				log.slow_print("Huh? How did you even do that?")
				log.slow_print("You must have somehow picked an option that doesn't exist.")
				log.slow_print("Maybe I just haven't gotten around to writing it?")
				menu_input.eat_input()
				menu_input.wait_for_input()
		
		log.clear()
		delay = 0