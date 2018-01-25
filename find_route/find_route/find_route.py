import sys

class Path(object):
    def __init__(self, origin, destination, distance):
        self.origin = origin
        self.destination = destination
        self.distance = distance

    def __repr__(self):
        return "%s to %s: %d miles" % (self.origin, self.destination, self.distance)

def load_paths(filename):
    paths = []
    with open(filename, "r") as input_file:
        lines =  input_file.readlines()
        for line in lines:
            if line == "END OF INPUT\n":
                break;
            else:
                items = line.split()
                paths.append(Path(items[0], items[1], int(items[2])))
            
    return paths

def main(args):
    #load paths into list of paths
    paths = load_paths(args[1])
    for path in paths:
        print path
    #find path given origin and destination
    #print results
    pass

if __name__ =='__main__':
    main(sys.argv)
