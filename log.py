import msvcrt

import os
#import textwrap
from time import sleep

def clear():
	"""Clears the console screen based on the operating system."""
	# Check the operating system name
	if os.name == 'nt':
		# Command for Windows
		_ = os.system('cls')
	else:
		# Command for Linux, macOS, and other POSIX systems
		_ = os.system('clear')

def slow_print(message, delay=None,  new_line=True):
	"""
	Just* like Print() but it has small delay between each character.
	:param message: Message to add to the queue.
	:type message: str
	:param new_line: Weather to add a "\\n" at the end.
	:type new_line: bool
	:param delay: Delay between each character.
	:type delay: float
	"""
	
	if new_line:
		message += "\n"
	
	if msvcrt.kbhit() != 0:
		print(end=message)
		return
	
	if delay is None:
		delay = 0.025
	
	skipping = False
	for char in message:
		print(char, end="", flush=True)
		
		if char == '\x1b':
			skipping = True
		if skipping and char == 'm':
			skipping = False
		
		if msvcrt.kbhit() == 0 and not skipping: # Reminder: msvcrt.kbhit() returns 0 if no key is queued up # I think it's 1 otherwise but not quite sure lol
			sleep(delay)

def undo_line(lines=1):
	for i in range(lines):
		print(end="\033[F") # Gemini says this one moves the cursor up 1...
		print(end="\033[2K")        # ...and this one clears the current line.
		
		# So basically just:
		#term.setCursorPos(1, y - lines)
		#term.clearLine()

message_queue = []

def add_message(message, new_line=True):
	"""
	Adds a message to the queue.
	:param message: Message to add to the queue.
	:type message: str
	:param new_line: Weather to add a "\\n" at the end.
	:type new_line: bool
	"""
	
	if new_line:
		message += "\n"
	
	message_queue.append(message)

def show_one():
	"""
	Prints a message in the queue.
	"""
	
	global message_queue
	
	slow_print(message_queue.pop(0),new_line=False)

def show_all(delay=None):
	"""
	Prints all messages in the queue.
	"""
	
	global message_queue
	
	for message in message_queue:
		slow_print(message,delay,False)
	message_queue.clear()