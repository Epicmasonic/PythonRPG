from random import random
from math import floor

def randomRound(value:float):
	"""
	A function to round a number randomly.
	:param value: Number to be rounded.
	:type value: float
	:return value: The rounded number.
	:rtype value: int
	:return rounded: If the number got rounded.
	:rtype rounded: bool
	"""
	
	fractional = value % 1
	value = floor(value)
	rounded = False
	
	if fractional > random():
		value += 1
		rounded = True
	return value, rounded

#def safe_index(target_list, index, get_many=False): # "get_many" is kinda a bad name for that lol
#	"""
#	A function to safely get an element from a list. (So it can't error)
#	:param target_list: The list.
#	:type target_list: list
#	:param index: The index.
#	:type index: int
#	:param get_many: Whether to also return all the elements after index.
#	:type get_many: bool
#	:return: list[index] or none
#	"""
#
#	if len(target_list) < index + 1:
#		return None
#	else:
#		if get_many:
#			return target_list[index:]
#		else:
#			return target_list[index]