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
    
    def deposit_pheromone_distance(self, ants):
    # 1. search for ants that uses the raod
    # 2. deposit pheromone using the inversely proportionate relationship between path length and deposited pheromone
        for ant in ants:
            for path in ant.path:
                if self == path:
                    self.pheromone += 5/(ant.get_path_distance())**1
                    break
                
    def deposit_pheromone_all_cost(self, ants):
        for ant in ants:
            for path in ant.path:
                if self == path:
                    self.pheromone += 5/(ant.get_path_all_cost())**1

class Ant:
    def __init__(self):
      self.nodes = [] # nodes the ant passes through, in sequence
      self.path = [] # roads the ant uses, in sequence
    
    def get_path(self, origin, destination, alpha, previous_nodes):
    # 1. append origin to the self.nodes
    # 2. if the last node is not destination, search for the next node to go
    # 3. after getting to the destination, remove the loop within the path, i.e. if there are repeated nodes in self.nodes, remove the nodes and the roads in between the repetition
        self.nodes.append(origin)
        while(not((self.nodes[-1] == destination) ^ (self.nodes[-1].category == destination)) or self.nodes[-1] in previous_nodes): 
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
        return self.nodes[-1]
    
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

def create_graph(nodes, fitness_all_cost):
    plt.figure()
    if fitness_all_cost:
        plt.suptitle("Optimal Path based on distance, time and stamina")
    else:  
        plt.suptitle("Optimal Path based on distance only")
    ax = plt.axes(projection='3d')
    nodes_x = [node.coordinates[0] for key, node in nodes.items()]
    nodes_y = [node.coordinates[1] for key, node in nodes.items()]
    nodes_z = [node.floor for key, node in nodes.items()]
    ax.scatter(nodes_x, nodes_y, nodes_z)
    for i, node in enumerate(nodes):
        ax.text(nodes_x[i], nodes_y[i], nodes_z[i], node, size=7, color="k")
    return ax

def draw_path(ax, solution):
    lines = []
    colors = []
    count = 0
    for i in range(len(solution)):
        colors.append('#%06X' % random.randint(0, 0xFFFFFF))
    for path in solution:
        for road in path:
            from_coord = road.connected_nodes[0].coordinates
            to_coord = road.connected_nodes[1].coordinates
            coord_x = [from_coord[0], to_coord[0]]
            coord_y = [from_coord[1], to_coord[1]]
            coord_z = [road.connected_nodes[0].floor, road.connected_nodes[1].floor]
            lines.append(ax.plot(coord_x, coord_y, coord_z, c=colors[count], linewidth=1))
        count += 1
    return lines

def aco(iteration, 
        roads,
        ants,
        origin,
        destination,
        fitness_all_cost,
        previous_nodes,
        max_iteration=200,
        percentage_of_dominant_path=0.9,
        alpha=1,
        rho=0.1):
    while iteration < max_iteration and get_percentage_of_dominant_path(ants) < percentage_of_dominant_path: # termination conditions
        # loop through all the ants to identify the path of each ant
        for ant in ants:
            ant.reset()
            # identify the path of the ant
            destination = ant.get_path(origin, destination, alpha, previous_nodes)

        # loop through all roads
        for road in roads:
            # evaporate the pheromone on the path
            road.evaporate_pheromone(rho)
            # deposit the pheromone
            if fitness_all_cost:
                road.deposit_pheromone_all_cost(ants)
            else:
                road.deposit_pheromone_distance(ants)
          
        # increase iteration count
        iteration += 1
    
    return destination

def get_user_input(location_list, nodes):
    categories = [node[1] for node in location_list]
    category_list = []
    [category_list.append(item) for item in categories if item not in category_list]
    category_list = category_list[:-3]
    
    category_count = {"Digital & Home Appliances": 2,
                  "Food & Beverages": 3,
                  "Supermarket": 2,
                  "Optical": 1,
                  "Bakery": 2,
                  "Fashion": 5,
                  "Leisure & Entertainment": 1,
                  "Jewellery": 1,
                  "Lifestyle & Home Living": 1
                  }
    
    current_category_count = {"Digital & Home Appliances": 0,
                  "Food & Beverages": 0,
                  "Supermarket": 0,
                  "Optical": 0,
                  "Bakery": 0,
                  "Fashion": 0,
                  "Leisure & Entertainment": 0,
                  "Jewellery": 0,
                  "Lifestyle & Home Living": 0
                  }
    
    shop_list = [node[0] for node in location_list]
    entrance_list = shop_list[-12:-6]
    shop_list = shop_list[:-12]
    
    print("---------- Entrances --------")
    [print(entrance) for entrance in entrance_list]
    
    print("------------ Shops -----------")
    [print(shop) for shop in shop_list]
    
    print("---------- Categories ----------")
    [print(category) for category in category_list]
      
    origin = input("Current location: ")
    
    while origin not in shop_list and origin not in entrance_list:
        print("Please enter a valid entrance or shop on your current location")
        origin = input("Current location: ")
    
    destination_list = [] 
    current_input = []
    
    destination_list.append(nodes[origin])
    current_input.append(origin)
    
    in_process = True
    
    while in_process:
        destination = input("Please enter your shop or category to visit or an exit: ")
        print()
        if destination not in shop_list and destination not in category_list and destination not in entrance_list:
            print("Please enter a valid input")
            
        if destination in shop_list:
            if destination not in current_input and current_category_count[nodes[destination].category] != category_count[nodes[destination].category]:
                destination_list.append(nodes[destination])
                current_input.append(destination)
                current_category_count[nodes[destination].category] += 1
            else:
                print("The destination has been selected before.")
        if destination in category_list:
            if current_category_count[destination] != category_count[destination]:
                destination_list.append(destination)
                current_input.append(destination)
                current_category_count[destination] += 1
            else:
                print("There is no remaining shop in this category.")
        if destination in entrance_list:
            destination_list.append(nodes[destination])
            current_input.append(destination)
            print("Current input:", current_input)
            break
        
        print("Current input:", current_input)
        
        if input("Do you wish do exit? (Y/N) ") == "Y":
            in_process = False
    
            
    if current_input[-1][0] != 'E' or current_input[-1][2] != '-':
        destination_list.append("Entrance")
        
    return destination_list

def final_aco(shop_list, fitness_all_cost):
    n_ant = 20
    
    initial_pheromone = 0.01
    
    ants = [Ant() for _ in range(n_ant)]
    
    iteration = 0
    
    solutions = []
    final_paths = []
    previous_nodes = []
    
    for i in range(len(shop_list)-1):
        for road in roads:
            road.set_pheromone(initial_pheromone)
        destination = aco(iteration, roads, ants, shop_list[i], shop_list[i+1], fitness_all_cost, previous_nodes)
        shop_list[i+1] = destination
        
        [freq, paths, nodes_used] = get_frequency_of_paths(ants)
        final_paths.append(paths[freq.index(max(freq))])
        solutions.append([n.name for n in nodes_used[freq.index(max(freq))]])
        previous_nodes.append(nodes[solutions[-1][-1]])
        for ant in ants:
            ant.reset()
        
    return shop_list, solutions, final_paths

def print_solution(solutions):        
    for i, solution in enumerate(solutions):
        if(i != len(solutions)-1):
            solution.pop(-1)
    solution = [item for sublist in solutions for item in sublist]
    print(solution)

if __name__ == "__main__":
    plt.close('all')
    location_list = [ # [ name, category, x, y, floor]
        # first floor
        ["Harvey Norman","Digital & Home Appliances", 5, 3, 1],
        ["McDonald" , "Food & Beverages", 7, 7, 1],
        ["KFC" , "Food & Beverages", 8, 4, 1],
        ["MyNews" , "Supermarket", 3, 6, 1],
        ["Optical Arts" , "Optical", 3, 4, 1],
        ["Lavender Bakery" , "Bakery", 2, 8, 1],
        ["7-Eleven" , "Supermarket", 9, 7, 1],
        # second floor
        ["Adidas","Fashion", 2, 7, 2],
        ["Uniqlo-2" , "Fashion", 8, 2, 2],
        ["Starbuck" , "Food & Beverages", 2, 2, 2],
        ["Popular" , "Leisure & Entertainment", 5, 2, 2],
        ["SenQ" , "Digital & Home Appliances", 8, 7, 2],
        ["Komugi" , "Bakery", 5, 7, 2],
        # floor 3
        ["Poh Kong","Jewellery", 4, 3, 3],
        ["Brands Outlet" , "Fashion", 2, 6, 3],
        ["Elle" , "Fashion", 7, 6, 3],
        ["Uniqlo-3" , "Fashion", 8, 2, 3],
        ["MR. DIY" , "Lifestyle & Home Living", 5, 7, 3],
        # transition
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
        # floor 1
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
        # floor 2
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
        # floor 3
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
        # transition between floor
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
      
    nodes_list = get_user_input(location_list, nodes) 
    
    ax = create_graph(nodes, False)
    ax2 = create_graph(nodes, True)
    
    shop_list_distance_only, solution_distance_only, path_distance_only = final_aco(nodes_list.copy(), False)
    shop_list_all_cost, solution_all_cost, path_all_cost = final_aco(nodes_list.copy(), True)
    
    print()
    print("Places to go considering only distance:")
    print([node.name for node in shop_list_distance_only])
    print()
    print("Path to go considering only distance:")
    print_solution(solution_distance_only)
    print()
    print("Places to go considering distance, time, stamina:")
    print([node.name for node in shop_list_all_cost])
    print()
    print("Path to go considering distance, time, stamina:")   
    print_solution(solution_all_cost)
    
    draw_path(ax, path_distance_only)
    draw_path(ax2, path_all_cost)
