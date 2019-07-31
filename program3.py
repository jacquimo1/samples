'''
Prolog:
	David Willis
	david.willis@uky.edu
	Program 3
	CS 115-04
	
	pre-conditions:
		user's name and command input, maze file maze.dat, descriptions file descriptions.dat
	post-conditions:
		updates game states and allows user to quit
	description:
		command line interface-based adventure game
'''

from random import randint

def main():
	'''
	main loop for game
	'''
	inventory = ["flashlight"]
	maze = get_maze()	# initializes maze
	descs = get_descriptions() # initializes descriptions
	key_room = randint(0,len(maze) -1) # randomly assigns room to append key of programming item
	maze[key_room][3].append("key of programming")
	for room in maze:
		room.append(False) # appends false to signal that the room has not yet been visited
	print("Adventure!\n")
	name = input("What's your name? ")
	cur_room = 0
	print(descs[cur_room][1])
	maze[cur_room][4] = True # signals that the start room has been visited
	_quit = False
	magic_words = False
	
	while not _quit:
		print("you are in", maze[cur_room][1]) # displays current room
		choice = command_menu() # gets user action
		if choice == "look":
			display(maze[cur_room][3],"You can see:") # displays list of items in room
		elif choice == "take":
			take_choice = pick_from(maze[cur_room][3]) # gets choice of item in room
			if take_choice is -1:
				print("There's nothing in the room")
			else:
				inventory.append(maze[cur_room][3][take_choice]) # adds chosen item to inventory
				print(maze[cur_room][3][take_choice], "picked up")
				maze[cur_room][3].remove(maze[cur_room][3][take_choice]) # removes item from room
		elif choice == "drop":
			drop_choice = pick_from(inventory)
			if drop_choice is -1:
				print("There's nothing in the inventory")
			else:
				[maze[cur_room][3].append(inventory[drop_choice])] # adds chosen item to drop to room
				print(inventory[drop_choice], "dropped")
				inventory.remove(inventory[drop_choice]) # removes item from inventory
		elif choice == "go":
			room_choice = choose_rooms(maze[cur_room][2]) # get choice from connected rooms
			cur_room = room_choice
			if maze[cur_room][4] is False: # if room hasn't yet been visited
				print(descs[cur_room][1]) # prints long description
				maze[cur_room][4] = True
			else:
				print(maze[cur_room][1]) # prints short descriptions
			if maze[cur_room][1] == "exit":
				print("You are in the Exit room")
				exit_choice = input("Do you want to leave the cave? (Y/N) ")
				exit_choice.lower()
				while exit_choice is not "y" and exit_choice is not "n":
					print("invalid choice")
					exit_choice = input("Do you want to leave the cave? (Y/N) ")
					exit_choice.lower()
				if exit_choice is "y":
					_quit = True
		elif choice == "say":
			print("\nPython is great!\n")
			magic_words = True
		elif choice == "status":
			display(inventory, "Inventory")
		elif choice == "quit":
			_quit = True

	if "key of programming" in inventory and magic_words == True and _quit == True:
		print("You won the game! You win 50000 gold pieces!\n\n")
		print("Congratulations " + name + " you made it through alive")
		print("you left through the exit!")
		display(inventory, "You left the game with")
	
def get_maze():
	'''
	Purpose: return maze as 3-d list from maze file
	Preconditions: nothing
	Postconditions: list of maze as <room number, short description, adjacency list (colons), objects (colons)>
	'''
	maze = []
	fileOK = False
	in_file = "maze.dat"
	while not fileOK:
		try:
			with open(in_file,"r") as maze_file:
				for line in maze_file:
					row = line.split(',')
					row[2] = row[2].strip().split(':') # creates list delimited by colon
					room_nums = []
					for item in row[2]:
						room_nums.append(int(item)) # typecasts strings to integers in new list
					row[2] = room_nums
					row[3] = row[3].strip().split(':') # creates list delimited by colon
					maze.append(row)
				fileOK = True
		except IOError:
			print("Unable to open file maze.dat")
			in_file = input("Please enter new file name: ")
	return maze
	
def get_descriptions():
	'''
	Purpose: read long room descriptions from file, clean up and return the list of strings
	Preconditions: none
	Postconditions:  returns list of strings containing descriptions of rooms
	'''
	descriptions = []
	fileOK = False
	in_file = "descriptions.dat"	
	while not fileOK:
		try:
			with open(in_file,"r") as desc_file:
				for line in desc_file:
					row = line.split(":") # creates list delimited by colon
					descriptions.append(row)
				fileOK = True
		except IOError:
			print("Unable to open file descriptions.dat")
			in_file = input("Please enter new file name: ")
	return descriptions

def pick_from(_list):
	'''
	Purpose: present a list of choices to the user, validate answer and return it
	Preconditions:  list of choices
	Postconditions:  returns integer which is position of choice in the list 
	'''
	num_list =[]
	if not _list:
		return -1
	else:
		print("Choose from:")
		for e in range(len(_list)):
			print(e+1, _list[e])	# prints numbered list of options
		choice = input("which one? ")
		while choice not in range(len(_list)+1): # while input not valid
			try:
				choice = int(choice)
			except ValueError:	
				print("invalid choice")
				choice = input("which one? ")
		return choice - 1

def display(_list, label):
	'''
	Purpose: put a list of elements on the screen, preceded by a label and numbered, and
		if list is empty, just print "nothing"
	Preconditions: list, label to display for list
	Postconditions: label is output, list put on screen, numbered from 1 to ...?, short lines
		before and after the list, prompts for Enter from keyboard nothing returned
	'''
	print(label)
	print("---------------------")
	for e in range(len(_list)):
		print(e+1, _list[e]) # displays numbered list
	print("---------------------")
	print("Press Enter")
	if input():
		return

def choose_rooms(room_nums):
	'''
	Purpose: displays list of room numbers, gets user's choice, validates it and returns it
	Preconditions: list of room numbers (integers)
	Postconditions: returns the integer the user entered 
	'''
	print()
	print("You can go to these locations")
	for room in room_nums:
		print("Room", room)
	print()
	choice = input("which room? ")
	while choice not in room_nums:
		try:
			choice = int(choice)
		except ValueError:	
			print("invalid choice")
			choice = input("which room? ")
	return choice
	
def command_menu():
	'''
	Purpose: display commands available, gets user's choice and validates it
		and returns the choice
	Preconditions: none
	Postconditions:  return validated user's choice (lower-case string)
	'''
	print("I know how to do these things:\n")
	print("Look - to see objects in the room")
	print("Take - pick up an object in the room")
	print("Drop - drop an object in inventory")
	print("Go   - go to a different room")
	print("Say  - say some words")
	print("Status - what are you holding")
	print("Quit - to end the game")
	choices = ["look","take","drop","go","say", "status", "quit"]
	choice = input("which? ")
	choice.lower()
	while not choice in choices:
		print("Command not understood")
		choice = input("which? ")
		choice.lower()
	return choice
	
if __name__ == '__main__':
	main()
