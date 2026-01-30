import sys
from dataclasses import dataclass
from PIL import Image
from heapq import heappush, heappop

# if len(sys.argv) < 4:
#     print("Usage: python3 lab1.py <terrain-image> <elevation-file> <path-file> <output-image-filename>")
#     sys.exit(1)

# terrain_image_name,elevation_file_name,path_file_name,output_file_name = sys.argv[1:]
terrain_image_name,elevation_file_name,path_file_name,output_file_name = "terrain.png","elevation.txt","path.txt","output.png"
terrian_types = {
                (248, 148, 18) : 1, #openLand 
                (255, 192, 0) : 2, #roughMeadow 
                (255, 255, 255) : 3, #easyMovementForest 
                (2, 208, 60) : 2, #slowRunForest 
                (2, 136, 40) : 1, #walkForest 
                (5, 73, 24) : 500, #impassibleVegetation 
                (0, 0, 255) : 1, #lakeSwampMarsh 
                (71, 51, 3) : 3, #pavedRoad 
                (0, 0, 0) : 1, #footpath 
                (205, 0, 101) : 500 #outOfBounds 
                }

px_lat = 7.55
px_lon = 10.29
max_x = 394
max_y = 499

with Image.open(terrain_image_name) as terrain_image:
    terrain_px_access = terrain_image.load()

with open(elevation_file_name) as elevation_file:
    elevation_list = [[float(_) for _ in line.split()] for line in elevation_file.readlines()]

with open(path_file_name) as path_file:
    path_lines = path_file.readlines()
    path_lines.reverse()
    path_list = [tuple(int(_) for _ in line.split()) for line in path_lines]

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
    d = (((x1-x2)*px_lon)**2 + ((y1-y2)*px_lat)**2 + (get_z(point1)-get_z(point2))**2)**0.5
    return d

def cost_and_est(point1,point2):
    cost = get_distance(point1,point2)*get_terrain_speed(point2)
    est = get_distance(point2,next_goal)
    return cost+est

def get_neighbors(point):
    x = point[0]
    y = point[1]
    neighbors = []
    if x < max_x: neighbors.append((x+1,y))
    if x > 0: neighbors.append((x-1,y))
    if y < max_y: neighbors.append((x,y+1))
    if y > 0: neighbors.append((x,y-1))
    return neighbors

start = path_list.pop()
print(start)
next_goal = path_list.pop()
print(next_goal)
target = path_list[0]
point_parent = {start: ""}
point_dist_start = {start: 0}
point_cost = {start: 0}

def update_parent(point, parent):
    point_parent[point] = parent
    point_dist_start[point] = get_distance(point,parent)
    point_cost[point] = cost_and_est(parent, point)

def is_next_goal(point):
    return (point == next_goal)

def path_to_top(point):
    current = point
    path = [current]
    total_distance = 0
    terrain_px_access[current[0],current[1]] = (177,86,237) #path
    while current != start:
        total_distance += point_dist_start[current]
        current = point_parent[current]
        terrain_px_access[current[0],current[1]] = (177,86,237) #path
        path.append(current)
    return path, total_distance

visited = set()
frontier_set = {start}
frontier = []
heappush(frontier,start)

while len(frontier):
    current = heappop(frontier)
    frontier_set.remove(current)
    visited.add(current)
    neighbors = get_neighbors(current)
    best_cost = cost_and_est(current,neighbors[0])
    for neighbor in neighbors:
        if is_next_goal(neighbor):
            print(next_goal)
            if len(path_list):
                next_goal = path_list.pop()
            else:
                path, total_distance, cost = path_to_top(neighbor)
                while path:
                    print(path.pop())
                print(total_distance)
                sys.exit(1)
        if neighbor not in visited and neighbor not in frontier_set:
            visited.add(neighbor)
            temp_cost = cost_and_est(current, neighbor)
            if temp_cost <= best_cost:
                best_cost = temp_cost
                heappush(frontier, neighbor)
                frontier_set.add(neighbor)
                update_parent(neighbor,current)     
print("No solution")
sys.exit(1)