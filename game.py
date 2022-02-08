import random, sys, time
import pygame
from pygame.locals import * 
from pygame import mixer
from pause import * 
colors = [
    (37, 235, 11), 
    (160, 154, 143), 
    (139, 176, 186), 
    (57, 217, 227), 
    (82, 30, 24),
    (13, 216, 46),
    (198, 39, 57)
]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY  = (128,128, 128)

level = 1
lines_to_clear = 1


class Tetris:
    lines_cleared = 0
    score = 0 
    state = "start"
    field = []  
    HEIGHT = 0
    WIDTH = 0 
    startX = 100 
    startY = 50
    zoom = 20 
    figure = None
    
    def __init__(self, height, width):
        self.field = []
        self.figure = None 
        self.height = height 
        self.width = width

        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
    
    def create_figure(self):
        self.figure = Figure(3, 0)
    
    def intersects(self):
        intersects = False 
        for i in range(4):
            for j in range(4):
                if (i * 4) + j in self.figure.get_image():
                    if (i + self.figure.y) > (self.height - 1) or \
                        (j + self.figure.x) > (self.width - 1) or \
                        (j + self.figure.x) < 0 or \
                        self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersects = True 
        return intersects 
            
    def freeze_figure(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.get_image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()   
        self.create_figure()
        if self.intersects():
            self.gameover()
               
    def gameover(self):
        mixer.music.stop()
        mixer.Sound('sounds\\gameover.wav').play()
        self.state = "gameover"
                
    def break_lines(self):
        lines = 0 
        for i in range(0, self.height):
            zeros = 0 
            for j in range(1, self.width):
                if self.field[i][j] == 0:
                    zeros += 1
                
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        
        mixer.Sound('sounds\\figure.wav').play()
        self.score += lines ** 2
        self.lines_cleared += lines             
        self.check_level_up()
        
    def check_level_up(self):
        global level 
        global lines_to_clear 
        if self.lines_cleared >= level: 
            level += 1
            lines_to_clear = level 
            self.lines_cleared = 0 
            mixer.Sound('sounds\\levelup.wav').play()
            return True 
        else:
            lines_to_clear = level - self.lines_cleared 
            return False 
        
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1 
        self.freeze_figure()
        
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze_figure()
            
    def go_sideways(self, dx):
        previous_x = self.figure.x 
        self.figure.x += dx  
        if self.intersects():
            self.figure.x = previous_x  
    
    def rotate(self):
        previous_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = previous_rotation  


class Figure:

    figures = [
        [[4, 5, 6, 7], [1, 5, 9, 13]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], 
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 8, 9], [4, 5, 6, 10]],  
        [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],
        [[5, 6, 9, 10]], 
        [[1, 2, 4, 5], [0, 4, 5, 9], [5, 6, 8, 9], [1, 5, 6, 10]], 
        [[1, 2, 6, 7], [3, 6, 7, 10], [5, 6, 10, 11], [2, 5, 6, 9]] 
    ]
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.type = random.randint(0, (len(self.figures) - 1))
        self.color = random.randint(1, (len(colors) - 1))
        self.rotation = 0 
    
    def get_image(self):
        return self.figures[self.type][self.rotation]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % (len(self.figures[self.type])) 
        
class Game():
    def __init__(self):
        global level 
        global lines_to_clear 
        self.screen_height = 500
        self.screen_width = 400 
        self.game_height = 20 
        self.game_width = 10 
        self.pressing_down = False 
        self.gameover = False 
        self.counter = 0 
        self.fps = 30 
        self.background = pygame.image.load('images\\bg.jpg')
        self.background = pygame.transform.scale(self.background, (400, 500))

    def start(self):
        if not pause_menu():
            change_play()
        playing = True
        while playing:
            pygame.init()
            mixer.music.load('sounds\\background_music.mp3')
            mixer.music.play(-1)
            window = pygame.display.set_mode((self.screen_width, self.screen_height))
            clock = pygame.time.Clock()
            game = Tetris(self.game_height, self.game_width)
            icon = pygame.image.load('images\\icon.png')
            pygame.display.set_icon(icon)
            name = pygame.display.set_caption("Tetris with Python")
            running = True
            if not pause_menu():
                    playing = False 
                    
            while running:
                if not pause_menu():
                    running =  False               
                window.fill(WHITE)
                window.blit(self.background, (0,0))
                if game.figure is None:
                    game.create_figure()
                self.counter += 1 
                if self.counter > 100000:
                    self.counter = 0 
                
                if self.counter % (self.fps // level // 2) == 0 or self.pressing_down:
                    if game.state == "start":
                        game.go_down()
            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameover = True
                        pygame.quit() 
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            game.go_sideways(1)
                        if event.key == pygame.K_LEFT:
                            game.go_sideways(-1)
                        if event.key == pygame.K_UP:
                            game.rotate()
                        if event.key == pygame.K_DOWN:
                            self.pressing_down = True 
                        if event.key == pygame.K_SPACE:
                            game.go_space()
                        if event.key == pygame.K_ESCAPE:
                            if game.state == "gameover":
                                running = False
                                playing = False
                            else:    
                                pause()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.pressing_down = False 
                
                for i in range(game.height):
                    for j in range(game.width):
                        pygame.draw.rect(window, GREY, [game.startX + game.zoom * j, game.startY + game.zoom * i, game.zoom, game.zoom], 1) 
                        if game.field[i][j] > 0:
                            pygame.draw.rect(window, colors[game.field[i][j]], 
                                [game.startX + game.zoom * j, game.startY + game.zoom * i, game.zoom - 2, game.zoom - 1])
                            
                if game.figure is not None:
                    for i in range(4):
                        for j in range(4):
                            p = i * 4 + j
                            if p in game.figure.get_image():
                                pygame.draw.rect(window, colors[game.figure.color],
                                                [
                                                    game.startX + game.zoom * (j + game.figure.x) + 1,
                                                    game.startY + game.zoom * (i + game.figure.y) + 1,
                                                    game.zoom -2, 
                                                    game.zoom - 2
                                                ])

                font1 = pygame.font.SysFont('Comic Sans MS', 11, bold=True)
                text_score = font1.render("Score: " + str(game.score), True, BLACK)
                text_level = font1.render("Level: " + str(level), True, BLACK)
                text_lines_to_clear = font1.render("Lines to next level: " + str(lines_to_clear), True, BLACK)
                text_game_over1 = font1.render("Game Over", True, BLACK)
                text_game_over2 = font1.render("Press ESC", True, BLACK)
                
                window.blit(text_score, [100, 20]) 
                window.blit(text_lines_to_clear, [230, 20])
                window.blit(text_level, [250, 5])
                if game.check_level_up():
                    game()
                if game.state == "gameover":
                    window.blit(text_game_over1, [20, 220])
                    window.blit(text_game_over2, [20, 275])
                pygame.display.flip()
                clock.tick(self.fps)



        

    
    
                    
                    
                    
            