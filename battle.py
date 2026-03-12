import enemies
import colors

import random

class BattleHandler:
	def __init__(self):
		self.player_team = []
@@ -55,7 +57,12 @@ def reset_battle(self):

	def start_battle(self):
		self.reset_battle()
		
		roll = random.randint(1, 10)
		if roll <= 9:
			self.enemy_team = [enemies.Inklin("A"),enemies.Inklin("B")]
		else:
			self.enemy_team = [enemies.Amalgam()]

		log.slow_print(f"TURN {self.turn_count}\n")
