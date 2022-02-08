import pygame, sys, time
from pygame import mixer
from button import Button
from game import Game
pygame.init()
#14,6h
SCREEN = pygame.display.set_mode((400, 500))
WHITE = (255, 255, 255)
NAVY  = (0,0,128)
icon = pygame.image.load('images\\icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Tetris with Python")
menu_image = pygame.image.load('images\\menu_image.jpg')
menu_image = pygame.transform.scale(menu_image, (400, 500))



def get_font(size): 
    return pygame.font.Font("images\\font.ttf", size)

def main_menu():
    mixer.music.stop()
    mixer.music.load('sounds\\menu_music.mp3')
    mixer.music.play(-1)
    while True:
        SCREEN.blit(menu_image, (0,0))
        
        mouse_pos = pygame.mouse.get_pos()
        
        menu_text = get_font(45).render("Main Menu", True, "Red")
        menu_rect = menu_text.get_rect(center=(200, 50))
        
        PLAY_BUTTON = Button(image=None, pos=(200, 230), text_input="START",
                             font=get_font(45), base_color="#191970", hovering_color=NAVY)
        #OPTIONS_BUTTON = Button(image=None, pos=(250, 280), text_input="OPTIONS", font=get_font(40),
            #base_color="#191970", hovering_color=NAVY)  #not using options yet.
        QUIT_BUTTON = Button(image=None, pos=(200, 390), text_input="QUIT",
            font=get_font(45), base_color="#191970", hovering_color=NAVY)

        SCREEN.blit(menu_text, menu_rect)
        
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(mouse_pos)
            button.update(SCREEN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse_pos):
                    play()
                #if OPTIONS_BUTTON.checkForInput(mouse_pos): #not using options yet.
                if QUIT_BUTTON.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def play():
    g = Game()
    playing = True
    mixer.music.stop()
    while playing:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        PLAY_TEXT = get_font(40).render("Commands:", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(200, 90))
        ESPACE_TEXT = get_font(20).render("Space: Go down", True, "White")  
        ESPACE_RECT = ESPACE_TEXT.get_rect(center=(200, 140))
        SIDE_ARROWS = get_font(13).render("Side arrows: move to left/right", True, "White")  
        SIDE_RECT = SIDE_ARROWS.get_rect(center=(200, 180))
        UP_ARROW = get_font(20).render("Up arrow: Rotate", True, "White") 
        UP_RECT = UP_ARROW.get_rect(center=(200, 220)) 
        DOWN_ARROW = get_font(15).render("Down arrow: Falls faster", True, "White") 
        DOWN_RECT = DOWN_ARROW.get_rect(center=(200, 260))  
        lst  = [[PLAY_TEXT, PLAY_RECT], [ESPACE_TEXT, ESPACE_RECT], [SIDE_ARROWS, SIDE_RECT],
                [UP_ARROW, UP_RECT], [DOWN_ARROW, DOWN_RECT]]                              
        for i in lst:
            SCREEN.blit(i[0], i[1])

        pygame.display.update()
        time.sleep(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
           
        g.start()
        pygame.display.update()
        main_menu()
        

if __name__ == '__main__':
    main_menu()