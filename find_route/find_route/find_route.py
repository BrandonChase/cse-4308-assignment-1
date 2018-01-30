"""
      Author: Brandon Chase
          ID: 1001132518
 Description: This program takes uses a Uniform Cost Graph Search to find the optimal path between a given origin city and a given destination city. The map of cities is provided by an input file.
  How to Use: In the terminal, do 'find_route input_file origin_city destination_city'.
"""

import sys #command-line arguments
import operator #sorting fringe

class Path(object):
    """Data stucture for storing paths between cities and associated distances"""
    def __init__(self, origin, destination, distance):
        self.origin = origin
        self.destination = destination
        self.distance = distance

    def __repr__(self):
        return "Path from %s to %s: %d miles" % (self.origin, self.destination, self.distance)

class Node(object):
    """Data structure for storing useful information about each node generated in the path search"""
    def __init__(self, city, previous_node=None, path_cost=None):
        """Can be used for both a root node with only the city name or as a child node with all arguments"""
        
        self.city = city

        if previous_node is None: #must be parent node, so initialize with appropriate values
            self.previous_node = None
            self.depth = 0
            self.distance = 0

        else: #node is a child node, so calculate its values based on previous node's values
            self.previous_node = previous_node
            self.depth = previous_node.depth + 1
            self.distance = previous_node.distance + path_cost

class RouteFinder(object):
    """Class that loads paths from file and can search for optimal route"""
    def __init__(self, filename):
        """Parameter is the name of the file that stores all the paths of the map"""
        self.paths = self.load_paths(filename)

    def __repr__(self):
        """Reports for each city, all the paths available from that city"""
        result = ""
        for origin_city in self.paths:
            for path in self.paths[origin_paths]:
                result += repr(path) + "\n"
        return result

    #public
    def search(self, origin, destination):
        """Given origin city and destination city, returns node that contains information to rebuild path"""
        fringe = [] #list of nodes that are next in line to be evaluated, sorted by total path distance
        previously_visited_cities = [] #used so that search does not get stuck in literal infinite loop
        fringe.append(Node(origin)) #initialize fringe with origin city

        while len(fringe) > 0: #fringe being empty means no path was able to be found
            current_node = fringe.pop(0) #next node to be evaluated is the one with shortest path distance (at front of fringe)
            if current_node.city == destination: #path found
                return current_node
            if current_node.city not in previously_visited_cities: #avoid looping back to previous city
                previously_visited_cities.append(current_node.city)
                fringe += self.expand(current_node)
                fringe.sort(key=operator.attrgetter('distance')) #in order to be Uniform Cost Search, fringe must be sorted by path distance

        return None #if no path is found, return node with no information

    def print_route(self, node):
        """Prints the route that the node contains; the node is the result of a map search for a route"""
        path = []
        if(node is None): #node is result of unsuccessful search
            print "distance: infinity\nroute:\nnone"
        
        else:
            print "distance: " + str(node.distance) + " km" #print total distance

            while node != None: #rebuild path by exploring all ancestor nodes until node before root node is reached 
                path.insert(0, node)
                node = node.previous_node

            print "route:"
            for i in range(0, len(path) - 1): #print the paths taken at each step of route and the distance of each path
                print path[i].city + " to " + path[i+1].city + ", " + str(path[i+1].distance - path[i].distance) + " km" #the distance between each node in path can be found by finding difference between total distance of child node and parent node

    #private
    def load_paths(self, filename):
        """Returns a dictionary representing the paths of the map given the name of a file that is the text representation of the map"""
        paths = {} #paths is a dictionary with the origin city as the key and a list of paths from the origin city as the value
        input_file = open(filename, "r")
        try:    
            lines =  input_file.readlines()
            for line in lines:
                if "END OF INPUT" in line:
                    break; #don't read past end of file
                else:
                    items = line.split() #items separated by space
                    #add path from origin to destination
                    paths.setdefault(items[0],[]).append(Path(items[0], items[1], int(items[2]))) #setdefault ensures that if the origin city is not in dictionary yet, initialize its value list before adding the path
                    #add path from destination to origin since it is a two way street
                    paths.setdefault(items[1],[]).append(Path(items[1], items[0], int(items[2]))) #setdefault ensures that if the origin city is not in dictionary yet, initialize its value list before adding the path
        finally:
            input_file.close()
        return paths
    
    def expand(self, parent_node):
        """Given parent node, generates children nodes using the map"""
        paths = self.get_paths_from_city(parent_node.city)
        children_nodes = []
        for path in paths:
            children_nodes.append(Node(path.destination, parent_node, path.distance)) #path.destination is city name of the child node
        return children_nodes

    def get_paths_from_city(self, city):
        """returns list of paths from origin city"""
        return self.paths[city]

def main(args):
    #load paths into list of paths
    map_filename = args[1]
    route_finder = RouteFinder(map_filename)

    #find path given origin and destination
    origin = args[2]
    destination = args[3]
    route = route_finder.search(origin, destination)

    #print results
    route_finder.print_route(route)

if __name__ =='__main__':
    main(sys.argv)
