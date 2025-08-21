# Implementación de Agentes de Búsqueda - Proyecto de Inteligencia Artificial

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/valtimore/MazeGameIA/blob/main/README.md)
[![es](https://img.shields.io/badge/lang-es-blue.svg)](https://github.com/valtimore/MazeGameIA/blob/main/README-es.md)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)  
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-orange?logo=pygame)  

Este proyecto implementa un juego basado en agentes de búsqueda donde el personaje 1 (Gon) debe encontrar a su enemigo el personaje 2 (Neferpitou) mientras evita a el personaje 3 (Killua), quien intenta interceptarla utilizando diferentes algoritmos de búsqueda.

## 📋 Descripción del Proyecto

El proyecto consiste en un laberinto donde dos agentes interactúan:
  
  - Gon: Utiliza búsqueda limitada por profundidad para encontrar a Neferpitou
  - Killua: Utiliza principalmente búsqueda por amplitud, pero con un 40% de probabilidad cambia a búsqueda A*
  - Power-up: Un ramen que reduce a la mitad el costo de movimientos cuando es recogida

## 🎯Características

  - Implementación de tres algoritmos de búsqueda: limitada por profundidad, por amplitud y A*
  - Interfaz gráfica desarrollada con Pygame
  - Sistema de power-ups que afecta el costo de movimientos
  - Comportamiento probabilístico para el agente Killua
  - Múltiples escenarios de finalización del juego

## 📋 Pre-requisitos 

  - Python 3.8 o superior
  - Pygame 2.0 o superior

## 🔧 Instalación 

Sigue estos pasos para instalar y preparar el proyecto:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/valtimore/MazeGameIA.git
   cd MazeGameIA
   ```
2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate  # Windows
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Ejecución

Para iniciar el juego, ejecuta:

```bash
python main.py
```

El juego se ejecuta automáticamente. Los agentes se mueven según sus algoritmos de búsqueda. Observa cómo interactúan en el laberinto.

## Autores ✒️

* **Juan David Cataño** - [Zers04](https://github.com/Zers04)
* **Valentina Londoño** - [Valtimore](https://github.com/valtimore)

## Licencia 📄

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE.md](LICENSE.md) para más detalles.

