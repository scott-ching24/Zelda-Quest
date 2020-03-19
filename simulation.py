from room import Room
from item import Item
from adventurer import Adventurer
from quest import Quest
import sys

def read_paths(source):
	"""Returns a list of lists according to the specifications in a config file, (source). Source contains path specifications of the form: origin > direction > destination.
	read_paths() interprets each line as a list with three elements, containing exactly those attributes. Each list is then added to a larger list, `paths`, which is returned."""
	infile = open(source, "r")
	lines = []

	while True:
		line = infile.readline()
		if line == "":
			break
		elif line == "\n":
			continue
		else:
			lines.append(line.strip())
	infile.close()
	
	if len(lines) < 1:
		print("No rooms exist! Exiting program...")
		sys.exit()
	paths = []
	for line in range(len(lines)):
		new_path = lines[line].split(" > ")
		if len(new_path) != 3:
			sys.exit("Please specify a valid configuration file.")
		else:
			paths.append(new_path)

	return paths


def create_rooms(paths):
	"""Receives a list of paths and returns a list of rooms based on those paths. Each room will be generated in the order that they are found. existing_rooms is a list of room objects that have been created and room_names 
	is a dictionary the maps string value for room names with the associated room object inside the list existing_rooms"""
	existing_rooms = []
	room_names = {}

	for rooms in range(len(paths)):

		#if the room objects already exist and are in existing_rooms, create the path between rooms
		if (room_names.get(paths[rooms][0]) != None) and (room_names.get(paths[rooms][2]) != None):
			room_names[paths[rooms][0]].set_path(paths[rooms][1], room_names[paths[rooms][2]])

		#if one of the room names are not in existing_rooms, create the room object and set the path
		elif (room_names.get(paths[rooms][0]) != None) and (room_names.get(paths[rooms][2]) == None):
			new_room = Room(paths[rooms][2])
			room_names[paths[rooms][2]] = new_room
			existing_rooms.append(new_room)
			room_names[paths[rooms][0]].set_path(paths[rooms][1], room_names[paths[rooms][2]])

		#if one of the room names are not in existing_rooms, create the room object and set the path
		elif (room_names.get(paths[rooms][0]) == None) and (room_names.get(paths[rooms][2]) != None):
			new_room = Room(paths[rooms][0])
			room_names[paths[rooms][0]] = new_room
			existing_rooms.append(new_room)
			room_names[paths[rooms][0]].set_path(paths[rooms][1], room_names[paths[rooms][2]])

		#if neither of the room names are objects, create two objects and append both objects (note that first object must be appended first) and then set the path
		elif (room_names.get(paths[rooms][0]) == None) and (room_names.get(paths[rooms][2]) == None):
			new_room_one = Room(paths[rooms][0])
			new_room_two = Room(paths[rooms][2])
			room_names[paths[rooms][0]] = new_room_one
			room_names[paths[rooms][2]] = new_room_two
			existing_rooms.append(new_room_one)
			existing_rooms.append(new_room_two)
			new_room_one.set_path(paths[rooms][1], room_names[paths[rooms][2]])

	return existing_rooms
	

def generate_items(source):
	"""Creates a list of items from a 'config' file entered as a command line argument. These items will be used as rewards for quests and stored in a character's inventory."""
	
	#read the lines from the infile
	infile = open(source, "r")
	total_lines = []
	line = None
	while True:
		line = infile.readline()
		if line == "":
			break
		elif line == "\n":
			continue
		else:
			total_lines.append(line.strip())
	items_removed = 0
	infile.close()
	
	#Create a list of objects (instances of the Item class) that will be returned to the main function
	total_items = []
	for line in range(len(total_lines)):
		new_item = total_lines[line]
		new_item = new_item.split(" | ")
		if len(new_item) != 4:
			sys.exit("Please specify a valid configuration file.")
		try:
			total_items.append(Item(new_item[0], new_item[1], int(new_item[2]), int(new_item[3])))
		except ValueError:
			sys.exit("Please specify a valid configuration file.")

	return total_items

def generate_quests(source, items, rooms):
	"""Returns a list of quests according to the specifications in a config file, (source). Source contains quest specifications of the form:
	reward | action | quest description | before_text | after_text | quest requirements | failure message | success message | quest location"""
	
	#Read the file for quests entered as a command line argument
	infile = open(source, "r")
	lines = []
	while True:
		line = infile.readline()
		if line == "":
			break
		elif line == "\n":
			continue
		else:
			lines.append(line.strip())
	infile.close()

	#Create quest objects (instances of the Quest class) that are appended to a list and returned. Check validity of rooms and rewards for quests and then assign the respective item/roomo object to the quest.
	total_quests = []
	for quests in range(len(lines)):
		quest = lines[quests].split(" | ")
		if len(quest) != 9:
			sys.exit("Please specify a valid configuration file.")
		else:
			new_quest = Quest(quest[0], quest[1], quest[2], quest[3], quest[4], quest[5], quest[6], quest[7], quest[8])
			new_quest.check_reward(items)
			new_quest.check_room(rooms)
			total_quests.append(new_quest)
			for room in range(len(rooms)):
				if new_quest.room.get_name() == rooms[room].get_name():
					rooms[room].quest = new_quest

	return total_quests	

#Begin the program only if the appropriate files are inserted into the command prompt. Retrieve info from CONFIG files and use this information to make Adventurer, Item, Quest, and Room objects.
if len(sys.argv) != 4:
	sys.exit("Usage: python3 simulation.py <paths> <items> <quests>")
	
#If the file name does not exist, raise the error and catch the exception.
try:
	paths = create_rooms(read_paths(sys.argv[1]))
	items = generate_items(sys.argv[2])
	quests = generate_quests(sys.argv[3], items, paths)
except FileNotFoundError:
	print("Please specify a valid configuration file.")
	sys.exit()
	
#Create the character and assign its location to the first room in the configuration file and then begin the game.	
character = Adventurer()
character.current_room = paths[0]
character.current_room.draw()
print()

while True:
	"""Receive commands from standard iput and act appropriately"""
	user_input = input(">>> ").lower()

	if user_input == "quit":
		"""Leave the game if user_input == QUIT"""
		print("Bye!")
		sys.exit()
	
	elif user_input == "help":
		"""List all valid commands and their usage"""
		print("HELP".ljust(10) + " - Shows some available commands.")
		print("LOOK or L".ljust(10) + " - Lets you see the map/room again.")
		print("QUESTS".ljust(10) + " - Lists all your active and completed quests.")
		print("INV".ljust(10) + " - Lists all the items in your inventory.")
		print("CHECK".ljust(10) + " - Lets you see an item (or yourself) in more detail.")
		print("NORTH or N".ljust(10) + " - Moves you to the north.") 
		print("SOUTH or S".ljust(10) + " - Moves you to the south.")
		print("EAST or E".ljust(10) + " - Moves you to the east.")
		print("WEST or W".ljust(10) + " - Moves you to the west.")
		print("QUIT".ljust(10) + " - Ends the adventure.")
	
	elif user_input == "look" or user_input == "l":
		"""Represent the look function by drawing the room and printing its description."""
		character.current_room.draw()
		

	elif user_input == "quests":
		"""Display all possible quests and their rewards and if a quest is complete, it should be displayed as such. If all quests are completed and this command is called, print success message and end the game"""
		quests_completed = 0
		for quest in range(len(quests)):
			if quests[quest].is_complete() == True:
				print("#{:02d}: ".format(quest) + ("{}".format(quests[quest].reward.get_name())).ljust(21) + "- {} [COMPLETED]".format(quests[quest].get_info()))
				quests_completed += 1
			else:
				print("#{:02d}: ".format(quest) + ("{}".format(quests[quest].reward.get_name())).ljust(21) + "- {}".format(quests[quest].get_info()))
		if quests_completed == len(quests):
			print("\n=== All quests complete! Congratulations! ===")
			sys.exit()

	elif user_input == "inv":
		"""Display the characters inventory and print out all items that they are carrying"""
		print("You are carrying:")
		characters_inventory = character.get_inv()
		if len(characters_inventory) == 0:
			print("Nothing.")
		else:
			for item in range(len(characters_inventory)):
				print("- A {}".format(character.inventory[item].get_name()))
		
	elif user_input == "check":
		"""Allows the user to examine items or themselves. This command will ask the user for a second input, which can be an item's name or its short name. If the user enters 'me', they are shown a description of their character"""
		user_input_two = input("Check what? ").lower()
		print()
		if user_input_two == "me":
			character.check_self()
		else:
			whether_carrying = False
			for item in range(len(character.get_inv())):
				if character.inventory[item].get_name().lower() == user_input_two or character.inventory[item].get_short().lower() == user_input_two:
					character.inventory[item].get_info()
					whether_carrying = True
					break
			if whether_carrying == False:
				print("You don't have that!")
	
	elif (user_input == "n") or (user_input == "north") or (user_input == "south") or (user_input == "east") or (user_input == "west") or (user_input == "w") or (user_input == "e") or (user_input == "s"):
		"""If the user input is a valid direction for their character's current location, move the character to the adjoining room and print the location's description"""
		if user_input in character.current_room.get_exits():
			direction, character.current_room = character.current_room.move(user_input)
			print("You move to the {}, arriving at the {}.".format(direction, character.current_room.get_name()))
			character.current_room.draw()
		else:
			print("You can't go that way.\n")
			continue

	elif (character.current_room.get_quest() != None) and (user_input == character.current_room.get_quest_action()):
		"""Allows a character to attempt a quest located in the character's current room. If successful, attributes of the room and character change. Otherwise, a fail message is printed and nothing changes."""
		if character.current_room.quest.is_complete() == False:
			character.current_room.quest.attempt(character)
		else:
			print("You have already completed this quest.")
	else:
		print("You can't do that.")
	
	print()
