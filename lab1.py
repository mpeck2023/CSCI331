import sys
from dataclasses import dataclass
from PIL import Image
from queue import Queue
from heapq import heappush, heappop

if len(sys.argv) < 4:
    print("Usage: python3 lab1.py <terrain-image> <elevation-file> <path-file> <output-image-filename>")
    sys.exit(1)

terrain_image_name,elevation_file_name,path_file_name,output_file_name = sys.argv[1:]

terrian_types = {
                (248, 148, 18) : 0, #openLand 
                (255, 192, 0) : 0, #roughMeadow 
                (255, 255, 255) : 0, #easyMovementForest 
                (2, 208, 60) : 0, #slowRunForest 
                (2, 136, 40) : 0, #walkForest 
                (5, 73, 24) : 0, #impassibleVegetation 
                (0, 0, 255) : 0, #lakeSwampMarsh 
                (71, 51, 3) : 0, #pavedRoad 
                (0, 0, 0) : 0, #footpath 
                (205, 0, 101) : 0 #outOfBounds 
                }

px_lat = 7.55
px_lon = 10.29

with Image.open(terrain_image_name) as terrain_image:
    terrain_px_access = terrain_image.load()

with open(elevation_file_name) as elevation_file:
    elevation_list = [float(line.split()) for line in elevation_file.readlines()]

with open(path_file_name) as path_file:
    path_list = Queue()
    for line in path_file.readlines():
        path_list.put(int(line.split()))

def get_z(point):
    x = point[0]
    y = point[1]
    return elevation_list[y][x]

def get_terrain_speed(point):
    x = point[0]
    y = point[1]
    return terrian_types[terrain_px_access[x,y][:3]]

def get_distance(point1,point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    d = (((x1-x2)*px_lon)**2 + ((y1-y2)*px_lat)**2 + (get_z(x1,y1)-get_z(x2,y2))**2)**0.5

def get_neighbors(point):
    x = point[0]
    y = point[1]
    return [(x,y+1),(x+1,y),(x,y-1),(x-1,y)]

start = path_list.get()
next_goal = path_list.get()
point_parents = {start: ("",0)}

def update_parent(point, parent, distance):
    point_parents[point] = (parent, distance)

def isNextGoal(point):
    return (point == next_goal)

def isTarget(point):
    return path_list.empty()

def path_to_top(point):
    current = point
    path = [current]
    total_distance = 0
    terrain_px_access[current[0],current[1]] = (177,86,237) #path
    while current != start:
        total_distance += point_parents[current][1]
        current = point_parents[current][0]
        terrain_px_access[current[0],current[1]] = (177,86,237) #path
        path.append(current)
    return path, total_distance

visited = set()
frontier_set = {start}
frontier = []
heappush(frontier,start)
while frontier.count:
    current = heappop(frontier)
    visited.add(current)
    neighbors = get_neighbors(current)
    for neighbor in neighbors[current]:
        if neighbor not in visited and neighbor not in frontier_set:
            heappush(frontier, neighbor)
            frontier_set.add(neighbor)
            update_parent(neighbor,current)
            if isNextGoal(neighbor):
                if isTarget(neighbor):
                    path, total_distance = path_to_top(neighbor)
                    while path:
                        print(path.pop())
                    print(total_distance)
                    sys.exit(1)
                else:
                    next_goal = path_list.get()
print("No solution")
sys.exit(1)