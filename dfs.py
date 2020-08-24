import sys

class Maze(object):

    def __init__(self):
        self.data = []

    def read_maze(self, path):       
        """reads the text file of the maze"""
        maze = []
        with open(path) as f:
            for line in f.read().splitlines():
                maze.append(list(line))
        self.data = maze

    def write_maze(self, path):
        """writes the new maze to the output file"""
        with open(path, 'w') as f:
            for r, line in enumerate(self.data):
                f.write('%s\n' % ''.join(line))

    def find_start(self):
        """returns the location of P to find the start of the maze"""
        for r, line in enumerate(self.data):
            try:
                return r, line.index('P')
            except ValueError:
                pass

    def get_symbol(self, location):
        """returns the symbol of the node in the given location"""
        """get the coordinates of the location"""
        r, c = location 
        return self.data[r][c]

    def set_symbol(self, location, symbol):
        """sets the symbol of the given location to the symbol given"""
        r, c = location
        self.data[r][c] = symbol

    def __str__(self):
        return '\n'.join(''.join(r) for r in self.data)


    def get_neighbours(self,location):
        """returns the neighbours of the given node"""
        r,c = location
        neighbours = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]    
        return neighbours
    

def solve(maze):
    """find the start of the maze and add it to the top of the stack"""
    start = maze.find_start()

    wall = '%'
    goal = '.'
    stack = set()
    visited = set()
    stack.add(start)
    count = 1 
    """count keeps track of the nodes expanded"""

    
    """keeps going until the stack is empty or the goal is reached"""
    while stack:
        current = stack.pop()
        """get the symbol of the current node to see if it is the goal and does not need to be expanded further"""
        symbol = maze.get_symbol(current)
        if current in visited:         
            continue
        if symbol == goal:
            return maze, visited,count
       

        for neighbour in maze.get_neighbours(current):
            n_symbol = maze.get_symbol(neighbour)
            count = count+1; 
            """makes sure the neighbour node is not a wall so that it is not added to the stack of nodes to be expanded on"""
            if n_symbol != wall:
                """adds to the neighbours of the current node to the dfs stack"""
                stack.add(neighbour)
        """keeps track of the nodes visited"""
        visited.add(current)
    
        if symbol == 'P':
            maze.set_symbol(current,'P')
        else:
            """creates the path of visited nodes"""
            maze.set_symbol(current,'.') 
                              

    
    
      
    
    
input_file, output_file = sys.argv[1:3]

maze = Maze()
maze.read_maze(input_file)

solution,visited, count = solve(maze)
print('steps taken: {0}'.format(len(visited)))
print('nodes expanded: {0}'.format(count))

print (maze)
maze.write_maze(output_file)


