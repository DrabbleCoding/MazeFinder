from queue import Queue

'''
Asks the user for file name to open.
Takes each line of the file and puts it into a list.
'''
def openFile():
    try:
        name = input("File name: ")
        file = open(name, 'r')
        lines = file.read().splitlines()
        file.close()
    except:
        print("Error opening file.")
        return [[]]
    
    return lines
    
'''
Given the maze in list form, return the coordinates in list form of the start and end
'''
def findKeyPoints(maze):
    length = len(maze)
    width = len(maze[0])
    i = 0
    j = 0
    start = {-1,-1}
    end = {-1, -1}
    flag = False
    
    while i < length and j < width and not flag:
        if maze[i][j] == 'P':
            start = [i, j]
        
        if maze[i][j] == '.':
            end = [i, j]
        
        i += 1
        
        if i >= length:
            i = 0
            j += 1
            
    return start, end

'''
Check current coordinates for adjacent accessible areas
'''
def findAccessibleArea(a, maze):
    result = []
    if maze[a[0]-1][a[1]] == ' ' or maze[a[0]-1][a[1]] == '.':
        result.append([a[0]-1, a[1]])
    if maze[a[0]+1][a[1]] == ' ' or maze[a[0]+1][a[1]] == '.':
        result.append([a[0]+1, a[1]])
    if maze[a[0]][a[1]-1] == ' ' or maze[a[0]][a[1]-1] == '.':
        result.append([a[0], a[1]-1])
    if maze[a[0]][a[1]+1] == ' ' or maze[a[0]][a[1]+1] == '.':
        result.append([a[0], a[1]+1])
    
    return result

'''
Perform a Breadth-first search given a start coordinate, end coordinate, and a maze list
'''
def solveMaze(start, end, maze):
    
    q = Queue()
    q.insert(start)
    
    explored = []
    
    while not q.isEmpty():
        state = q.remove()
        explored.append(state)
        
        if state == end:
            path = findPath(explored)
            return path, explored
        
        neighbours = findAccessibleArea(state, maze)
        
        for neighbour in neighbours:
            if neighbour not in explored and neighbour not in q.contents():
                q.insert(neighbour)
                
    return [], []

'''
Given a list of explored nodes, find the nodes that connect the start to the end
'''
def findPath(explored):
    path = [explored[-1]]
    for i in range(len(explored) - 2, 0, -1):
        if (path[-1][0] == explored[i][0] and abs(path[-1][1] - explored[i][1]) == 1) or (path[-1][1] == explored[i][1] and abs(path[-1][0] - explored[i][0]) == 1):
            path.append(explored[i])
    return path

'''
Takes a list of coordinates and replaces the characters in the maze at the given coordinates with '.'
'''
def highlightSolution(maze, path):
    newMaze = ""
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            value = [i, j]
            if value in path:
                newMaze += '.'
            else:
                newMaze += maze[i][j]
        newMaze += '\n'
    
    return newMaze


'''
Run the file. Prints the Solution path cost, total nodes visited, and the maze solution.
'''
maze = openFile()

start, end = findKeyPoints(maze)
path, explored = solveMaze(start, end, maze)
solution = highlightSolution(maze, path)

print("Path cost from initial state to the goal state: " + str(len(path)))
print("Nodes expanded by search: " + str(len(explored)))
print(solution)