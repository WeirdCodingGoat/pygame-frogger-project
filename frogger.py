
# Play with the arrow keys!

# 1. The frog class
# 2. Car class
# 3. log class + water zone
#   -x- a. move player with log -x-
# 4. goal
# 5. timmer
# 6. score


import pygame, sys, random, math

def goal_check(goals):
    # Checks for all goals used and returns true if all are used.
    total=0
    for goal in goals:
        if goal.used == True:
            total+=1
    if total == len(goals):
        return True
    else:
        return False

def set_goals(start):
    goals = pygame.sprite.Group()
    
    goals.add(start)
    for i in range(6):
        goals.add(GoalBox((50,100),(150+(100*i),580)))
    return goals

def food_collection(meals,enemy):
    if len(meals) > 0:
        for meal in meals:
                    if meal != enemy:
                        if math.dist(enemy.rect.center, meal.rect.center) < 22.5: # random 12.5 for the player and a 10 for enimies
                                return True, meal
    meal = 0
    return False, meal

class GoalBox(pygame.sprite.Sprite):
    def __init__(self,dimensions,cordinates):
        super(GoalBox,self).__init__()
        self.color = "#107500"
        self.used = False
        self.image = pygame.Surface(dimensions)
        self.image.convert_alpha()
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center = cordinates)

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
 
    
    def move(self):
        if self.rect.right <= -15:
            self.rect = self.image.get_rect(center = (820,self.rect.centery))
        elif self.rect.left >= 840:
            self.rect = self.image.get_rect(center = (0,self.rect.centery))
            

        self.rect.centerx += self.deltax
        

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.index = 2
        self.files = ["frogger0.png","frogger1.png","frogger2.png","frogger3.png","hidden.png"]
        self.images = [pygame.image.load(filename).convert_alpha() for filename in self.files]
        self.image = self.images[self.index]
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center = (400,50))

    def move(self, deltax, deltay):
        if deltax < 0 or deltay<0:
            if self.rect.left <100:
                deltax = 0
            if self.rect.top <= 50:
                deltay = 0
        elif deltax > 0 or deltay > 0:
            if self.rect.right>700:
                deltax = 0
            if self.rect.bottom > 550:
                deltay = 0
       
        self.rect.centerx += deltax
        self.rect.centery += deltay

        
    def visible_update(self,visible):
        if visible == False:
            self.image = self.images[4]
        else:
            self.image = self.images[self.index]



pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Frogger")


clock = pygame.time.Clock()
enemies = pygame.sprite.Group()
lives = pygame.sprite.Group()
start=GoalBox((screen_width,80),(400,40))
start.used = True

goals = set_goals(start)
    

for i in range(7):
    enemies.add(Enemy(random.choice([20,780]),150+(i*50)))
# Main game loop

running = True
player = Player()
lives.add(player)
for i in range(3):
    lives.add(Enemy(20,20+(i*20)))

resume_time=0
score=0
laps=0
in_control=True
life_count=0
deaths=0

    
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False
        elif in_control == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0,-50)
                    player.image = player.images[0]
                    player.index=0
                    
                elif event.key == pygame.K_DOWN:
                    player.move(0,50)
                    player.image = player.images[2]
                    player.index=2
                    
                    if 9*5*laps+(player.rect.centery/50)*5>score:
                        score=9*5*laps+((player.rect.centery)/50)*5
                    
                elif event.key == pygame.K_LEFT:
                    player.move(-50,0)
                    player.image = player.images[3]
                    player.index=3
                    
                elif event.key == pygame.K_RIGHT:
                    player.move(50,0)
                    player.image = player.images[1]
                    player.index=1
                    
            if player.rect.centery == 550:
                
                for goal in goals:
                    if goal.used == False and player.rect.clip(goal):
                        laps+=1
                        in_control = False
                        goal.used = True
                        goal.image.fill("blue")

                        if goal_check(goals) == True:
                            resume_time=clock.get_time()+15
                            in_control=False
                            if resume_time>30:
                                resume_time=resume_time-30
                            

                        else:
                            player.rect.center = (400,50)
                            in_control=True
                            
                  
                        
        elif life_count == 3:
            if event.type == pygame.KEYDOWN:
                life_count=0
                laps=0
                goals = set_goals(start)
                for i in range(3):
                    lives.add(Enemy(20,20+(i*20)))
                player.visible_update(True)
    #if life_count == 3:
    
    #  ----- Add game over screen here ------
    
    if clock.get_time()+8 >= resume_time and clock.get_time()-8 <= resume_time and goal_check(goals):
        goals = set_goals(start)
        player.rect.center = (400,50)
        in_control=True
    # Fill the screen with a color (e.g., white)
    player.update()
    screen.fill("black")
    goals.draw(screen)
    enemies.draw(screen)
    lives.draw(screen)
    if pygame.font:
        font = pygame.font.Font(None, 32)
        text = font.render(str(score), True, (10, 10, 10))
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=10)
        screen.blit(text, textpos)
    
    for enemy in enemies:
        enemy.move()
        if life_count < 3:
            colided, meal = food_collection(lives,enemy)
            if colided == True:
            # animation?
                in_control = False
                player.visible_update(in_control)
                for sprite in lives:
                    if sprite != player and deaths == 0:
                        deaths +=1
                        life_count+=1
                        sprite.kill()
                        
                deaths=0
                player.rect.center = (400,50)
          #      while player.rect.center != (400,50):
           #         if player.rect.centerx > 400:
            #            player.move(-50,0)
             #       elif player.rect.centerx < 400:
              #          player.move(50,0)
               #     player.move(0,-50)
            if life_count<3:
                in_control = True
                player.visible_update(in_control)
     #   while life_count >2:
      #      if life_count > 3:
       #         pygame.display.flip()
        
        

        

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()

# Code written by Weirdo Goat. ;3

