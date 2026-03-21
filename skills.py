import colors
from log import add_message

import random

class Skill:
	"""
	A skill to be used in combat.
	"""
	
	def __init__(self, name, description, cost=None, is_physical=True, elements=None):
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
		
		if cost is None:
			cost = {
			#	"Basic": 0,
			#	"Fire": 0,
			#	"Rock": 0,
			#	"Zap": 0,
			#	"Life": 0, # Do I need all this?
			#	"Water": 0,
			#	"Poison": 0,
			#	"Truth": 0,
			#	"Lie": 0
			}
		if elements is None:
			elements = []
		
		self.name = name
		self.description = description
		self.cost = cost
		self.is_physical = is_physical
		self.elements = elements
	
	def __str__(self):
		return f"{colors.BLUE}{str.upper(self.name)}{colors.NORMAL}:\n{self.description}"
	
	def check_cost(self, user):
		for key in self.cost:
			if user.inspirations[key] < self.cost[key]:
				return False
		return True
	
	def pay_cost(self, user):
		for key in self.cost:
			user.change_inspiration(key, -self.cost[key])
	
	def check_usability(self, battle_handler, user):
		"""
		Check if this skill can be used right now.
		:param battle_handler: A battle handler to pass around.
		:type battle_handler: BattleHandler
		:param user: The party member using the skill.
		:type user: PartyMember
		:return: If it can be used.
		"""
		# This function will often be overwritten so this code MIGHT never run
		
		return self.check_cost(user)
	
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
		
		self.pay_cost(user)
		print(f"It looks like {user.name} is misusing {self.name}. Please stop them, they're gonna break something.")

class Prepare(Skill):
	def __init__(self):
		super().__init__(
			"Prepare",
			f"Gain 2 basic inspiration ({colors.BASIC})."
		)
	
	def check_usability(self, battle_handler, user):
		return user.creativity - user.get_total_inspirations() >= 2
	
	def use(self, battle_handler, user):
		inspiration_gained = user.change_inspiration("Basic", 2)
		
		add_message(f"{user.name} used {self.name}.")
		add_message(f"{user.name} gained {inspiration_gained} basic inspiration.")
		
		return {
			"Caster": user,
			"Selected Target": user,
			"Targets": [user],
			"Inspiration Gained": {
				"Basic": inspiration_gained,
			}
		}

class Splash(Skill):
	def __init__(self):
		super().__init__(
			"Splash",
			f"Gain 1 Water inspiration ({colors.WATER}) and deal 1 damage."
		)
	
	def check_usability(self, battle_handler, user):
		return user.creativity - user.get_total_inspirations() >= 1
	
	def use(self, battle_handler, user):
		inspiration_gained = user.change_inspirations("Water", 1)
		
		enemy = random.choice(battle_handler.get_living_enemies())
		
		add_message(f"{user.name} used {self.name} on {enemy.name}.")
		add_message(f"{user.name} gained {inspiration_gained} Water inspiration.")
		damage = enemy.take_damage(2)
		
		return {
			"Caster": user,
			"Selected Target": enemy,
			"Targets": [enemy],
			"Inspiration Gained": {
				"Water": inspiration_gained,
			},
			"Damage Done": [damage]
		}

class Attack(Skill):
	def __init__(self):
		super().__init__(
			"Attack",
			f"Use 1 basic inspiration ({colors.BASIC}) to deal 2 damage.",
			{
				"Basic": 1
			}
		)
	
	def use(self, battle_handler, user):
		self.pay_cost(user)
		
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
		super().__init__(
			"Electrify",
			f"Convert 1 {colors.BASIC} to 1 {colors.ZAP} and heal 1.",
			{
				"Basic": 1
			}
		)
	
	def use(self, battle_handler, user):
		self.pay_cost(user)
		inspiration_gained = user.change_inspiration("Zap", 1)
		
		add_message(f"{user.name} used {self.name}.")
		add_message(f"{user.name} gained {inspiration_gained} Zap inspiration.")
		healing = user.heal(1)
		
		return {
			"Caster": user,
			"Selected Target": user,
			"Targets": [user],
			"Inspiration Gained": {
				"Zap": inspiration_gained,
			},
			"healing Done": [healing]
		}

class HammerChop(Skill):
	def __init__(self):
		super().__init__(
			"Hammer Chop",
			f"Use 2 {colors.BASIC} and 1 {colors.ZAP} to deal 3 damage to all enemies.",
			{
				"Basic": 2,
				"Zap": 1
			}
		)
	
	def use(self, battle_handler, user):
		self.pay_cost(user)
		
		living_enemies = battle_handler.get_living_enemies()
		
		enemy = random.choice(living_enemies)
		
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

class Reboot(Skill):
	def __init__(self):
		super().__init__(
			"Reboot",
			f"Use all of your inspiration to heal 2 per inspiration used.",
			{}
		)
	
	def check_usability(self, battle_handler, user):
		return user.get_total_inspirations() >= 1
	
	def use(self, battle_handler, user):
		self.pay_cost(user)
		
		add_message(f"{user.name} used {self.name}.")
		healing = user.heal(user.get_totalinspirations() * 2)
		user.reset_inspiration()
		
		return {
			"Caster": user,
			"Selected Target": user,
			"Targets": [user],
			"healing Done": [healing]
		}

class Wonder(Skill):
	def __init__(self):
		super().__init__(
			"Wonder",
			f"Convert 1 {colors.BASIC} into a random inspiration.",
			{
				"Basic": 1
			}
		)
	
	def use(self, battle_handler, user):
		self.pay_cost(user)
		
		inspiration_type = random.choice(["Fire","Rock","Zap","Life","Water","Poison","Truth","Lie"])
		
		inspiration_gained = user.change_inspiration(inspiration_type, 1)
		
		add_message(f"{user.name} used {self.name}.")
		add_message(f"{user.name} gained {inspiration_gained} {inspiration_type} inspiration.")
		
		return {
			"Caster": user,
			"Selected Target": user,
			"Targets": [user],
			"Inspiration Gained": {
				inspiration_type: inspiration_gained,
			}
		}