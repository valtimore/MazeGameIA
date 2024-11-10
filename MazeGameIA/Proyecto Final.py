import pygame
from collections import deque

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
pucca_pos = (2,3)

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

# Función preliminar, por ahora es búsqueda por amplitud (de René) :P 

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
running = True
depth_limit = 6  # Límite de profundidad bajo para probar la búsqueda
print("Iniciando búsqueda DFS limitada por profundidad.")
path, _ = dfs_limited(maze, agent_pos, goal_pos, depth_limit)  # La búsqueda
print("Búsqueda completada. Camino encontrado:", path)

agent_path_idx = 0  # Índice para seguir el camino del agente
visited_positions = []  # Lista de posiciones donde el agente ha estado

while running:
    screen.fill(WHITE)

    # ****************** Dibujar el laberinto
    draw_maze()

    # ****************** Dibujar el camino recorrido (todas las posiciones visitadas)
    for position in visited_positions:
        x, y = position
        rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GREEN, rect)

    # ****************** Dibujar la meta 
    screen.blit(goal_icon, (goal_pos[1] * cell_size, goal_pos[0] * cell_size))
    screen.blit(cookie_icon, (cookie_pos[1] * cell_size, cookie_pos[0] * cell_size))
    screen.blit(pucca_icon, (pucca_pos[1] * cell_size, pucca_pos[0] * cell_size))      

    # ****************** Dibujar al agente y hacer la animación de moverlo
    if agent_path_idx < len(path):
        agent_pos = path[agent_path_idx]  # Asegúrate de que agent_pos es una tupla (x, y)
        visited_positions.append(agent_pos)  # Agregar la posición visitada solo cuando el agente llega a ella
        screen.blit(agent_icon, (agent_pos[1] * cell_size, agent_pos[0] * cell_size))  # Dibujar al agente
        agent_path_idx += 1  # Avanzar al siguiente paso del camino
        pygame.time.delay(500)  # Pausa para animación (ms)
        print("Posición del agente:", agent_pos)
    
    pygame.display.update()  # Actualizar la pantalla

    # ****************** Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()







pygame.quit()