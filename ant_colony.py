class Shop:
    def __init__(self, name, category, floor):
        self.name = name
        self.category = category
        self.floor = floor
        self.paths = []
        self.coordinates = []
    
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    
    def add_path(self, path):
        if path not in self.paths:
          self.paths.append(path)
        
class Stair:
    def __init__(self, name, floor):
        self.name = name
        self.floor = floor
        self.paths = []
        self.coordinates = []
    
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    
    def add_path(self, path):
        if path not in self.paths:
          self.paths.append(path)
        
class Lift:
    def __init__(self, name, floor):
        self.name = name
        self.floor = floor
        self.paths = []
        self.coordinates = []
    
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    
    def add_path(self, path):
        if path not in self.paths:
          self.paths.append(path)
        
        
class AccessWay:
    def __init__(self, name, floor):
        self.name = name
        self.floor = floor
        self.paths = []
        self.coordinates = []
    
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    
    def add_path(self, path):
        if path not in self.paths:
          self.paths.append(path)
        
class Path:
    def __init__(self, connected_nodes, distance, time, stamina, pheromone=0): # or random small number
        self.connected_nodes = connected_nodes
        self.distance = distance
        self.time = time
        self.stamina = stamina
        self.pheromone = pheromone
        
    def set_pheromone(self, pheromone):
        self.pheromone = pheromone
        
    def evaporate_pheromone(self, rho):
    # update the pheromone of the road
        ...
    
    def deposit_pheromone(self, ants):
    # 1. search for ants that uses the raod
    # 2. deposit pheromone using the inversely proportionate relationship between path length and deposited pheromone
        ...
    
    

class Ant:
    def __init__(self):
      self.shops = [] # shops the ant passes through, in sequence
      self.path = [] # paths the ant uses, in sequence
        
    def get_path(self, origin, destination, alpha):
        ...
        
    def get_path_length(self):
        ...
    # calculate path length based on self.path
       # return path_length
       
    def reset(self):
        self.path = []
        self.cities = []
        
def get_percentage_of_dominant_path(ants):
    ...
    #return percentage
        
if __name__ == "__main__":
    
    shop_list = [ # [ name, category, x, y, floor]
        ["Harvey Norman","Digital & Home Appliances", 2, 8, 1],
        ["McDonald" , "Food & Beverages", 7, 7, 1],
        ["KFC" , "Food & Beverages", 3, 4, 1],
        ["MyNews" , "Supermarket", 3, 6, 1],
        ["Optical Arts" , "Optical", 3, 4, 1],
        ["Lavender Bakery" , "Bakery", 2, 8, 1],
        ["7-Eleven" , "Supermarket", 9, 7, 1],
        ["Adidas","Fashion", 2, 7, 2],
        ["Uniqlo" , "Fashion", 5, 7, 2],
        ["Starbuck" , "Food & Beverages", 2, 2, 2],
        ["Popular" , "Leisure & Entertainment", 5, 2, 2],
        ["SenQ" , "Digital & Home Appliances", 8, 7, 2],
        ["Komugi" , "Bakery", 8, 2, 2],
        ["Poh Kong ","Jewellery", 2, 3, 3],
        ["Brands Outlet" , "Fashion", 2, 7, 3],
        ["Elle" , "Fashion", 8, 7, 3],
        ["Uniqlo" , "Fashion", 8, 8, 3],
        ["MR. DIY" , "Lifestyle & Home Living", 5, 1, 3],
        ]
    misc_list = [
        ["E1-1", 0, 5, 1],
        ["E2-1", 10, 5, 1],
        ["S-1", 5, 5, 1],
        ["L-1", 5, 9, 1],
        ["E1-2", 0, 5, 2],
        ["E2-2", 10, 5, 2],
        ["S-2", 5, 5, 2],
        ["L-2", 5, 9, 2],
        ["E1-3", 0, 5, 3],
        ["E2-3", 10, 5, 3],
        ["S-3", 5, 5, 3],
        ["L-3", 5, 9, 3]
    ]
    
    paths = [ # shop1, shop2, distance, time, stamina
        "Harvey Norman", "McDonald", 34, 156, 324
        ],
        ["Poh Kong", "E1-3", 180, 620, 1344],
        ["Poh Kong", "S-3", 50, 210, 429],
        ["Poh Kong", "Uniqlo", 120, 520, 1040],
        ["Uniqlo", "S-3", 174, 612, 1202],
        ["Uniqlo", "E2-3", 200, 900, 1800],
        ["S-3", "E2-3", 180, 620, 1344],
        ["Elle", "E2-3", 96, 378, 780],
        ["Elle", "S-3", 72, 280, 560],
        ["Elle", "L-3", 150, 600, 1200],
        ["MR. DIY", "S-3", 70, 280, 560],
        ["MR. DIY", "L-3", 50, 210, 429],
        ["Brands Outlet", "L-3", 160, 640, 1300],
        ["Brands Outlet", "S-3", 90, 360, 720],
        ["Brands Outlet", "E1-3", 30, 120, 240],
        ["S-3", "E1-3", 176, 616, 1212]

    
    shops = {}
    for coord1, coord2, name, floor in shop_list:
      shops[name] = Shop(name)
      shops[name].set_coordinates([coord1, coord2])
      
    paths = []
    for shop1, shop2, distance, time, stamina in paths:
      path = Path([shops[shop1], shops[shop2]], distance, time, stamina)
      shops[shop1].add_path(path)
      shops[shop2].add_path(path)
      paths.append(path)
      
    origin = shops['Harvey Norman']
    destination = shops['Family Mart']
    
    n_ant = 10
    alpha = 1
    rho = 0.1
    
    initial_pheromone = 0.01
    
    for path in paths:
      path.set_pheromone(initial_pheromone)
      
    ants = [Ant() for _ in range(n_ant)]
    
    
        
    # state_space = [
    #     Path(Node('a', 't', 1), Node('b', 't', 1), 1, 1, 1), 
    #     Path(Node('a', 't', 1), Node('c', 't', 1), 2, 2, 3), 
    #     Path(Node('a', 't', 1), Node('d', 't', 1), 3, 3, 3)
    #     ]
