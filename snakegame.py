import pygame
import random
import time

#initialization
snake_speed = 10
w_x = 720
w_y = 480
pygame.init()
fps = pygame.time.Clock()
score = 0
game_w = pygame.display.set_mode((w_x,w_y))
pygame.display.set_caption("Py-Move.Eat.Repeat")
spos = [100,220]         #-->snake head position
sbody = [[100,220],[90,220],[80,220],[70,220]]
fpos = [random.randrange(1,(w_x//10))*10,random.randrange(1,(w_y//10))*10]
fspawn = True
direction = 'r'
pressed_key = direction
started = False

#images
apple=pygame.image.load(r"C:\\Users\Gaurav\Desktop\py4e\Py-Move.Eat.Repeat\new\\apple.png")
food=pygame.transform.scale(apple, (15,15))

#sound
crunch=pygame.mixer.Sound(r"C:\\Users\Gaurav\Desktop\py4e\Py-Move.Eat.Repeat\new\\Crunch.mp3")
gameoversound=pygame.mixer.Sound(r"C:\\Users\Gaurav\Desktop\py4e\Py-Move.Eat.Repeat\new\\end.mp3")

def restart():
    global spos, sbody, fpos, fspawn, snake_speed, score
    score=0
    snake_speed = 10
    spos = [100,220]         #-->snake head position
    sbody = [[100,220],[90,220],[80,220],[70,220]]
    fpos = [random.randrange(1,(w_x//10))*10,random.randrange(1,(w_y//10))*10]
    direction = 'r'
    pressed_key=direction
    fspawn = True
    pygame.display.update()
    snake(pressed_key)

def game_over():
    global pressed_key
    print("go")
    gameoversound.play()
    my_font = pygame.font.SysFont('LUCIDACONSOLE', 50)
    game_over_surface = my_font.render('GAME OVER', True, pygame.Color(10,10,10))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (w_x/2-10, w_y/4-50)
    game_w.blit(game_over_surface, game_over_rect)
    pygame.display.update()
    my_font2 = pygame.font.SysFont('comicsansms', 40)
    score_surface = my_font2.render('Your score is: ' + str(score), True, pygame.Color(10,10,10))
    score_rect = score_surface.get_rect()
    score_rect.midtop = (w_x/2-20, w_y/4+50)
    game_w.blit(score_surface, score_rect)
    pygame.display.flip()
    my_font3=pygame.font.SysFont("consolas", 30)
    replay_surface=my_font3.render("Press Enter key to replay", True, pygame.Color(0,0,0))
    quitsurface=my_font3.render("Press Backspace key to quit", True, pygame.Color(0,0,0))
    quit_rect=quitsurface.get_rect(topleft=(100, 280))
    replay_rect=replay_surface.get_rect(topleft=(110, 320))
    game_w.blits(blit_sequence=((replay_surface, replay_rect), (quitsurface, quit_rect)))
    pygame.display.update()
    pygame.time.wait(5000)
    restartvariable=False
    main_loopbreaker=False
    for e in pygame.event.get():
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_RETURN:
                restartvariable=True
                break
            elif e.type==pygame.K_BACKSPACE:
                main_loopbreaker==True
                pygame.quit()
        
    if restartvariable==True:
        restart()
    else:
        main_loopbreaker==True
        quit()
    restart()

def getkey(newevent):
    global pressed_key, current_direction
    if newevent.type==pygame.KEYDOWN or newevent.type==pygame.KEYUP:
        if newevent.scancode == 82:
            change_to = 'u'
        elif newevent.scancode == 81:
            change_to = 'd'
        elif newevent.scancode == 80:
            change_to = 'l'
        elif newevent.scancode == 79:
            change_to = 'r'
        else:
            change_to=current_direction
    else:
        change_to=pressed_key
    return change_to

def snake(change):
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
    pygame.event.set_blocked(pygame.MOUSEWHEEL)
    global direction, spos, score, sbody, fspawn, fpos, snake_speed, current_direction
    #no 2 keys usage and don't move reverse
    if change == 'u' and direction != 'd':
        direction = 'u'
    elif change == 'd' and direction != 'u':
        direction = 'd'
    elif change == 'l' and direction != 'r':
        direction = 'l'
    elif change == 'r' and direction != 'l':
        direction = 'r'
    current_direction=direction
    # Movement
    if direction == 'u':
        spos[1] -= 10
    elif direction == 'd':
        spos[1] += 10
    elif direction == 'l':
        spos[0] -= 10
    elif direction == 'r':
        spos[0] += 10 
    # Snake body growth : if they overlap then score+10
    sbody.insert(0, list(spos))
    if spos[0] in range(fpos[0], fpos[0]+15) and spos[1] in range(fpos[1], fpos[1]+15):
        score += 10
        snake_speed+=1
        crunch.play()
        fspawn = False
        food_generator()
    else:
        sbody.pop()
    # Game Over conditions
    if spos[0] < 0 or spos[0] > w_x-10 or spos[1]< 0 or spos[1] > w_y-10:
        snake_speed = 10
        spos = [100,220]         #-->snake head position
        sbody = [[100,220],[90,220],[80,220],[70,220]]
        fpos = [random.randrange(1,(w_x//10))*10,random.randrange(1,(w_y//10))*10]
        direction = 'r'
        pressed_key=direction
        fspawn = True
        game_over()
    # Touching itzself
    for block in sbody[1:]:
        if spos[0] == block[0] and spos[1] == block[1]:
            snake_speed = 10
            spos = [100,220]         #-->snake head position
            sbody = [[100,220],[90,220],[80,220],[70,220]]
            fpos = [random.randrange(1,(w_x//10))*10,random.randrange(1,(w_y//10))*10]
            direction = 'r'
            pressed_key=direction
            fspawn = True
            print("snake")
            game_over()
            break
    add_to_screen()
    food_generator()
    pygame.display.update()
    fps.tick(snake_speed)  

def food_generator():
    global fspawn, fpos, sbody
    if not fspawn:
        while True:
            fpos = [random.randrange(1, (w_x//10)-2) * 10,
                            random.randrange(1, (w_y//10)-2) * 10]
            if fpos not in sbody:
                break
    game_w.blit(food, pygame.Rect(fpos[0], fpos[1], 15,15))
    fspawn = True

def add_to_screen():
    game_w.fill(pygame.Color(157, 255, 92))
    for pos in sbody:
        pygame.draw.rect(game_w,pygame.Color(0,0,255), pygame.Rect(pos[0], pos[1], 13, 13),border_radius=6)    
    pygame.display.update()

def main():
    #this is the main function
    global snake_speed
    close=False
    while not close:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                close=True
           
            else:
                pressed_key=getkey(event)
         if main_loopbreaker=True:
             pygame.quit()
             break
        snake(pressed_key)
main()

""" a function that returns the key that was pressed
pass that as argument to snake()
then run snake() outside the for loop in main()

Now, to get enter key before starting:
 in game over,
 add condition
 enter key - run snake
 quit - Quit
 else - sleep screen


def start_page():
    global started, key
    if started==False:
        welcome_msg=pygame.font.SysFont("lucidaconsole", 30, bold=True)
        start=welcome_msg.render("PRESS ENTER KEY TO START", True, (255, 255, 255))
        start_rect=start.get_rect()
        game_w.blit(start, start_rect)
        pygame.display.update()
        key=getkey(event) """
