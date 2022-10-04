import random
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name, category, floor):
        self.name = name
        self.category = category
        self.floor = floor
        self.roads = []
        self.coordinates = []
    
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    
    def add_road(self, path):
        if path not in self.roads:
          self.roads.append(path)
        
class Road:
    def __init__(self, connected_nodes, distance, time, stamina, pheromone=0): # or random small number
        self.connected_nodes = connected_nodes
        self.distance = distance
        self.time = time
        self.stamina = stamina
        self.pheromone = pheromone
        
    def set_pheromone(self, pheromone):
        self.pheromone = pheromone
        
    def evaporate_pheromone(self, rho):
    # update the pheromone of the path
        self.pheromone = (1-rho)*self.pheromone
    
    def deposit_pheromone(self, ants):
    # 1. search for ants that uses the raod
    # 2. deposit pheromone using the inversely proportionate relationship between path length and deposited pheromone
        for ant in ants:
            for path in ant.path:
                if self == path:
                    self.pheromone += 1/(ant.get_path_all_cost())**1
                    break

class Ant:
    def __init__(self):
      self.nodes = [] # nodes the ant passes through, in sequence
      self.path = [] # roads the ant uses, in sequence
    
    def get_path(self, origin, destination, alpha):
    # 1. append origin to the self.nodes
    # 2. if the last node is not destination, search for the next node to go
    # 3. after getting to the destination, remove the loop within the path, i.e. if there are repeated nodes in self.nodes, remove the nodes and the roads in between the repetition
        self.nodes.append(origin)
        while self.nodes[-1] is not destination:
            if len(self.path) > 0:
                available_roads = [r for r in self.nodes[-1].roads if r is not self.path[-1]]
            else:
                available_roads = self.nodes[-1].roads
            if len(available_roads) == 0:
                available_roads = [self.path[-1]]
            pheromones_alpha = [r.pheromone**alpha for r in available_roads]
            probabilities = [pa/sum(pheromones_alpha) for pa in pheromones_alpha]
            acc_probabilities = [sum(probabilities[:i+1]) for i,p in enumerate(probabilities)]
            chosen_value = random.random()
            for ai, ap in enumerate(acc_probabilities):
                if ap > chosen_value:
                    break
            self.path.append(available_roads[ai])
            if self.path[-1].connected_nodes[0] is self.nodes[-1]:
                self.nodes.append(self.path[-1].connected_nodes[1])
            else:
                self.nodes.append(self.path[-1].connected_nodes[0])
            
        while len(set(self.nodes)) != len(self.nodes):
            for i, node in enumerate(set(self.nodes)):
                node_indices = [i for i, x in enumerate(self.nodes) if x == node]
                if len(node_indices) > 1:
                    self.nodes = self.nodes[:node_indices[0]] + self.nodes[node_indices[-1]:]
                    self.path = self.path[:node_indices[0]] + self.path[node_indices[-1]:]
                    break
        
    def get_path_distance(self):
        path_distance = sum([i.distance for i in self.path])
        return path_distance
    # calculate path distance based on self.path
       # return path_distance
       
    def get_path_all_cost(self):
        path_all_cost = sum([i.distance for i in self.path]) + sum([i.time for i in self.path]) + sum([i.stamina for i in self.path])
        return path_all_cost
    
    def reset(self):
        self.path = []
        self.nodes = []

def get_frequency_of_paths(ants):
    paths = []
    nodes = []
    frequencies = []
    for ant in ants:
        if len(ant.path) != 0:
            if ant.path in paths:
                frequencies[paths.index(ant.path)] += 1
            else:
                paths.append(ant.path)
                nodes.append(ant.nodes)
                frequencies.append(1)
    return [frequencies, paths, nodes]

def get_percentage_of_dominant_path(ants):
    [frequencies, _, _] = get_frequency_of_paths(ants)
    if len(frequencies) == 0:
        percentage = 0
    else:
        percentage = max(frequencies)/sum(frequencies)
    return percentage

def create_graph(nodes):
      plt.figure()
      ax = plt.axes(projection='3d')
      nodes_x = [node.coordinates[0] for key, node in nodes.items()]
      nodes_y = [node.coordinates[1] for key, node in nodes.items()]
      nodes_z = [node.floor for key, node in nodes.items()]
      ax.scatter(nodes_x, nodes_y, nodes_z)
      for i, node in enumerate(nodes):
          ax.text(nodes_x[i], nodes_y[i], nodes_z[i], node, size=7, color="k")
      return ax
    
def draw_pheromone(ax, roads):
  lines = []
  for road in roads:
    from_coord = road.connected_nodes[0].coordinates
    to_coord = road.connected_nodes[1].coordinates
    coord_x = [from_coord[0], to_coord[0]]
    coord_y = [from_coord[1], to_coord[1]]
    coord_z = [road.connected_nodes[0].floor, road.connected_nodes[1].floor]
    lines.append(ax.plot(coord_x, coord_y, coord_z, c='red', linewidth=road.pheromone*5))
  return lines

def draw_path(ax, solution):
    lines = []
    colors = []
    count = 0
    for i in range(20):
        colors.append('#%06X' % random.randint(0, 0xFFFFFF))
    for path in solution:
        for road in path[0]:
            from_coord = road.connected_nodes[0].coordinates
            to_coord = road.connected_nodes[1].coordinates
            coord_x = [from_coord[0], to_coord[0]]
            coord_y = [from_coord[1], to_coord[1]]
            coord_z = [road.connected_nodes[0].floor, road.connected_nodes[1].floor]
            lines.append(ax.plot(coord_x, coord_y, coord_z, c=colors[count], linewidth=1))
        count += 1
    return lines

def aco(iteration, roads, ants, origin, destination, max_iteration=200, percentage_of_dominant_path=0.9):
    while iteration < max_iteration or get_percentage_of_dominant_path(ants) < percentage_of_dominant_path: # termination conditions
      # loop through all the ants to identify the path of each ant
      for ant in ants:
        # reset the path of the ant
        ant.reset()
        # identify the path of the ant
        ant.get_path(origin, destination, alpha)

      # loop through all roads
      for road in roads:
        # evaporate the pheromone on the path
        road.evaporate_pheromone(rho)
        # deposit the pheromone
        road.deposit_pheromone(ants)
        
      # increase iteration count
      iteration += 1
      
if __name__ == "__main__":
    
    location_list = [ # [ name, category, x, y, floor]
        ["Harvey Norman","Digital & Home Appliances", 5, 3, 1],
        ["McDonald" , "Food & Beverages", 7, 7, 1],
        ["KFC" , "Food & Beverages", 8, 4, 1],
        ["MyNews" , "Supermarket", 3, 6, 1],
        ["Optical Arts" , "Optical", 3, 4, 1],
        ["Lavender Bakery" , "Bakery", 2, 8, 1],
        ["7-Eleven" , "Supermarket", 9, 7, 1],
        ["Adidas","Fashion", 2, 7, 2],
        ["Uniqlo-2" , "Fashion", 5, 7, 2],
        ["Starbuck" , "Food & Beverages", 2, 2, 2],
        ["Popular" , "Leisure & Entertainment", 5, 2, 2],
        ["SenQ" , "Digital & Home Appliances", 8, 7, 2],
        ["Komugi" , "Bakery", 8, 2, 2],
        ["Poh Kong","Jewellery", 2, 3, 3],
        ["Brands Outlet" , "Fashion", 2, 7, 3],
        ["Elle" , "Fashion", 8, 7, 3],
        ["Uniqlo-3" , "Fashion", 5, 7, 3],
        ["MR. DIY" , "Lifestyle & Home Living", 5, 1, 3],
        ["E1-1","Entrance", 0, 5, 1],
        ["E2-1","Entrance", 10, 5, 1],
        ["E1-2","Entrance", 0, 5, 2],
        ["E2-2","Entrance", 10, 5, 2],
        ["E1-3","Entrance", 0, 5, 3],
        ["E2-3","Entrance", 10, 5, 3],
        ["L-1","Lift", 5, 9, 1],
        ["L-2","Lift", 5, 9, 2],
        ["L-3","Lift", 5, 9, 3],
        ["S-1","Stair", 5, 5, 1],
        ["S-2","Stair", 5, 5, 2],
        ["S-3","Stair", 5, 5, 3]
        ]
    
    step_cost = [ # node1, node2, distance, time, stamina
        #floor 1
        ["E1-1","Optical Arts", 110, 110, 110],
        ["E1-1","Lavender Bakery", 132, 132, 132],
        ["E1-1","MyNews", 105, 105, 105],
        ["Optical Arts","MyNews", 65, 65, 65],
        ["Optical Arts","S-1", 90, 90, 90],
        ["Optical Arts","Harvey Norman", 96, 96, 96],
        ["Harvey Norman","S-1", 100, 100, 100],
        ["Harvey Norman","KFC", 158, 158, 158],
        ["KFC","E2-1", 69, 69, 69],
        ["E2-1","S-1", 250, 250, 250],
        ["E2-1","7-Eleven", 75, 75, 75],
        ["7-Eleven","McDonald", 80, 80, 80],
        ["MyNews","S-1", 85, 85, 85],
        ["MyNews","McDonald", 200, 200, 200],
        ["MyNews","Lavender Bakery", 70, 70, 70],
        ["S-1","McDonald", 114, 114, 114],
        ["Lavender Bakery","L-1", 120, 120, 120],
        ["L-1","McDonald", 100, 100, 100],
        #floor 2
        ["Adidas", "L-2", 126, 126, 126],
        ["Komugi", "L-2", 54, 54, 54],
        ["SenQ", "L-2", 126, 126, 126],
        ["Adidas", "Komugi", 79, 79, 79],
        ["Komugi", "SenQ", 98, 98, 98],
        ["Adidas", "E1-2", 67, 67, 67],
        ["Adidas", "S-2", 56, 56, 56],
        ["Komugi", "S-2", 34, 34, 34],
        ["SenQ", "S-2", 97, 97, 97],
        ["SenQ", "E2-2", 67, 67, 67],
        ["E1-2", "S-2", 180, 180, 180],
        ["E2-2", "S-2", 219, 219, 219],
        ["Starbuck", "E1-2", 164, 164, 164],
        ["Starbuck", "S-2", 158, 158, 158],
        ["Popular", "S-2", 116, 116, 116],
        ["Uniqlo-2", "S-2", 149, 149, 149],
        ["Uniqlo-2", "E2-2", 92, 92, 92],
        ["Starbuck", "Popular", 84, 84, 84],
        ["Popular", "Uniqlo-2", 72, 72, 72],
        #floor 3
        ["Poh Kong", "E1-3", 180, 180, 180],
        ["Poh Kong", "S-3", 50, 50, 50],
        ["Poh Kong", "Uniqlo-3", 120, 120, 120],
        ["Uniqlo-3", "S-3", 174, 174, 174],
        ["Uniqlo-3", "E2-3", 200, 200, 200],
        ["S-3", "E2-3", 180, 180, 180],
        ["Elle", "E2-3", 96, 96, 96],
        ["Elle", "S-3", 72, 72, 72],
        ["Elle", "L-3", 150, 150, 150],
        ["MR. DIY", "S-3", 70, 70, 70],
        ["MR. DIY", "L-3", 50, 50, 50],
        ["Brands Outlet", "L-3", 160, 160, 160],
        ["Brands Outlet", "S-3", 90, 90, 90],
        ["Brands Outlet", "E1-3", 30, 30, 30],
        ["S-3", "E1-3", 176, 176, 176],
        #transition between floor
        ["S-1","S-2",50, 100, 100],
        ["S-2","S-3",50, 100, 100],
        ["L-1","L-2",50, 25, 0],
        ["L-2","L-3",50, 25, 0],
        ["L-1","L-3",50, 30, 0],
        ["Uniqlo-2","Uniqlo-3",50, 100, 100]
        ]
    
    nodes = {}
    for name, category, coord1, coord2, floor in location_list:
      nodes[name] = Node(name, category, floor)
      nodes[name].set_coordinates([coord1, coord2])
    roads = []
    for node1, node2, distance, time, stamina in step_cost:
      road = Road([nodes[node1], nodes[node2]], distance, time, stamina)
      nodes[node1].add_road(road)
      nodes[node2].add_road(road)
      roads.append(road)
      
    shop_list = [nodes['E1-1'],
             nodes['Harvey Norman'],
             nodes['Brands Outlet'],
             nodes['Starbuck'],
             nodes['KFC'],
             nodes['Poh Kong'],
             nodes['E1-1']]
    
    n_ant = 20
    alpha = 1
    rho = 0.1
    
    initial_pheromone = 0.01
    
    ants = [Ant() for _ in range(n_ant)]
    
     # termination threshold
    max_iteration = 200
    percentage_of_dominant_path = 0.9
    
    ax = create_graph(nodes)
    lines = draw_pheromone(ax, roads)
    iteration = 0
    
    solutions = []
    final_paths = []
    
    for i in range(len(shop_list)-1):
        for road in roads:
            road.set_pheromone(initial_pheromone)
        aco(iteration, roads, ants, shop_list[i], shop_list[i+1])
        
        [freq, paths, nodes_used] = get_frequency_of_paths(ants)
        final_paths.append(paths)
        solutions.append([n.name for n in nodes_used[freq.index(max(freq))]])
            # after exiting the loop, return the most occurred path as the solution
            # visualise
            
    for i, solution in enumerate(solutions):
        if(i != len(solutions)-1):
            solution.pop(-1)
    solution = [item for sublist in solutions for item in sublist]
    print(solution)
    for l in lines:
      del l
    # lines = draw_pheromone(ax, roads)
    draw_path(ax, final_paths)
    plt.pause(0.05)
