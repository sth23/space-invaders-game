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
    square = RectangleAsset(30, 30, noline, black)
    
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
        
class Ship(Sprite):
    ship = PolygonAsset([(0,30), (15,0), (30,30), (15,15)], noline, black)
    
    def __init__(self, position, width):
        super().__init__(Ship.ship, position)
        self.gamewidth = width
        self.speed = 5
        self.vx = 0
        
        SpaceInvadersGame.listenKeyEvent("keydown", "space", self.shoot)

        SpaceInvadersGame.listenKeyEvent("keydown", "right arrow", self.moveRightOn)
        SpaceInvadersGame.listenKeyEvent("keyup", "right arrow", self.moveRightOff)
        SpaceInvadersGame.listenKeyEvent("keydown", "left arrow", self.moveLeftOn)
        SpaceInvadersGame.listenKeyEvent("keydown", "left arrow", self.moveLeftOff)

    def shoot(self, event):
        Bullet((self.x + 15, self.y), -1)

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
        
class SpaceInvadersGame(App):
    def __init__(self):
        super().__init__()
        
        self.player1 = Ship((self.width / 2, self.height - 40), self.width)
        
    def step(self):
        self.player1.step()
        
        for bullet in self.getSpritesbyClass(Bullet):
            bullet.step()
        
myapp = SpaceInvadersGame()
myapp.run()
        
