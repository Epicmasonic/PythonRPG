import random
import re

import colors
import log
from party_members import Battler

# The imports of shame
import os
from openai import OpenAI

try:
	token = os.environ["GITHUB_TOKEN"]
except KeyError:
	log.clear()
	log.slow_print(f"{colors.RED}Oops!{colors.NORMAL} It seems like the you haven't set up your AI API key yet.")
	log.slow_print("Please use the following command to set it up:")
	log.slow_print(f"{colors.GREEN}$Env:GITHUB_TOKEN{colors.NORMAL}{colors.GRAY}={colors.NORMAL}{colors.BLUE}\"your_token_here\"{colors.NORMAL}\n")
	
	token = None
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o-mini"

client = OpenAI(
	base_url=endpoint,
	api_key=token,
)

# result = {
# 	party: [mem1, mem2],
# 	response:{
# 		party_member: "selected  party member from party, return as a string"
# 		average_strength: "total the strength of all party members and return the average as an integer here"
# 	}
# }

SYSTEM = [
	"You are an enemy in a simple RPG.",
	"You will be given info on the game state and must use the following commands to defeat the player. You can only use 1 command each turn. You MUST include the backticks around your command.",
	"\nDeal physical damage",
	"`Attack <target> for <damage>`",
	
	"\nDeal mental damage",
	"`Convince <target> for <damage>`",
	
	"\nHeal damage",
	"`Heal <target> for <healing>`",
	
	"\nBuff or debuff",
	"`Change <target> <stat> by <amount>`",
	
	"\nThe stats of this game are the following.",
	
	"\nWill: Goes down when taking damage. If it hits 0 you'll give up fighting.",
	"Inspiration: Needed to use skills.",
	"Willpower: The maximum amount of Will you can have at once.",
	"Creativity: The maximum amount of Inspirations you can have at once.",
	"Attack: Increases physical damage dealt.",
	"Defence: Decreases physical damage received.",
	"Charisma: Increases mental damage dealt.",
	"Resolve: Decreases mental damage received."
]
SYSTEM = '\n'.join(SYSTEM)
#SYSTEM + str(result)

class Enemy(Battler):
	def __init__(self, name, health, reward, attack=0, defense=0, charisma=0, resolve=0, elemental_weaknesses=None, elemental_resistances=None):
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
		
		self.reward = reward
	
	def get_defeated(self):
		log.add_message(f"{self.name} was defeated!")

class Inklin(Enemy):
	def __init__(self,suffix=""):
		super().__init__("Inklin" + suffix, 5, 3, elemental_weaknesses=["Water"], elemental_resistances=["Poison", "Lie"])
	
	def take_turn(self, battle_handler):
		party_member = random.choice(battle_handler.get_living_party_members())
		log.add_message(f"{self.name} bites at {party_member.name}.")
		damage = party_member.take_damage(1 + self.attack)
		
		return {
			"Caster": self,
			"Selected Target": party_member,
			"Targets": [party_member],
			"Damage Done": damage
		}

class Amalgam(Enemy):
	def __init__(self,suffix=""):
		super().__init__("Amalgam" + suffix, 30, 0, 1.5, 2, 0.5)
	
	def take_turn(self, battle_handler):
		game_state = f"Turn {battle_handler.turn_count}"
		game_state += f"\n\n# You"
		game_state += f"\nWill: {self.health}/{self.max_health}"
		game_state += f"\nAttack: {self.attack}"
		game_state += f"\nDefence: {self.defense}"
		game_state += f"\nCharisma: {self.charisma}"
		game_state += f"\nResolve: {self.resolve}"
		
		for party_member in battle_handler.player_team:
			game_state += f"\n\n# {party_member.name}"
			game_state += f"\nWill {party_member.health}/{party_member.max_health}"
			game_state += f"\nAttack: {party_member.attack}"
			game_state += f"\nDefence: {party_member.defense}"
			game_state += f"\nCharisma: {party_member.charisma}"
			game_state += f"\nResolve: {party_member.resolve}"
		
		# noinspection PyBroadException
		try:
			response = client.chat.completions.create(
				messages=[
					{
						"role": "system",
						"content": SYSTEM,
					},
					{
						"role": "user",
						"content": game_state,
					}
				],
			model = "openai/gpt-4o-mini",
			temperature = 1,
			max_tokens = 4096,
			top_p = 1
			)
		except Exception:
			self.health = 0
			return {}
		
		message = re.search("`(.+?)`", response.choices[0].message.content).group(1)
#		log.add_message(game_state+"\n")
#		log.add_message(message)
		message = message.split(" ")
		
		battlers = battle_handler.player_team + battle_handler.enemy_team
		
		if message[0] == "Attack":
			for battler in battlers:
				if battler.name.lower() == message[1].lower():
					battler.take_damage(int(message[3]), True)
					break
		elif message[0] == "Convince":
			for battler in battlers:
				if battler.name.lower() == message[1].lower():
					battler.take_damage(int(message[3]), False)
					break
		
		
		return {}
