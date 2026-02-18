import sys
from PIL import Image
from heapq import heappush, heappop

if len(sys.argv) < 4:
    print("Usage: python3 lab1.py <terrain-image> <elevation-file> <path-file> <output-image-filename>")
    sys.exit(1)

terrain_image_name,elevation_file_name,path_file_name,output_file_name = sys.argv[1:]
# terrain_image_name,elevation_file_name,path_file_name,output_file_name = "terrain.png","elevation.txt","path.txt","output.png"
terrain_types = {
                (248, 148, 18) : 1, #openLand 
                (255, 192, 0) : 2, #roughMeadow 
                (255, 255, 255) : 1, #easyMovementForest 
                (2, 208, 60) : 2, #slowRunForest 
                (2, 136, 40) : 3, #walkForest 
                (5, 73, 24) : 500, #impassibleVegetation 
                (0, 0, 255) : 5, #lakeSwampMarsh 
                (71, 51, 3) : 1, #pavedRoad 
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
    path_lines = [tuple(int(_) for _ in line.split()) for line in path_file.readlines()]
path_lines.reverse()
path_list = path_lines

def get_z(point):
    x, y = point
    return elevation_list[y][x]

def get_terrain_speed(point):
    x, y = point
    color = terrain_px_access[x, y][:3]
    if color not in terrain_types:
        return 1
    return terrain_types[color]


def get_distance(a, b):
    x1, y1 = a
    x2, y2 = b
    d = (((x1 - x2) * px_lon) ** 2 + ((y1 - y2) * px_lat) ** 2 + (get_z(a) - get_z(b)) ** 2) ** 0.5
    return d

def get_neighbors(point):
    x, y = point
    neighbors = []
    if x < max_x:
        neighbors.append((x + 1, y))
    if x > 0:
        neighbors.append((x - 1, y))
    if y < max_y:
        neighbors.append((x, y + 1))
    if y > 0:
        neighbors.append((x, y - 1))
    return neighbors

min_multiplier = min(v for v in terrain_types.values() if v < 100)

def heuristic(a, b):
    return get_distance(a, b) * min_multiplier


def path_to_top(parent, end):
    path = []
    current = end
    while current in parent and parent[current] != None:
        path.append(current)
        current = parent[current]
    path.append(current)
    path.reverse()
    return path


def paint_path(path):
    for p in path:
        terrain_px_access[p[0], p[1]] = (177, 86, 237)

def a_star_search(start, goal):
    frontier = []
    point_g = {start: 0.0}
    parent = {start: None}

    heappush(frontier, (heuristic(start, goal), 0.0, start))

    while frontier:
        g_current, current = heappop(frontier)[1:]

        if g_current > point_g.get(current, float("inf")):
            continue

        if current == goal:
            path = path_to_top(parent, current)
            return path, point_g[current]

        for neighbor in get_neighbors(current):
            speed = get_terrain_speed(neighbor)
            if speed >= 500:
                continue
            move_cost = get_distance(current, neighbor) * speed
            tentative_g = g_current + move_cost

            if tentative_g < point_g.get(neighbor, float("inf")):
                point_g[neighbor] = tentative_g
                parent[neighbor] = current
                heappush(frontier, (tentative_g + heuristic(neighbor, goal), tentative_g, neighbor))

start = path_list.pop()

total_cost = 0.0
total_distance = 0.0
step = 0
final_path = []
while path_list:
    next_goal = path_list.pop()
    step += 1

    path, cost = a_star_search(start, next_goal)
    if path is None:
        print("No Solution")
        break

    leg_dist = 0.0
    for a, b in zip(path, path[1:]):
        leg_dist += get_distance(a, b)

    final_path+=path
    total_cost += cost
    total_distance += leg_dist
    start = next_goal

paint_path(final_path)
terrain_image.save(output_file_name)
print(total_distance)
sys.exit(0)