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
goal_pos = (2, 0)

# ****************** Aquí se cargan las fotos (CAMBIARLAS LUEGO)
try:
    agent_icon = pygame.image.load('./agent_icon.png')
    print("Imagen del agente cargada correctamente.")
except pygame.error as e:
    print(f"Error al cargar la imagen del agente: {e}")

try:
    goal_icon = pygame.image.load('goal_icon.png')
    print("Imagen del objetivo cargada correctamente.")
except pygame.error as e:
    print(f"Error al cargar la imagen del objetivo: {e}")

agent_icon = pygame.transform.scale(agent_icon, (cell_size, cell_size))
goal_icon = pygame.transform.scale(goal_icon, (cell_size, cell_size))

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
def bfs(maze, start, goal):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        print("nodo", current)
        if current == goal:
            break
        
        x, y = current
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Operadores: derecha, abajo, izquierda, arriba
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and (nx, ny) not in visited:
                if maze[nx][ny] == 0:  
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
    
    # ****************** Dibujar el recorrido que hace René
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path

# ****************** Loop principal
running = True
path = bfs(maze, agent_pos, goal_pos)  # La búsqueda 
agent_path_idx = 0  # Índice para seguir el camino del agente
visited_positions = []  # Lista de posiciones donde ha estado el agente

while running:
    screen.fill(WHITE)

    # ****************** Dibujar el laberinto
    draw_maze()

    # ****************** Dibujar el camino paso a paso, solo las posiciones que ya ha visitado el agente
    for position in visited_positions:
        x, y = position
        rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GREEN, rect)

    # ****************** Dibujar la meta (por ahora es la galleta, pendiente de agregar a elmo)
    screen.blit(goal_icon, (goal_pos[1] * cell_size, goal_pos[0] * cell_size))  

    # ****************** Dibujar al agente y hacer la animación de moverlo
    if agent_path_idx < len(path):
        agent_pos = path[agent_path_idx]
        visited_positions.append(agent_pos)  # Agregar la posición visitada
        screen.blit(agent_icon, (agent_pos[1] * cell_size, agent_pos[0] * cell_size))  # Agente en cada paso
        agent_path_idx += 1  # Avanzar al siguiente paso del camino
        pygame.time.delay(500)  # Pausa para animación (ms)

    pygame.display.update()

    # ****************** Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
