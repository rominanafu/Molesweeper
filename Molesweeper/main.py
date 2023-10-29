"""

MOLESWEEPER Nafu 2.0

A game based in Minesweeper
(but they aren't the same >:/)

Romina Nájera Fuentes

"""

import pygame
import random
import os
import time

class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
        self.down = pygame.Surface((70, 70))
        self.down.fill(dark_green)
        self.up = pygame.Surface((60, 60))
        self.up.fill(light_green)
        self.rect = self.down.get_rect()
        
class Nothing(pygame.sprite.Sprite):
    def __init__(self):
        super(Nothing, self).__init__()
        self.down = pygame.Surface((50, 50))
        self.down.fill(dark_brown)
        self.up = pygame.Surface((40, 40))
        self.up.fill(light_brown)
        self.rect = self.down.get_rect()
        
class Mole(pygame.sprite.Sprite):
    def __init__(self):
        super(Mole, self).__init__()
        self.surf = pygame.image.load("Molesweeper/Images/Mole.png").convert()
        self.surf = pygame.transform.scale(self.surf, (70, 70))
        self.surf.set_colorkey(black, pygame.RLEACCEL)
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

def grid_setup(down_square_base, between_squares, letter_size, pos_y0):
    # Show the moles and the holes (with their respective numbers)
    # stablished in the moles_grid
    
    margin = 5
    pos_x0 = window_base/2 - ((columns / 2) * down_square_base + ((columns - 1) / 2) * between_squares)
    
    hole = Nothing()
    hole_margin = margin*2
    down_hole_base = down_square_base - hole_margin*2
    up_hole_base = down_hole_base - margin*2
    hole.up = pygame.transform.scale(hole.up, (up_hole_base, up_hole_base))
    hole.down = pygame.transform.scale(hole.down, (down_hole_base, down_hole_base))
    
    mole_temp = Mole()
    mole_temp.surf = pygame.transform.scale(mole_temp.surf, (down_square_base, down_square_base))
    
    for f in range(rows):
        add_y = f * (down_square_base + between_squares)
        for c in range(columns):
            add_x = c * (down_square_base + between_squares)
            if moles_grid[f][c] == -1:
                window.blit(mole_temp.surf, (pos_x0 + add_x, pos_y0 + add_y))
            else:
                window.blit(hole.down, (pos_x0 + add_x+hole_margin,
                                                      pos_y0 + add_y+hole_margin))
                window.blit(hole.up, (pos_x0 + add_x+hole_margin+margin,
                                                    pos_y0 + add_y+hole_margin+margin))
            if moles_grid[f][c] != -1 and moles_grid[f][c] != 0:
                font = pygame.font.Font(None, letter_size)
                text = str(moles_grid[f][c])
                message = font.render(text, 10, white)
                window.blit(message, (pos_x0 + add_x+(down_square_base/2-5),
                                      pos_y0 + add_y+(down_square_base/2-8)))       

def update_grid(down_square_base, between_squares, pos_y0):
    # Show the squares of the grid that haven't been revealed
    # and the mole-warning signs on top of them

    margin = 5
    up_square_base = down_square_base - (margin*2)
    pos_x0 = window_base/2 - ((columns / 2) * down_square_base + ((columns - 1) / 2) * between_squares)
    
    square = Square()
    square.up = pygame.transform.scale(square.up, (up_square_base, up_square_base))
    square.down = pygame.transform.scale(square.down, (down_square_base, down_square_base))
    
    alert_in_square = pygame.transform.scale(alert_icon, (down_square_base, down_square_base))
    
    squares_grid = []
    for f in range(rows):
        squares_grid.append([])
        add_y = f * (down_square_base + between_squares)
        for c in range(columns):
            add_x = c * (down_square_base + between_squares)
            squares_grid[f].append(square)
            if user_grid[f][c] == '*':
                window.blit(squares_grid[f][c].down, (pos_x0 + add_x, pos_y0 + add_y))
                window.blit(squares_grid[f][c].up, (pos_x0 + add_x + margin, pos_y0 + add_y + margin))
            elif user_grid[f][c] == 'T':
                window.blit(squares_grid[f][c].down, (pos_x0 + add_x, pos_y0 + add_y))
                window.blit(squares_grid[f][c].up, (pos_x0 + add_x + margin, pos_y0 + add_y + margin))
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

def main_page_setup():
    # Display the main page
    # with: easy-medium-hard options,
    #       turning on and off the sound effects,
    #       changing the scenario
    window.fill((88, 57, 39))
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True, italic=False), 57)
    title_main_page = font.render("MOLESWEEPER", 1, white)
    window.blit(title_main_page, (50, 25))
    if sound:
        window.blit(sound_on, (405, 130))
    else:
        window.blit(sound_off, (405, 130))
    
    window.blit(configuration_icon, (405, 210))

    color = (125, 102, 66)
    position = (50, 130)
    pygame.draw.rect(window, color, pygame.Rect(position, (220, 50)),  0, 5)
    pygame.draw.rect(window, color, pygame.Rect((285, 140), (40, 7)), 0, 5)
    pygame.draw.rect(window, color, pygame.Rect((285, 152), (40, 7)), 0, 5)
    pygame.draw.rect(window, color, pygame.Rect((285, 164), (40, 7)), 0, 5)

    position = (50, 200)
    pygame.draw.rect(window, color, pygame.Rect(position, (220, 50)),  0, 5)
    pygame.draw.rect(window, color, pygame.Rect((285, 210), (40, 7)), 0, 5)
    pygame.draw.rect(window, color, pygame.Rect((285, 222), (40, 7)), 0, 5)
    pygame.draw.rect(window, color, pygame.Rect((285, 234), (40, 7)), 0, 5)

    position = (50, 270)
    pygame.draw.rect(window, color, pygame.Rect(position, (220, 50)),  0, 5)
    pygame.draw.rect(window, color, pygame.Rect((285, 280), (40, 7)), 0, 5)
    pygame.draw.rect(window, color, pygame.Rect((285, 292), (40, 7)), 0, 5)
    pygame.draw.rect(window, color, pygame.Rect((285, 304), (40, 7)), 0, 5)
    
    text = "Easy"
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 25)
    message = font.render(text, 7, white)
    window.blit(message, (130, 140))
    
    text = "Medium"
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 25)
    message = font.render(text, 7, white)
    window.blit(message, (115, 210))
    
    text = "Hard"
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 25)
    message = font.render(text, 7, white)
    window.blit(message, (130, 280))

def display_elements(current_time):
    # Show menu bar in the lower part of the playing window,
    # number of moles, timer, and title
    window.blit(background, (0, 0))
    window.blit(title, (60, 7))
    pygame.draw.rect(window, dark_brown,
                     pygame.Rect((0, window_height-65), (window_base, 65)))
    window.blit(mole_icon, (450, window_height-65))
    window.blit(house_icon, (window_base/2-20, window_height-50))

    number = str(moles)
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 30)
    message_number = font.render(number, 7, white)
    window.blit(message_number, (540, window_height-45))

    if playing and not counting_time:
        minutes = "0"
        seconds = "0"
    else:
        minutes = str(int(current_time // 60))
        seconds = str(int(current_time % 60))
    message_time = minutes + " M " + seconds + " S"
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 25)
    message_time = font.render(message_time, 2, white)
    window.blit(message_time, (500, 20))

pygame.init()  # Pygame initialization
pygame.font.init()
pygame.mixer.init()

# Colors:
white = (255, 255, 255)
black = (0, 0, 0)
dark_green = (37, 65, 23)
light_green = (0, 128, 0)
dark_brown = (92, 64, 51)
light_brown = (150, 100, 80)

# Declare the window
window_base = 650
window_height = 580
window = pygame.display.set_mode((500, 400))

background = pygame.image.load("Molesweeper/Images/Grass.png").convert()
background = pygame.transform.scale(background, (window_base+50, window_height))

alert_icon = pygame.image.load("Molesweeper/Images/Alert.png").convert()
alert_icon.set_colorkey(black, pygame.RLEACCEL)
alert = pygame.transform.scale(alert_icon, (45, 45))

eyes = pygame.image.load("Molesweeper/Images/Eyes.png").convert()
eyes.set_colorkey((249, 209, 0), pygame.RLEACCEL)
eyes = pygame.transform.scale(eyes, (45, 45))

sound_off = pygame.image.load("Molesweeper/Images/No_Sound.png").convert()
sound_off.set_colorkey((153, 0, 48), pygame.RLEACCEL)
sound_off = pygame.transform.scale(sound_off, (55, 55))

sound_on = pygame.image.load("Molesweeper/Images/Sound_On.png").convert()
sound_on.set_colorkey((153, 0, 48), pygame.RLEACCEL)
sound_on = pygame.transform.scale(sound_on, (55, 55))

configuration_icon = pygame.image.load("Molesweeper/Images/Configuration.png").convert()
configuration_icon.set_colorkey((153, 0, 48), pygame.RLEACCEL)
configuration_icon = pygame.transform.scale(configuration_icon, (50, 50))

house_icon = pygame.image.load("Molesweeper/Images/House.png").convert()
house_icon.set_colorkey((153, 0, 48), pygame.RLEACCEL)
house_icon = pygame.transform.scale(house_icon, (40, 40))

mole_icon = pygame.image.load("Molesweeper/Images/Mole2.png").convert()
mole_icon.set_colorkey((5, 165, 44), pygame.RLEACCEL)
mole_icon = pygame.transform.scale(mole_icon, (70, 70))

selected_movement = pygame.Surface((65, 45))
selected_movement.fill(light_green)

opaque_window = pygame.Surface((window_base+50, window_height))
opaque_window.fill(black)
opaque_window.set_alpha(150)

button = pygame.Surface((300, 50), pygame.SRCALPHA)

# Display title
pygame.display.set_caption("MOLESWEEPER (Nafu 2.0 version)")

font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True, italic=False), 60)
text = "MOLESWEEPER"
title = font.render(text, 10, white)

font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 20)

# Sound effects:
click = pygame.mixer.Sound(os.path.join('Molesweeper/Sound/Click_Sound.wav'))
losing_sound = pygame.mixer.Sound(os.path.join('Molesweeper/Sound/Losing_Sound.wav'))
winning_sound = pygame.mixer.Sound(os.path.join('Molesweeper/Sound/Winning_Sound.wav'))

rows = 7
columns = 7

moles = 10
moles_level = [7, 10, 15]
level = 0
sound = True
reveal = True
playing = True
first_reveal = True
not_revealed = rows * columns - moles
square_base = 70
between_squares = 5
letter_size = 30
pos_y0 = 0

time_ini = 0
time_end = 0

# [rows, columns, square_base, between_squares, letter_size, y_ini] per level
grid_sizes = [[5, 8, 70, 7, 30, 90], [6, 9, 60, 5, 25, 95], [8, 11, 50, 5, 20, 70]]

moles_grid = []
user_grid = []

window_open = True
main_page = True
change_size = True
play_sound = False
counting_time = False

while window_open:

    if main_page:
        if change_size:
            window = pygame.display.set_mode((500, 400))
            change_size = False
        main_page_setup()
        buttons_positions = [[50, 130], [50, 200], [50, 270]]
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                # The user closes the window
                window_open = False
            elif event.type == pygame.MOUSEBUTTONUP:
                
                # if easy/medium/hard button was pressed 
                for i in range(3):
                    rect = pygame.Rect((buttons_positions[i][0], buttons_positions[i][1]), (220, 50))
                    if rect.collidepoint(event.pos):
                        if sound:
                            pygame.mixer.Sound.play(click)
                        main_page = False
                        playing = True
                        level = i
                        
                        # Change values of grid and moles depending on the level
                        moles = moles_level[level]
                        rows = grid_sizes[i][0]
                        columns = grid_sizes[i][1]
                        square_base = grid_sizes[i][2]
                        between_squares = grid_sizes[i][3]
                        letter_size = grid_sizes[i][4]
                        pos_y0 = grid_sizes[i][5]
                        
                        not_revealed = rows * columns - moles
                        change_size = True
                        counting_time = False
                        playing = True
                        first_reveal = True
                        moles_grid = create_moles_grid(moles, 0, 0)
                        user_grid = create_user_grid()
                        
                        break
                
                # if sound effects button was pressed
                rect = pygame.Rect((405, 130), (55, 55))
                if rect.collidepoint(event.pos):
                    pygame.mixer.Sound.play(click)
                    sound = not sound

                # Check if rankings list was pressed
                # (display top 10 times, from "records_easy.txt", "records_medium.txt"
                #   and "records_hard.txt", depending on what was selected)
                # ---
                # Check if configuration button was pressed
                # (configuration_page=True, main_page=False)
    else:
        if change_size:
            window = pygame.display.set_mode((window_base, window_height))
            change_size = False
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                # The user closes the window
                window_open = False
            elif event.type == pygame.MOUSEBUTTONUP and playing:
                for f in range(rows):
                    for c in range(columns):
                        pos_x0 = window_base/2 - ((columns/2) * square_base + ((columns-1)/2) * between_squares)
                        rect = pygame.Rect((pos_x0 + (c * (square_base + between_squares)),
                                            pos_y0 + (f * (square_base + between_squares))),
                                           (square_base, square_base))
                        if rect.collidepoint(event.pos):
                            if sound:
                                pygame.mixer.Sound.play(click)
                            if reveal:
                                if user_grid[f][c] == '*':
                                    if first_reveal:
                                        # The map is created and time begins to count
                                        moles_grid = create_moles_grid(moles, f, c)
                                        time_ini = time.time()
                                        counting_time = True
                                        first_reveal = False
                                    if moles_grid[f][c] == -1:
                                        playing = False
                                        counting_time = False
                                        time_end = time.time()
                                        play_sound = True
                                        user_grid[f][c] = moles_grid[f][c]
                                        break
                                    user_grid[f][c] = moles_grid[f][c]
                                    not_revealed -= 1
                                    if user_grid[f][c] == 0:
                                        not_revealed = bfs(f, c, not_revealed)
                                    if not_revealed == 0:
                                        playing = False
                                        counting_time = False
                                        time_end = time.time()
                                        play_sound = True
                                elif user_grid[f][c] == 'T':
                                    user_grid[f][c] = '*'
                                    moles += 1
                            else:
                                if user_grid[f][c] == '*':
                                    user_grid[f][c] = 'T'
                                    moles -= 1
                
                # Reveal button or Mark-as-mole button was pressed
                rect_alert = pygame.Rect((150, window_height-55), (40, 40))
                rect_eyes = pygame.Rect((75, window_height-55), (40, 40))
                if rect_alert.collidepoint(event.pos):
                    reveal = False
                    if sound:
                        pygame.mixer.Sound.play(click)
                elif rect_eyes.collidepoint(event.pos):
                    reveal = True
                    if sound:
                        pygame.mixer.Sound.play(click)

                rect_house = pygame.Rect((window_base/2-20, window_height-50), (40, 40))
                if rect_house.collidepoint(event.pos):
                    main_page = True
                    change_size = True
                    if sound:
                        pygame.mixer.Sound.play(click)
                
            elif event.type == pygame.MOUSEBUTTONUP and not playing:
                # Play again
                position = (window_base/2-130, window_height/2+55)
                button_rect = pygame.Rect(position, (250, 60))
                if button_rect.collidepoint(event.pos):
                    if sound:
                        pygame.mixer.Sound.play(click)
                    playing = True
                    first_reveal = True
                    reveal = True
                    moles = moles_level[level]
                    not_revealed = rows * columns - moles
                    not_revealed = rows * columns - moles
                    moles_grid = create_moles_grid(moles, 0, 0)
                    user_grid = create_user_grid()

        if not playing:
            current_time = time_end - time_ini
        else:
            current_time = time.time() - time_ini
        
        display_elements(current_time)
        
        if reveal:
            window.blit(selected_movement, (65, window_height-55))
        else:
            window.blit(selected_movement, (140, window_height-55))
        
        window.blit(alert, (150, window_height-55))
        window.blit(eyes, (75, window_height-55))
        
        grid_setup(square_base, between_squares, letter_size, pos_y0)
        update_grid(square_base, between_squares, pos_y0)
        
        if not playing:
            window.blit(opaque_window, (0, 0))
            if play_sound:
                if sound:
                    if not_revealed == 0:
                        pygame.mixer.Sound.play(winning_sound)
                    else:
                        pygame.mixer.Sound.play(losing_sound)
                play_sound = False
            if not_revealed == 0:
                you_win = pygame.image.load("Molesweeper/Images/You_Win.png").convert()
                you_win.set_colorkey((153, 0, 48), pygame.RLEACCEL)
                you_win = pygame.transform.scale(you_win, (600, 600))
                window.blit(you_win, (0, 0))
            else:
                game_over = pygame.image.load("Molesweeper/Images/Game_Over.png").convert()
                game_over.set_colorkey((153, 0, 48), pygame.RLEACCEL)
                game_over = pygame.transform.scale(game_over, (600, 600))
                window.blit(game_over, (20, -100))
            
            position = (window_base/2-130, window_height/2+55)
            color = white
            pygame.draw.rect(window, color, pygame.Rect(position, (250, 60)),  0, 5)

            position = (window_base/2-125, window_height/2+60)
            color = (125, 102, 66)
            pygame.draw.rect(window, color, pygame.Rect(position, (240, 50)),  0, 5)
            
            text = "Play again"
            font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 25)
            message = font.render(text, 7, (210, 210, 210))
            window.blit(message, (window_base/2-80, window_height/2+70))
    
    pygame.display.flip()

pygame.quit()
