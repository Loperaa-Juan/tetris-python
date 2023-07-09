import pygame
import random

# Dimensiones de la ventana
WIDTH = 800
HEIGHT = 600

# Tamaño de una sola celda del Tetris
CELL_SIZE = 30

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Matriz para representar el tablero del juego
grid = [[BLACK] * (WIDTH // CELL_SIZE) for _ in range(HEIGHT // CELL_SIZE)]

# Lista de formas de Tetris
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [0, 0, 1]],  # L
    [[1, 1, 1], [1, 0, 0]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]  # Z
]

# Clase para representar una pieza
class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice([RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE])
        self.x = (WIDTH // CELL_SIZE) // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def rotate(self):
        self.shape = list(zip(*reversed(self.shape)))

    def draw(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    pygame.draw.rect(screen, self.color, (self.x * CELL_SIZE + j * CELL_SIZE,
                                                          self.y * CELL_SIZE + i * CELL_SIZE,
                                                          CELL_SIZE, CELL_SIZE))

    def collides_with_wall(self):
        return self.x < 0 or self.x + len(self.shape[0]) > WIDTH // CELL_SIZE

    def collides_with_floor(self):
        return self.y + len(self.shape) >= HEIGHT // CELL_SIZE

    def collides_with_piece(self, pieces):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] and (self.y + i + 1 >= HEIGHT // CELL_SIZE or
                                        pieces[self.y + i + 1][self.x + j] != BLACK):
                    return True
        return False

    def merge_with_grid(self, grid):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    grid[self.y + i][self.x + j] = self.color

# Inicializar Pygame
pygame.init()

# Configurar la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

fall_time = 0
fall_speed = 0.5

pieces = []
current_piece = None

score = 0

def check_rows():
    global score
    for i in range(len(grid)):
        if all(cell != BLACK for cell in grid[i]):
            # Eliminar la fila completa
            del grid[i]
            # Agregar una nueva fila vacía en la parte superior
            grid.insert(0, [BLACK] * (WIDTH // CELL_SIZE))
            # Incrementar la puntuación
            score += 10

def draw_grid():
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(screen, grid[i][j], (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (20, 20))

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_piece and not current_piece.collides_with_wall():
                current_piece.move_left()
            elif event.key == pygame.K_RIGHT and current_piece and not current_piece.collides_with_wall():
                current_piece.move_right()
            elif event.key == pygame.K_DOWN and current_piece:
                fall_speed = 0.05
            elif event.key == pygame.K_UP and current_piece and not current_piece.collides_with_wall():
                current_piece.rotate()

    if not current_piece:
        current_piece = Piece()
        if current_piece.collides_with_piece(grid):
            running = False
        else:
            pieces.append(current_piece)

    time_passed = clock.tick()
    fall_time += time_passed

    if fall_time / 1000 >= fall_speed:
        if current_piece and (current_piece.collides_with_floor() or current_piece.collides_with_piece(grid)):
            current_piece.merge_with_grid(grid)
            check_rows()
            current_piece = None
            fall_speed = 0.5
        elif current_piece:
            current_piece.move_down()

        fall_time = 0

    draw_grid()

    if current_piece:
        current_piece.draw()

    draw_score()

    pygame.display.flip()

pygame.quit()
