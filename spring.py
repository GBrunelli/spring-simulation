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
pixels_per_meter = 500  # 100 pixels representam 1 metro

# Posição inicial e velocidade em metros
x = x0 / pixels_per_meter
v = v0 / pixels_per_meter

# Posição de equilíbrio (lado esquerdo da tela)
equilibrium_x = 50  # Posição fixa do início da mola

# Propriedades da massa
mass_radius = 20  # Raio da massa (em pixels)

# Variável para arrastar a massa
dragging = False

# Classe para criar caixas de entrada
class InputBox:
    def __init__(self, x, y, w, h, text='', label=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = font.render(text, True, BLACK)
        self.active = False
        self.label = label
        self.label_surface = font.render(label, True, BLACK)

    def handle_event(self, event):
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
        screen.blit(self.label_surface, (self.rect.x - self.label_surface.get_width() - 10, self.rect.y + 5))
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Criar caixas de entrada no lado direito da tela
input_box_m = InputBox(WIDTH - 180, 100, 140, 32, text=str(m), label='Massa (kg):')
input_box_k = InputBox(WIDTH - 180, 150, 140, 32, text=str(k), label='Constante k (N/m):')
input_box_b = InputBox(WIDTH - 180, 200, 140, 32, text=str(b), label='Amortecimento b (kg/s):')
input_boxes = [input_box_m, input_box_k, input_box_b]

# Função para desenhar a mola
def draw_spring(screen, start_pos, end_pos, color, num_coils=20, coil_radius=10, width=2):
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
            mass_x = equilibrium_x + x * pixels_per_meter
            mass_y = HEIGHT // 2
            distance = math.hypot(mouse_x - mass_x, mouse_y - mass_y)
            if distance <= mass_radius:
                dragging = True
                v = 0.0
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            v = 0.0
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            x = max(0, (mouse_x - equilibrium_x) / pixels_per_meter)

    if not dragging:
        spring_force = -k * x
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
    mass_x = equilibrium_x + x * pixels_per_meter
    draw_spring(screen, (equilibrium_x, HEIGHT // 2), (mass_x, HEIGHT // 2), BLACK, num_coils=15, coil_radius=10, width=2)
    mass_color = RED if dragging else BLACK
    pygame.draw.circle(screen, mass_color, (int(mass_x), HEIGHT // 2), mass_radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
