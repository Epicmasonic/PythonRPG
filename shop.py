#from index import battle
from log import add_message

class Shop:
	def __init__(self):
		self.gold = 0
		self.reward_mode = "Balanced"
		
		self.store_front = []
	
	def gain_rewards(self, reward):
		self.gold += reward
		add_message(f"You earned {reward} bits!")