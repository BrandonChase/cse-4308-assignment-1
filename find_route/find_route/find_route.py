import sys
import operator

class Path(object):
    def __init__(self, destination, distance):
        self.destination = destination
        self.distance = distance

    def __repr__(self):
        return "to %s: %d miles" % (self.destination, self.distance)

class Node(object):
    def __init__(self, city, previous_node=None, path_cost=None):
        self.city = city
        self.previous_node = previous_node
        if previous_node is None:
            self.previous_node = None
            self.depth = 0
            self.distance = 0
        else:
            self.depth = previous_node.depth + 1
            self.distance = previous_node.distance + path_cost

class PathFinder(object):
    def __init__(self, filename):
        self.load_tree(filename)

    def __repr__(self):
        result = ""
        for city in self.tree:
            result += city + ":\n"
            for path in self.tree[city]:
                result += "\t" + repr(path) + "\n"
        return result

    def load_tree(self, filename):
        tree = {}
        with open(filename, "r") as input_file:
            lines =  input_file.readlines()
            for line in lines:
                if line == "END OF INPUT\n":
                    break;
                else:
                    items = line.split()
                    #add path from origin to destination
                    tree.setdefault(items[0],[]).append(Path(items[1], int(items[2])))
                    #add path from destination to origin since it is a two way street
                    tree.setdefault(items[1],[]).append(Path(items[0], int(items[2])))
        self.tree = tree

    def get_paths_from_city(self, city):
        return self.tree[city]

    def get_path_distance(self, origin, destination):
        paths = self.tree[origin]
        for path in paths:
            if path.destination == destination:
                return path.distance

    def search(self, origin, destination):
        fringe = []
        visited_cities = []
        fringe.append(Node(origin))
        while len(fringe) > 0:
            current_node = fringe.pop(0)
            if current_node.city == destination:
                return current_node
            if current_node.city not in visited_cities:
                visited_cities.append(current_node.city)
                fringe += self.expand(current_node)
                fringe.sort(key=operator.attrgetter('distance'))
        return None
    def expand(self, parent_node):
        paths = self.get_paths_from_city(parent_node.city)
        nodes = []
        for path in paths:
            nodes.append(Node(path.destination, parent_node, path.distance))
        return nodes

    def print_path(self, node):
        path = []
        if(node is None):
            print "distance: infinity\nroute:\nnone"
        
        else:
            print "distance: " + str(node.distance) + " km"
            while node != None:
                path.insert(0, node)
                node = node.previous_node

            print "route:"
            for i in range(0, len(path) - 1):
                print path[i].city + " to " + path[i+1].city + ": " + str(self.get_path_distance(path[i].city, path[i+1].city)) + " km"

def main(args):
    #load paths into list of paths
    pf = PathFinder(args[1])
    #find path given origin and destination
    origin = str(raw_input("Origin: "))
    destination = str(raw_input("Destination: "))
    final_node = pf.search(origin, destination)
    #print results
    pf.print_path(final_node)

if __name__ =='__main__':
    main(sys.argv)
