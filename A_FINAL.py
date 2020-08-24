#A* search algorithm

import numpy as np

class Node:
    #This will be the node class used for this assignment question
    #location is location relative to the maze
    #parent precedes child node
    #f is the total cost of the node, where f = g+h
    #g = cost from start to current node
    #h = heuristic cost from current node to end

#initialize the node
    def __init__(self, parent=None, location=None):
        self.parent = parent
        self.location = location

        self.f = 0
        self.h = 0
        self.g = 0

#comparative function for evaluation nodes
    def __eq__(self, other):
        return self.location == other.location

#find optimal path and return it
def return_path(current_node,map):
    path = []
    no_rows, no_columns = np.shape(map)
    # initialize a 2d array as the maze with a -1 for all the value
    res = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.location)
        current = current.parent
    # reverse the path and return it from start to finish
    path = path[::-1]
    start_value = 0
    # assign unique values to every node included in the final path, starting at 0 and incrementing by 1
    for i in range(len(path)):
        res[path[i][0]][path[i][1]] = start_value
        start_value += 1
        
        #uncomment the line below to find the highest start value and therefore the path cost for a given maze
        #print(start_value)
    return res


def search(map, cost, start, end):
    
    # Returns a list of tuples as a path from the given start to the given end in the given maze
    # :param map:
    # :param cost
    # :param start:
    # :param end:
    # :return:

    # Create start and end node with initized values for g, h and f
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both yet_to_visit and visited list
    # in this list we will put all node that are yet_to_visit for exploration. 
    # From here we will find the lowest cost node to expand next
    yet_to_visit_list = []  
    # in this list we will put all node those already explored so that we don't explore it again
    visited_list = [] 
    
    # Add the start node
    yet_to_visit_list.append(start_node)
    
    # Adding a stop condition. This is to avoid any infinite loop and stop 
    # execution after some reasonable number of steps
    outer_iterations = 0
    max_iterations = (len(map) // 2) ** 10

    # what squares do we search . serarch movement is left-right-top-bottom 
    #(4 movements) from every positon

    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ]] # go right



    #find maze has got how many rows and columns 
    no_rows, no_columns = np.shape(map)
    
    # Loop until you find the end
    
    while len(yet_to_visit_list) > 0:
        
        # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
        outer_iterations += 1    
        # outer operations counts the number of expanded by the search algorithm, uncomment the line below to see the total count
        #print(outer_iterations)
        
        # Get the current node
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        # if we hit this point return the path such as it may be no solution or 
        # computation cost is too high
        if outer_iterations > max_iterations:
            print("giving up on pathfinding too many iterations")
            return return_path(current_node,map)

        # Pop current node out off yet_to_visit list, add to visited list
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        # test if goal is reached or not, if yes then return the path
        if current_node == end_node:
            return return_path(current_node,map)

        # Generate children from all adjacent squares
        children = []

        for new_location in move: 

            # Get node location
            node_location = (current_node.location[0] + new_location[0], current_node.location[1] + new_location[1])

            # Make sure within range (check if within map boundary)
            if (node_location[0] > (no_rows - 1) or 
                node_location[0] < 0 or 
                node_location[1] > (no_columns -1) or 
                node_location[1] < 0):
                continue

            # Make sure walkable terrain
            if map[node_location[0]][node_location[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_location)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            
            # Child is on the visited list (search entire visited list)
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + cost
            ## Heuristic costs calculated here, this is using eucledian distance
            child.h = (((child.location[0] - end_node.location[0]) ** 2) + 
                       ((child.location[1] - end_node.location[1]) ** 2)) 

            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and g cost is already lower
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            # Add the child to the yet_to_visit list
            yet_to_visit_list.append(child)


if __name__ == '__main__':

    #convert input into 2d number array so that the values are easier to work with
    def map_construct(filename):
            
            f = open(filename, "r")
            map = f.read()
            row = []
            col = []
            Rcount = 0
            Ccount = 0
            for i in map:
                
                if i == '\n':
                    col.append(row)
                    Ccount = 0
                    Rcount +=1
                    row = []
                else:
                    if i == "%":
                        row.append(-1)
                    if i == " ":
                        row.append(0)
                    if i == ".":
                        row.append(0)
                        start = [Rcount, Ccount]
                    if i == "P":
                        row.append(0)
                        end = [Rcount, Ccount]
                    
                    Ccount+=1
                
            #print(map)
            #for i in col:
                #print(i)
            return start, end, col
    start, end, map = map_construct("mediumMaze.txt")
    cost = 1 # cost per movement



    path = search(map,cost, start, end)
    Iint= 0
    Jint = 0
    

    for i in map:
        for j in i:
            if start[0] == Iint and start[1] == Jint:
                map[Iint][Jint] = 1
            if path[Iint][Jint] > 0:
                map[Iint][Jint] = path[Iint][Jint]
            Jint+=1
        Iint +=1
        Jint = 0
    file = open("solutionMedium.txt", "w")
    
    #print 2d map array back into text file
    for i in map:
        for j in i:
            line = ""
            if j == -1:
                file.write("$")
            if j == 0:
                file.write(" ")
            if j > 0:
                file.write(".")
        file.write("\n")
        
    start, end, map = map_construct("bigMaze.txt")
    cost = 1 # cost per movement

    path = search(map,cost, start, end)
    Iint= 0
    Jint = 0
    for i in map:
        for j in i:
            if start[0] == Iint and start[1] == Jint:
                map[Iint][Jint] = 1
            if path[Iint][Jint] > 0:
                map[Iint][Jint] = path[Iint][Jint]
            Jint+=1
        Iint +=1
        Jint = 0
    file = open("solutionBig.txt", "w")
    #print 2d map array back into text file
    for i in map:
        for j in i:
            line = ""
            if j == -1:
                file.write("$")
            if j == 0:
                file.write(" ")
            if j > 0:
                file.write(".")
        file.write("\n")
     
        
        