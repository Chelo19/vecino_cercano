import math

file_name = "48nodes.txt"
nodes = {}
route = []

def getNodes():
    with open(file_name, 'r') as file:
        lines = file.readlines()

        reading_coordinates = False

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.startswith("NODE_COORD"):
                reading_coordinates = True

            if reading_coordinates:
                parts = line.split()

                if len(parts) >= 3:
                    node_number = int(parts[0])
                    coordinates = (float(parts[1]), float(parts[2]))
                    nodes[node_number] = coordinates

def getDistanceBetween2Points(point1, point2):
    distance = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return distance

def individualProcess(start_node):
    getNodes()
    start_node_item = nodes[start_node]
    total_distance = 0
    current_node = start_node
    temp_nodes = nodes
    while len(temp_nodes) > 0:
        if(len(temp_nodes) != 1):
            min_distance_node = 0
            min_distance = 999999999999999
            for node_number, coordinates in temp_nodes.items():
                if(node_number != current_node):
                    current_distance = getDistanceBetween2Points(temp_nodes[current_node], temp_nodes[node_number])
                    print(f'Disponible: {current_node} hacia {node_number} = {current_distance}')
                    if(current_distance < min_distance):
                        min_distance = current_distance
                        min_distance_node = node_number
            total_distance += min_distance
        else:
            current_distance = getDistanceBetween2Points(temp_nodes[current_node], start_node_item)     # esta línea es para regresar al punto inicial
            total_distance += current_distance
        print(f'Se selecciona: {min_distance_node}')
        route.append(current_node)
        temp_nodes.pop(current_node)
        current_node = min_distance_node
    print(total_distance)
    return total_distance

def showResults(start_points_total_distance):
    sorted_data = dict(sorted(start_points_total_distance.items(), key=lambda item: item[1]['result']))

    sorted_list = [(key, value) for key, value in sorted_data.items()]
    for key, value in sorted_list:
        print(f'Key: {key}, Result: {value["result"]}')
    
def mainProcess():
    getNodes()
    start_points_total_distance = {}
    for i in range(1, len(nodes) + 1):
        print(f'*** SE INICIA EL PROCESO EMPEZANDO POR {i} ***')
        start_points_total_distance[i] = {
            "result": individualProcess(i),
            "route": list(route)
        }
        print(route)
        route.clear()
    print(start_points_total_distance)
    showResults(start_points_total_distance)
    


if __name__ == "__main__":
    mainProcess()