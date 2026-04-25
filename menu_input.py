import colors
import log

import msvcrt
from time import sleep
from math import ceil

def test_key():
	"""
	Get key from keyboard. This is technically the same as msvcrt.getch() but it's forced to run once.
	:return: Key pressed
	:rtype: bytes
	"""
	
	key = [None, None]
	key[0] = msvcrt.getch()
	if key[0] == b'\000' or key[0] == b'\xe0':
		key[1] = msvcrt.getch()
	
	eat_input()
	return key

def eat_input():
	while msvcrt.kbhit() > 0:
		get_key()

def wait_for_input():
	print("\n" + colors.GRAY + "Press any button" + colors.NORMAL)
	msvcrt.getch()
	eat_input()

def cancelable_sleep(wait_time):
	WAIT_STEP = 0.1
	for i in range(round(wait_time / WAIT_STEP)):
		if msvcrt.kbhit() > 0:
			break
		sleep(WAIT_STEP)

def get_key():
	"""
	Get key from keyboard. This is technically the same as msvcrt.getch() but it's forced to run once.
	:return: Key pressed
	:rtype: str
	"""
	
	key = msvcrt.getch()
	match key:
		case b'\000' | b'\xe0':
			key = msvcrt.getch()
			
			match key:
				case b'H':
					key = "up"
				case b'P':
					key = "down"
				case b'K':
					key = "left"
				case b'M':
					key = "right"
		case b'x1b':
			key = "esc"
		case b'\r':
			key = "enter"
		case b' ':
			key = "space"
		case _:
			key = key.decode()
	
	eat_input()
	return key


def get_choice(options, labels=None):
	page = 1
	max_page = ceil(len(options) / 10)
	
	while True:
		page_contents = options[(page - 1) * 10:page * 10]
		try:
			page_labels = labels[(page - 1) * 10:page * 10]
		except Exception:
			print(end="") # I don't care lol
		
		lines = len(page_contents) + 2  # That plus 2 is because of the next line.
		
		log.slow_print(f"{colors.GRAY}Page: {page}/{max_page}{colors.NORMAL}\n")
		
		valid_keys = []
		for i in range(len(page_contents)):
			key = str((i + 1) % 10)
			valid_keys.append(key)
			
			try:
				log.slow_print(f"{colors.GRAY}[{key}]{colors.NORMAL} " + page_labels[i]) # I intentionally make this more prone to errors lol
			except Exception:
				log.slow_print(f"{colors.GRAY}[{key}]{colors.NORMAL} {page_contents[i]}")
		if max_page > 1:
			log.slow_print(f"{colors.GRAY}[>]{colors.NORMAL} Next page")
			log.slow_print(f"{colors.GRAY}[<]{colors.NORMAL} Previous page")
			
			lines += 2
			valid_keys.extend(["right", "left"])
		
		eat_input()
		while True:
			key = get_key()
			if key in valid_keys:
				if key == "right":
					page += 1
				elif key == "left":
					page -= 1
				else:
					if key == "0":
						key = 10
					else:
						key = int(key)
					return page_contents[key - 1]
				break
			else:  # This line technically could be deleted. :P
				print(f"\n{colors.RED}Please pick one of the keys shown.{colors.NORMAL}")
				# sleep(1)
				log.undo_line(
					2)  # For reasons I can't see, this line only runs once you make an input? This is kinda a good thing though lol
		
		# This block is gross. I don't think I could make it better though. :(
		page = (page - 1) % max_page
		if page < 0:
			page = 1
		else:
			page += 1
		
		log.undo_line(lines)