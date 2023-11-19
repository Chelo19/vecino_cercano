import pandas as pd
import numpy as np

data = pd.read_excel('ftv33.xlsx', index_col=0)

matrix = data.values

def nearest_neighbor(matrix, start_node):
    n = len(matrix)
    visited = [False] * n
    path = [start_node]
    current_node = start_node
    total_distance = 0

    while len(path) < n:
        visited[current_node] = True
        nearest_node = None
        min_distance = np.inf

        for i in range(n):
            if i != current_node and not visited[i] and matrix[current_node][i] < min_distance:
                min_distance = matrix[current_node][i]
                nearest_node = i

        if nearest_node is not None:
            total_distance += matrix[current_node][nearest_node]
            path.append(nearest_node)
            current_node = nearest_node
        else:
            break

    total_distance += matrix[current_node][start_node]
    path.append(start_node)

    return path, total_distance


start_node = 12

path, total_distance = nearest_neighbor(matrix, start_node)

print("Ruta:", path)
print("Distancia:", total_distance)
