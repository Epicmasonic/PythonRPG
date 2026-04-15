#from index import battle
import skills
from log import add_message

class Shop:
	def __init__(self):
		self.gold = 0
		self.reward_mode = "Balanced"
		
		self.store_front = []
		self.possible_items = [
			BuyableSkill(skills.Electrify(), 10),
			BuyableSkill(skills.HammerChop(), 15),
			BuyableSkill(skills.Reboot(), 20)
		]
		
		self.create_store_front()
	
	def gain_rewards(self, reward):
		self.gold += reward
		add_message(f"You earned {reward} bits!")
	
	def create_store_front(self):
		self.store_front = []
		
		for i in range(3):
			self.store_front.append({
				"name": "Health Potion",
				"cost": 10,
				"description": "Restores 20 health."
			})

class BuyableItem:
	def __init__(self, name, cost, description):
		self.name = name
		self.cost = cost
		self.description = description

class BuyableSkill(BuyableItem):
	def __init__(self, skill, cost):
		super().__init__(skill.name, cost, skill.description)
		self.skill = skill
		self.cost = cost