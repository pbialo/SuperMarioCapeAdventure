# Source File Name: A4_1_5.py
# Author's Name: Paul Bialo
# Date Last Modified: July 12, 2012
# Program Description: Help caped Mario collect coins while avoiding enemies!
# Revision History: Version 1.0 - Implementing Mario's flying animation and control with mouse
#                   Version 1.1 - Adding in coins for Mario to collect
#                   Version 1.2 - Adding in enemies for Mario to avoid
#                   Version 1.3 - Adding sound, collision, and the background
#                   Version 1.4 - Implementing score and lives; fixes to sprite updating in main
#                   Version 1.5 - Adding the introduction and gameover states; one-up implemented; scoring + difficulty updated
#                   Version 2.0 - Final touch-ups for launch

import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 480))

# The class for the player controlled Mario sprite
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/mario0.gif")
        self.image = self.image.convert()
        tranColor = self.image.get_at((1, 1))
        self.image.set_colorkey(tranColor)
        self.rect = self.image.get_rect()
        self.img = []
        
        self.loadPics()
        self.frame = 0
        self.delay = 8
        self.pause = self.delay
                   
        self.sndLoseLife = pygame.mixer.Sound("sound/loselife.ogg")           
        self.sndCoin = pygame.mixer.Sound("sound/coin.ogg") 
        self.sndOneup = pygame.mixer.Sound("sound/oneup.ogg")  

    # Mario's position is completely mouse controlled
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, mousey)
        
        # For some animation of Mario
        self.pause -= 1
        if self.pause <= 0:
            self.pause = self.delay
            
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            
            self.image = self.img[self.frame]

    # This is used to switch between the two images for Mario for the flying animation
    def loadPics(self):
        for i in range(2):
            imgName = "img/mario%d.gif" % i
            tmpImg = pygame.image.load(imgName)
            tmpImg.convert()
            tranColor = tmpImg.get_at((0, 0))
            tmpImg.set_colorkey(tranColor)
            self.img.append(tmpImg)                    

# The coin sprite, Mario attempts to collect these            
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/coin0.gif")
        self.image = self.image.convert()
        tranColor = self.image.get_at((1, 1))
        self.image.set_colorkey(tranColor)
        self.rect = self.image.get_rect()
        self.img = []
        self.reset()
        
        self.loadPics()
        self.frame = 0
        self.delay = 4
        self.pause = self.delay
        self.dx = 8
    
    # Coins start at the right of the screen at a random y value and move to the left    
    def update(self):
        self.rect.centerx -= self.dx
        
        # Animating the coin 
        self.pause -= 1
        if self.pause <= 0:
            self.pause = self.delay           
            self.frame += 1
            if self.frame > 3:
                self.frame = 0           
            self.image = self.img[self.frame]

    # When a coin reaches the left of the screen, it gets reset on the right
    def reset(self):
        self.rect.top = random.randrange(20, 460)
        self.rect.left = 640
            
    # This is used to switch between the spinning coin images
    def loadPics(self):
        for i in range(4):
            imgName = "img/coin%d.gif" % i
            tmpImg = pygame.image.load(imgName)
            tmpImg.convert()
            tranColor = tmpImg.get_at((1, 1))
            tmpImg.set_colorkey(tranColor)
            self.img.append(tmpImg)        

# Sprite for enemy; a large bullet that travels horizontally
class BanzaiBill(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/banzaibill.gif")
        self.image = self.image.convert()
        tranColor = self.image.get_at((1, 1))
        self.image.set_colorkey(tranColor)
        self.rect = self.image.get_rect()
        self.sndBill = pygame.mixer.Sound("sound/bill.wav")  
        self.reset()       
        
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
    
    def reset(self):
        self.rect.top = random.randrange(20, 396)
        self.rect.left = 660
        self.dx = random.randrange(8, 11)
        self.sndBill.play()

# Sprite for enemy; a small bullet that travels horizontally and fast     
class BulletBill(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bulletbill.gif")
        self.image = self.image.convert()
        tranColor = self.image.get_at((1, 1))
        self.image.set_colorkey(tranColor)
        self.rect = self.image.get_rect()
        self.sndBill = pygame.mixer.Sound("sound/bill.wav")  
        self.reset()

    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
    
    def reset(self):
        self.rect.top = random.randrange(20, 440)
        self.rect.left = 680
        self.dx = random.randrange(11, 14)        
        self.sndBill.play() 
        
# Sprite for enemy; a flying koopa that travels diagonally.        
class WingKoopa(pygame.sprite.Sprite):        
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/wingkoopa0.gif")
        self.image = self.image.convert()
        tranColor = self.image.get_at((1, 1))
        self.image.set_colorkey(tranColor)
        self.rect = self.image.get_rect()
        self.img = []
        self.loadPics()
        self.frame = 0
        self.delay = 8
        self.pause = self.delay
        self.reset()

    def update(self):
        self.rect.centerx -= self.dx
        self.rect.centery -= self.dy
        self.pause -= 1
        
        if self.rect.top < 0:
            self.dy = -self.dy
        if self.rect.bottom > 480:
            self.dy = -self.dy 
        if self.rect.right < 0:
            self.reset()

        # Animating the winged koopa
        if self.pause <= 0:
            self.pause = self.delay
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.img[self.frame]

    def reset(self):
        self.dy = 4
        self.rect.top = random.randrange(30, 420)
        self.rect.left = 640
        self.dx = random.randrange (5, 13)
        self.dy = random.randrange (8, 14)
            
    def loadPics(self):
        for i in range(2):
            imgName = "img/wingkoopa%d.gif" % i
            tmpImg = pygame.image.load(imgName)
            tmpImg.convert()
            tranColor = tmpImg.get_at((0, 0))
            tmpImg.set_colorkey(tranColor)
            self.img.append(tmpImg)      

# Sprite for one-up mushroom. Falls from the top of the screen
class OneUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/oneup.gif")
        self.image = self.image.convert()
        tranColor = self.image.get_at((1, 1))
        self.image.set_colorkey(tranColor)
        self.rect = self.image.get_rect()
        self.reset()       
        
    def update(self):
        self.rect.centerx -= 5
        self.rect.centery += 5
        if self.rect.top > 500:
            self.reset()
    
    def reset(self):
        self.rect.top = -500
        self.rect.left = random.randrange(400, 600)
            
# The background sprite that loops endlessly  
class Sky(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/background.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.dx = 4
        self.reset()
        
    def update(self):
        self.rect.left -= self.dx
        if self.rect.right <= 640:
            self.reset() 
    
    def reset(self):
        self.rect.left = 0
        
# The scoreboard sprite that keeps track of the player's score
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "Score: %d" % (self.score)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()        

# The lives sprite that keeps track of the player's lives
class Livesboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "Lives: %d" % (self.lives)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()    
        self.rect.right = 639
 
# Sprite used for instructions image at start of game 
class Instructions(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/instructions.gif")
        self.image = self.image.convert()
        tranColor = self.image.get_at((1, 1))
        self.image.set_colorkey(tranColor)
        self.rect = self.image.get_rect()

# Sprite used for gameover image
class GameoverScore(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/gameover.gif")
        self.image = self.image.convert()
        tranColor = self.image.get_at((1, 1))
        self.image.set_colorkey(tranColor)
        self.rect = self.image.get_rect()      
        
def game():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Super Mario Cape Adventure")
    
    # Playing the game music
    sndGame = pygame.mixer.Sound("sound/gamemusic.ogg")
    sndGame.play(-1)
        
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    # Adding the sprites
    coin = Coin()
    banzaibill1 = BanzaiBill()
    banzaibill2 = BanzaiBill()
    banzaibill3 = BanzaiBill()
    bulletbill1 = BulletBill()
    bulletbill2 = BulletBill()
    bulletbill3 = BulletBill()
    wingkoopa1 = WingKoopa()
    wingkoopa2 = WingKoopa()
    oneup = OneUp()
    mario = Mario()
    sky = Sky()
    scoreboard = Scoreboard()
    livesboard = Livesboard()
    
    # Grouping the sprites
    backgroundSprites = pygame.sprite.Group(sky)
    infoSprites = pygame.sprite.Group(scoreboard, livesboard)
    goodSprites = pygame.sprite.Group(mario, coin)
    enemySprites = pygame.sprite.Group(oneup, banzaibill1, banzaibill1, banzaibill2, bulletbill2, bulletbill3, bulletbill3, wingkoopa1, wingkoopa2)
    
    clock = pygame.time.Clock()
    gameOver = False
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        # Checking for collision with coin, add to score if so
        if mario.rect.colliderect(coin.rect):
            mario.sndCoin.play()
            coin.reset()
            scoreboard.score += 10
        
        # Lose score if a coin reaches the left of the screen and reset the coin
        if coin.rect.right <= 0:
            scoreboard.score -= 25
            coin.reset()

        # Checking for collision with one up, add to life and score if so
        if mario.rect.colliderect(oneup.rect):
            oneup.reset()
            livesboard.lives += 1
            scoreboard.score += 50
            mario.sndOneup.play()
            
        # Checking for collision with enemies, lose a life if so
        hitEnemies = pygame.sprite.spritecollide (mario, enemySprites, False)
        if hitEnemies:
            mario.sndLoseLife.play()
            livesboard.lives -= 1
            if livesboard.lives <= 0:
                gameOver = True
                keepGoing = False
            
            for theEnemy in hitEnemies:
                theEnemy.reset()
                
        # Updating the sprites, was having some problems so I split it up like so:
        backgroundSprites.update()
        goodSprites.update()
        enemySprites.update()
        infoSprites.update()
        backgroundSprites.draw(screen)
        goodSprites.draw(screen)
        enemySprites.draw(screen)
        infoSprites.draw(screen)
        
        pygame.display.flip()
    
    #return mouse cursor
    sndGame.stop()
    pygame.mouse.set_visible(True) 
    return scoreboard.score, gameOver

# The introduction screen    
def introduction():
    instructions = Instructions()
    sky = Sky()
    pygame.display.set_caption("Super Mario Cape Adventure")
    introductionSprites = pygame.sprite.Group(instructions, sky)
    
    # Introduction music
    pygame.mixer.init()
    sndIntro= pygame.mixer.Sound("sound/intromusic.ogg")
    sndIntro.play(-1)
    
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                startPlaying = True
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
                    
        introductionSprites.draw(screen)        
        introductionSprites.update()

        pygame.display.flip()

    sndIntro.stop()
    pygame.mouse.set_visible(True)
    return startPlaying
 
# The gameover screen 
def gameover(score):
    gameoverScore = GameoverScore()
    sky = Sky()
    pygame.display.set_caption("Super Mario Cape Adventure")
    skySprite = pygame.sprite.Group(sky)
    gameoverSprite = pygame.sprite.Group(gameoverScore)
    
    # Gameover music
    pygame.mixer.init()
    sndGameover= pygame.mixer.Sound("sound/gameover.ogg")
    sndGameover.play()
    
    # Label for score that will be blitted
    gameoverFont = pygame.font.SysFont(None, 50)
    gameoverScore = "%d" % score
    gameoverLabel = gameoverFont.render(gameoverScore, 1, (0, 0, 0))
    
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
                    
        skySprite.draw(screen)  
        gameoverSprite.draw(screen)  
        skySprite.update()        
        gameoverSprite.update()
        
        screen.blit(gameoverLabel, (390, 260))

        pygame.display.flip()

    sndGameover.stop()
    pygame.mouse.set_visible(True)
    return donePlaying
    
def main():
    donePlaying = False
    score = 0
    if introduction() == True:
        while not donePlaying:
            score, gameOver = game()
            if gameOver:
                donePlaying = gameover(score)
                  
                
if __name__ == "__main__":
    main()
    
    
