import sys
import pygame as pg
from math import *
from random import *

pg.init()
W, H = 900, 800
screen = pg.display.set_mode((W, H))
pg.display.set_caption("Perfect Paced Butterfly Heart")

layer = pg.Surface((W, H))
fade = pg.Surface((W, H))
fade.set_alpha(70)
clock = pg.time.Clock()

def heart(t, s):
    x = 16 * sin(t) ** 3
    y = 13*cos(t) - 5*cos(2*t) - 2*cos(3*t) - cos(4*t)
    return W/2 + x*s, H/2 - y*s

def glow():
    screen.blit(layer, (0, 0))
    for k in (10,):
        img = pg.transform.smoothscale(layer, (W // k, H // k))
        img = pg.transform.smoothscale(img, (W, H))
        screen.blit(img, (0, 0), special_flags=pg.BLEND_RGB_ADD)

WING = [(0, 0), (.5, -1.2), (1.2, -1), (1.3, -.2),
        (1, .3), (.9, .9), (.3, .7)]

def butterfly(x, y, s, flap, ang, col):
    w = abs(sin(flap))
    for d in (-1, 1):
        pts = []
        for px, py in WING:
            px, py = px * d * w * s, py * s
            pts.append((x + px*cos(ang) - py*sin(ang),
                        y + px*sin(ang) + py*cos(ang)))
        pg.draw.polygon(layer, col, pts)
        pg.draw.polygon(layer, (255, 150, 230), pts, 1)

dots = [heart(i / 120 * 2 * pi, 22) for i in range(120)]
tilt = [uniform(-.6, .6) for _ in dots]
flyers = []
t = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
    layer.blit(fade, (0, 0))
    
    # 1-SECOND DELAY: Everything waits until t reaches 30 (1 second at 30 FPS)
    if t >= 30:
        # PHASE 1 (Starts at 1s): Draw the simple dotted heart outline
        dots_to_draw = min(120, t - 30)
        for p in dots[:dots_to_draw]:
            pg.draw.circle(layer, (255, 80, 200), p, 3) 
                
        # PHASE 2 (Starts at 5s): Dots are covered by flapping butterflies
        if t >= 150:
            butterflies_to_draw = min(120, t - 150)
            for i, p in enumerate(dots[:butterflies_to_draw]):
                if i % 6 == 0:
                    col = (200, 40, 150) if i % 8 else (110, 50, 220)
                    butterfly(*p, 15, t * .3 + i, tilt[i], col)
                    
        # PHASE 3 (Starts at 9s): Inner pulsating rings appear
        if t >= 270:
            rings_to_draw = min(6, (t - 270) // 40 + 1)
            for k in range(1, rings_to_draw):
                s = 22 * (k + sin(t * .08 - k) * .4) / 6
                for i in range(0, 120, 3):
                    x, y = heart(i / 120 * 2 * pi, s)
                    pg.draw.circle(layer, (150, 80, 255), (x, y), 2)
                    
        # PHASE 4 (Starts at 13s): Smaller butterflies spawn and fly away
        if t >= 390:
            if t % 6 == 0:
                x, y = choice(dots)
                flyers.append([x, y, uniform(-2, 2), uniform(-4, -1.5), 0])
                
    for f in flyers:
        f[0] += f[2]
        f[1] += f[3]
        f[4] += 1
        butterfly(f[0], f[1], 10, f[4]*.5, f[2]*.2, (230, 90, 190))
        
    glow()
    pg.display.flip()
    clock.tick(30)
    t += 1