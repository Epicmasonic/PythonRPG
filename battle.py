import log

import enemies
import colors

import random

class BattleHandler:
	def __init__(self, shop_handler=None):
		self.shop_handler = shop_handler
		
		self.player_team = []
		self.enemy_team = []
		
		self.turn_count = 0
		self.player_tick = 0
		self.enemy_tick = 0
		
		self.seen_win = None
	
	def get_living_party_members(self):
		living_party_members = []
		
		for party_member in self.player_team:
			if party_member.is_living():
				living_party_members.append(party_member)
		
		return living_party_members
	
	def get_living_enemies(self):
		living_enemies = []
		
		for enemy in self.enemy_team:
			if enemy.is_living():
				living_enemies.append(enemy)
		
		return living_enemies
	
	def check_for_win(self):
		for enemy in self.enemy_team:
			if enemy.is_living():
				return False
		return True
	
	def check_for_loss(self):
		for party_member in self.player_team:
			if party_member.is_living():
				return False
		return True
	
	def reset_battle(self):
		self.turn_count = 0
		self.player_tick = -1
		self.enemy_tick = -1
		
		self.enemy_team = []
		
		self.seen_win = False
	
	def start_battle(self, skip_intro=False):
		self.reset_battle()
		
		roll = random.randint(1, 10)
		if roll <= 9:
			self.enemy_team = [enemies.Inklin("A"),enemies.Inklin("B")]
		else:
			self.enemy_team = [enemies.Amalgam()]
		
		delay = None
		if skip_intro:
			delay = 0
		
		log.slow_print(f"TURN {self.turn_count}\n", delay)
		
		log.slow_print(f"{colors.GREEN}PLAYER TEAM:{colors.NORMAL}\n", delay)
		for party_member in self.player_team:
			log.slow_print(f"{party_member.name}:", delay)
			log.slow_print(f"[{party_member.stringify_health()}] {party_member.health}/{party_member.max_health}", delay)
			log.slow_print(f"[{party_member.stringify_inspirations()}] {party_member.get_total_inspirations()}/{party_member.creativity}\n", delay)
		
		log.slow_print(f"{colors.GREEN}ENEMY TEAM:{colors.NORMAL}\n", delay)
		for enemy in self.enemy_team:
			log.slow_print(f"{enemy.name}:", delay)
			log.slow_print(f"[{enemy.stringify_health()}] {enemy.health}/{enemy.max_health}\n", delay)
		
		log.slow_print(f"{colors.GREEN}BATTLE LOG:{colors.NORMAL}\n", delay)
		
		log.add_message("This is a battle intro message. (I couldn't think of anything lol)")
		log.show_all(delay)
	
	def check_defeated(self, was_living_enemies):
		for enemy in was_living_enemies:
			if enemy.health <= 0:
				self.shop_handler.gain_rewards(enemy.reward)
	
	def run_turn(self, skip_header=False, skip_log=False, extra_info=False): # or more accurately, get_someone_to_run_turn_for_me()
		if not self.enemy_team:
			self.start_battle(skip_header)
			return
		
		print("Loading...")
		
		delay = None
		if skip_header:
			delay = 0
		
		turn_info = {"Turn Owner": "Nobody"}
		
		if self.check_for_loss():
			log.add_message("Nobody is willing to fight...")
		elif self.check_for_win():
			self.seen_win = True
			log.add_message("You win!")
		else:
			self.turn_count += 1
			
			if self.turn_count % 3 == 0:
				living_enemies = []
				for enemy in self.enemy_team:
					if enemy.health > 0:
						living_enemies.append(enemy)

				self.enemy_tick = (self.enemy_tick + 1) % len(living_enemies)
				turn_info["Turn Owner"] = living_enemies[self.enemy_tick]
			else:
				living_party_members = []
				for party_member in self.player_team:
					if party_member.health > 0:
						living_party_members.append(party_member)
				
				self.player_tick = (self.player_tick + 1) % len(living_party_members)
				turn_info["Turn Owner"] = living_party_members[self.player_tick]
			
			was_living_enemies = self.get_living_enemies()
			turn_info = turn_info | turn_info["Turn Owner"].take_turn(self)
			self.check_defeated(was_living_enemies)
		
		log.undo_line()
		log.slow_print(f"TURN {self.turn_count}\n", delay)
		
		log.slow_print(f"{colors.GREEN}PLAYER TEAM:{colors.NORMAL}\n", delay)
		for party_member in self.player_team:
			name_color = ""
			if not party_member.is_living():
				name_color = colors.GRAY
			elif party_member == turn_info["Turn Owner"]:
				name_color = colors.YELLOW
			log.slow_print(f"{name_color}{party_member.name}{colors.NORMAL}:", delay)
			
			log.slow_print(f"[{party_member.stringify_health()}] {party_member.health}/{party_member.max_health}", delay)
			log.slow_print(f"[{party_member.stringify_inspirations()}] {party_member.get_total_inspirations()}/{party_member.creativity}\n", delay)
		
		log.slow_print(f"{colors.GREEN}ENEMY TEAM:{colors.NORMAL}\n", delay)
		for enemy in self.enemy_team:
			name_color = ""
			if not enemy.is_living():
				name_color = colors.GRAY
			elif enemy == turn_info["Turn Owner"]:
				name_color = colors.YELLOW
			log.slow_print(f"{name_color}{enemy.name}{colors.NORMAL}:", delay)
			
			log.slow_print(f"[{enemy.stringify_health()}] {enemy.health}/{enemy.max_health}\n", delay)
		
		log.slow_print(f"{colors.GREEN}BATTLE LOG:{colors.NORMAL}\n", delay)
		
		if skip_log:
			delay = 0
		else:
			delay = None
		
		log.show_all(delay)
		
		if extra_info:
			log.slow_print(f"\n{colors.GREEN}DEBUG INFO:{colors.NORMAL}\n")
			if len(turn_info) > 0:
				for info, value in turn_info.items():
					log.slow_print(f"{info}: {repr(value)}")
			else:
				log.slow_print("None :(")
		
		if self.seen_win:
			self.reset_battle()
