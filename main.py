import pygame
from pygame.locals import *
import time
import random
import threading

SIZE = 40
BACKGROUND_COLOR = (50,180,100)
pygame.font.get_fonts()

class Snake:
    def __init__(self, parent_screen, moved):
        self.image = pygame.image.load("resources/Snake.jpeg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE* random.randint(1,23)
        self.y = SIZE * random.randint(1,18)
        self.moved = False
    def draw(self):
        self.show = True
        self.parent_screen.blit(self.image, (self.x, self.y))
    def move(self):
        self.x = SIZE* random.randint(1,23)
        self.y = SIZE * random.randint(1,18) 
        

class Border:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/border.jpeg").convert()
        self.parent_screen = parent_screen
        self.x = 0
        self.y = 0
    def draw(self):
        for i in range(0,1000,40):
            self.parent_screen.blit(self.image, (i,0))
            self.parent_screen.blit(self.image, (i,760))
        for j in range(0,800,40):
            self.parent_screen.blit(self.image, (0,j))
            self.parent_screen.blit(self.image, (960,j))
       
class Cookie:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/cookie.png").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = SIZE* random.randint(1,23)
        self.y = SIZE * random.randint(1,18)

class Chicken:
    def __init__(self, parent_screen, length, speed, egg):
        self.length = length
        self.parent_screen = parent_screen
        self.speed = speed
        self.egg = False
        self.block = pygame.image.load("resources/chicken-right.jpeg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
        self.block = pygame.image.load("resources/egg.png").convert()
        self.egg = True
        if self.length%3 == 0:
            self.speed -= 0.015
            sound = pygame.mixer.Sound("resources/SpeedUp.mp3")
            pygame.mixer.Sound.play(sound)
        into_chicken = threading.Thread(target=self.egg_to_chicken)
        into_chicken.start()
    def egg_to_chicken(self):
        time.sleep(1.5)
        self.egg = False
        if self.direction == 'right':
            self.block = pygame.image.load("resources/chicken-right.jpeg").convert()
        if self.direction == 'left':
            self.block = pygame.image.load("resources/chicken-left.jpeg").convert()
        

    def draw(self):
        for i in range(self.length):
           self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
    def move_left(self):
        self.direction = 'left'
        if self.egg == False:
            self.block = pygame.image.load("resources/chicken-left.jpeg").convert()
    
    def move_right(self):
        self.direction = 'right'
        if self.egg == False:
            self.block = pygame.image.load("resources/chicken-right.jpeg").convert()
    
    def move_up(self):
        self.direction ='up'
      
    def move_down(self):
        self.direction = 'down'
        
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Watch Out For The Snake")
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((1000,800)) 
        self.surface.fill(BACKGROUND_COLOR)
        self.chicken = Chicken(self.surface, 1, 0.3, False)
        self.cookie = Cookie(self.surface)
        self.border = Border(self.surface)
        self.snake = Snake(self.surface, False)
        
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.chicken.walk()
        self.cookie.draw()
        self.border.draw()
        self.display_score()
        self.snake.draw()
        pygame.display.flip()

        if self.snake.x == self.cookie.x and self.snake.y == self.cookie.y:
            self.cookie.move()

        if self.is_collision(self.chicken.x[0], self.chicken.y[0], self.cookie.x, self.cookie.y):
            sound = pygame.mixer.Sound("resources/eat.wav")
            pygame.mixer.Sound.play(sound)
            self.cookie.move()
            self.chicken.increase_length()
            self.snake.moved = False
        
        if self.chicken.length%4==0 and self.snake.moved == False:
            self.snake.move()
            self.snake.moved = True
            sound = pygame.mixer.Sound("resources/RattleSnake.mp3")
            pygame.mixer.Sound.play(sound)
            
        for i in range(3, self.chicken.length):
            if self.is_collision(self.chicken.x[0],self.chicken.y[0], self.chicken.x[i], self.chicken.y[i]):
                raise ValueError("Game over") 

        if (self.chicken.x[0] == 0) or (self.chicken.x[0] == 960) or (self.chicken.y[0] == 0) or (self.chicken.y[0] == 760):
            raise ValueError("Game Over")

        if self.is_collision(self.chicken.x[0], self.chicken.y[0], self.snake.x, self.snake.y):
            raise ValueError("Game over")
        
        
    
    def display_score(self):
        font = pygame.font.SysFont("San Francisco",40,True)
        score = font.render(f"Score: {self.chicken.length-1}", True, (255,255,255),(0,0,0))
        self.surface.blit(score, (800,5))

    def welcome_screen(self):
        bg = pygame.image.load("resources/welcomeTexture.jpg")
        self.surface.blit(bg, (0,0))
        font = pygame.font.SysFont("San Francisco", 40)
        line1 = font.render("Welcome to Watch Out For The Snake!", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("Eat the cookies, stay away from the snake.", True, (255,255,255))
        self.surface.blit(line2,(200,350))
        line3 = font.render("Press ENTER to start the game.", True, (255,255,255))
        self.surface.blit(line3,(200,400))
        pygame.display.flip()
        sound = pygame.mixer.Sound("resources/crow.mp3")
        pygame.mixer.Sound.play(sound)
        self.play_background_music()

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("San Francisco", 40)
        line1 = font.render(f"Game over! Your score is {self.chicken.length-1}", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("Press Enter to start another game. Press Escape to exit.", True, (255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()
    
    def reset(self):
        self.chicken = Chicken(self.surface, 1, 0.3, False)
        self.cookie = Cookie(self.surface)

    def run(self):
        running = True
        pause = True
        welcome_screen = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.play(-1)

                    
                    if not pause:
                        if event.key == K_UP:
                            self.chicken.move_up()
                        if event.key == K_DOWN:
                            self.chicken.move_down()
                        if event.key == K_LEFT:
                            self.chicken.move_left()
                        if event.key == K_RIGHT:
                            self.chicken.move_right()
                elif event.type == QUIT:
                    running = False
            try: 
                if not pause:
                    self.play()

                if welcome_screen:
                    self.welcome_screen()
                    welcome_screen = False
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_RETURN:
                             pause = False
                
                
            except ValueError:
                self.show_game_over()
                sound = pygame.mixer.Sound("resources/Oh-no.mp3")
                pygame.mixer.Sound.play(sound)
                pause = True
                self.reset()

            time.sleep(self.chicken.speed)

if __name__ == "__main__":
    game = Game()
    game.run()
    

