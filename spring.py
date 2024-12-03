import pygame
import sys
import math
import matplotlib.pyplot as plt
import matplotlib

# Configurar o backend do Matplotlib para evitar conflitos com Pygame
matplotlib.use("TkAgg")
#matplotlib.use("MacOSX") #caso queira rodar em Mac, comente a linha de cima e descomente essa

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 1500, 800
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
EQUILIBRIUM_X = 250  # Posição fixa do início da mola

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

# Coeficiente de restituição (elasticidade)
e = 0.8  # Valor entre 0 e 1 para controlar a elasticidade

# Limite de colisão
collision_threshold = 0.02  # Distância mínima da parede em metros

# Variáveis para gravação de dados e controle
graph_create = False
time_data = []
position_data = []
velocity_data = []
acceleration_data = []
collecting_data = False

# Variável para controle do gráfico
generate_graph_flag = False  # Modificação aqui
plot_open = False  # Adicionado para controlar se o plot está aberto

# Função que controla a coleta de dados
def handle_graph_toggle():
    global collecting_data, generate_graph_flag
    if graph_create and not collecting_data:
        # Começa a gravar dados
        collecting_data = True
        time_data.clear()
        position_data.clear()
        velocity_data.clear()
        acceleration_data.clear()
    elif not graph_create and collecting_data:
        # Para de gravar e sinaliza para gerar o gráfico
        collecting_data = False
        generate_graph_flag = True  # Modificação aqui

def generate_graph():
    global plot_open
    if not time_data:
        print("Nenhum dado para gerar o gráfico.")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(time_data, position_data, label="Posição (m)", color="blue")
    plt.plot(time_data, velocity_data, label="Velocidade (m/s)", color="green")
    plt.plot(time_data, acceleration_data, label="Aceleração (m/s²)", color="orange")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Valores")
    plt.title("Gráfico de Posição, Velocidade e Aceleração")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    def on_close(event):
        global plot_open
        plot_open = False

    plt.gcf().canvas.mpl_connect('close_event', on_close)

    plt.show(block=False)
    plot_open = True

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

# Classe para criar um botão de toggle
class ToggleButton:
    def __init__(self, x, y, w, h, text='', variable_name=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.variable_name = variable_name
        self.txt_surface = font.render(text, True, BLACK)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                current_value = globals()[self.variable_name]
                globals()[self.variable_name] = not current_value

    def draw(self, screen):
        current_value = globals()[self.variable_name]
        button_color = LIGHT_GREEN if current_value else GRAY
        pygame.draw.rect(screen, button_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
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
    ToggleButton(WIDTH - 180, 490, 140, 32, text='Gerar Gráfico', variable_name='graph_create'),
]

def draw_spring(screen, start_pos, end_pos, color, num_coils=20, coil_radius=10, width=2):
    x1, y1 = start_pos
    x1 = x1 - 20
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
    pygame.draw.line(screen, color, start_pos, end_pos, width)
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
start_time = pygame.time.get_ticks() / 1000.0  # Tempo inicial em segundos
while running:
    screen.fill(WHITE)

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

        # Tratamento de colisão suave com a parede
        if x < collision_threshold:
            x = collision_threshold  # Reposicionar a massa para evitar atravessar a parede
            v = -v * e  # Inverter a velocidade com coeficiente de restituição

    # Desenhar a parede no lado esquerdo
    max_wall_height = HEIGHT//2 - 100
    min_wall_height = HEIGHT//2 + 100
    pygame.draw.line(screen, BLACK, (EQUILIBRIUM_X - 20, max_wall_height - 10), (EQUILIBRIUM_X - 20, min_wall_height), 4)
    for i in range(max_wall_height, min_wall_height, 20):
        pygame.draw.line(screen, BLACK, (EQUILIBRIUM_X - 20, i), (EQUILIBRIUM_X - 40, i + 10), 2)
  
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
        displacement_text = f"Deslocamento: {x:.2f} m"
        displacement_surface = font.render(displacement_text, True, BLUE)
        screen.blit(displacement_surface, (20, 50))

    # Desenhar o vetor velocidade se habilitado
    if show_velocity_vector:
        velocity_scale = 0.1  # Fator de escala para visualização
        velocity_pixels = v * PIXELS_PER_METER * velocity_scale
        start_pos = (mass_x, reference_y)
        end_pos = (mass_x + velocity_pixels, reference_y)
        draw_vector(screen, start_pos, end_pos, color=GREEN, width=3)
        velocity_text = f"Velocidade: {abs(v):.2f} m/s"
        velocity_surface = font.render(velocity_text, True, GREEN)
        screen.blit(velocity_surface, (20, 80))

    # Desenhar o vetor aceleração se habilitado
    if show_acceleration_vector:
        acceleration_scale = 0.1  # Fator de escala para visualização
        acceleration_pixels = a * PIXELS_PER_METER * acceleration_scale
        start_pos = (mass_x, reference_y + 30)
        end_pos = (mass_x + acceleration_pixels, reference_y + 30)
        draw_vector(screen, start_pos, end_pos, color=ORANGE, width=3)
        acceleration_text = f"Aceleração: {abs(a):.2f} m/s²"
        acceleration_surface = font.render(acceleration_text, True, ORANGE)
        screen.blit(acceleration_surface, (20, 110))

    # Desenhar o vetor força da mola se habilitado
    if show_spring_force_vector:
        force_scale = 50  # Fator de escala para visualização
        spring_force_pixels = spring_force * force_scale
        start_pos = (mass_x, reference_y + 60)
        end_pos = (mass_x + spring_force_pixels, reference_y + 60)
        draw_vector(screen, start_pos, end_pos, color=PURPLE, width=3)
        spring_force_text = f"Força da Mola: {abs(spring_force):.2f} N"
        spring_force_surface = font.render(spring_force_text, True, PURPLE)
        screen.blit(spring_force_surface, (20, 140))

    # Desenhar o vetor força de amortecimento se habilitado
    if show_damping_force_vector:
        force_scale = 50  # Fator de escala para visualização
        damping_force_pixels = damping_force * force_scale
        start_pos = (mass_x, reference_y + 90)
        end_pos = (mass_x + damping_force_pixels, reference_y + 90)
        draw_vector(screen, start_pos, end_pos, color=CYAN, width=3)
        damping_force_text = f"Força de Amort.: {abs(damping_force):.2f} N"
        damping_force_surface = font.render(damping_force_text, True, CYAN)
        screen.blit(damping_force_surface, (20, 170))

    # Desenhar o vetor força resultante se habilitado
    if show_net_force_vector:
        force_scale = 50  # Fator de escala para visualização
        net_force_pixels = net_force * force_scale
        start_pos = (mass_x, reference_y + 120)
        end_pos = (mass_x + net_force_pixels, reference_y + 120)
        draw_vector(screen, start_pos, end_pos, color=BROWN, width=3)
        net_force_text = f"Força Resultante: {abs(net_force):.2f} N"
        net_force_surface = font.render(net_force_text, True, BROWN)
        screen.blit(net_force_surface, (20, 200))

    # Caso a coleta esteja ligada, salva os dados para plotar
    if collecting_data:
        current_time = pygame.time.get_ticks() / 1000.0 - start_time  # Tempo em segundos desde o início da simulação
        time_data.append(current_time)
        position_data.append(x)
        velocity_data.append(v)
        acceleration_data.append(a)
    
    # Controla quando os dados são coletados e quando o plot é feito
    handle_graph_toggle()

    # Checa se é hora de gerar o gráfico
    if generate_graph_flag:
        generate_graph()
        generate_graph_flag = False

    # Se o gráfico está aberto, atualiza a interface do matplotlib
    if plot_open:
        plt.pause(0.001)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
