import sys

class Path(object):
    def __init__(self, destination, distance):
        self.destination = destination
        self.distance = distance

    def __repr__(self):
        return "%s: %d miles" % (self.destination, self.distance)

def load_tree(filename):
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

    return tree

def main(args):
    #load paths into list of paths
    tree = load_tree(args[1])
    print tree
    #find path given origin and destination
    #print results
    pass

if __name__ =='__main__':
    main(sys.argv)
