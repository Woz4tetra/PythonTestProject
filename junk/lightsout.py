
import copy
import time

def create_array(value, width, height):
    return [[copy.copy(value) for _ in xrange(width)] for _ in xrange(height)]

class Board():
    def __init__(self, width, height, *init_state):
        self.parent = None
        self.state = 0
        self.width = width
        self.height = height
        
        for (row, col) in init_state:
            self.flip(row, col)
    
    def get(self, index):
        return self.state >> index & 1
    
    def to_index(self, row, col):
        return row * self.width + col
    
    def __repr__(self):
        board_str = "\n"
        for row in xrange(self.width):
            for col in xrange(self.height):
                if self.get(self.to_index(row, col)) == True:
                    board_str += "#"
                else:
                    board_str += "0"
            board_str += "\n"
        return board_str
    
    def tolist(self):
        list_board = []
        for row in xrange(self.width):
            for col in xrange(self.height):
                if self.get(self.to_index(row, col)) == True:
                    list_board.append([row, col])
        return list_board
    
    def flip(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            index = self.to_index(row, col)
            bit = (not self.get(index)) << index
            upper = (self.state >> (index + 1)) << (index + 1)
            if index > 0:
                lower = self.state % (2 << (index - 1))
            else:
                lower = 0
            self.state = upper + bit + lower
    
    def touch(self, row, col):
        if 0 <= row < self.width and 0 <= col < self.height:
            new_board = Board(self.width, self.height, *self.tolist())
            
            new_board.flip(row, col - 1)
            
            new_board.flip(row - 1, col)
            new_board.flip(row, col)
            new_board.flip(row + 1, col)
            
            new_board.flip(row, col + 1)
            
            return new_board
        else:
            return self
    
    def solved(self):
        for row in xrange(self.width):
            for col in xrange(self.height):
                if self.get(self.to_index(row, col)) == True:
                    return False
        return True
    
    def __hash__(self):
        return hash(str(self))

def solve_board(init_board):
    considered_boards = {}
    board_queue = [init_board]
    
    while len(board_queue) > 0:
        board = board_queue.pop(0)
        
        for row in xrange(board.width):
            for col in xrange(board.height):
                new_board = board.touch(row, col)
                
                if hash(new_board) not in considered_boards:
                    new_board.parent = board
                    considered_boards[hash(new_board)] = new_board
                    board_queue.append(new_board)
                if new_board.solved():
                    solution = []
                    trace_board = new_board.parent
                    while trace_board != None:
                        solution.append(trace_board)
                        trace_board = trace_board.parent
                    
                    solution.insert(0, new_board)
                    return solution[::-1]
    return None

def solve():
    my_board = Board(3, 3, (1, 1))
    print hex(my_board.state)
    
    time0 = time.time()
    solution = solve_board(my_board)
    time1 = time.time()
    
    print time1 - time0
    return solution



print solve()
