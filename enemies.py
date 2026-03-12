import colors
from log import add_message
#from index import battle_handler
from party_members import Battler

import random

class Enemy(Battler):
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
		
		super().__init__(name, health, attack, defense, charisma, resolve, elemental_weaknesses, elemental_resistances)

class Inklin(Enemy):
	def __init__(self,suffix=""):
		super().__init__("Inklin" + suffix, 5, elemental_weaknesses=["Water"], elemental_resistances=["Poison", "Lie"])
	
	def take_turn(self, battle_handler):
		living_party_members = []
		for party_member in battle_handler.player_team:
			if party_member.health > 0:
				living_party_members.append(party_member)
		
		party_member = random.choice(living_party_members)
		add_message(f"{self.name} bites at {party_member.name}.")
		damage = party_member.take_damage(2)
		
		return {
			"Caster": self,
			"Selected Target": party_member,
			"Targets": [party_member],
			"Damage Done": damage
		}

class Amalgam(Enemy):
	def __init__(self,suffix=""):
		super().__init__("Amalgam" + suffix, 30)
	
	def take_turn(self, battle_handler):
		plan = {}
		dice = random.randint(1, 2)
		
		if dice == 1:
			plan["Team"] = "Player"
			plan["Selected Target"] = random.choice(battle_handler.get_living_party_members())
			plan["Targets"] = [random.choice(battle_handler.get_living_party_members())]
		else:
			plan["Team"] = "Enemy"
			plan["Selected Target"] = random.choice(battle_handler.get_living_enemies())
			plan["Targets"] = [random.choice(battle_handler.get_living_enemies())]
		
		dice = random.randint(1, 4)
		if dice == 4:
			if plan["Team"] == "Player":
				plan["Targets"] = battle_handler.get_living_party_members()
			else:
				plan["Targets"] = battle_handler.get_living_enemies()
		
		
		add_message(f"{self.name}... did... something?")
		damage = random.randint(1, 10)
		
		plan["Damage Done"] = []
		for battler in plan["Targets"]:
			plan["Damage Done"].append(battler.take_turn(damage))
		
		plan["Caster"] = self
		return plan
