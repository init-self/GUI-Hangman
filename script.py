"""

"""

import os
import pygame
import math
import random


pygame.init() # necessary step

#constants
WIDTH, HEIGHT = 800, 500
RADIUS = 20
GAP = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHARCOAL = (38, 70, 83)
BUTTON_FONT = pygame.font.SysFont(name="Calibri", size= 30)
DISPLAYWORD_FONT = pygame.font.SysFont(name= "ComicSans", size=40)
END_MSG = pygame.font.SysFont(name= "ComicSans", size=100)
SMALL_TEXT = pygame.font.SysFont(name= "ComicSans", size= 20)

# initialising the screen of pygame
window = pygame.display.set_mode((WIDTH, HEIGHT))


# title of the screen
title = pygame.display.set_caption("Hangman Game")

# Filepath of images and their surfaces
images = [0,1,2,3,4,5,6] # numbers of the hangman images
image_surfaces = [] # pygame generated list of all hangaman image's surface.



# game variables
status_code = 0 # the number of the image to be displayed while playing i.e if status_code is 0, '0.png' will be displayed
letters = []
words = "developer, hero, computer, science, user, artist, checker, blackboard, whiteboard".upper().split(sep= ",")
word = random.choice(words).strip()
guessed = []    

startx = round((WIDTH - (RADIUS*2 + GAP)*13) / 2 )
starty = 400
A =  65

for i in range(26):
    x = startx + 2*GAP + ((RADIUS*2 + GAP) * (i % 13))
    y = starty + ((RADIUS*2 + GAP) * (i // 13) )
    letters.append([x, y, chr(A + i), True])


FPS = 60 # frames per second
clock = pygame.time.Clock()

run = True


# -------------------------------------------------------------------------------------------------    

def draw_images(enable: bool):
    if enable:
        for i in images:
            image = pygame.image.load("images/" + str(i) + ".png")
            image_surfaces.append(image)



def draw_blanks(enable: bool):
    if enable:
        # Blanks in the screen
        displayWord = "" # how the word would be displayed on screen - with blanks
        for ltr in word:
            if ltr in guessed:
                displayWord += ltr + " "
            else:
                displayWord += "_ "
        wrd = DISPLAYWORD_FONT.render(displayWord, 1, BLACK)
        window.blit(source= wrd, dest= (400, 150))


def draw(enable: bool):
    if enable:
        window.fill(WHITE)

        draw_images(True) # hangman images
        draw_blanks(True) # word blanks
        draw_buttons(True) # character buttons


def draw_buttons(visibility: bool):
    # drawing buttons
    if visibility:
        for letter in letters:
            x, y, character, visible = letter
            if visible:
                pygame.draw.circle(surface= window, color= CHARCOAL, center= (x,y), radius= RADIUS, width= 3)
                text = BUTTON_FONT.render(character, 1, CHARCOAL)  
                window.blit(source= text, dest= (x - (text.get_width()/2), y - (text.get_height()/2) ) ) # rendering the letter on screen - drawing on the screen


    window.blit(source= image_surfaces[status_code], dest= (100, 36))
    pygame.display.update()

    
# ---------------------------------------------------------------------------------------------

# The Original game loop
while run:
    clock.tick(FPS) # clock will tick at FPS speed
    
    for  event in pygame.event.get():
        # first event to check
        if event.type == pygame.QUIT: # if user clicks the cross [upper right hand corner] on the window
            run = False
            continue
        
        draw(True)

        # mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, character, visible = letter
                if visible:
                    dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                    if dis < RADIUS:
                        letter[3] = False
                        guessed.append(character.upper())
                        if character not in word:
                            status_code += 1
    
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
    if won:
        draw_buttons(False)
        window.fill(WHITE)
        text = DISPLAYWORD_FONT.render("You Won!", 1, BLACK)
        window.blit(source= text, dest= ((WIDTH/2 - text.get_width()/2), (HEIGHT/2 - text.get_height()/2) ))
        pygame.display.update()
        pygame.time.delay(3000) # after 3 seconds window will close
        break
    elif status_code == 6:
        window.fill(WHITE)
        text = END_MSG.render("You Lost!", 1, BLACK)
        window.blit(source= text, dest= ( (WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2 ))
        small_text = SMALL_TEXT.render("Better luck next time...", 1, BLACK)
        window.blit(source= small_text, dest= ((WIDTH - small_text.get_width())/2, (HEIGHT - small_text.get_height())/2 + 65))
        pygame.display.update()
        pygame.time.delay(3000) # after 3 seconds window will close
        break




pygame.quit() # close the window