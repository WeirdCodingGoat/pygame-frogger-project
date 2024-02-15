import pygame, sys, random, math
from pygame.math import Vector2
def draw_grid():
    #Horizontal
    for y in range(0,800,50):
        pygame.draw.line(screen, (200,200,200,50), (0, y), (1400, y))
    #Vertical
    for x in range(0,1400,50):
        pygame.draw.line(screen, (200,200,200,50), (x, 0), (x, 800))

class Square(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super(Square, self).__init__()
        self.image = pygame.Surface((100,100), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect(center = (x,y))
    
    def move(self, deltax, deltay):
        if deltax < 0 or deltay<0:
            if self.rect.left <100:
                deltax = 0
            if self.rect.top <= 50:
                deltay = 0
        elif deltax > 0 or deltay > 0:
            if self.rect.right>1100:
                deltax = 0
            if self.rect.bottom > 500:
                deltay = 0
       
        self.rect.centerx += deltax
        self.rect.centery += deltay
        print("\nDelta",deltax,deltay,"Pos",self.rect.center)




# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("frog test")

# Create clock to later control frame rate
clock = pygame.time.Clock()

sq1 = Square(650,550,"red")
squares = pygame.sprite.Group()
squares.add(sq1)


# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sq1.move(0,-100)
            elif event.key == pygame.K_DOWN:
                sq1.move(0,100)
            elif event.key == pygame.K_LEFT:
                sq1.move(-100,0)
            elif event.key == pygame.K_RIGHT:
                sq1.move(100,0)
        
        #while event.type == pygame.KEYDOWN:
         #   if event.key == pygame.K_UP:
          #      sq1.move(0,-100)
           # elif event.key == pygame.K_DOWN:
            #    sq1.move(0,100)
           # elif event.key == pygame.K_LEFT:
            #    sq1.move(-100,0)
           # elif event.key == pygame.K_RIGHT:
            #    sq1.move(100,0)
    



    screen.fill((0,0,0))
    draw_grid()

    sq1.update()


    squares.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()






