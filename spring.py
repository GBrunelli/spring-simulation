import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mass-Spring System Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 24)

# Simulation parameters (initial values)
m = 1.0       # Mass (kg)
k = 10.0      # Spring constant (N/m)
b = 0.5       # Damping coefficient (kg/s), represents dispersion forces
x0 = 100.0    # Initial displacement from equilibrium (pixels)
v0 = 0.0      # Initial velocity (pixels/s)

# Time parameters
clock = pygame.time.Clock()
dt = 0.01     # Time step (s)

# Scale conversion (pixels to meters)
pixels_per_meter = 500  # 100 pixels represent 1 meter

# Initial position and velocity in meters
x = x0 / pixels_per_meter
v = v0 / pixels_per_meter

# Equilibrium position (center of the screen)
equilibrium_x = WIDTH // 2

# Variables for dragging
dragging = False

# Mass properties
mass_radius = 20  # in pixels

# Input boxes for parameters
input_boxes = []

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
            # Check if the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the color of the input box.
            self.color = RED if self.active else GRAY

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # When Enter is pressed, update the simulation parameter.
                    self.update_parameter()
                    self.active = False
                    self.color = GRAY
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Limit input to 10 characters and valid characters
                    if len(self.text) < 10 and (event.unicode.isdigit() or event.unicode == '.' or event.unicode == '-'):
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, BLACK)

    def update_parameter(self):
        global m, k, b
        try:
            value = float(self.text)
            if self.label == 'Mass (kg):':
                m = value if value != 0 else 0.1  # Prevent division by zero
            elif self.label == 'Spring k (N/m):':
                k = value if value != 0 else 0.1
            elif self.label == 'Damping b (kg/s):':
                b = value
            x = 0.0  # Reset position to equilibrium or desired value
            v = 0.0  # Reset velocity

        except ValueError:
            pass  # Ignore invalid input

    def draw(self, screen):
        # Blit the label
        screen.blit(self.label_surface, (self.rect.x - self.label_surface.get_width() - 10, self.rect.y + 5))
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Create input boxes for m, k, b
input_box_m = InputBox(600, 400, 140, 32, text=str(m), label='Mass (kg):')
input_box_k = InputBox(600, 440, 140, 32, text=str(k), label='Spring k (N/m):')
input_box_b = InputBox(600, 480, 140, 32, text=str(b), label='Damping b (kg/s):')
input_boxes = [input_box_m, input_box_k, input_box_b]

def draw_spring(screen, start_pos, end_pos, color, num_coils=20, coil_radius=10, width=2):
    """
    Draw a spring-like texture between two points.

    Parameters:
        screen: The Pygame surface to draw on.
        start_pos: Tuple (x, y) for the start point.
        end_pos: Tuple (x, y) for the end point.
        color: Color of the spring.
        num_coils: Number of coils in the spring.
        coil_radius: Radius of each coil (wave amplitude).
        width: Line width.
    """
    x1, y1 = start_pos
    x2, y2 = end_pos

    # Calculate the vector from start to end
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)

    # Number of points along the spring
    num_points = int(length / 2)  # Increase for smoother spring

    if num_points < 2:
        num_points = 2  # Minimum number of points

    # List to hold the points
    points = []

    for i in range(num_points + 1):
        # Interpolation parameter from 0 to 1
        t = i / num_points

        # Linear interpolation along the line
        x = x1 + t * dx
        y = y1 + t * dy

        # Calculate the displacement perpendicular to the line
        offset = coil_radius * math.sin(t * num_coils * 2 * math.pi)
        offset_x = offset * math.cos(angle + math.pi / 2)
        offset_y = offset * math.sin(angle + math.pi / 2)

        # Add the point with displacement
        points.append((x + offset_x, y + offset_y))

    # Draw the spring
    if len(points) >= 2:
        pygame.draw.lines(screen, color, False, points, width)

# Main simulation loop
running = True
while running:
    # Event handling (e.g., window close)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle events for input boxes
        for box in input_boxes:
            box.handle_event(event)

        # Handle events for dragging the mass
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is over the mass
            mouse_x, mouse_y = event.pos
            mass_x = equilibrium_x + x * pixels_per_meter
            mass_y = HEIGHT // 2
            distance = math.hypot(mouse_x - mass_x, mouse_y - mass_y)
            if distance <= mass_radius:
                dragging = True
                v = 0.0  # Reset velocity when starting to drag

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                v = 0.0  # Reset velocity when the mass is released

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                # Update the position of the mass to follow the mouse
                mouse_x, mouse_y = event.pos
                # Calculate x in meters from mouse_x in pixels
                x = (mouse_x - equilibrium_x) / pixels_per_meter
                # Optionally, calculate the velocity based on mouse movement
                # v = 0.0  # Reset velocity during dragging or calculate based on mouse movement

    if not dragging:
        # Calculate forces
        spring_force = -k * x  # Hooke's Law: F = -kx
        damping_force = -b * v  # Damping force proportional to velocity
        net_force = spring_force + damping_force  # Total force

        # Calculate acceleration (Newton's 2nd law: F = ma)
        a = net_force / m

        # Update velocity and position (Euler method)
        v += a * dt
        x += v * dt

    # Clear the screen
    screen.fill(WHITE)

    # Draw input boxes
    for box in input_boxes:
        box.draw(screen)

    # Draw parameter values
    param_text = f"Mass (m): {m:.2f} kg   Spring Constant (k): {k:.2f} N/m   Damping Coefficient (b): {b:.2f} kg/s"
    param_surface = font.render(param_text, True, BLACK)
    screen.blit(param_surface, (10, HEIGHT - 30))

    # Calculate mass position in pixels
    mass_x = equilibrium_x + x * pixels_per_meter

    # Draw the spring (line from equilibrium to mass)
    #pygame.draw.line(screen, BLACK, (equilibrium_x, HEIGHT // 2), (mass_x, HEIGHT // 2), 2)
    draw_spring(
        screen,
        (equilibrium_x, HEIGHT // 2),
        (mass_x, HEIGHT // 2),
        BLACK,
        num_coils=15,
        coil_radius=10,
        width=2
    )

    # Draw the mass (circle)
    mass_color = (255, 0, 0) if dragging else BLACK
    pygame.draw.circle(screen, mass_color, (int(mass_x), HEIGHT // 2), mass_radius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Clean up and exit
pygame.quit()
sys.exit()