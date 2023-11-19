import pandas as pd
import numpy as np

# Se cargan los datos
nodes_df = pd.read_excel('files/E_n13_k4_coords.xlsx', index_col=0)
demanda_df = pd.read_excel('files/E_n13_k4_demanda.xlsx', index_col=0)
with open('files/E_n13_k4_cap.txt', 'r') as file:
    capacity = int(file.read())

# Matriz de distancias entre nodos
matrix = nodes_df.values

def nearest_neighbor(matrix, start_node, capacity):
    n = len(matrix)
    visited = [False] * n
    routes = []
    total_distance = 0

    while np.sum(visited) < n:  # Mientras no se hayan visitado todos los nodos
        path = []
        current_node = start_node
        current_capacity = demanda_df.iloc[start_node]['Demanda']  # Capacidad del nodo de inicio

        while True:
            visited[current_node] = True
            path.append(current_node)
            nearest_node = None
            min_distance = np.inf

            for i in range(n):
                if i != current_node and not visited[i] and matrix[current_node][i] < min_distance \
                        and current_capacity + demanda_df.iloc[i]['Demanda'] <= capacity:
                    min_distance = matrix[current_node][i]
                    nearest_node = i

            if nearest_node is not None:
                total_distance += matrix[current_node][nearest_node]
                current_node = nearest_node
                current_capacity += demanda_df.iloc[nearest_node]['Demanda']
            else:
                path.append(start_node)  # Regresar al nodo inicial para completar la ruta
                total_distance += matrix[current_node][start_node]
                break

        routes.append((path, current_capacity))

        for i, visited_node in enumerate(visited):
            if not visited_node:
                start_node = i
                break

    return routes, total_distance

start_node = 0

routes, total_distance = nearest_neighbor(matrix, start_node, capacity)

print("Rutas:")
for i, (route, capacity) in enumerate(routes):
    print(f"Ruta {i+1}: {route}, Capacidad acumulada: {capacity}")
print("Distancia total:", total_distance)
