import pygame
import os
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dodge!')

FPS = 60
SHIP_WIDTH, SHIP_HEIGHT = 55, 40
WHITE = [255, 255, 255]
VEL = 5
OBSTACLE_VEL = 8
OBSTACLE_WIDTH = 15
OBSTACLE_HEIGHT = 10
MAX_OBSTACLES = 10
MAX_BOUNCE = 8
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
HIGHSCORE_FONT = pygame.font.SysFont('comicsans', 30)
CURRENTSCORE_FONT = pygame.font.SysFont('comicsans', 30)

OBSTACLE_GENERATE = pygame.USEREVENT + 1

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets','bg5.jpg')), (WIDTH, HEIGHT))

# OBSTACLE_IMAGE = pygame.image.load(os.path.join('assets/obstacles','Hurricane.png'))
# OBSTACLE = pygame.transform.scale(OBSTACLE_IMAGE, (OBSTACLE_WIDTH,OBSTACLE_HEIGHT))

class Ship(pygame.sprite.Sprite):
    def __init__(self, velocity=[5,5]):
        pygame.sprite.Sprite.__init__(self)
        self.img_path = os.path.join('assets/ships','3.png')
        self.image = pygame.transform.scale(pygame.image.load(self.img_path), (SHIP_WIDTH, SHIP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.velocity = velocity

    def handle_keys(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and self.rect.x - self.velocity[0] > 0: # LEFT
            self.rect.x -= self.velocity[0]
        if keys_pressed[pygame.K_RIGHT] and self.rect.x + self.velocity[0] + self.rect.width < WIDTH: # RIGHT
            self.rect.x += self.velocity[0]
        if keys_pressed[pygame.K_UP] and self.rect.y > 10: # UP
            self.rect.y -= self.velocity[1]
        if keys_pressed[pygame.K_DOWN] and self.rect.y + self.rect.height < HEIGHT - 5: # DOWN
            self.rect.y += self.velocity[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # def change_ship(self, score, ship):
    #     if score <= 5:
    #         ship.img_path = os.path.join('assets/ships','1.png')
    #     if score <= 10:
    #         ship.img_path = os.path.join('assets/ships','2.png')
    #     if score <= 15:
    #         ship.img_path = os.path.join('assets/ships','3.png')


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('assets/obstacles','Hurricane.png')), (OBSTACLE_WIDTH,OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(100, WIDTH-100),random.randrange(100,HEIGHT-100))
        self.velocity = [4,4]
        self.bounce = 0

    def move(self, bounce):
        if ((self.rect.x <= 0) or (self.rect.x >= WIDTH - self.rect.width)) and self.bounce <= MAX_BOUNCE:
            self.velocity[0] *= -1
            self.bounce += 1

        if ((self.rect.y <= 0) or (self.rect.y > HEIGHT - self.rect.height)) and self.bounce <= MAX_BOUNCE:
            self.velocity[1] *= -1
            self.bounce += 1

        self.rect.x = self.rect.x + self.velocity[0]
        self.rect.y = self.rect.y + self.velocity[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(1000)

def draw_current_score(text):
    draw_text = CURRENTSCORE_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (10,10+draw_text.get_height()))
    pygame.display.update()


def draw_highscore(text):
    draw_text = HIGHSCORE_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (10,10))
    pygame.display.update()


def change_speed(score, obstacle):
    if score <= 5:
        obstacle.velocity = [3,3]
    if score <= 10:
        obstacle.velocity = [5,5]
    if score <= 15:
        obstacle.velocity = [7,7]

def writeHighScore(fileName: str, score: int) -> None:
    '''Writes a score to the file'''
    file = open(fileName, "w")
    file.write(str(score))
    file.close()

def readHighScore(fileName: str) -> int:
    '''Reads the previous high score from a file'''
    try:
        file = open(fileName, "r")
        data = int(file.read())
        file.close()

    except FileNotFoundError:
        return 0

    return data


def main():

    obstacle_lst = []
    score = 0
    score_lst = [readHighScore(".highScore.txt")]
    highestScore = max(score_lst)

    all_sprites = pygame.sprite.Group()
    ship = Ship()
    all_sprites.add(ship)

    # GAME LOOP
    clock = pygame.time.Clock()
    pygame.time.set_timer(OBSTACLE_GENERATE, 1500)
    run = True
    bounce = 0
    while run:
        clock.tick(FPS)
        # ship.change_ship(score, ship)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == OBSTACLE_GENERATE:    # IF THIS USEREVENT IS ON EVENT QUEUE,
                obstacle = Obstacle()              # SPAWN AN OBSTACLE

                obstacle_lst.append(obstacle)
                score += 1
                
        WIN.blit(SPACE_BACKGROUND,(0,0))

        for item in obstacle_lst:
            item.move(bounce)
            item.draw(WIN)
            if ship.rect.colliderect(item.rect):
                if score > highestScore:
                    writeHighScore(".highScore.txt", score)
                score_lst.append(score)
                obstacle_lst.clear()
                draw_winner('Score: '+ str(score))
                score = 0
                break

        ship.draw(WIN)
        ship.handle_keys()
        
        draw_highscore('Highscore: ' + str(max(score_lst)))
        draw_current_score('Current Score: ' + str(score))

        pygame.display.update()

    main()

if __name__ == '__main__':
    main()
