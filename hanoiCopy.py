import os



class GameBoard(object):

	def __init__(self, NumDisks):
		self.NumDisks = NumDisks
		self.maxradius = self.NumDisks; # disk radius: disk "1" is actually 3 characters wide including its center; disk 2 is 5 characters wide, etc.
		self.towerwidth = 1 + 2 * self.maxradius # leave enough room for the center tower plus the max radius of a disk on each side of the tower
		self.boardheight = self.maxradius + 1 # height of towers is enough for all disks on one tower, plus one empty bit at the top

	def start_game(self):
		#TODO:  need some doc strings for the most important methods?
		#TODO:  change to the popular python method naming style for all methods
		self.towers = []

		# game board is three towers, each can have a varying number of "disk IDs" on it, starting at the bottom of the stack
		for tower in range (0, 3):
			self.towers.append([])
		
		# stack all the disks on the left tower at first--starting with the largest disk on the bottom
		for disk in range (self.NumDisks, 0, -1):
			self.towers[0].append(disk)
	
	def is_end_game(self):
		# are all disks on the rightmost tower?
		return len(self.towers[2]) == self.NumDisks
			
	def _debug_print(self):
		# debug method, show the contents of the towers
		for i in range (0, 3):
			print (self.towers[i])

	def show(self):
		if debug: self._debug_print()

		print ('')

		# for each vertical text printing row in the board printout, print what is at each tower, horizontally
		for row in range(0, self.boardheight):
			for tower in range(0, 3):
				self.show_disk(row, tower)
			print ('');

		# at the bottom of the board, below the towers, show a base for the board
		print ((self.towerwidth * 3 + 2) * "-")
		#TODO:  label the towers with the numbers that are valid for user input
		
	def show_disk(self, row, tower):
		# if this tower has enough disks to reach the current print row,
		if row >= self.boardheight - len(self.towers[tower]):
			# then create a disk of proper width and center it on the tower
			disksize = self.towers[tower][self.boardheight - 1 - row]
			disk = "*"  * (1 + 2 * disksize)
			print " " * (self.NumDisks - disksize) + disk + \
							" " * (self.NumDisks - disksize),
		else:
			# this part of the tower is empty, so show the tower, centered in its space
			print " " * self.maxradius + "|" + " " * self.maxradius,
		
	def move_disk(self, fromtower, totower):
		if debug: print ("call move_disk: ", fromtower, totower)
		
		# check for a disk, if any, and its size, at the top of the stack on the "from" tower
		disk = self.top_disk_size(fromtower)
		
		if debug: print ("return: ", disk)
		
		if disk == None:
			print ("There are no disks on that tower to move!")
			return False

		# check the size of the disk (if any) at the top of the stack on the "to" tower
		topdisk = self.top_disk_size(totower)
		
		if debug: print ("return: ", topdisk)

		# check for a legal move:  no bigger disk on a smaller one!
		if topdisk != None and topdisk < disk:
			print ("Can't move a disk onto a smaller one!")
			return False

		# move the disk to the new tower
		self.towers[fromtower].pop()
		self.towers[totower].append(disk)
		
		# signal a successful move (no errors) so the caller can redraw the new board position
		return True

	def top_disk_size(self, tower):
		if debug: print ("call TopDisk: ", tower)

		# find the top disk on the tower
		numdisks = len(self.towers[tower])
		if debug: print ("num disks:", numdisks)

		# if a disk was found, return its size
		if numdisks > 0:
			return self.towers[tower][numdisks-1]
		
		# no disk was found on the tower
		return None
	
def input_or_quit(prompt, min=None, max=None):

	amount = None

	# we try not to let the program proceed without a valid input for the given prompt!
	while amount == None:
		response = raw_input("\n"+prompt)
		if response == 'q' or response == "quit":
			print ("\n\n\nOkay, come back later, then!\n")
			exit(0)
		else:	#TODO:  graceful handling of invalid non-numeric inputs here
			amount = int(response)
			if min != None and amount < min:
				print ("Range is %d to %d, use a higher value!" % (min, max))
				amount = None
			elif max != None and amount > max:
				print ("Range is %d to %d, use a lower value!" % (min, max))
				amount = None
	
	return amount

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')
	

# MAIN GAME LOGIC


if __name__ == "__main__":

	# TODO: make debug (informational output) mode an optional command line option
	# TODO: make number-of-disks required input an optional command line
	#	argument that skips prompt

	debug = False

	clear_screen()

	#TODO:  add zero player mode:  computer solves the game itself, with recursion
	#			(disable clear-screen so user can scroll back and see computer's solution!)
	#TODO:  add two player mode:  saves the board and next-player ID somewhere and
	#			each player's session watches for their turn
	#		add multi-player mode?

	print "\n\nLet's play!"
	numdisks = input_or_quit("How many disks (q to quit)? ", 1, 16)

	#TODO:  move board initialization and game turn loop into a method in board class,
	#TODO:		so main program is super simple!  (board.start_game() would become game.start(), etc.)	
	board = GameBoard(numdisks)
	
	board.start_game()

	clear_screen()
	board.show()

	while (not board.is_end_game()):

		fromtower = input_or_quit("From tower (q to quit)? ", 1, 3) - 1
		totower = input_or_quit("To tower (q to quit)? ", 1, 3) - 1

		clear_screen()
	
		board.move_disk(fromtower, totower)
		board.show()

	print "\n","*" * 20, "You did it!\n"
	
	print ("Thanks for playing!\n\n")
	exit(0)
	
else:
	debug = True # debug mode on if we imported Hanoi to play with it in interactive mode
