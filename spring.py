"""
Nome do Projeto: Simulação de Sistema Massa-Mola

Descrição: Este programa simula o movimento de uma massa presa a uma mola com amortecimento. A massa pode ser arrastada para a esquerda, e a mola a retornará ao ponto de equilíbrio, que está fixado no lado esquerdo da tela. O usuário pode ajustar parâmetros como a massa, a constante da mola e o coeficiente de amortecimento.

Autores: 
  [Seu Nome] ([Número USP])

Este projeto faz parte do processo avaliativo da disciplina 7600105 - Física Básica I (2024) da USP-São Carlos ministrada pela(o) [Prof. Krissia de Zawadzki/Esmerindo de Sousa Bernardes]
"""

import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de Sistema Massa-Mola")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Fonte
font = pygame.font.SysFont(None, 24)

# Parâmetros da simulação (valores iniciais)
m = 1.0       # Massa (kg)
k = 10.0      # Constante da mola (N/m)
b = 0.5       # Coeficiente de amortecimento (kg/s)
x0 = 100.0    # Deslocamento inicial (em pixels)
v0 = 0.0      # Velocidade inicial (em pixels/s)

# Parâmetros de tempo
clock = pygame.time.Clock()
dt = 0.01     # Intervalo de tempo (s)

# Conversão de escala (pixels para metros)
PIXELS_PER_METER = 500  # 100 pixels representam 1 metro

# Posição inicial e velocidade em metros
x = x0 / PIXELS_PER_METER
v = v0 / PIXELS_PER_METER

# Posição de equilíbrio (lado esquerdo da tela)
EQUILIBRIUM_X = 50  # Posição fixa do início da mola

EQUILIBRIUM_OFFSET = 1

# Propriedades da massa
MASS_RADIUS = 20  # Raio da massa (em pixels)

# Variável para arrastar a massa
dragging = False

# Classe para criar caixas de entrada
class InputBox:
    def __init__(self, x, y, w, h, text='', label=''):
        """
        Inicializa a caixa de entrada para modificar parâmetros de simulação.

        Parâmetros:
        - x (int): Posição horizontal da caixa de entrada.
        - y (int): Posição vertical da caixa de entrada.
        - w (int): Largura da caixa de entrada.
        - h (int): Altura da caixa de entrada.
        - text (str): Texto inicial na caixa de entrada.
        - label (str): Rótulo associado à caixa de entrada.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = font.render(text, True, BLACK)
        self.active = False
        self.label = label
        self.label_surface = font.render(label, True, BLACK)

    def handle_event(self, event):
        """
        Trata os eventos de interação com a caixa de entrada.

        Parâmetros:
        - event (pygame.event.Event): Evento gerado pela interação do usuário.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = RED if self.active else GRAY
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.update_parameter()
                self.active = False
                self.color = GRAY
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 10 and (event.unicode.isdigit() or event.unicode in '.-'):
                self.text += event.unicode
            self.txt_surface = font.render(self.text, True, BLACK)

    def update_parameter(self):
        """
        Atualiza o valor do parâmetro com base no texto da caixa de entrada.

        A atualização considera os parâmetros de massa, constante da mola e amortecimento.
        """
        global m, k, b
        try:
            value = float(self.text)
            if self.label == 'Massa (kg):':
                m = max(value, 0.1)
            elif self.label == 'Constante k (N/m):':
                k = max(value, 0.1)
            elif self.label == 'Amortecimento b (kg/s):':
                b = value
        except ValueError:
            pass

    def draw(self, screen):
        """
        Desenha a caixa de entrada na tela.

        Parâmetros:
        - screen (pygame.Surface): Superfície onde a caixa de entrada será desenhada.
        """
        screen.blit(self.label_surface, (self.rect.x - self.label_surface.get_width() - 10, self.rect.y + 5))
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Criar caixas de entrada no lado direito da tela
input_box_m = InputBox(WIDTH - 180, 100, 140, 32, text=str(m), label='Massa (kg):')
input_box_k = InputBox(WIDTH - 180, 150, 140, 32, text=str(k), label='Constante k (N/m):')
input_box_b = InputBox(WIDTH - 180, 200, 140, 32, text=str(b), label='Amortecimento b (kg/s):')
input_boxes = [input_box_m, input_box_k, input_box_b]

def draw_spring(screen, start_pos, end_pos, color, num_coils=20, coil_radius=10, width=2):
    """
    Desenha uma mola entre dois pontos dados.

    Parâmetros:
    - screen (pygame.Surface): Superfície onde a mola será desenhada.
    - start_pos (tuple): Posição de início da mola (x, y).
    - end_pos (tuple): Posição de fim da mola (x, y).
    - color (tuple): Cor da mola.
    - num_coils (int): Número de espirais da mola.
    - coil_radius (int): Raio das espirais da mola.
    - width (int): Largura da linha da mola.
    """
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    num_points = max(int(length / 2), 2)
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        x = x1 + t * dx
        y = y1 + t * dy
        offset = coil_radius * math.sin(t * num_coils * 2 * math.pi)
        offset_x = offset * math.cos(angle + math.pi / 2)
        offset_y = offset * math.sin(angle + math.pi / 2)
        points.append((x + offset_x, y + offset_y))
    if len(points) >= 2:
        pygame.draw.lines(screen, color, False, points, width)

# Loop principal da simulação
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in input_boxes:
            box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            mass_x = EQUILIBRIUM_X + x * PIXELS_PER_METER
            mass_y = HEIGHT // 2
            distance = math.hypot(mouse_x - mass_x, mouse_y - mass_y)
            if distance <= MASS_RADIUS:
                dragging = True
                v = 0.0
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            v = 0.0
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            x = max(0, (mouse_x - EQUILIBRIUM_X) / PIXELS_PER_METER)

    if not dragging:
        spring_force = -k * (x - EQUILIBRIUM_OFFSET)
        damping_force = -b * v
        net_force = spring_force + damping_force
        a = net_force / m
        v += a * dt
        x += v * dt
        x = max(0, x)

    screen.fill(WHITE)
    for box in input_boxes:
        box.draw(screen)
    param_text = f"Massa (m): {m:.2f} kg   Constante (k): {k:.2f} N/m   Amortecimento (b): {b:.2f} kg/s"
    param_surface = font.render(param_text, True, BLACK)
    screen.blit(param_surface, (20, 20))
    mass_x = EQUILIBRIUM_X + x * PIXELS_PER_METER + EQUILIBRIUM_OFFSET
    draw_spring(screen, (EQUILIBRIUM_X + EQUILIBRIUM_OFFSET, HEIGHT // 2), (mass_x, HEIGHT // 2), BLACK, num_coils=15, coil_radius=10, width=2)
    mass_color = RED if dragging else BLACK
    pygame.draw.circle(screen, mass_color, (int(mass_x), HEIGHT // 2), MASS_RADIUS)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
