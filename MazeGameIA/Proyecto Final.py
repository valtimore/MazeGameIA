import pygame
from collections import deque
import random

pygame.init()

# ****************** Ajustes de la ventana y definición de los colores a usar 
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Búsqueda en Laberinto - Proyecto de IA")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (190, 212, 191)

# ****************** Tamaño de cada celda del laberinto
cell_size = 160  

# ****************** Laberinto del enunciado
maze = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
]

# ****************** Donde va a estar nuestro agente y la meta
agent_pos = (0, 4)
cookie_pos = (1, 1)
goal_pos = (2, 0)
pucca_pos = (3,3)

# ****************** Aquí se cargan las fotos 
try:
    agent_icon = pygame.image.load('agent_icon.png')
    print("Imagen del agente cargada correctamente.")
    
    cookie_icon = pygame.image.load('cookie_icon.png')
    print("Imagen de la galleta cargada correctamente.")
    
    goal_icon = pygame.image.load('goal_icon.png')
    print("Imagen del objetivo cargada correctamente.")

    pucca_icon = pygame.image.load('pucca_icon.png')
    print("Imagen del objetivo cargada correctamente.")
    
except pygame.error as e:
    print(f"Error al cargar la imagen del agente: {e}")
    print(f"Error al cargar la imagen de la galleta: {e}")
    print(f"Error al cargar la imagen del objetivo: {e}")
    print(f"Error al cargar la imagen del objetivo: {e}")
    


    

agent_icon = pygame.transform.scale(agent_icon, (cell_size, cell_size))
cookie_icon = pygame.transform.scale(cookie_icon, (cell_size, cell_size))
goal_icon = pygame.transform.scale(goal_icon, (cell_size, cell_size))
pucca_icon = pygame.transform.scale(pucca_icon, (cell_size, cell_size))

# ****************** Dibujar el laberinto
def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            if maze[row][col] == 1:  # ****************** Obstáculos
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)  # ****************** Bordes

# ********************* Búsqueda de Pucca

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def bfs_pucca(maze, start, goal):
    queue = deque([(start, [])])  # La cola almacena tuplas (nodo, camino seguido)
    visited = set([start])  # Conjunto de nodos visitados
    
    while queue:
        current, path = queue.popleft()  # Extraemos el primer elemento de la cola

        # Añadir la posición actual al camino
        path = path + [current]

        # Si llegamos al objetivo, retornar el camino
        if current == goal:
            print(f"Pucca encontró el objetivo: {current}")
            return path
        
        # Explorar las celdas adyacentes
        x, y = current
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and (nx, ny) not in visited:
                if maze[nx][ny] == 0:  # Movimiento solo a celdas libres
                    queue.append(((nx, ny), path))  # Añadir a la cola

                    visited.add((nx, ny))  # Marcar como visitado

    print("Pucca no encontró el objetivo.")
    return path  # Retorna el camino explorado

def move_pucca(pucca_pos, agent_pos, maze):
    # Recalcular el camino cada vez que Pucca se mueva
    path = bfs(maze, pucca_pos, agent_pos)

    if len(path) > 1:
        return path[1]  # Mover a la siguiente posición en el camino
    return pucca_pos  # Si no hay camino, Pucca no se mueve






def a_star(maze, start, goal):
    open_set = [(manhattan_distance(start, goal), start)]
    came_from = {start: None}
    g_score = {start: 0}
    visited = set([start])

    while open_set:
        _, current = open_set.pop(0)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        x, y = current
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]):
                if maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                    tentative_g_score = g_score[current] + 1
                    if neighbor == (1, 1):  # Galleta
                        tentative_g_score *= 0.5
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + manhattan_distance(neighbor, goal)
                        open_set.append((f_score, neighbor))
                        visited.add(neighbor)
                        open_set.sort()  # Ordenar para que el nodo con menor f_score esté al frente

    return []  # Retornar camino vacío si no se encontró










# Actualización del código de búsqueda, manteniendo el camino como lista de tuplas (x, y)
def dfs_limited(maze, start, goal, depth_limit):
    stack = [(start, 0)]  # La pila contiene (nodo, profundidad)
    visited = set([start])
    path = []  # Inicializar el camino
    cost = -1
    reduced_cost = 1  # Costo por defecto para cada movimiento
    cookie_found = False  # Bandera para reducir costo si pasamos por la cookie

    while stack:
        current, depth = stack.pop()
        cost += reduced_cost  # Acumular el costo del movimiento
        print(f"Visitando nodo: {current} con profundidad: {depth}, y costo acumulado: {cost}")

        # Añadir la posición actual al camino
        path.append(current)

        # Comprobación si el nodo actual es el objetivo
        if current == goal:
            print("Objetivo encontrado.")
            return path, cost  # Retorna el camino y el costo acumulado

        # Verificar si estamos en la celda de la cookie
        if current == (1, 1) and not cookie_found:
            reduced_cost /= 2  # Reducir el costo si pasamos por la cookie
            cookie_found = True

        if depth < depth_limit:
            x, y = current
            for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and (nx, ny) not in visited:
                    if maze[nx][ny] == 0:  
                        stack.append(((nx, ny), depth + 1))
                        visited.add((nx, ny))
                        print(f"Añadiendo nodo: {(nx, ny)} con profundidad: {depth + 1}")

    print("Objetivo no encontrado dentro del límite de profundidad.")
    return path, cost  # Retorna el camino explorado y el costo acumulado






# ****************** Loop principal
print("Posición inicial de Pucca:", pucca_pos)
pucca_path = []
running = True
depth_limit = 3  # Límite de profundidad bajo para probar la búsqueda
print("Iniciando búsqueda DFS limitada por profundidad.")
path, _ = dfs_limited(maze, agent_pos, goal_pos, depth_limit)  # La búsqueda
print("Búsqueda completada. Camino encontrado:", path)
pucca_path_idx = 0
agent_path_idx = 0  # Índice para seguir el camino del agente
visited_positions = []  # Lista de posiciones donde el agente ha estado

while running:
    screen.fill(WHITE)

    # Dibujar el laberinto
    draw_maze()

    # Dibujar la meta, cookie y posición inicial de Pucca
    screen.blit(goal_icon, (goal_pos[1] * cell_size, goal_pos[0] * cell_size))
    screen.blit(cookie_icon, (cookie_pos[1] * cell_size, cookie_pos[0] * cell_size))
    
    # ********** Dibujar a Pucca en su posición actual
    screen.blit(pucca_icon, (pucca_pos[1] * cell_size, pucca_pos[0] * cell_size))

    # Movimiento del agente
    if agent_path_idx < len(path):
        agent_pos = path[agent_path_idx]
        visited_positions.append(agent_pos)
        screen.blit(agent_icon, (agent_pos[1] * cell_size, agent_pos[0] * cell_size))
        agent_path_idx += 1
        pygame.time.delay(800)

    # Movimiento de Pucca

    if agent_pos != pucca_pos:
    # Solo recalcular el camino si Pucca no tiene uno (cuando empieza a moverse)
        if not pucca_path:
            # Usamos BFS para encontrar un camino de Pucca hacia el agente
            pucca_path = bfs_pucca(maze, pucca_pos, agent_pos)
            print(f"Camino inicial de Pucca: {pucca_path}")

        # Si Pucca ha recorrido todo su camino, recalcularlo
        if pucca_path_idx >= len(pucca_path):
            print("Recalculando el camino de Pucca...")
            pucca_path = bfs_pucca(maze, pucca_pos, agent_pos)
            pucca_path_idx = 0  # Reiniciar el índice

        # Si aún hay pasos en el camino, mover a la siguiente posición
        if pucca_path_idx < len(pucca_path):
            # Mover Pucca a la siguiente posición en el camino
            pucca_pos = pucca_path[pucca_path_idx]
            print(f"Pucca se mueve a la posición: {pucca_pos}")
            pucca_path_idx += 1  # Incrementar el índice de Pucca para el siguiente paso

            # Verificar si Pucca ha atrapado al agente
            if pucca_pos == agent_pos:
                print(f"Pucca ha atrapado al agente en la posición: {pucca_pos}")
                running = False  # Finalizar el juego si Pucca alcanza al agente
            

    # Actualizar pantalla
    pygame.display.update()

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()







pygame.quit()