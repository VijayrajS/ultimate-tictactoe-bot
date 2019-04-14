import copy
import time

class Team70:
	def __init__(self):
		self.board = None
		self.hash_table = {}
		self.max_depth = 4
		self.bonus_mov = 1
		self.bonus_mov_old = 0

		self.was_bonus_move = False
		self.playing_bonus = False
		self.current_time = time.time()
		
		self.depth_current = 0
		self.playing_bonus = False
		

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		# self.board = board
		self.current_time = time.time()
		self.who = flag
		valid_moves = board.find_valid_move_cells(old_move)
		best_mov_o =  100000
		best_mov_x = -100000
		best_mov_index = -1
		if flag=='x':
			self.ply = 'x'
			self.not_ply = 'o'
		else:
			self.ply = 'o'
			self.not_ply = 'x'


		#if bonus move, increment 1.
		#keep track of previous bonus_mov
		#if difference is more than 1

		# if wasbonusmove = true
		self.depth_current = 0
		
		
		for j in range(4):
			self.depth_current = 3 + j
			self.alpha = -10000
			self.beta  =  10000

			best_mov_o =  100000
			best_mov_x = -100000

			for i in range(len(valid_moves)):
				
				if time.time()-self.current_time > 20:
					# print "Broke due to time constraint"
					break
				
				move_board = copy.deepcopy(board);

				if flag=='x':

					temp_val = self.mini_max(0, True, self.alpha, self.beta, move_board, valid_moves[i], self.playing_bonus, old_move)
					if best_mov_x <= temp_val:
						best_mov_x = temp_val
						best_mov_index = i
				
				if flag=='o':
					temp_val = self.mini_max(0, False, self.alpha, self.beta, move_board, valid_moves[i], self.playing_bonus, old_move)
					if best_mov_o >= temp_val:
						best_mov_o = temp_val
						best_mov_index = i
			
			if time.time()-self.current_time > 20:
				break
			
			best_mov_index = -1
		
		move_board_temp = copy.deepcopy(board);
		current_move = valid_moves[best_mov_index]
		(message, success) = move_board_temp.update(old_move, current_move, flag)

		
		if self.playing_bonus:
			if success:
				self.playing_bonus = False
		else:
			if success:
				self.playing_bonus = True
		
		if not success:
			self.playing_bonus = False
		return current_move


	def mini_max(self, depth, isMax, alpha, beta, board, old_move, playing_bonus, current_move_temp):
		# print depth
		move_board = copy.deepcopy(board);
		if isMax:
			move_board.update(current_move_temp, old_move, 'x')
		else:
			move_board.update(current_move_temp, old_move, 'o')
		
		if depth > self.max_depth:
			self.max_depth = depth
		
		if depth == self.depth_current or time.time() - self.current_time > 20:
			if isMax:
				return self.hueristic_1('x', board)
			else:
				return self.hueristic_1('o', board)

		
			
		valid_moves_mini = board.find_valid_move_cells(old_move)
		
		if isMax:
			bestVal = -100000
		else:
			bestVal = 100000
		
		for i in range(len(valid_moves_mini)):
			board_temp = copy.deepcopy(move_board)

			current_move = valid_moves_mini[i]

			if isMax:
				(message, isBonus) = board_temp.update(old_move, current_move, 'x')
				if isBonus:
					if playing_bonus:
						value = self.mini_max( depth+1, False, alpha, beta, board_temp, current_move, False,old_move)
					else:
						value = self.mini_max( depth+1, True, alpha, beta, board_temp, current_move, True,old_move)
				else:
					value = self.mini_max( depth+1, False, alpha, beta, board_temp, current_move, False,old_move)
					
				bestVal = max(bestVal, value)
				alpha = max(alpha, bestVal)
				if beta <= alpha:
					break

			else:
				
				(message, isBonus) = board_temp.update(old_move, current_move, 'o')
				if isBonus:
					if playing_bonus:
						value = self.mini_max(depth+1, True, alpha, beta, board_temp, current_move, False, old_move)
					else:
						value = self.mini_max(depth+1, False, alpha, beta, board_temp, current_move, True, old_move)
				else:
					value = self.mini_max(depth+1, True, alpha, beta, board_temp, current_move, False, old_move)
				
				bestVal = min(bestVal, value)
				beta = min(beta, bestVal)
				if beta <= alpha:
					break
		
		return bestVal

	# def winning_patterns(self, small_board):
	# 	flag = 'x'
	# 	if [small_board[0][0], small_board[0][1], small_board[0][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[1][0], small_board[1][1], small_board[1][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[2][0], small_board[2][1], small_board[2][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][0], small_board[1][0], small_board[2][0]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][1], s100000mall_board[1][1], small_board[2][1]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][2], small_board[1][2], small_board[2][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][0], small_board[1][1], small_board[2][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][2], small_board[1][1], small_board[2][0]] == [flag, flag, flag] :
	# 		return 100
		
	# 	flag = 'o'
	# 	if [small_board[0][0], small_board[0][1], small_board[0][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[1][0], small_board[1][1], small_board[1][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[2][0], small_board[2][1], small_board[2][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][0], small_board[1][0], small_board[2][0]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][1], small_board[1][1], small_board[2][1]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][2], small_board[1][2], small_board[2][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][0], small_board[1][1], small_board[2][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][2], small_board[1][1], small_board[2][0]] == [flag, flag, flag] :
	# 		return 0		
		
	# 	return 50

	

	# def blocking_patterns(self, small_board, flag):
	# 	count = 0
	# 	if flag == 'x':
	# 		op_flag = 'o'
	# 	else:
	# 		op_flag = 'x'

	# 	if sorted([small_board[0][0], small_board[0][1], small_board[0][2]]) == [op_flag, flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[1][0], small_board[1][1], small_board[1][2]]) == [op_flag, flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[2][0], small_board[2][1], small_board[2][2]]) ==  [op_flag, flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][0], small_board[2][0]]) ==  [op_flag, flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][1], small_board[1][1], small_board[2][1]]) ==  [op_flag, flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[0][2], small_board[1][2], small_board[2][2]]) ==  [op_flag, flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][1], small_board[2][2]]) ==  [op_flag, flag, flag]  :
	# 		count = 4

	# 	if sorted([small_board[0][2], small_board[1][1], small_board[2][0]]) ==  [op_flag, flag, flag]  :
	# 		count = 4
	# 	#
	# 	op_flag = 'd'
	# 	if sorted([small_board[0][0], small_board[0][1], small_board[0][2]]) == [op_flag, flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[1][0], small_board[1][1], small_board[1][2]]) == [op_flag, flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[2][0], small_board[2][1], small_board[2][2]]) ==  [op_flag, flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][0], small_board[2][0]]) ==  [op_flag, flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][1], small_board[1][1], small_board[2][1]]) ==  [op_flag, flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[0][2], small_board[1][2], small_board[2][2]]) ==  [op_flag, flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][0], s100000mall_board[1][1], small_board[2][2]]) ==  [op_flag, flag, flag]  :
	# 		count = 4

	# 	if sorted([small_board[0][2], small_board[1][1], small_board[2][0]]) ==  [op_flag, flag, flag]  :
	# 		count = 4
		
	# 	#break
	# 	if flag == 'x':
	# 		op_flag = 'o'
	# 	else:
	# 		op_flag = 'x'

	# 	if sorted([small_board[0][0], small_board[0][1], small_board[0][2]]) == [op_flag, op_flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[1][0], small_board[1][1], small_board[1][2]]) == [op_flag, op_flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[2][0], small_board[2][1], small_board[2][2]]) ==  [op_flag, op_flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][0], small_board[2][0]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][1], small_board[1][1], small_board[2][1]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[0][2], small_board[1][2], small_board[2][2]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][1], small_board[2][2]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 4

	# 	if sorted([small_board[0][2], small_board[1][1], small_board[2][0]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 4
		
	# 	if flag == 'x':
	# 		return 100 - count
	# 	if flag == 'o':
	# 		return 50 + 20*count

	# def probabilty_board(self, small_board):
	# 	count = 0
	# 	for i in range(3):
	# 		for j in range(3):
	# 			if small_board[i][j] == 'x':
	# 				count += 1
	# 	return count/9


	# def small_heur(self, board, flag, op_flag):
	# 	op = 0
	# 	c = 0
	# 	small_h = [[7, 6, 4], [7, 7, 2], [7, 4, 4]]    #meddle
	# 	for i in range(3):
	# 		for j in range(3):
	# 			if board[i][j] == op_flag :
	# 				op += 1
		
	# 	if op >= 4:
	# 		return 0
	# 	#meddle with x (the c+= x)
	# 	else:
	# 		if board[1][1] == flag:
	# 			c += 5

	# 		if board[0][1] == flag:
	# 			c += 2
	# 		if board[1][0] == flag:
	# 			c += 2
	# 		if board[2][1] == flag:
	# 			c += 2
	# 		if board[1][2] == flag:
	# 			c += 2

	# 		if board[0][0] == flag:
	# 			c += 4 
	# 		if board[0][2] == flag:
	# 			c += 4 
	# 		if board[2][2] == flag:
	# 			c += 4 
	# 		if board[2][0] == flag:
	# 			c += 4 
	# 	return c

	# def heuristic(self, flag, board):

	# 	curr_heur = 0
	# 	sb_stats = board.small_boards_status 
	# 	bb_stats = board.big_boards_status

	# 	if flag=='x':
	# 		op_flag = 'o'
	# 	else:
	# 		op_flag = 'x'

		

	# 	if self.winning_patterns(sb_stats[0]) > 50:
	# 		return 300

	# 	if self.winning_patterns(sb_stats[1]) > 50:
	# 		return 300

	# 	if self.winning_patterns(sb_stats[0]) < 50:
	# 		return -300

	# 	if self.winning_patterns(sb_stats[1]) < 50:
	# 		return -300

	
		

		

	# 	blockWts = [[[7,2,3], [6,40,2], [5,2,3]], [[3,2,3], [2,40,2], [8,8,8]]]                               # meddle with these values

	# 	for boa in range(2):
	# 		for r in range(0, 3, 6):
	# 			for c in range(0, 3, 6):

	# 				tiny_board = [[bb_stats[boa][r][c], bb_stats[boa][r][c+1],bb_stats[boa][r][c+2]], 
	# 							  [bb_stats[boa][r+1][c], bb_stats[boa][r+1][c+1],bb_stats[boa][r+1][c+2]], 
	# 							  [bb_stats[boa][r+2][c], bb_stats[boa][r+2][c+1],bb_stats[boa][r+2][c+2]]];

	# 				curr_heur += self.blocking_patterns(tiny_board, 'x')
	# 				temp = blockWts[boa][r/3][c/3]*(self.probabilty_board(tiny_board))*40
					
	# 				if temp < 50:
	# 					curr_heur -= temp
	# 				else:
	# 					curr_heur += temp

					

	# 				if self.winning_patterns(tiny_board) < 50:
	# 					curr_heur -= 50
	# 				if self.winning_patterns(tiny_board) > 50:
	# 					curr_heur += 50

	# 	return curr_heur

	# # def newHeur(self, flag, board) :

	# # 	small_x_count = 0
	# # 	small_o_count = 0
	# # 	big_x_count = 0
	# # 	big_o_count = 0
	# # 	for i in range(0, 2) :
	# # 		for j in range(0, 3) :
	# # 			for k in range(0, 3) :	# def winning_patterns(self, small_board):
	# 	flag = 'x'
	# 	if [small_board[0][0], small_board[0][1], small_board[0][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[1][0], small_board[1][1], small_board[1][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[2][0], small_board[2][1], small_board[2][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][0], small_board[1][0], small_board[2][0]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][1], s100000mall_board[1][1], small_board[2][1]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][2], small_board[1][2], small_board[2][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][0], small_board[1][1], small_board[2][2]] == [flag, flag, flag] :
	# 		return 100

	# 	if [small_board[0][2], small_board[1][1], small_board[2][0]] == [flag, flag, flag] :
	# 		return 100
		
	# 	flag = 'o'
	# 	if [small_board[0][0], small_board[0][1], small_board[0][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[1][0], small_board[1][1], small_board[1][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[2][0], small_board[2][1], small_board[2][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][0], small_board[1][0], small_board[2][0]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][1], small_board[1][1], small_board[2][1]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][2], small_board[1][2], small_board[2][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][0], small_board[1][1], small_board[2][2]] == [flag, flag, flag] :
	# 		return 0

	# 	if [small_board[0][2], small_board[1][1], small_board[2][0]] == [flag, flag, flag] :
	# 		return 0		
		
	# 	return 50

	

	# def blocking_patterns(self, small_board, flag):
	# 	count = 0
	# 	if flag == 'x':
	# 		op_flag = 'o'
	# 	else:
	# 		op_flag = 'x'

	# 	if sorted([small_board[0][0], small_board[0][1], small_board[0][2]]) == [op_flag, flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[1][0], small_board[1][1], small_board[1][2]]) == [op_flag, flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[2][0], small_board[2][1], small_board[2][2]]) ==  [op_flag, flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][0], small_board[2][0]]) ==  [op_flag, flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][1], small_board[1][1], small_board[2][1]]) ==  [op_flag, flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[0][2], small_board[1][2], small_board[2][2]]) ==  [op_flag, flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][1], small_board[2][2]]) ==  [op_flag, flag, flag]  :
	# 		count = 4

	# 	if sorted([small_board[0][2], small_board[1][1], small_board[2][0]]) ==  [op_flag, flag, flag]  :
	# 		count = 4
	# 	#
	# 	op_flag = 'd'
	# 	if sorted([small_board[0][0], small_board[0][1], small_board[0][2]]) == [op_flag, flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[1][0], small_board[1][1], small_board[1][2]]) == [op_flag, flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[2][0], small_board[2][1], small_board[2][2]]) ==  [op_flag, flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][0], small_board[2][0]]) ==  [op_flag, flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][1], small_board[1][1], small_board[2][1]]) ==  [op_flag, flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[0][2], small_board[1][2], small_board[2][2]]) ==  [op_flag, flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][0], s100000mall_board[1][1], small_board[2][2]]) ==  [op_flag, flag, flag]  :
	# 		count = 4

	# 	if sorted([small_board[0][2], small_board[1][1], small_board[2][0]]) ==  [op_flag, flag, flag]  :
	# 		count = 4
		
	# 	#break
	# 	if flag == 'x':
	# 		op_flag = 'o'
	# 	else:
	# 		op_flag = 'x'

	# 	if sorted([small_board[0][0], small_board[0][1], small_board[0][2]]) == [op_flag, op_flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[1][0], small_board[1][1], small_board[1][2]]) == [op_flag, op_flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[2][0], small_board[2][1], small_board[2][2]]) ==  [op_flag, op_flag, flag] :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][0], small_board[2][0]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][1], small_board[1][1], small_board[2][1]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 3

	# 	if sorted([small_board[0][2], small_board[1][2], small_board[2][2]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 1

	# 	if sorted([small_board[0][0], small_board[1][1], small_board[2][2]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 4

	# 	if sorted([small_board[0][2], small_board[1][1], small_board[2][0]]) ==  [op_flag, op_flag, flag]  :
	# 		count = 4
		
	# 	if flag == 'x':
	# 		return 100 - count
	# 	if flag == 'o':
	# 		return 50 + 20*count

	# def probabilty_board(self, small_board):
	# 	count = 0
	# 	for i in range(3):
	# 		for j in range(3):
	# 			if small_board[i][j] == 'x':
	# 				count += 1
	# 	return count/9


	# def small_heur(self, board, flag, op_flag):
	# 	op = 0
	# 	c = 0
	# 	small_h = [[7, 6, 4], [7, 7, 2], [7, 4, 4]]    #meddle
	# 	for i in range(3):
	# 		for j in range(3):
	# 			if board[i][j] == op_flag :
	# 				op += 1
		
	# 	if op >= 4:
	# 		return 0
	# 	#meddle with x (the c+= x)
	# 	else:
	# 		if board[1][1] == flag:
	# 			c += 5

	# 		if board[0][1] == flag:
	# 			c += 2
	# 		if board[1][0] == flag:
	# 			c += 2
	# 		if board[2][1] == flag:
	# 			c += 2
	# 		if board[1][2] == flag:
	# 			c += 2

	# 		if board[0][0] == flag:
	# 			c += 4 
	# 		if board[0][2] == flag:
	# 			c += 4 
	# 		if board[2][2] == flag:
	# 			c += 4 
	# 		if board[2][0] == flag:
	# 			c += 4 
	# 	return c

	# def heuristic(self, flag, board):

	# 	curr_heur = 0
	# 	sb_stats = board.small_boards_status 
	# 	bb_stats = board.big_boards_status

	# 	if flag=='x':
	# 		op_flag = 'o'
	# 	else:
	# 		op_flag = 'x'

		

	# 	if self.winning_patterns(sb_stats[0]) > 50:
	# 		return 300

	# 	if self.winning_patterns(sb_stats[1]) > 50:
	# 		return 300

	# 	if self.winning_patterns(sb_stats[0]) < 50:
	# 		return -300

	# 	if self.winning_patterns(sb_stats[1]) < 50:
	# 		return -300

	
		

		

	# 	blockWts = [[[7,2,3], [6,40,2], [5,2,3]], [[3,2,3], [2,40,2], [8,8,8]]]                               # meddle with these values

	# 	for boa in range(2):
	# 		for r in range(0, 3, 6):
	# 			for c in range(0, 3, 6):

	# 				tiny_board = [[bb_stats[boa][r][c], bb_stats[boa][r][c+1],bb_stats[boa][r][c+2]], 
	# 							  [bb_stats[boa][r+1][c], bb_stats[boa][r+1][c+1],bb_stats[boa][r+1][c+2]], 
	# 							  [bb_stats[boa][r+2][c], bb_stats[boa][r+2][c+1],bb_stats[boa][r+2][c+2]]];

	# 				curr_heur += self.blocking_patterns(tiny_board, 'x')
	# 				temp = blockWts[boa][r/3][c/3]*(self.probabilty_board(tiny_board))*40
					
	# 				if temp < 50:
	# 					curr_heur -= temp
	# 				else:
	# 					curr_heur += temp

					

	# 				if self.winning_patterns(tiny_board) < 50:
	# 					curr_heur -= 50
	# 				if self.winning_patterns(tiny_board) > 50:
	# 					curr_heur += 50

	# 	return curr_heur

	# # def newHeur(self, flag, board) :

	# # 	small_x_count = 0
	# # 	small_o_count = 0
	# # 	big_x_count = 0
	# # 	big_o_count = 0
	# # 	for i in range(0, 2) :
	# # 		for j in range(0, 3) :
	# # 			for k in range(0, 3) :
	# # 				if 

	# # 				if 

	def hueristic_1(self, flag, board):

		
		terminal_state = 100000
		heuristic_value = 0
		small_board_multiplier = 50



		status_player, status = board.find_terminal_state()
		if status == "WON" :
			if status_player == "P1" :
				if flag == 'x':
					return terminal_state
			if status_player == "P2":
				if flag == 'o':
					return -terminal_state


		k,x,y = 0,0,0
		while k < 2 :
			while x < 9 :
				while y < 9 :
					if board.small_boards_status[k][x//3][y//3] == '-' and board.big_boards_status[k][x][y] == 'o' and x % 3 == 1 and y % 3 == 1 :
						heuristic_value = heuristic_value - 4
					elif board.small_boards_status[k][x//3][y//3] == '-' and board.big_boards_status[k][x][y] == 'o' and x % 3 != 1 and y % 3 != 1 :
						heuristic_value = heuristic_value - 3
					elif board.small_boards_status[k][x//3][y//3] == '-' and board.big_boards_status[k][x][y] == 'o' :
						heuristic_value = heuristic_value - 2
					elif board.small_boards_status[k][x//3][y//3] == '-' and board.big_boards_status[k][x][y] == 'x' and x % 3 == 1 and y % 3 == 1 :
						heuristic_value = heuristic_value + 4
					elif board.small_boards_status[k][x//3][y//3] == '-' and board.big_boards_status[k][x][y] == 'x' and x % 3 != 1 and y % 3 != 1 :
						heuristic_value = heuristic_value + 3
					elif board.small_boards_status[k][x//3][y//3] == '-' and board.big_boards_status[k][x][y] == 'x' :
						heuristic_value = heuristic_value + 2
					y += 1
				x += 1
			k += 1

		k,x,y = 0,0,0
		while k < 2 :
			while x < 3 :
				while y < 3 :
					if board.small_boards_status[k][x][y] == 'o' and x % 3 == 1 and y % 3 == 1 :
						heuristic_value = heuristic_value - small_board_multiplier * 4 
					elif board.small_boards_status[k][x][y] == 'o' and x % 3 != 1 and y % 3 != 1 :
						heuristic_value = heuristic_value - small_board_multiplier * 3 
					elif board.small_boards_status[k][x][y] == 'o' :
						heuristic_value = heuristic_value - small_board_multiplier * 2 
					elif board.small_boards_status[k][x][y] == 'x' and x % 3 == 1 and y % 3 == 1 :
						heuristic_value = heuristic_value + small_board_multiplier * 4 
					elif board.small_boards_status[k][x][y] == 'x' and x % 3 != 1 and y % 3 != 1 :
						heuristic_value = heuristic_value + small_board_multiplier * 3 
					elif board.small_boards_status[k][x][y] == 'x' :
						heuristic_value = heuristic_value + small_board_multiplier * 2 
					y += 1
				x += 1
			k += 1
		
		return heuristic_value
