import colors
import data_handling
import log
import skills
#import traits

import math

class Battler:
	"""
	A parent object for anything that can participate in a battle.
	"""
	def __init__(self, name, health, attack=0, defense=0, charisma=0, resolve=0, elemental_weaknesses=None, elemental_resistances=None):
		"""
		:param name: Name of the character.
		:type name: str
		:param health: How much damage they can take before they die.
		:type health: int
		:param attack: Affects physical damage dealt.
		:type attack: float
		:param defense: Affects physical damage received.
		:type defense: float
		:param charisma: Affects mental damage dealt.
		:type charisma: float
		:param resolve: Affects mental damage received.
		:type resolve: float
		:param elemental_weaknesses: A list of elements that the character is weak to.
		:type elemental_weaknesses: list[str]
		:param elemental_resistances: A list of elements that the character is strong against.
		:type elemental_resistances: list[str]
		"""
		
		if elemental_resistances is None:
			elemental_resistances = []
		if elemental_weaknesses is None:
			elemental_weaknesses = []
		
		self.name = name
		self.max_health = health
		self.health = health
		self.attack = attack
		self.defense = defense
		self.charisma = charisma
		self.resolve = resolve
		self.elemental_resistances = elemental_resistances
		self.elemental_weaknesses = elemental_weaknesses
	
	#def __str__(self):
	#	return self.name
	
	def __repr__(self):
		return self.name
	
	def is_living(self):
		return self.health > 0
	
	def stringify_health(self):
		"""
		:return: A health bar
		:rtype: str
		"""
		
		string = ""
		
		if self.health > self.max_health:
			string += colors.BLUE
		elif self.health > round(self.max_health / 3 * 2):
			string += colors.GREEN
		elif self.health > round(self.max_health / 3):
			string += colors.YELLOW
		else:
			string += colors.RED
		
		string += "■" * min(self.health, self.max_health) + " " * (self.max_health - self.health)
		string += colors.NORMAL
		
		return string
	
	def take_damage(self, damage, physical=True, elements=None):
		"""
		Lowers the battler's health by a value
		:param damage: Base damage value
		:type damage: int
		:param physical: Whether this is physical or mental damage
		:type physical: bool
		:param elements:
		:type elements: list[str]
		:return:
		"""

		if elements is None:
			elements = []
		
		lucky = False
		if physical:
			blocked, lucky = data_handling.randomRound(self.defense)
			damage -= blocked
		else:
			blocked, lucky = data_handling.randomRound(self.resolve)
			damage -= blocked
		
		if damage < 0:
			damage = 0
		
		self.health -= damage
		if self.health < 0:
			self.health = 0
		
		if lucky:
			if physical:
				log.add_message(f"{self.name} holds strong!")
			else:
				log.add_message(f"{self.name} doesn’t budge!")
		log.add_message(f"{self.name} took {damage} damage.")
		
		if self.health == 0:
			self.get_defeated()
		
		return damage
	
	def get_defeated(self):
		log.add_message(f"{self.name} forgot to update their get_defeated()")
	
	def heal(self, healing=0):
		self.health += healing
		if self.health > self.max_health:
			self.health = self.max_health
		log.add_message(f"{self.name} healed {healing}.")
	
	def take_turn(self, battle_handler):
		"""
		Runs though battler specific code to handle each turn.
		:param battle_handler: A battle handler to pass around.
		:type battle_handler: BattleHandler
		"""
		
		# This function should be overwritten so this code SHOULD never run
		print(f"{self.name} seems to have forgotten how battles work. Please stop them, they're gonna break something.")
		return {}

class PartyMember(Battler):
	def __init__(self, name, health, creativity, attack=0, defense=0, charisma=0, resolve=0, elemental_weaknesses=None, elemental_resistances=None):
		"""
		:param name: Name of the character.
		:type name: str
		:param health: How much damage they can take before they die.
		:type health: int
		:param creativity: How many inspirations they can hold.
		:type creativity: int
		:param attack: Affects physical damage dealt.
		:type attack: float
		:param defense: Affects physical damage received.
		:type defense: float
		:param charisma: Affects mental damage dealt.
		:type charisma: float
		:param resolve: Affects mental damage received.
		:type resolve: float
		:param elemental_weaknesses: A list of elements that the character is weak to.
		:type elemental_weaknesses: list[str]
		:param elemental_resistances: A list of elements that the character is strong against.
		:type elemental_resistances: list[str]
		"""
		
		super().__init__(name, health, attack, defense, charisma, resolve, elemental_weaknesses, elemental_resistances)
		self.creativity = creativity
		self.experience = 0
		
		self.inspirations = {}
		self.reset_inspiration()
		
		self.known_skills = []
		
		self.equipped_skills = []
	
	def get_defeated(self):
		log.add_message(f"{self.name} has given up...")
	
	def edit_skill(self, skill, target):
		if skill in self.equipped_skills:
			self.equipped_skills.remove(skill)
		
		if target == -2:
			self.equipped_skills.append(skill)
		elif target != -1:
			self.equipped_skills.insert(target, skill)
	
	def change_inspiration(self, inspiration_type, count):
		if -count > self.inspirations[inspiration_type]:
			count = -self.inspirations[inspiration_type]
		
		empty_slots = self.creativity - self.get_total_inspirations()
		if count > empty_slots:
			count = empty_slots
		
		self.inspirations[inspiration_type] += count
		return count
	
	def reset_inspiration(self):
		self.inspirations = {
			"Basic": 0,
			"Fire": 0,
			"Rock": 0,
			"Zap": 0,
			"Life": 0,
			"Water": 0,
			"Poison": 0,
			"Truth": 0,
			"Lie": 0
		}
	
	def get_total_inspirations(self):
		total = 0
		for count in self.inspirations.values():
			total += count
		
		return total
	
	def stringify_inspirations(self):
		string = ""
		total_inspirations = 0
		
		for inspiration, count in self.inspirations.items():
			total_inspirations += count
			match inspiration:
				case "Basic":
					string += colors.BASIC * count
				case "Fire":
					string += colors.FIRE * count
				case "Rock":
					string += colors.ROCK * count
				case "Zap":
					string += colors.ZAP * count
				case "Life":
					string += colors.LIFE * count
				case "Water":
					string += colors.WATER * count
				case "Poison":
					string += colors.POISON * count
				case "Truth":
					string += colors.TRUTH * count
				case "Lie":
					string += colors.LIE * count
		string += " " * (self.creativity - total_inspirations) # If only there was a blank emoji... (For keeping the spacing the same)
		
		return string
	
	def take_turn(self, battle_handler):
		"""
		Tries to decide what skill to use on their turn.
		:param battle_handler: A battle handler to pass around.
		:type battle_handler: BattleHandler
		"""
		if len(self.equipped_skills) > 0:
			for skill in self.equipped_skills:
				if skill.check_usability(battle_handler, self):
					return skill.use(battle_handler, self)
		
		log.add_message(f"{self.name} couldn't think of a skill to use!")
		return {}

class Groove(PartyMember):
	def __init__(self):
		"""
		It him! :D
		"""
		super().__init__("Groove",15,5,1,0.2,0,1.0,["Water"],["Lie"])
		
		self.known_skills = [
			skills.Prepare(),
			skills.Attack()
		]