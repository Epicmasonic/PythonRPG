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
		party_member = random.choice(battle_handler.get_living_party_members())
		add_message(f"{self.name} bites at {party_member.name}.")
		damage = party_member.take_damage(2)
		
		return {
			"Caster": self,
			"Selected Target": party_member,
			"Targets": [party_member],
			"Damage Done": damage
		}