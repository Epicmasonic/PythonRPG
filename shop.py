import random

#import colors
import colors
import skills
import log
import menu_input as menu

class Shop:
	def __init__(self, battle_handler):
		self.battle_handler = battle_handler
		self.gold = 0
		self.reward_mode = "Balanced"
		
		self.store_front = []
		self.possible_items = [
			BuyableSkill(skills.Electrify(), 10, battle_handler),
			BuyableSkill(skills.Splash(), 10, battle_handler),
			BuyableSkill(skills.Burn(), 10, battle_handler),
			BuyableSkill(skills.HammerChop(), 15, battle_handler),
			BuyableSkill(skills.Reboot(), 20, battle_handler),
			BuyableSkill(skills.Wonder(), 15, battle_handler)
		]
		
		self.create_store_front()
	
	def gain_rewards(self, reward):
		self.gold += reward
		log.add_message(f"You earned {reward} bits!")
	
	def create_store_front(self):
		self.store_front = []
		
		for i in range(3):
			self.store_front.append(random.choice(self.possible_items))
		self.store_front.append(Reroll())
	
	def store_menu(self): # This feels like it should be in commands.py but it probably make more sense here?
		log.slow_print("Welcome to the shop! Here are the items available for purchase:\n")
		
		item_labels = []
		for item in self.store_front:
			item_labels.append(f"{colors.GREEN}{item.name}{colors.NORMAL} - {colors.BLUE}✦ {item.cost}{colors.NORMAL}\n\t{item.description}\n")
		
		bought = menu.get_choice(self.store_front, item_labels)
		bought.buy(self)

class BuyableItem:
	def __init__(self, name, cost, description):
		self.name = name
		self.cost = cost
		self.description = description
	
	def buy(self, shop_handler):
		if shop_handler.gold >= self.cost:
			shop_handler.gold -= self.cost
			log.slow_print(f"You bought {self.name} for {self.cost} bits!")
			self.use(shop_handler)
			return True
		else:
			log.slow_print("You don't have enough bits to buy that item.")
			return False
	
	def use(self, shop_handler):
		pass

class BuyableSkill(BuyableItem):
	def __init__(self, skill, cost, battle_handler):
		super().__init__(skill.name, cost, skill.description)
		self.skill = skill
		
		self.battle_handler = battle_handler
	
	def use(self, shop_handler):
		menu.wait_for_input()
		while True:
			log.clear()
			log.slow_print(f"You who should learn {self.name}?")
			student = menu.get_choice(self.battle_handler.player_team)
			if self.skill in student.known_skills:
				log.slow_print(f"{student.name} already knows {self.name}.\n")
				log.slow_print(f"What do you want to do about this?\n")
				answer = menu.get_choice([True, False], ["Give me a refund", "Pick someone else"])
				if answer:
					shop_handler.gold += self.cost
					log.slow_print("Refunded!")
					return
			else:
				log.slow_print(f"\n{student.name} learned {self.name}!")
				student.known_skills.append(self.skill)
				return

class Reroll(BuyableItem):
	def __init__(self):
		super().__init__("Restock", 5, "Restocks the items in the shop.")
	
	def use(self, shop_handler):
		shop_handler.create_store_front()