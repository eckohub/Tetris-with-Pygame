from button import Button
import pygame, sys


NAVY  = (0,0,128)
SCREEN = pygame.display.set_mode((300, 250))
menu_image = pygame.image.load('images\\pause.png')
menu_image = pygame.transform.scale(menu_image, (300, 250))

def get_font(size): 
    return pygame.font.Font("images\\font.ttf", size)

play = True

def change_play():
    global play
    if play:
        play = False
    else:
        play = True

def pause_menu():
    return play

def pause():
    global play
    pygame.mixer.music.pause()
    paused = True
    while paused:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(menu_image, (50,100))
        
        RESUME_BUTTON = Button(image=None, pos=(200, 200), text_input="RESUME",
                                font=get_font(20), base_color="#191970", hovering_color=NAVY)
        MAIN_MENU = Button(image=None, pos=(200, 250), text_input="MAIN MENU", font=get_font(20),
            base_color="#191970", hovering_color=NAVY)
        QUIT_BUTTON = Button(image=None, pos=(200, 300), text_input="QUIT",
            font=get_font(20), base_color="#191970", hovering_color=NAVY)

        
        for button in [RESUME_BUTTON, MAIN_MENU, QUIT_BUTTON]:
            button.changeColor(mouse_pos)
            button.update(SCREEN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()
                    paused = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(mouse_pos):
                    pygame.mixer.music.unpause()
                    paused = False
                    
                if MAIN_MENU.checkForInput(mouse_pos):
                    change_play()
                    paused = False
                
                if QUIT_BUTTON.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
   