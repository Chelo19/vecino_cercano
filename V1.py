import math
import time

file_name = "6nodes.txt"
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
                    # print(f'Disponible: {current_node} hacia {node_number} = {current_distance}')     # descomentar esto hace que se muestren las distancias
                    if(current_distance < min_distance):
                        min_distance = current_distance
                        min_distance_node = node_number
            total_distance += min_distance
        else:
            current_distance = getDistanceBetween2Points(temp_nodes[current_node], start_node_item)     # esta línea es para regresar al punto inicial
            total_distance += current_distance
        # print(f'Se selecciona: {min_distance_node}')      # descomentar esto hace que se muestre la selección
        route.append(current_node)
        temp_nodes.pop(current_node)
        current_node = min_distance_node
    # print(total_distance)     # descomentar esto hace que se muestre la distancia de la selección
    return total_distance

def showResults(start_points_total_distance, preference):
    # la mejora que considero conveniente ocurre dentro de esta función, la idea de esta función, seguido de la estructura del resto del código
    # es que se pueda saber aparte de la mejor ruta, también las siguientes mejores rutas para así poder encontrar, en caso de tener una preferencia,
    # una ruta que tenga la misma distancia recorrida que la mejor ruta pero que se acerque lo máximo posible a la preferencia del usuario

    sorted_data = dict(sorted(start_points_total_distance.items(), key=lambda item: item[1]['result']))

    sorted_list = [(key, value) for key, value in sorted_data.items()]
    # for key, value in sorted_list:        # descomentar esto hace que se muestren los resultados en orden de menor a mayor distancia total recorrida
    #     print(f'Key: {key}, Result: {value["result"]}')

    first_result = sorted_list[0][1]["result"]
    equal_results = [(key, value) for key, value in sorted_list if value["result"] == first_result]

    getNodes()
    min_distance_index = 0
    min_distance = 999999999
    for i in range(len(equal_results)):
        current_distance = getDistanceBetween2Points(nodes[preference], nodes[equal_results[i][0]])
        if(current_distance < min_distance):
            min_distance_index = i
            min_distance = current_distance
    print('**********************************************')
    print(f'Mejor resultado a partir de preferencia: {equal_results[min_distance_index]}')
    print('**********************************************')

def mainProcess():
    getNodes()
    start_points_total_distance = {}
    for i in range(1, len(nodes) + 1):
        # print(f'*** SE INICIA EL PROCESO EMPEZANDO POR {i} ***')     # descomentar esto hace que se muestre el cambio de nodo de inicio
        start_points_total_distance[i] = {
            "result": individualProcess(i),
            "route": list(route)
        }
        # print(route)  # descomentar esto hace que se muestre la ruta tomada en ese paso
        route.clear()
    preference = 1      # aquí es donde se establece el punto de partida de preferencia del usuario
    showResults(start_points_total_distance, preference)
    
if __name__ == "__main__":
    tic = time.time()
    mainProcess()
    toc = time.time()
    tic_toc = toc - tic
    print(f'Tiempo en encontrar la mejor ruta: {round(tic_toc, 5)}s')
    print('**********************************************')