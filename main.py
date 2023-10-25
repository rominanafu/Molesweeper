"""

MOLESWEEPER Nafu 1.0

A game based in Minesweeper
(but they aren't the same >:/)

Romina Nájera Fuentes

"""

import pygame
import random

class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
        self.down = pygame.Surface((70, 70))
        self.down.fill((37, 65, 23))
        self.up = pygame.Surface((60, 60))
        self.up.fill((0, 128, 0))
        self.rect = self.down.get_rect()
        
class Nothing(pygame.sprite.Sprite):
    def __init__(self):
        super(Nothing, self).__init__()
        self.down = pygame.Surface((50, 50))
        self.down.fill((92, 64, 51))
        self.up = pygame.Surface((40, 40))
        self.up.fill((150, 100, 80))
        self.rect = self.down.get_rect()
        
class Mole(pygame.sprite.Sprite):
    def __init__(self):
        super(Mole, self).__init__()
        self.surf = pygame.image.load("Images/Mole.png").convert()
        self.surf = pygame.transform.scale(self.surf, (70, 70))
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        
def create_moles_grid(moles, x, y):
    # Create moles grid
    # (indicating position of each mole and number in each square)

    grid = []
    positions_list = []
    mat_mov = [[1, 0], [0, 1], [1, 1], [-1, 0], [0, -1], [-1, -1], [1, -1], [-1, 1]]
    
    for f in range(rows):
        grid.append([])
        for c in range(columns):
            grid[f].append(0)
            if x == f and y == c:
                continue
            skip = False
            for mov in mat_mov:
                if x+mov[0] == f and y+mov[1] == c:
                    skip = True
                    break
            if skip:
                continue
            positions_list.append([f, c])
    
    random.shuffle(positions_list)
    
    for m in range(moles):
        x = positions_list[m][0]
        y = positions_list[m][1]
        grid[x][y] = -1 # -1 represents a mole
        for mov in mat_mov:
            if x + mov[0] < 0 or x + mov[0] >= rows:
                pass
            elif y + mov[1] < 0 or y + mov[1] >= columns:
                pass
            elif grid[x + mov[0]][y + mov[1]] == -1:
                pass
            else:
                grid[x + mov[0]][y + mov[1]] += 1
    return grid

def create_user_grid():
    # Create user grid
    # (shows the status of each square - revealed or not, marked as mole or not)

    grid = []
    for f in range(rows):
        grid.append([])
        for c in range(columns):
            grid[f].append('*')
    return grid

def grid_setup():
    pos_x0 = window_base/2 - (3.5*70 + 3*5)
    pos_y0 = 70
    objects_grid = []
    for f in range(rows):
        objects_grid.append([])
        add_x = f * (70 + 5)
        for c in range(columns):
            add_y = c * (70 + 5)
            if moles_grid[f][c] == -1:
                objects_grid[f].append(Mole())
                window.blit(objects_grid[f][c].surf, (pos_x0 + add_x, pos_y0 + add_y))
            else:
                objects_grid[f].append(Nothing())
                window.blit(objects_grid[f][c].down, (pos_x0 + add_x+10, pos_y0 + add_y+10))
                window.blit(objects_grid[f][c].up, (pos_x0 + add_x+15, pos_y0 + add_y+15))
            if moles_grid[f][c] != -1 and moles_grid[f][c] != 0:
                font = pygame.font.Font(None, 30)
                text = str(moles_grid[f][c])
                message = font.render(text, 10, (255, 255, 255))
                window.blit(message, (pos_x0 + add_x+30, pos_y0 + add_y+27))
            

def update_grid():
    pos_x0 = window_base/2 - ((columns / 2) * 70 + ((columns - 1) / 2) * 5)
    pos_y0 = 70
    squares_grid = []
    for f in range(rows):
        squares_grid.append([])
        add_x = f * (70 + 5)
        for c in range(columns):
            add_y = c * (70 + 5)
            squares_grid[f].append(Square())
            if user_grid[f][c] == '*':
                window.blit(squares_grid[f][c].down, (pos_x0 + add_x, pos_y0 + add_y))
                window.blit(squares_grid[f][c].up, (pos_x0 + add_x + 5, pos_y0 + add_y + 5))
            elif user_grid[f][c] == 'T':
                window.blit(squares_grid[f][c].down, (pos_x0 + add_x, pos_y0 + add_y))
                window.blit(squares_grid[f][c].up, (pos_x0 + add_x + 5, pos_y0 + add_y + 5))
                window.blit(alert_in_square, (pos_x0 + add_x, pos_y0 + add_y))

        
def bfs(x, y, not_revealed):
    # Breadth First Search to reveal the 8 squares
    # around a square with 0 adjacent moles

    adj_positions = []
    mat_mov = [[1, 0], [0, 1], [1, 1], [-1, 0], [0, -1], [-1, -1], [1, -1], [-1, 1]]
    adj_positions.append([x, y])
    
    while len(adj_positions) != 0:
        x = adj_positions[0][0]
        y = adj_positions[0][1]
        adj_positions.pop(0)
        for mov in mat_mov:
            new_x = x + mov[0]
            new_y = y + mov[1]
            if new_x < 0 or new_x >= rows:
                continue
            elif new_y < 0 or new_y >= columns:
                continue
            elif user_grid[new_x][new_y] != '*':
                continue
            else:
                user_grid[new_x][new_y] = moles_grid[new_x][new_y]
                not_revealed -= 1
                if user_grid[new_x][new_y] == 0:
                    adj_positions.append([new_x, new_y])
    return not_revealed
        
pygame.init()  # Pygame initialization
pygame.font.init()

# Declare the window
window_base = 600
window_height = 600
window = pygame.display.set_mode((window_base+50, window_height))

background = pygame.image.load("Images/Grass.png").convert()
background = pygame.transform.scale(background, (window_base+50, window_height))

alert = pygame.image.load("Images/Alert.png").convert()
alert.set_colorkey((0, 0, 0), pygame.RLEACCEL)
alert_in_square = pygame.transform.scale(alert, (70, 70))
alert = pygame.transform.scale(alert, (45, 45))

eyes = pygame.image.load("Images/Eyes.png").convert()
eyes.set_colorkey((249, 209, 0), pygame.RLEACCEL)
eyes = pygame.transform.scale(eyes, (45, 45))

rectangle_1 = pygame.Surface((60, 105))
rectangle_1.fill((37, 65, 23))

selected_movement = pygame.Surface((45, 45))
selected_movement.fill((0, 128, 0))

opaque_window = pygame.Surface((window_base+50, window_height))
opaque_window.fill((0, 0, 0))
opaque_window.set_alpha(150)

button = pygame.Surface((300, 50), pygame.SRCALPHA)

# Display title
pygame.display.set_caption("MOLESWEEPER (Nafu 1.0 version)")

font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True, italic=False), 60)
text = "MOLESWEEPER"
title = font.render(text, 10, (255, 255, 255))

font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 20)

rows = 7
columns = 7

moles = 10
reveal = True
playing = True
first_reveal = True
not_revealed = rows * columns - moles

moles_grid = create_moles_grid(moles, 0, 0)
user_grid = create_user_grid()

window_open = True

while window_open:

    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            # The user closes the window
            window_open = False
        elif event.type == pygame.MOUSEBUTTONUP and playing:
            for f in range(rows):
                for c in range(columns):
                    pos_x0 = window_base/2 - ((columns / 2) * 70 + ((columns - 1) / 2) * 5)
                    pos_y0 = 70
                    rect = pygame.Rect((pos_x0 + (f * (70 + 5)), pos_y0 + (c * (70 + 5))), (70, 70))
                    if rect.collidepoint(event.pos):
                        if reveal:
                            if user_grid[f][c] == '*':
                                if first_reveal:
                                    # The map is created
                                    moles_grid = create_moles_grid(moles, f, c)
                                    first_reveal = False
                                if moles_grid[f][c] == -1:
                                    playing = False
                                    user_grid[f][c] = moles_grid[f][c]
                                    break
                                user_grid[f][c] = moles_grid[f][c]
                                not_revealed -= 1
                                if user_grid[f][c] == 0:
                                    not_revealed = bfs(f, c, not_revealed)
                            elif user_grid[f][c] == 'T':
                                user_grid[f][c] = '*'
                                moles += 1
                        else:
                            if user_grid[f][c] != 'T':
                                user_grid[f][c] = 'T'
                                moles -= 1
            
            # Reveal button or Mark-as-mole button was pressed
            rect_alert = pygame.Rect((window_base - 20, window_height / 2), (40, 40))
            rect_eyes = pygame.Rect((window_base - 18, window_height / 2 + 50), (40, 40))
            if rect_alert.collidepoint(event.pos):
                reveal = False
            elif rect_eyes.collidepoint(event.pos):
                reveal = True
            
        elif event.type == pygame.MOUSEBUTTONUP and not playing:
            # Play again
            position = (window_base/2-130, window_height/2+55)
            button_rect = pygame.Rect(position, (250, 60))
            if button_rect.collidepoint(event.pos):
                playing = True
                first_reveal = True
                reveal = True
                moles = 10
                not_revealed = rows * columns - moles
                moles_grid = create_moles_grid(moles, 0, 0)
                user_grid = create_user_grid()
            
    window.blit(background, (0, 0))
    window.blit(title, (120, 7))
    window.blit(rectangle_1, (window_base - 27, window_height / 2 - 4))
    
    if reveal:
        window.blit(selected_movement, (window_base - 18, window_height/2+50))
    else:
        window.blit(selected_movement, (window_base - 20, window_height/2))
    
    window.blit(alert, (window_base - 20, window_height/2))
    window.blit(eyes, (window_base - 18, window_height/2+50))
    
    grid_setup()
    update_grid()
    
    text = "Moles:"
    numero = str(moles)
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 20)
    message = font.render(text, 7, (255, 255, 255))
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 35)
    message_numero = font.render(numero, 7, (255, 0, 0))
    window.blit(message, (window_base-30, 20))
    window.blit(message_numero, (window_base-30, 40))
    
    
    if not playing:
        window.blit(opaque_window, (0, 0))
        if not_revealed == 0:
            you_win = pygame.image.load("Images/You_Win.png").convert()
            you_win.set_colorkey((153, 0, 48), pygame.RLEACCEL)
            you_win = pygame.transform.scale(you_win, (600, 600))
            window.blit(you_win, (0, 0))
        else:
            game_over = pygame.image.load("Images/Game_Over.png").convert()
            game_over.set_colorkey((153, 0, 48), pygame.RLEACCEL)
            game_over = pygame.transform.scale(game_over, (600, 600))
            window.blit(game_over, (20, -100))
            
        """
        cool_mole = pygame.image.load("Images/Topo_Pixelart.png").convert()
        cool_mole.set_colorkey((249, 209, 0), pygame.RLEACCEL)
        cool_mole = pygame.transform.scale(cool_mole, (120, 120))
        window.blit(cool_mole, (window_base-120, window_height-130))
        """
        
        position = (window_base/2-130, window_height/2+55)
        color = (255, 255, 255)
        pygame.draw.rect(window, color, pygame.Rect(position, (250, 60)),  0, 5)

        position = (window_base/2-125, window_height/2+60)
        color = (125, 102, 66)
        pygame.draw.rect(window, color, pygame.Rect(position, (240, 50)),  0, 5)
        
        text = "Play again"
        font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 25)
        message = font.render(text, 7, (210, 210, 210))
        window.blit(message, (window_base/2-80, window_height/2+70))
    
    if not_revealed == 0:
        playing = False
    
    pygame.display.flip()

    # Add house of Menu, and sound effects

pygame.quit()
