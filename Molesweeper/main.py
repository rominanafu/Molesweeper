"""

MOLESWEEPER Nafu 3.0

A game based in Minesweeper
(but they aren't the same >:/)

"""

import pygame
import random
import os
import time

class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
        self.down = pygame.Surface((70, 70))
        self.up = pygame.Surface((60, 60))
        self.rect = self.down.get_rect()
        
class Nothing(pygame.sprite.Sprite):
    def __init__(self):
        super(Nothing, self).__init__()
        self.down = pygame.Surface((50, 50))
        self.up = pygame.Surface((40, 40))
        self.rect = self.down.get_rect()
        
class Mole(pygame.sprite.Sprite):
    def __init__(self):
        super(Mole, self).__init__()
        self.surf = pygame.image.load("Molesweeper/Images/Mole2.png").convert()
        self.surf = pygame.transform.scale(self.surf, (70, 70))
        self.surf.set_colorkey((5, 165, 44), pygame.RLEACCEL)
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
    if background == 0:
        hole.down.fill(dark_brown)
        hole.up.fill(light_brown)
    elif background == 1:
        hole.down.fill(sea_blue)
        hole.up.fill(light_sea_blue)
    else:
        hole.down.fill(azureish_white)
        hole.up.fill(snow_white)
    
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
                if background == 2:
                    message = font.render(text, 10, dark_blue)
                window.blit(message, (pos_x0 + add_x+(down_square_base/2-5),
                                      pos_y0 + add_y+(down_square_base/2-8)))       

def update_grid(down_square_base, between_squares, pos_y0):
    # Show the squares of the grid that haven't been revealed
    # and the mole-warning signs on top of them

    margin = 5
    up_square_base = down_square_base - (margin*2)
    pos_x0 = window_base/2 - ((columns / 2) * down_square_base + ((columns - 1) / 2) * between_squares)
    
    square = Square()
    if background == 0:
        square.up.fill(light_green)
        square.down.fill(dark_green)
    elif background == 1:
        square.up.fill(light_sand_yellow)
        square.down.fill(sand_yellow)
    else:
        square.up.fill(light_blue)
        square.down.fill(dark_blue)
    square.up = pygame.transform.scale(square.up, (up_square_base, up_square_base))
    square.down = pygame.transform.scale(square.down, (down_square_base, down_square_base))
    
    alert_in_square = pygame.transform.scale(alert_icon, (down_square_base, down_square_base))
    
    for f in range(rows):
        add_y = f * (down_square_base + between_squares)
        for c in range(columns):
            add_x = c * (down_square_base + between_squares)
            if user_grid[f][c] == '*':
                window.blit(square.down, (pos_x0 + add_x, pos_y0 + add_y))
                window.blit(square.up, (pos_x0 + add_x + margin, pos_y0 + add_y + margin))
            elif user_grid[f][c] == 'T':
                window.blit(square.down, (pos_x0 + add_x, pos_y0 + add_y))
                window.blit(square.up, (pos_x0 + add_x + margin, pos_y0 + add_y + margin))
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

def main_window_setup():
    # Display the main page
    # with: easy-medium-hard options,
    #       turning on and off the sound effects,
    #       changing the background
    window.fill((88, 57, 39))
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True, italic=False), 57)
    title_main_window = font.render("MOLESWEEPER", 1, white)
    window.blit(title_main_window, (50, 25))
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

def display_playing_elements(current_time):
    # Show menu bar in the lower part of the playing window,
    # number of moles, timer, and title
    if background == 0:
        window.blit(grass, (0, 0))
    elif background == 1:
        window.blit(sand, (0, 0))
    else:
        window.blit(snow, (0, 0))
    window.blit(title, (60, 7))
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

def add_time(current_time):
    if level == 0:
        file = open("Molesweeper/Time_Records/Easy_Level.txt", "r+")
    elif level == 1:
        file = open("Molesweeper/Time_Records/Medium_Level.txt", "r+")
    else:
        file = open("Molesweeper/Time_Records/Hard_Level.txt", "r+")
    content = file.readlines()
    added = False
    for i in range(len(content)):
        time = content[i].split()
        if int(time[0]) > current_time//60:
            content.insert(i, "%i %i\n" %(current_time//60, current_time%60))
            added = True
            break
        elif int(time[0]) == current_time//60:
            if int(time[1]) > current_time%60:
                content.insert(i, "%i %i\n" %(current_time//60, current_time%60))
                added = True
                break
    if len(content) > 10:
        content.pop(10)
    elif len(content) < 10 and not added:
        content.insert(len(content), "%i %i\n" %(current_time//60, current_time%60))
    file.seek(0)
    file.writelines(content)
    file.close()

def display_best_times():
    window.fill((88, 57, 39))
    window.blit(arrow_icon, (30, 25))
    if level == 0:
        file = open("Molesweeper/Time_Records/Easy_Level.txt", "r")
        message = "Easy"
        position = (170, 30)
    elif level == 1:
        file = open("Molesweeper/Time_Records/Medium_Level.txt", "r")
        message = "Medium"
        position = (150, 30)
    else:
        file = open("Molesweeper/Time_Records/Hard_Level.txt", "r")
        message = "Hard"
        position = (170, 30)
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True, italic=False), 20)
    message = font.render(message, 10, white)
    font = pygame.font.Font(pygame.font.match_font('couriernew', bold=False, italic=False), 20)
    window.blit(message, position)
    content = file.readlines()
    position = [40, 80]
    for i in range(len(content)):
        line = content[i].split()
        message = "%2i. %3s m %3s s" %(i+1, line[0], line[1])
        message = font.render(message, 10, white)
        window.blit(message, (position[0], position[1]))
        position[1] += 25
    file.close()

def display_backgrounds():
    window.fill((88, 57, 39))
    window.blit(arrow_icon, (30, 25))

    grass_mole_image = pygame.image.load("Molesweeper/Images/Grass_Mole.png").convert()
    sand_mole_image = pygame.image.load("Molesweeper/Images/Sand_Mole.png").convert()
    snow_mole_image = pygame.image.load("Molesweeper/Images/Snow_Mole.png").convert()
    grass_mole_image = pygame.transform.scale(grass_mole_image, (200, 200))
    sand_mole_image = pygame.transform.scale(sand_mole_image, (200, 200))
    snow_mole_image = pygame.transform.scale(snow_mole_image, (200, 200))

    if background == 0:
        pygame.draw.rect(window, light_brown, pygame.Rect((10, 60), (220, 220)))
    elif background == 1:
        pygame.draw.rect(window, light_brown, pygame.Rect((230, 60), (220, 220)))
    else:
        pygame.draw.rect(window, light_brown, pygame.Rect((450, 60), (220, 220)))

    window.blit(grass_mole_image, (20, 70))
    window.blit(sand_mole_image, (240, 70))
    window.blit(snow_mole_image, (460, 70))

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
sand_yellow = (208, 168, 80)
light_sand_yellow = (255, 222, 144)
sea_blue = (0, 105, 148)
light_sea_blue = (49, 149, 202)
dark_blue = (21, 27, 141)
light_blue = (105, 96, 236)
snow_white = (241, 245, 241)
azureish_white = (150, 179, 241)

# Declare the window
window_base = 650
window_height = 580
window = pygame.display.set_mode((500, 400))

grass = pygame.image.load("Molesweeper/Images/Grass_Background.png").convert()
sand = pygame.image.load("Molesweeper/Images/Sand_Background.png").convert()
snow = pygame.image.load("Molesweeper/Images/Snow_Background.png").convert()

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

arrow_icon = pygame.image.load("Molesweeper/Images/Return_Arrow.png").convert()
arrow_icon.set_colorkey((153, 0, 48), pygame.RLEACCEL)
arrow_icon = pygame.transform.scale(arrow_icon, (30, 30))

selected_movement = pygame.Surface((65, 45))

opaque_window = pygame.Surface((window_base+50, window_height))
opaque_window.fill(black)
opaque_window.set_alpha(150)

button = pygame.Surface((300, 50), pygame.SRCALPHA)

# Display title
pygame.display.set_caption("MOLESWEEPER (Nafu 3.0 version)")

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
background = 0 # 0=grass, 1=sand, 2=snow
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
main_window = True
rankings_window = False
backgrounds_window = False
change_size = True
play_ending_sound = False
counting_time = False

while window_open:

    if main_window:
        if change_size:
            window = pygame.display.set_mode((500, 400))
            change_size = False
        main_window_setup()
        buttons_positions = [[50, 130], [50, 200], [50, 270],
                             [285, 140], [285, 210], [285, 280]]
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
                        main_window = False
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
                
                # if rankings list was pressed
                for i in range(3, 6):
                    rect = pygame.Rect((buttons_positions[i][0], buttons_positions[i][1]), (40, 31))
                    if rect.collidepoint(event.pos):
                        if sound:
                            pygame.mixer.Sound.play(click)
                        rankings_window = True
                        main_window = False
                        level = i-3
                        change_size = True

                # if configuration icon was pressed
                rect = pygame.Rect((405, 210), (50, 50))
                if rect.collidepoint(event.pos):
                    if sound:
                        pygame.mixer.Sound.play(click)
                    backgrounds_window = True
                    main_window = False
                    change_size = True
                    
    elif rankings_window:
        if change_size:
            window = pygame.display.set_mode((280, 400))
            change_size = False
        display_best_times()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                # The user closes the window
                window_open = False
            elif event.type == pygame.MOUSEBUTTONUP:
                #  Return to main page
                rect = pygame.Rect((30, 25), (30, 30))
                if rect.collidepoint(event.pos):
                    if sound:
                        pygame.mixer.Sound.play(click)
                    main_window = True
                    rankings_window = False
                    change_size = True
                    break

    elif backgrounds_window:
        if change_size:
            window = pygame.display.set_mode((680, 300))
            change_size = False
        display_backgrounds()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                # The user closes the window
                window_open = False
            elif event.type == pygame.MOUSEBUTTONUP:
                #  Return to main page
                rect = pygame.Rect((30, 25), (30, 30))
                if rect.collidepoint(event.pos):
                    if sound:
                        pygame.mixer.Sound.play(click)
                    main_window = True
                    backgrounds_window = False
                    change_size = True
                    break

                # Background selection
                position = [[20, 70], [240, 70], [460, 70]]
                for i in range(3):
                    rect = pygame.Rect((position[i][0], position[i][1]), (200, 200))
                    if rect.collidepoint(event.pos):
                        if sound:
                            pygame.mixer.Sound.play(click)
                        background = i
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
                                        play_ending_sound = True
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
                                        play_ending_sound = True
                                        add_time(time_end - time_ini)
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
                    main_window = True
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
        
        display_playing_elements(current_time)
        
        if background == 0:
            color = light_green
        elif background == 1:
            color = sea_blue
        else:
            color = dark_blue
        selected_movement.fill(color)

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
            if play_ending_sound:
                if sound:
                    if not_revealed == 0:
                        pygame.mixer.Sound.play(winning_sound)
                    else:
                        pygame.mixer.Sound.play(losing_sound)
                play_ending_sound = False
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
            if background == 0:
                color = light_brown
            elif background == 1:
                color = sea_blue
            else:
                color = light_blue
            pygame.draw.rect(window, color, pygame.Rect(position, (240, 50)),  0, 5)
            
            text = "Play again"
            font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 25)
            message = font.render(text, 7, white)
            window.blit(message, (window_base/2-80, window_height/2+70))
    
    pygame.display.flip()

pygame.quit()
