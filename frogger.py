print("Frogger")
# 1. The frog class
# 2. Car class
# 3. log class + water zone
#   a. move player with log
# 4. goal
# 5. timmer
# 6. score

import pygame, sys, random, math

def food_collection(meals,enemy):
    if len(meals) > 0:
        for meal in meals:
                    if meal != enemy:
                        if math.dist(enemy.rect.center, meal.rect.center) < enemy.radius+meal.radius:
                                return True, meal
    meal = 0
    return False, meal

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.color = "red"
        self.radius = 20
        self.image = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image,self.color, (self.radius,self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(10,790),random.randint(10,590)))

        self.deltax = random.choice([-1,1])
        self.deltay = random.choice([-1,1])
    
    def move(self):
        if self.rect.left <= -0 or self.rect.right >= 800:
            self.deltax *= -1
        if self.rect.top <= -100 or self.rect.bottom >= 600:
            self.deltay *= -1

        self.rect.centerx += self.deltax
        self.rect.centery += self.deltay  
    def grow(self):
        self.image = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image,self.color, (self.radius,self.radius), self.radius)

class Player(Enemy):
    def __init__(self):
        super().__init__()
        self.color = "green"
        self.radius = 40
        self.image = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image,self.color, (self.radius,self.radius), self.radius)
        self.rect = self.image.get_rect(center = (50,50))

    def move(self):
        x,y = self.rect.center
        mx,my = pygame.mouse.get_pos()
        distance=math.sqrt((mx-x)**2 + (my-y)**2)
        if distance != 0:
            self.rect.center = (x+(mx-x)/distance, y+(my-y)/distance)




pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Tutorial")

clock = pygame.time.Clock()
enemies = pygame.sprite.Group()
lives = pygame.sprite.Group()

for i in range(5):
    enemies.add(Enemy())
# Main game loop
BLUE = (0, 0, 255)
WHITE = "#FFFFFF"
running = True
player = Player()
lives.add(player)

while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    
    screen.fill(WHITE)
    enemies.draw(screen)
    lives.draw(screen)
    for enemy in enemies:
        enemy.move()
        colided, meal = food_collection(lives,enemy)
        if colided == True:
            player.kill()
        
            
        
        

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()