import pygame
import sys
import math

# --- Basic Setup ---
pygame.init()

# Window Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ruler Drawing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)  # <<< FIX: Re-added the missing color definition
LIGHT_BLUE = (173, 216, 230)
RED = (255, 100, 100)
GREEN = (0, 200, 0)

# Ruler Color Palette
RULER_COLORS = {
    "Yellow": (255, 204, 0),
    "Blue": (100, 149, 237),
    "Green": (119, 172, 48),
    "Red": (210, 43, 43),
}

def darken_color(color, factor=0.8):
    return tuple(max(0, int(c * factor)) for c in color)

def fade_color(color, amount=0.6):
    gray_value = 180
    r = int(color[0] * (1 - amount) + gray_value * amount)
    g = int(color[1] * (1 - amount) + gray_value * amount)
    b = int(color[2] * (1 - amount) + gray_value * amount)
    return (r, g, b)

# Fonts
FONT = pygame.font.SysFont("Calibri", 36, bold=True)
FONT_MEDIUM = pygame.font.SysFont("Calibri", 32)
FONT_SMALL = pygame.font.SysFont("Calibri", 28)
FONT_INSTRUCTION = pygame.font.SysFont("Calibri", 24)

# --- ICON DRAWING FUNCTIONS ---
def draw_straight_ruler_icon(surface, rect, color):
    pygame.draw.rect(surface, color, rect, border_radius=5)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=5)
    for i in range(1, 4):
        x = rect.left + i * (rect.width / 4)
        pygame.draw.line(surface, BLACK, (x, rect.top), (x, rect.top + rect.height / 1.5), 2)

def draw_triangle_ruler_icon(surface, rect, color):
    points = [(rect.left, rect.bottom), (rect.right, rect.bottom), (rect.left, rect.top)]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, BLACK, points, 2)

def draw_protractor_icon(surface, rect, color):
    center_x = rect.centerx
    bottom_y = rect.bottom
    radius = rect.width / 2
    points = [(rect.left, bottom_y)]
    for i in range(181):
        angle = math.radians(i)
        x = center_x - radius * math.cos(angle)
        y = bottom_y - radius * math.sin(angle)
        points.append((x, y))
    points.append((rect.right, bottom_y))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, BLACK, points, 2)
    for i in [30, 60, 90, 120, 150]:
        angle = math.radians(i)
        start_x = center_x - radius * math.cos(angle)
        start_y = bottom_y - radius * math.sin(angle)
        end_x = center_x - (radius * 0.8) * math.cos(angle)
        end_y = bottom_y - (radius * 0.8) * math.sin(angle)
        pygame.draw.line(surface, BLACK, (start_x, start_y), (end_x, end_y), 1)

# --- Game Settings & State ---
MAX_L = 1000
MAX_H = 10
clock = pygame.time.Clock()

# --- Game State Variables ---
game_state = "SELECTION"
selected_ruler_type = "Straight"
selected_color_name = "Yellow"

input_text_L = "900"
input_text_h = "7"
active_box = None
error_message = ""

draw_queue = []
drawn_lines = []
last_draw_time = 0
DRAW_DELAY = 25

# --- UI RECT DEFINITIONS ---
type_buttons = {
    "Straight": pygame.Rect(250, 300, 200, 70),
    "Triangle": pygame.Rect(500, 300, 200, 70),
    "Protractor": pygame.Rect(750, 300, 200, 70),
}
icon_height = 80
icon_padding = 20
icon_rects = {
    "Straight": pygame.Rect(type_buttons["Straight"].centerx - 75, type_buttons["Straight"].y - icon_height - icon_padding, 150, 40),
    "Triangle": pygame.Rect(type_buttons["Triangle"].centerx - 50, type_buttons["Triangle"].y - icon_height - icon_padding, 100, icon_height),
    "Protractor": pygame.Rect(type_buttons["Protractor"].centerx - 75, type_buttons["Protractor"].y - icon_height - icon_padding, 150, 75),
}
icon_draw_functions = { "Straight": draw_straight_ruler_icon, "Triangle": draw_triangle_ruler_icon, "Protractor": draw_protractor_icon }
color_swatches = {name: pygame.Rect(325 + i*150, 450, 100, 100) for i, name in enumerate(RULER_COLORS)}
continue_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 125, 650, 250, 70)

input_rect_L = pygame.Rect(SCREEN_WIDTH/2 - 100, 250, 200, 50)
input_rect_h = pygame.Rect(SCREEN_WIDTH/2 - 100, 320, 200, 50)
start_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, 500, 200, 60)
back_button_rect = pygame.Rect(30, 30, 120, 50)
reset_button_rect = pygame.Rect(SCREEN_WIDTH - 200, 30, 170, 50)


# --- TICK GENERATION LOGIC (Unchanged) ---
def generate_straight_ruler_ticks(left, right, current_level, initial_h, base_y):
    if current_level <= 0: return
    center_x = (left + right) / 2
    if initial_h > 1:
        ratio = (current_level - 1) / (initial_h - 1); line_height = 15 + ratio * (60 - 15)
    else: line_height = 60
    draw_queue.append(((center_x, base_y), (center_x, base_y + line_height)))
    generate_straight_ruler_ticks(left, center_x, current_level - 1, initial_h, base_y)
    generate_straight_ruler_ticks(center_x, right, current_level - 1, initial_h, base_y)
def generate_triangle_ruler_ticks(p1, p2, current_level, initial_h):
    if current_level <= 0: return
    center_x = (p1[0] + p2[0]) / 2; center_y = (p1[1] + p2[1]) / 2
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]; length = math.hypot(dx, dy)
    nx, ny = dy / length, -dx / length
    if initial_h > 1:
        ratio = (current_level - 1) / (initial_h - 1); line_height = 10 + ratio * (40 - 10)
    else: line_height = 40
    p_end = (center_x + nx * line_height, center_y + ny * line_height)
    draw_queue.append(((center_x, center_y), p_end))
    generate_triangle_ruler_ticks(p1, (center_x, center_y), current_level - 1, initial_h)
    generate_triangle_ruler_ticks((center_x, center_y), p2, current_level - 1, initial_h)
def generate_protractor_ticks(center_pos, radius, start_angle, end_angle, current_level, initial_h):
    if current_level <= 0: return
    mid_angle_deg = (start_angle + end_angle) / 2; mid_angle_rad = math.radians(mid_angle_deg)
    if initial_h > 1:
        ratio = (current_level - 1) / (initial_h - 1); tick_length = 20 + ratio * (60 - 20)
    else: tick_length = 60
    p_inner_x = center_pos[0] + radius * math.cos(mid_angle_rad); p_inner_y = center_pos[1] - radius * math.sin(mid_angle_rad)
    p_outer_x = center_pos[0] + (radius - tick_length) * math.cos(mid_angle_rad); p_outer_y = center_pos[1] - (radius - tick_length) * math.sin(mid_angle_rad)
    draw_queue.append(((p_inner_x, p_inner_y), (p_outer_x, p_outer_y)))
    generate_protractor_ticks(center_pos, radius, start_angle, mid_angle_deg, current_level - 1, initial_h)
    generate_protractor_ticks(center_pos, radius, mid_angle_deg, end_angle, current_level - 1, initial_h)


# --- MAIN GAME LOOP ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "SELECTION":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in type_buttons.items():
                    if rect.collidepoint(event.pos): selected_ruler_type = name
                for name, rect in color_swatches.items():
                    if rect.collidepoint(event.pos): selected_color_name = name
                if continue_button_rect.collidepoint(event.pos):
                    game_state = "INPUT"; error_message = ""
        elif game_state == "INPUT":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos): game_state = "SELECTION"
                elif start_button_rect.collidepoint(event.pos):
                    try:
                        L = int(input_text_L); h = int(input_text_h)
                        if not (0 < L <= MAX_L): error_message = f"Length L must be between 1 and {MAX_L}."
                        elif not (0 < h <= MAX_H): error_message = f"Levels h should be between 1 and {MAX_H}."
                        else:
                            game_state = "DRAWING"; error_message = ""; draw_queue.clear(); drawn_lines.clear()
                            if selected_ruler_type == "Straight":
                                x_start = (SCREEN_WIDTH - L) / 2; y_pos = (SCREEN_HEIGHT - 80) / 2
                                generate_straight_ruler_ticks(x_start, x_start + L, h, h, y_pos)
                            elif selected_ruler_type == "Triangle":
                                side_len = min(L, 600)
                                p1 = ((SCREEN_WIDTH-side_len)/2, (SCREEN_HEIGHT+side_len)/2); p2 = ((SCREEN_WIDTH+side_len)/2, (SCREEN_HEIGHT+side_len)/2); p3 = ((SCREEN_WIDTH-side_len)/2, (SCREEN_HEIGHT+side_len)/2 - side_len)
                                generate_triangle_ruler_ticks(p1, p2, h, h); generate_triangle_ruler_ticks(p2, p3, h, h); generate_triangle_ruler_ticks(p3, p1, h, h)
                            elif selected_ruler_type == "Protractor":
                                radius = L / 2; center_pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 150)
                                generate_protractor_ticks(center_pos, radius, 0, 180, h, h)
                    except ValueError: error_message = "Please enter valid numbers."
                else:
                    active_box = None
                    if input_rect_L.collidepoint(event.pos): active_box = "L"
                    elif input_rect_h.collidepoint(event.pos): active_box = "h"
            if event.type == pygame.KEYDOWN:
                if active_box == "L":
                    if event.key == pygame.K_BACKSPACE: input_text_L = input_text_L[:-1]
                    elif event.unicode.isdigit(): input_text_L += event.unicode
                elif active_box == "h":
                    if event.key == pygame.K_BACKSPACE: input_text_h = input_text_h[:-1]
                    elif event.unicode.isdigit(): input_text_h += event.unicode
        elif game_state == "DONE":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button_rect.collidepoint(event.pos): game_state = "SELECTION"

    # --- Game State Logic ---
    if game_state == "DRAWING":
        current_time = pygame.time.get_ticks()
        if current_time - last_draw_time > DRAW_DELAY:
            if draw_queue:
                drawn_lines.append(draw_queue.pop(0)); last_draw_time = current_time
            else: game_state = "DONE"
    
    # --- Drawing ---
    screen.fill(WHITE)
    if game_state == "SELECTION":
        title_surf = FONT.render("Choose a Ruler Type", True, BLACK); screen.blit(title_surf, (SCREEN_WIDTH/2 - title_surf.get_width()/2, 100))
        
        base_color = RULER_COLORS[selected_color_name]
        for name, rect in icon_rects.items():
            draw_func = icon_draw_functions[name]
            icon_color = base_color if name == selected_ruler_type else fade_color(base_color)
            draw_func(screen, rect, icon_color)
        
        for name, rect in type_buttons.items():
            is_selected = (name == selected_ruler_type)
            pygame.draw.rect(screen, LIGHT_BLUE if is_selected else GRAY, rect, border_radius=12)
            pygame.draw.rect(screen, BLACK, rect, 4 if is_selected else 2, border_radius=12)
            text_surf = FONT_MEDIUM.render(name, True, BLACK)
            screen.blit(text_surf, (rect.centerx - text_surf.get_width()/2, rect.centery - text_surf.get_height()/2))
        
        color_title_surf = FONT.render("Choose a Color", True, BLACK); screen.blit(color_title_surf, (SCREEN_WIDTH/2 - color_title_surf.get_width()/2, 400))
        for name, rect in color_swatches.items():
            is_selected = (name == selected_color_name)
            pygame.draw.rect(screen, RULER_COLORS[name], rect, border_radius=10)
            if is_selected: pygame.draw.rect(screen, BLACK, rect, 5, border_radius=10)
        
        pygame.draw.rect(screen, GREEN, continue_button_rect, border_radius=10)
        continue_text = FONT.render("Continue", True, WHITE)
        screen.blit(continue_text, (continue_button_rect.centerx - continue_text.get_width()/2, continue_button_rect.centery - continue_text.get_height()/2))

    elif game_state == "INPUT":
        title_surf = FONT.render(f"{selected_ruler_type} Ruler Settings", True, BLACK); screen.blit(title_surf, (SCREEN_WIDTH/2 - title_surf.get_width()/2, 100))
        pygame.draw.rect(screen, GRAY, back_button_rect, border_radius=8); back_text = FONT_MEDIUM.render("Back", True, BLACK); screen.blit(back_text, (back_button_rect.centerx - back_text.get_width()/2, back_button_rect.centery - back_text.get_height()/2))
        label_h_surf = FONT_MEDIUM.render("Number of Levels (h):", True, BLACK); screen.blit(label_h_surf, (input_rect_h.x - 300, input_rect_h.y + 5))
        pygame.draw.rect(screen, LIGHT_BLUE if active_box == "h" else GRAY, input_rect_h, border_radius=8); pygame.draw.rect(screen, BLACK, input_rect_h, 2, border_radius=8)
        text_h_surf = FONT_MEDIUM.render(input_text_h, True, BLACK); screen.blit(text_h_surf, (input_rect_h.x + 10, input_rect_h.y + 10))
        label_L_surf = FONT_MEDIUM.render("Ruler Length (L):", True, BLACK); screen.blit(label_L_surf, (input_rect_L.x - 235, input_rect_L.y + 5))
        pygame.draw.rect(screen, LIGHT_BLUE if active_box == "L" else GRAY, input_rect_L, border_radius=8); pygame.draw.rect(screen, BLACK, input_rect_L, 2, border_radius=8)
        text_L_surf = FONT_MEDIUM.render(input_text_L, True, BLACK); screen.blit(text_L_surf, (input_rect_L.x + 10, input_rect_L.y + 10))
        instruction_surf = FONT_INSTRUCTION.render(f"(Hint: Max L is {MAX_L}, h should be <= {MAX_H})", True, DARK_GRAY); screen.blit(instruction_surf, (SCREEN_WIDTH/2 - instruction_surf.get_width()/2, 420))
        pygame.draw.rect(screen, GREEN, start_button_rect, border_radius=10); start_text_surf = FONT.render("Draw", True, WHITE); screen.blit(start_text_surf, (start_button_rect.centerx - start_text_surf.get_width()/2, start_button_rect.centery - start_text_surf.get_height()/2))
        if error_message:
            error_surf = FONT_SMALL.render(error_message, True, RED); screen.blit(error_surf, (SCREEN_WIDTH/2 - error_surf.get_width()/2, 580))

    elif game_state == "DRAWING" or game_state == "DONE":
        color = RULER_COLORS[selected_color_name]; shadow_color = darken_color(color); L = int(input_text_L)
        if selected_ruler_type == "Straight":
            ruler_height = 80; ruler_y_pos = (SCREEN_HEIGHT - ruler_height) / 2; ruler_x_start = (SCREEN_WIDTH - L) / 2; shadow_offset = 10
            pygame.draw.rect(screen, shadow_color, (ruler_x_start + shadow_offset, ruler_y_pos + shadow_offset, L, ruler_height), border_radius=10)
            pygame.draw.rect(screen, color, (ruler_x_start, ruler_y_pos, L, ruler_height), border_radius=10)
            pygame.draw.rect(screen, BLACK, (ruler_x_start, ruler_y_pos, L, ruler_height), 4, border_radius=10)
        elif selected_ruler_type == "Triangle":
            side_len = min(L, 600)
            p1 = ((SCREEN_WIDTH-side_len)/2, (SCREEN_HEIGHT+side_len)/2); p2 = ((SCREEN_WIDTH+side_len)/2, (SCREEN_HEIGHT+side_len)/2); p3 = ((SCREEN_WIDTH-side_len)/2, (SCREEN_HEIGHT+side_len)/2 - side_len)
            points = [p1,p2,p3]; shadow_points = [(x+10, y+10) for x,y in points]
            pygame.draw.polygon(screen, shadow_color, shadow_points); pygame.draw.polygon(screen, color, points); pygame.draw.polygon(screen, BLACK, points, 5)
        elif selected_ruler_type == "Protractor":
            radius = L / 2; center_pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 150)
            rect_arc = pygame.Rect(center_pos[0]-radius, center_pos[1]-radius, radius*2, radius*2)
            shadow_rect = pygame.Rect(rect_arc.left+10, rect_arc.top+10, rect_arc.width, rect_arc.height)
            pygame.draw.arc(screen, shadow_color, shadow_rect, 0, math.pi, 70); pygame.draw.arc(screen, color, rect_arc, 0, math.pi, 60)
            pygame.draw.arc(screen, BLACK, rect_arc, 0, math.pi, 5); pygame.draw.line(screen, BLACK, (center_pos[0]-radius, center_pos[1]), (center_pos[0]+radius, center_pos[1]), 5)
        for line in drawn_lines:
            pygame.draw.line(screen, BLACK, line[0], line[1], 2)
        if game_state == "DONE":
            pygame.draw.rect(screen, LIGHT_BLUE, reset_button_rect, border_radius=8)
            reset_text_surf = FONT_MEDIUM.render("Draw Again", True, BLACK)
            screen.blit(reset_text_surf, (reset_button_rect.centerx - reset_text_surf.get_width()/2, reset_button_rect.centery - reset_text_surf.get_height()/2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()