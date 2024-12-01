import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 1600, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de Sistema Massa-Mola")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
LIGHT_GREEN = (100, 255, 100)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
BROWN = (165, 42, 42)

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
PIXELS_PER_METER = 250  # 500 pixels representam 1 metro

# Posição inicial e velocidade em metros
x = x0 / PIXELS_PER_METER
v = v0 / PIXELS_PER_METER

# Posição de equilíbrio (lado esquerdo da tela)
EQUILIBRIUM_X = 50  # Posição fixa do início da mola

EQUILIBRIUM_OFFSET = 2

# Propriedades da massa
MASS_RADIUS = 20  # Raio da massa (em pixels)

# Variável para arrastar a massa
dragging = False

# Variáveis para mostrar ou ocultar os vetores
show_displacement_vector = False
show_velocity_vector = False
show_acceleration_vector = False
show_spring_force_vector = False
show_damping_force_vector = False
show_net_force_vector = False

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

# Classe para criar um botão de toggle
class ToggleButton:
    def __init__(self, x, y, w, h, text='', variable_name=''):
        """
        Inicializa o botão de toggle.

        Parâmetros:
        - x (int): Posição horizontal do botão.
        - y (int): Posição vertical do botão.
        - w (int): Largura do botão.
        - h (int): Altura do botão.
        - text (str): Texto do botão.
        - variable_name (str): Nome da variável global a ser alternada.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.variable_name = variable_name
        self.txt_surface = font.render(text, True, BLACK)

    def handle_event(self, event):
        """
        Trata os eventos de interação com o botão.

        Parâmetros:
        - event (pygame.event.Event): Evento gerado pela interação do usuário.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Alternar a variável correspondente
                current_value = globals()[self.variable_name]
                globals()[self.variable_name] = not current_value

    def draw(self, screen):
        """
        Desenha o botão na tela.

        Parâmetros:
        - screen (pygame.Surface): Superfície onde o botão será desenhado.
        """
        # Obter o valor atual da variável
        current_value = globals()[self.variable_name]
        # Mudar a cor do botão com base no estado
        button_color = LIGHT_GREEN if current_value else GRAY
        pygame.draw.rect(screen, button_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        # Centralizar o texto
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

# Criar caixas de entrada no lado direito da tela
input_box_m = InputBox(WIDTH - 180, 100, 140, 32, text=str(m), label='Massa (kg):')
input_box_k = InputBox(WIDTH - 180, 150, 140, 32, text=str(k), label='Constante k (N/m):')
input_box_b = InputBox(WIDTH - 180, 200, 140, 32, text=str(b), label='Amortecimento b (kg/s):')
input_boxes = [input_box_m, input_box_k, input_box_b]

# Criar botões de toggle para cada vetor
toggle_buttons = [
    ToggleButton(WIDTH - 180, 250, 140, 32, text='Deslocamento', variable_name='show_displacement_vector'),
    ToggleButton(WIDTH - 180, 290, 140, 32, text='Velocidade', variable_name='show_velocity_vector'),
    ToggleButton(WIDTH - 180, 330, 140, 32, text='Aceleração', variable_name='show_acceleration_vector'),
    ToggleButton(WIDTH - 180, 370, 140, 32, text='Força da Mola', variable_name='show_spring_force_vector'),
    ToggleButton(WIDTH - 180, 410, 140, 32, text='Força de Amort.', variable_name='show_damping_force_vector'),
    ToggleButton(WIDTH - 180, 450, 140, 32, text='Força Resultante', variable_name='show_net_force_vector'),
]

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

def draw_vector(screen, start_pos, end_pos, color=(0, 0, 255), width=3):
    """
    Desenha um vetor como uma linha com uma ponta de flecha.

    Parâmetros:
    - screen (pygame.Surface): Superfície onde o vetor será desenhado.
    - start_pos (tuple): Posição inicial do vetor.
    - end_pos (tuple): Posição final do vetor.
    - color (tuple): Cor do vetor.
    - width (int): Largura da linha do vetor.
    """
    pygame.draw.line(screen, color, start_pos, end_pos, width)
    # Desenhar a ponta da flecha
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
    arrow_length = 10
    arrow_width = 5
    left = (end_pos[0] - arrow_length * math.cos(angle - math.pi / 6),
            end_pos[1] - arrow_length * math.sin(angle - math.pi / 6))
    right = (end_pos[0] - arrow_length * math.cos(angle + math.pi / 6),
             end_pos[1] - arrow_length * math.sin(angle + math.pi / 6))
    pygame.draw.polygon(screen, color, [end_pos, left, right])

# Loop principal da simulação
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in input_boxes:
            box.handle_event(event)
        for button in toggle_buttons:
            button.handle_event(event)
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
    for button in toggle_buttons:
        button.draw(screen)
    param_text = f"Massa (m): {m:.2f} kg   Constante (k): {k:.2f} N/m   Amortecimento (b): {b:.2f} kg/s"
    param_surface = font.render(param_text, True, BLACK)
    screen.blit(param_surface, (20, 20))
    mass_x = EQUILIBRIUM_X + x * PIXELS_PER_METER + EQUILIBRIUM_OFFSET
    draw_spring(screen, (EQUILIBRIUM_X + EQUILIBRIUM_OFFSET, HEIGHT // 2), (mass_x, HEIGHT // 2), BLACK, num_coils=15, coil_radius=10, width=2)
    mass_color = RED if dragging else BLACK
    pygame.draw.circle(screen, mass_color, (int(mass_x), HEIGHT // 2), MASS_RADIUS)

    # Ponto de referência para vetores
    reference_y = HEIGHT // 2

    # Desenhar o vetor deslocamento se habilitado
    if show_displacement_vector:
        start_pos = (EQUILIBRIUM_X + EQUILIBRIUM_OFFSET, reference_y - 30)
        end_pos = (mass_x, reference_y - 30)
        draw_vector(screen, start_pos, end_pos, color=BLUE, width=3)
        displacement = x - EQUILIBRIUM_OFFSET
        displacement_text = f"Deslocamento: {displacement:.2f} m"
        displacement_surface = font.render(displacement_text, True, BLUE)
        screen.blit(displacement_surface, (20, 50))

    # Desenhar o vetor velocidade se habilitado
    if show_velocity_vector:
        velocity_scale = 0.1  # Fator de escala para visualização
        velocity_pixels = v * PIXELS_PER_METER * velocity_scale
        start_pos = (mass_x, reference_y)
        end_pos = (mass_x + velocity_pixels, reference_y)
        draw_vector(screen, start_pos, end_pos, color=GREEN, width=3)
        velocity_text = f"Velocidade: {v:.2f} m/s"
        velocity_surface = font.render(velocity_text, True, GREEN)
        screen.blit(velocity_surface, (20, 80))

    # Desenhar o vetor aceleração se habilitado
    if show_acceleration_vector:
        acceleration_scale = 0.1  # Fator de escala para visualização
        acceleration_pixels = a * PIXELS_PER_METER * acceleration_scale
        start_pos = (mass_x, reference_y + 30)
        end_pos = (mass_x + acceleration_pixels, reference_y + 30)
        draw_vector(screen, start_pos, end_pos, color=ORANGE, width=3)
        acceleration_text = f"Aceleração: {a:.2f} m/s²"
        acceleration_surface = font.render(acceleration_text, True, ORANGE)
        screen.blit(acceleration_surface, (20, 110))

    # Desenhar o vetor força da mola se habilitado
    if show_spring_force_vector:
        force_scale = 50  # Fator de escala para visualização
        spring_force_pixels = spring_force * force_scale
        start_pos = (mass_x, reference_y + 60)
        end_pos = (mass_x + spring_force_pixels, reference_y + 60)
        draw_vector(screen, start_pos, end_pos, color=PURPLE, width=3)
        spring_force_text = f"Força da Mola: {spring_force:.2f} N"
        spring_force_surface = font.render(spring_force_text, True, PURPLE)
        screen.blit(spring_force_surface, (20, 140))

    # Desenhar o vetor força de amortecimento se habilitado
    if show_damping_force_vector:
        force_scale = 50  # Fator de escala para visualização
        damping_force_pixels = damping_force * force_scale
        start_pos = (mass_x, reference_y + 90)
        end_pos = (mass_x + damping_force_pixels, reference_y + 90)
        draw_vector(screen, start_pos, end_pos, color=CYAN, width=3)
        damping_force_text = f"Força de Amort.: {damping_force:.2f} N"
        damping_force_surface = font.render(damping_force_text, True, CYAN)
        screen.blit(damping_force_surface, (20, 170))

    # Desenhar o vetor força resultante se habilitado
    if show_net_force_vector:
        force_scale = 50  # Fator de escala para visualização
        net_force_pixels = net_force * force_scale
        start_pos = (mass_x, reference_y + 120)
        end_pos = (mass_x + net_force_pixels, reference_y + 120)
        draw_vector(screen, start_pos, end_pos, color=BROWN, width=3)
        net_force_text = f"Força Resultante: {net_force:.2f} N"
        net_force_surface = font.render(net_force_text, True, BROWN)
        screen.blit(net_force_surface, (20, 200))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
