print("Frogger")
# 1. The frog class
# 2. Car class
# 3. log class + water zone
#   -x- a. move player with log -x-
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
    def __init__(self,x,y):
        super(Enemy,self).__init__()
        self.color = "red"
        self.radius = 10
        self.image = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image,self.color, (self.radius,self.radius), self.radius)
        self.rect = self.image.get_rect(center = (x,y))
        
           #     random.choice([20,780]),random.randint(10,590))
        self.deltax = (random.choice([5,10,15]))*(random.choice([-1,1]))
        print(self.deltax,y)
    
    def move(self):
        if self.rect.right <= -15:
            self.rect = self.image.get_rect(center = (820,self.rect.centery))
        elif self.rect.left >= 840:
            self.rect = self.image.get_rect(center = (0,self.rect.centery))
            

        self.rect.centerx += self.deltax
        

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.color = "green"
        self.radius = 20
        self.image = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image,self.color, (self.radius,self.radius), self.radius)
        self.rect = self.image.get_rect(center = (400,50))

    def move(self, deltax, deltay):
        if deltax < 0 or deltay<0:
            if self.rect.left <100:
                deltax = 0
            if self.rect.top <= 50:
                deltay = 0
        elif deltax > 0 or deltay > 0:
            if self.rect.right>1100:
                deltax = 0
            if self.rect.bottom > 550:
                deltay = 0
       
        self.rect.centerx += deltax
        self.rect.centery += deltay
        print("\nDelta",deltax,deltay,"Pos",self.rect.center)
        
    def visible_update(self,visible):
        if visible == False:
            pygame.draw.circle(self.image,(0,0,0,0), (self.radius,self.radius), self.radius)
        else:
            pygame.draw.circle(self.image,self.color, (self.radius,self.radius), self.radius)



pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Frogger")

clock = pygame.time.Clock()
enemies = pygame.sprite.Group()
lives = pygame.sprite.Group()

for i in range(7):
    enemies.add(Enemy(random.choice([20,780]),150+(i*50)))
# Main game loop

running = True
player = Player()
lives.add(player)
in_control=True
life_count=0
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame   .KEYDOWN:
            if in_control == True:
                if event.key == pygame.K_UP:
                    player.move(0,-50)
                elif event.key == pygame.K_DOWN:
                    player.move(0,50)
                elif event.key == pygame.K_LEFT:
                    player.move(-50,0)
                elif event.key == pygame.K_RIGHT:
                    player.move(50,0)

    # Fill the screen with a color (e.g., white)
    player.update()
    screen.fill("black")
    enemies.draw(screen)
    lives.draw(screen)
    for enemy in enemies:
        enemy.move()
        if life_count < 3:
            colided, meal = food_collection(lives,enemy)
            if colided == True:
            # animation?
                in_control = False
                player.visible_update(in_control)
                player.rect.center = (400,50)
          #      while player.rect.center != (400,50):
           #         if player.rect.centerx > 400:
            #            player.move(-50,0)
             #       elif player.rect.centerx < 400:
              #          player.move(50,0)
               #     player.move(0,-50)
                in_control = True
                player.visible_update(in_control)
        
        
        
        

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
