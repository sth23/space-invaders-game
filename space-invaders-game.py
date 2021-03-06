from ggame import App, RectangleAsset, PolygonAsset, CircleAsset, LineAsset, ImageAsset, Frame, Sprite, LineStyle, Color
import math
import random

# Colors & lines
red = Color(0xff0000, 1.0)
orange = Color(0xffa500, 1.0)
yellow = Color(0xffff00, 1.0)
green = Color(0x00ff00, 1.0)
blue = Color(0x0000ff, 1.0)
purple = Color(0x800080, 1.0)
black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)
gray = Color(0x888888, 0.5)
noline = LineStyle(0, black)
whiteline = LineStyle(1, white)
blackline = LineStyle(1, black)

class Barrier(Sprite):
    square = RectangleAsset(15, 15, noline, black)
    
    def __init__(self, position):
        super().__init__(Barrier.square, position)
        
class Bullet(Sprite):
    rect = RectangleAsset(4, 20, noline, black)
    
    def __init__(self, position, direction):
        super().__init__(Bullet.rect, position)
        self.speed = 5
        self.vy = self.speed * direction
        
    def step(self):
        self.y += self.vy
        
class Invader(Sprite):
    rect = RectangleAsset(15, 15, noline, black)
    
    def __init__(self, position):
        super().__init__(Invader.rect, position)
        self.rotation = math.pi / 4
        self.speed = 2.5
        self.vx = 0
        self.vy = 0
        
    def shoot(self):
        Bullet((self.x + 7.5, self.y + 15), 1)
        
    def step(self):
        self.x += self.vx
        self.y += self.vy
        
        if random.randint(0,500) == 0:
            self.shoot()
class Ship(Sprite):
    ship = PolygonAsset([(0,30), (15,0), (30,30), (15,15)], noline, black)
    
    def __init__(self, position, width):
        super().__init__(Ship.ship, position)
        self.gamewidth = width
        self.speed = 5
        self.vx = 0
        self.shootcooldown = 10
        self.count = 0
        
        SpaceInvadersGame.listenKeyEvent("keydown", "space", self.shoot)

        SpaceInvadersGame.listenKeyEvent("keydown", "right arrow", self.moveRightOn)
        SpaceInvadersGame.listenKeyEvent("keyup", "right arrow", self.moveRightOff)
        SpaceInvadersGame.listenKeyEvent("keydown", "left arrow", self.moveLeftOn)
        SpaceInvadersGame.listenKeyEvent("keyup", "left arrow", self.moveLeftOff)

    def shoot(self, event):
        if self.count > self.shootcooldown:
            Bullet((self.x + 13, self.y - 20), -1)
            self.count = 0

    def moveRightOn(self, event):
        self.vx = self.speed
        
    def moveRightOff(self, event):
        self.vx = 0
        
    def moveLeftOn(self, event):
        self.vx = -self.speed
        
    def moveLeftOff(self, event):
        self.vx = 0

    def step(self):
        self.x += self.vx
        self.count += 1
        
class SpaceInvadersGame(App):
    def __init__(self):
        super().__init__()
        
        self.player1 = Ship((self.width / 2, self.height - 40), self.width)
        
        self.numbarriers = self.width // (2 * 120)
        self.barriergap = (self.width - 120 * self.numbarriers) / self.numbarriers
        self.createBarriers()
        self.createInvaders()
        
    def createBarriers(self):
        for x in range(0, 8):
            for y in range(0,4):
                for z in range(0,self.numbarriers):
                    Barrier((self.barriergap / 2 + (self.barriergap + 120) * z + x * 15, self.height - 150 + y * 15))
                    
    def createInvaders(self):
        for y in range(0, 5):
            for x in range(0,10):
                Invader((self.width / 8 + (self.width * 3 / 4) * x / 10, 50 + y * 40))
        
    def step(self):
        self.player1.step()
        
        for invader in self.getSpritesbyClass(Invader):
            invader.step()
        
        for bullet in self.getSpritesbyClass(Bullet):
            bullet.step()
            
            if bullet.y < -20:
                bullet.destroy()
            else:
                if bullet.y <= self.height - 150:
                    barriers = bullet.collidingWithSprites(Barrier)
                    if barriers:
                        for barrier in barriers:
                            barrier.destroy()
                        bullet.destroy()
                elif bullet.y > self.height - 90:
                    if bullet.collidingWithSprites(Ship):
                        self.player1.destroy()
                        bullet.destroy()
                for invader in bullet.collidingWithSprites(Invader):
                    invader.destroy()
                    bullet.destroy()
                    
        
myapp = SpaceInvadersGame()
myapp.run()
        
