import pygame
from collections import deque
import random

pygame.init()

# ****************** Ajustes de la ventana y definición de los colores a usar 
width, height = 800, 600 # Tamaño de la ventana
screen = pygame.display.set_mode((width, height)) # Crear la ventana
pygame.display.set_caption("Búsqueda en Laberinto - Proyecto de IA") # Título de la ventana
# Colores
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
powerUp_pos = (0, 1)
goal_pos = (2, 0)
agent2_pos = (2,3)


# ****************** Aquí se cargan las fotos 
try:
    agent_icon = pygame.image.load('gon.png')
    print("Imagen del agente cargada correctamente.")
    
    powerUp_icon = pygame.image.load('ramen.png')
    print("Imagen de la galleta cargada correctamente.")
    
    goal_icon = pygame.image.load('pitou.png')
    print("Imagen del objetivo cargada correctamente.")

    agent2_icon = pygame.image.load('killua.png')
    print("Imagen del objetivo cargada correctamente.")
    
except pygame.error as e:
    print(f"Error al cargar la imagen del agente: {e}")
    print(f"Error al cargar la imagen de la galleta: {e}")
    print(f"Error al cargar la imagen del objetivo: {e}")
    print(f"Error al cargar la imagen del objetivo: {e}")


# ****************** Redimensionar las imágenes
agent_icon = pygame.transform.scale(agent_icon, (cell_size, cell_size))
powerUp_icon = pygame.transform.scale(powerUp_icon, (cell_size, cell_size))
goal_icon = pygame.transform.scale(goal_icon, (cell_size, cell_size))
agent2_icon = pygame.transform.scale(agent2_icon, (cell_size, cell_size))

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

# Metodo de busqueda limitada por profundidad
def Blimitada(maze, start, goal, powerUp_pos, depth_limit, path, cost, powerUp): 
    stack = [(start, 0)]  # La pila contiene (nodo, profundidad)
    visited = set(path)  # Asegurar que no regrese a nodos ya visitados en `path`
    visited.add(start)   # También marcamos el nodo inicial como visitado
    parent = {start: None}  # Para rastrear el camino
    costA = cost-1 # Costo acumulado
    reduced_cost = 1  # Costo por defecto para cada movimiento

    while stack:
        current, depth = stack.pop()
        costA += reduced_cost
        #print(f"* Visitando nodo: {current} con profundidad: {depth}, y costo acumulado: {costA}")
        

        # Comprobación si el nodo actual es el objetivo
        if current == goal:
            cost += reduced_cost
            
            # Reconstruir el camino desde el objetivo hasta el inicio
            complete_path = []
            while current:
                complete_path.append(current)
                current = parent[current]
            complete_path.reverse()  # Invertir para obtener el camino desde el inicio
            
            # Retornar solo el primer movimiento después del inicio
            if len(complete_path) > 1:
                return complete_path[1], cost, powerUp  # Devuelve la primera tupla después del inicio
            else:
                return start, cost, powerUp  # Si ya estamos en el objetivo, no hay siguiente movimiento

        # Verificar si estamos en la celda de el powerUp
        if current == powerUp_pos and not powerUp:
            reduced_cost /= 2  # Reducir el costo si pasamos por la cookie
            powerUp = True

        if depth < depth_limit: # Verificar si hemos alcanzado el límite de profundidad
            x, y = current
            for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:  # izquierda, abajo, derecha, arriba
                nx, ny = x + dx, y + dy
                next_node = (nx, ny) # Siguiente nodo
                
                if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and next_node not in visited: # Verificar si el vecino está dentro de los límites y no es una pared
                    
                    stack.append((next_node, depth + 1)) 
                    visited.add(next_node) 
                    parent[next_node] = current  # Registrar el camino 

    print("Objetivo no encontrado dentro del límite de profundidad. \n") 
    return complete_path[1], cost, powerUp  # Retorna lo maximo alcanzado si no se encuentra el objetivo

# Calcula la distancia de Manhattan entre dos posiciones
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Metodo de busqueda en amplitud
def Bamplitud(maze, start, goal, path ):
    queue = deque([start])  # Cola para gestionar los nodos a visitar
    visited = set(path)  # Asegurar que no regrese a nodos ya visitados en `path`
    visited.add(start)   # También marcamos el nodo inicial como visitado
    parent = {start: None}  # Diccionario para rastrear el camino

    # Movimiento en el orden: izquierda, abajo, derecha, arriba
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    while queue:
        current = queue.popleft() # Extraer el primer elemento de la cola
        
        # Comprobación si el nodo actual es el objetivo
        if current == goal:
            # Reconstruir el camino desde el objetivo hasta el inicio
            print(f"* Visitando nodo: {current}.")
            path_complete = []
            while current:
                path_complete.append(current)
                current = parent[current]
            path_complete = path_complete[::-1]  # Revertir para obtener el camino desde el inicio

            # Retornar solo el primer movimiento después del inicio
            if len(path_complete) > 1:
                return path_complete[1]   # Devuelve el primer movimiento después del inicio
            else:
                return start   # Si ya estamos en el objetivo, no hay siguiente movimiento

        # Expandir nodos vecinos
        x, y = current
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            next_node = (nx, ny)

            # Verificar si el vecino está dentro de los límites y no es una pared ni está visitado
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and next_node not in visited:
                queue.append(next_node)
                visited.add(next_node)
                parent[next_node] = current  # Registrar el camino

    print("Objetivo no encontrado.\n")
    return None   # Retorna None si no se encuentra el objetivo

# Metodo de busqueda A*
def a_star(maze, start, goal, power_up_pos, power_up_collected):
    open_set = [(manhattan_distance(start, goal), start, power_up_collected)] # Lista de nodos abiertos (f_score, nodo, tiene_power_up)
    came_from = {} # Diccionario para rastrear el camino
    g_score = {start: (0, power_up_collected)}  # (costo_g, tiene_power_up)
    visited = set([start]) # Conjunto de nodos visitados

    while open_set:
        # Ordenar la lista para que el nodo con menor f_score esté al frente
        open_set.sort(key=lambda x: x[0]) # Ordenar por f_score
        _, current, has_power_up = open_set.pop(0) # Extraer el nodo con menor f_score

        # Si llegamos al objetivo, reconstruimos el camino
        if current == goal: 
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::-1]  # Devolver el camino completo

            # Retornar solo el primer movimiento después del inicio
            if len(path) > 1:
                return path[1]  # Devuelve el primer paso después de la posición inicial
            else:
                return start  # Si ya estamos en el objetivo, no hay movimiento

        x, y = current
        move_cost = 0.5 if has_power_up else 1  # Determinar costo basado en si se activó el power-up

        # Revisar movimientos posibles en el orden: izquierda, derecha, abajo, arriba
        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            neighbor = (x + dx, y + dy)

            # Verificar que el vecino esté dentro del laberinto y no sea una pared
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]):
                if maze[neighbor[0]][neighbor[1]] == 0:
                    # Determinar si el vecino es la posición exacta del power-up
                    if neighbor == power_up_pos and not has_power_up:
                        new_power_up_status = True
                        new_move_cost = 0.5
                    else:
                        new_power_up_status = has_power_up
                        new_move_cost = move_cost

                    tentative_g_score = g_score[current][0] + new_move_cost

                    # Actualizar g_score solo si es un mejor camino
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor][0]:
                        came_from[neighbor] = current
                        g_score[neighbor] = (tentative_g_score, new_power_up_status)
                        f_score = tentative_g_score + manhattan_distance(neighbor, goal)
                        open_set.append((f_score, neighbor, new_power_up_status))
                        visited.add(neighbor)

    return None  # Retorna None si no se encuentra el objetivo

# ****************** Loop principal
agent2_path = [] # Camino de Agente2
agent2_cost = 0  # Costo total de Agente2

agent_path = [] # Camino de Agente
agent_cost = 0  # Costo total de Agente

powerUp = False  # Indica si el agente ha pasado por el powerUp

running = True
depth_limit = 13  # Límite de profundidad bajo para probar la búsqueda


while running:
    screen.fill(WHITE)

    # Dibujar el laberinto
    draw_maze()

    # Dibujar la meta, powerUp y posición inicial de Agente 1 y 2
    screen.blit(goal_icon, (goal_pos[1] * cell_size, goal_pos[0] * cell_size))
    screen.blit(powerUp_icon, (powerUp_pos[1] * cell_size, powerUp_pos[0] * cell_size))

    if (agent_pos == powerUp_pos) or (agent2_pos == powerUp_pos):
        powerUp_icon = pygame.image.load('ramen-empty.png')
        powerUp_icon = pygame.transform.scale(powerUp_icon, (cell_size, cell_size))
        screen.blit(powerUp_icon, (powerUp_pos[1] * cell_size, powerUp_pos[0] * cell_size)) 
    
    screen.blit(agent_icon, (agent_pos[1] * cell_size, agent_pos[0] * cell_size))
    screen.blit(agent2_icon, (agent2_pos[1] * cell_size, agent2_pos[0] * cell_size))
    
    pygame.time.delay(1000)

    # Verificar si el agente ha llegado a la meta
    if agent_pos == goal_pos:
       
        agent_icon = pygame.image.load('pitou-gon.png')
        agent_icon = pygame.transform.scale(agent_icon, (cell_size, cell_size))
        goal_icon = pygame.image.load('pitou-gon.png')
        goal_icon = pygame.transform.scale(goal_icon, (cell_size, cell_size))
        screen.blit(goal_icon, (goal_pos[1] * cell_size, goal_pos[0] * cell_size))
        screen.blit(agent_icon, (agent_pos[1] * cell_size, agent_pos[0] * cell_size))
        pygame.display.update()
        print("El agente ha llegado a la meta.")
        pygame.time.delay(1000)
        running = False  # Finalizar el juego si el agente llega a la meta
    
    # Verificar si Agente2 ha atrapado al agente
    if agent2_pos == agent_pos:
        agent_icon = pygame.image.load('gon-killua.png')
        agent_icon = pygame.transform.scale(agent_icon, (cell_size, cell_size))
        agent2_icon = pygame.image.load('gon-killua.png')
        agent2_icon = pygame.transform.scale(agent2_icon, (cell_size, cell_size))    
        screen.blit(agent_icon, (agent_pos[1] * cell_size, agent_pos[0] * cell_size))
        screen.blit(agent2_icon, (agent2_pos[1] * cell_size, agent2_pos[0] * cell_size))
        pygame.display.update()
        print(f"agente2 ha atrapado al agente en la posición: {agent2_pos}")
        pygame.time.delay(1000)
        running = False  # Finalizar el juego si Agente2 alcanza al agente

    # Movimiento del agente
    if agent_pos != goal_pos:
        # Usamos DFS limitada para encontrar un camino del agente hacia la meta
        agent_pos, agent_cost, powerUp = Blimitada(maze, agent_pos, goal_pos, powerUp_pos, depth_limit, agent_path, agent_cost, powerUp)
        agent_path.append(agent_pos) #agrergar el camino de Agente
        depth_limit -= 1
        print(f"agente se mueve a la posición: {agent_pos} \n")   
    
    # Movimiento de Agente2
    if agent_pos != agent2_pos:
        #probabilidad de 60% de que Agente2 use amplitud y 40% de que use A*

        if random.random() < 0.6:
            agent2_pos = Bamplitud(maze, agent2_pos, agent_pos, agent2_path )
        else:
            agent2_pos = a_star(maze, agent2_pos, agent_pos, powerUp_pos, powerUp)
        agent2_path.append(agent2_pos)

        print(f"agente2 se mueve a la posición: {agent2_pos}\n")

    # Actualizar pantalla
    pygame.display.update()

pygame.quit()