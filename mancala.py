import random
import time

bins = [4]*14
PLAYER_HOME = 6
AI_HOME = 13

# 0 for player, 1 for AI
PLAYER = 0
AI = 1
TURN = PLAYER

#no stones in homes to start
bins[PLAYER_HOME] = 0
bins[AI_HOME] = 0

def on_player_side(bin_num):
	return bin_num >= 0 and bin_num < PLAYER_HOME

def on_ai_side(bin_num):
	return bin_num > PLAYER_HOME and bin_num < AI_HOME

def print_current_board():
	print '    ({}) ({}) ({}) ({}) ({}) ({}) '.format(bins[12],bins[11],bins[10],bins[9],bins[8],bins[7])
	print '({})                         ({})'.format(bins[13],bins[6])
	print '    ({}) ({}) ({}) ({}) ({}) ({}) '.format(bins[0],bins[1],bins[2],bins[3],bins[4],bins[5])
	print '     1   2   3   4   5   6'.format(bins[0],bins[1],bins[2],bins[3],bins[4],bins[5])

def parse_input(num):
	try:
		num = int(num)
		if num < 1 or num > 6:
			return False
		distribute_stones(num-1)
		return True
	except:
		return False

def get_current_home():
	if TURN==AI:
		return AI_HOME
	elif TURN==PLAYER:
		return PLAYER_HOME
	
def get_opposite_bin(bin_num):
	return 6 + (6-bin_num)

def distribute_stones(num):
	last_bin_filled = 0
	stones_to_place = 0

	def place_in_circle(start_bin):
		for i in range(bins[start_bin]):
			destination_bin = num+i+1

			# circle back around loop
			if destination_bin >= len(bins):
				destination_bin = destination_bin - len(bins)

			# skip opponents home bin
			if (destination_bin==PLAYER_HOME and TURN==AI) or (destination_bin==AI_HOME and TURN==PLAYER):
				#save it for later
				print "skipping home"
				stones_to_place += 1
				continue

			print destination_bin
			
			bins[destination_bin]+=1
			last_bin_filled = destination_bin

	place_in_circle(num)

	# place stones from skipped bins (home bins)
	while(stones_to_place>0):
		place_in_circle(last_bin_filled)

	bins[num] = 0

	# get another turn if you land in your home
	if last_bin_filled == get_current_home():
		pass

	# TODO: only on your side
	# if you landed in an empty hole you get opposite bin's contents
	if bins[last_bin_filled] == 1:
		print "opposite-bin rule in effect"
		opp_bin = get_opposite_bin(last_bin_filled)
		bins[get_current_home()] += bins[opp_bin]
		bins[opp_bin] = 0

def ai_random_move():
	rand_bin = int(random.random()*6) + 7
	print rand_bin
	distribute_stones(rand_bin)

if __name__ == '__main__':
	print_current_board()

	while(True):

		TURN = PLAYER
		valid_input = False
		while not valid_input:
			inp = raw_input("Enter bin number: ")
			if not parse_input(inp):
				print "Invalid Input, try again"
			else:
				valid_input = True
		print_current_board()

		# check game over

		TURN = AI
		print "...Computer turn..."
		time.sleep(2)
		ai_random_move()
		print_current_board()

		#check game over
