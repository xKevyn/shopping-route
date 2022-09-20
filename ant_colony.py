class Node:
    def __init__(self, name, category, floor):
        self.name = name
        self.category = category
        self.floor = floor
    
class Path:
    def __init__(self, node1, node2, distance, time, stamina):
        self.node1 = node1
        self.node2 = node2
        self.distance = distance
        self.time = time
        self.stamina = stamina
        
class AntColony:
    def __init__(self, paths):
        self.paths = paths
        
    def initialisation():
        ...
        
if __name__ == "__main__":
    state_space = [
        Path(Node('a', 't', 1), Node('b', 't', 1), 1, 1, 1), 
        Path(Node('a', 't', 1), Node('c', 't', 1), 2, 2, 3), 
        Path(Node('a', 't', 1), Node('d', 't', 1), 3, 3, 3)
        ]
    
    print(state_space[0].node1.name)
