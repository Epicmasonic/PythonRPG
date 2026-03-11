import colors
from log import add_message

import random

class Skill:
	"""
	A skill to be used in combat.
	"""
	
	def __init__(self, name, description, is_physical=True, elements=None):
		"""
		:param name: Name of the skill.
		:type name: str
		:param description: Description of the skill.
		:type description: str
		:param is_physical: Whether the skill is physical or mental.
		:type is_physical: bool
		:param elements: List of the elements of the skill.
		:type elements: list[str]
		"""
		
		if elements is None:
			elements = []
		
		self.name = name
		self.description = description
		self.is_physical = is_physical
		self.elements = elements
	
	def __str__(self):
		return f"{colors.BLUE}{str.upper(self.name)}{colors.NORMAL}:\n{self.description}"
	
	def check_usability(self, battle_handler, user):
		"""
		Check if this skill can be used right now.
		:param battle_handler: A battle handler to pass around.
		:type battle_handler: BattleHandler
		:param user: The party member using the skill.
		:type user: PartyMember
		:return: If it can be used.
		"""
		# This function should be overwritten so this code SHOULD never run
		
		return True
	
	def use(self, battle_handler, user):
		"""
		Runs the skill.
		:param battle_handler: A battle handler to pass around.
		:type battle_handler: BattleHandler
		:param user: The party member using the skill.
		:type user: PartyMember
		:return: Various information on the used skill that might be useful for other effects to know.
		:rtype: dict
		"""
		# This function should be overwritten so this code SHOULD never run
		
		print(f"It looks like {user.name} is misusing {self.name}. Please stop them, they're gonna break something.")

class Prepare(Skill):
	def __init__(self):
		super().__init__("Prepare",f"Gain 2 basic inspiration ({colors.BASIC}).")
	
	def use(self, battle_handler, user):
		user.inspirations["Basic"] += 2
		
		add_message(f"{user.name} used {self.name}.")
		add_message(f"{user.name} gained 2 basic inspiration.")
		
		return {
			"Caster": user,
			"Selected Target": user,
			"Targets": [user]
		}

class Splash(Skill):
	def __init__(self):
		super().__init__("Splash", f"Gain 1 Water inspiration ({colors.WATER}) and deal 1 damage.")
	
	def use(self, battle_handler, user):
		user.inspirations["Water"] += 1
		
		enemy = random.choice(battle_handler.get_living_enemies())
		
		add_message(f"{user.name} used {self.name} on {enemy.name}.")
		add_message(f"{user.name} gained 1 Water inspiration.")
		damage = enemy.take_damage(2)
		
		return {
			"Caster": user,
			"Selected Target": enemy,
			"Targets": [enemy],
			"Damage Done": [damage]
		}

class Attack(Skill):
	def __init__(self):
		super().__init__("Attack",f"Use 1 basic inspiration ({colors.BASIC}) to deal 2 damage.")
	
	def check_usability(self, battle_handler, user):
		return user.inspirations["Basic"] >= 1
	
	def use(self, battle_handler, user):
		user.inspirations["Basic"] -= 1
		
		enemy = random.choice(battle_handler.get_living_enemies())
		
		add_message(f"{user.name} used {self.name} on {enemy.name}.")
		damage = enemy.take_damage(2)
		
		return {
			"Caster": user,
			"Selected Target": enemy,
			"Targets": [enemy],
			"Damage Done": [damage]
		}

class Electrify(Skill):
	def __init__(self):
		super().__init__("Electrify",f"Convert 1 {colors.BASIC} to 1 {colors.ZAP} and heal 1.")
	
	def check_usability(self, battle_handler, user):
		return user.inspirations["Basic"] >= 1
	
	def use(self, battle_handler, user):
		user.inspirations["Basic"] -= 1
		user.inspirations["Zap"] += 1
		
		add_message(f"{user.name} used {self.name}.")
		add_message(f"{user.name} gained 1 Zap inspiration.")
		healing = user.heal(1)
		
		return {
			"Caster": user,
			"Selected Target": user,
			"Targets": [user],
			"healing Done": [healing]
		}

class HammerChop(Skill):
	def __init__(self):
		super().__init__("Hammer Chop",f"Use 2 {colors.BASIC} and 1 {colors.ZAP} to deal 3 damage to all enemies.")
	
	def check_usability(self, battle_handler, user):
		return (
			user.inspirations["Basic"] >= 2 and
			user.inspirations["Zap"] >= 1
		)
	
	def use(self, battle_handler, user):
		user.inspirations["Basic"] -= 2
		user.inspirations["Zap"] -= 1
		
		living_enemies = battle_handler.get_living_enemies()
		
		add_message(f"{user.name} used {self.name}.")
		damage = []
		for enemy in living_enemies:
			damage.append(enemy.take_damage(3))
		
		return {
			"Caster": user,
			"Selected Target": enemy,
			"Targets": living_enemies,
			"Damage Done": damage
		}