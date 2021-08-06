import pygame
import os
import math
import time
pygame.font.init()

earth_mass = 5.972 * (10**24) #kg
moon_mass = 7.348 * (10**22) #kg

moon_radius = 1737.5*1000 #m
earth_radius = 6371*1000 #m

G=6.673*(10**-11) #Nm2/kg2
smooth = 10**(-12)*1.5

WIDTH = 500
HEIGHT = 500
FPS = 120
pygame.display.set_caption("Newton Motion Simulation")

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
BG = pygame.transform.scale(pygame.image.load(os.path.join("venv/assets", "background-black.png")), (WIDTH,HEIGHT))

class Planet:
    def __init__(self,x,y,r,mass,vel_x,vel_y,accel_x=0,accel_y=0):
        self.x = x
        self.y = y
        self.r = r
        self.mass = mass
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.accel_x = accel_x
        self.accel_y = accel_y
    def draw(self, window):
        pygame.draw.circle(window,(255,255,255),(self.x, self.y),self.r)

earth = Planet(WIDTH/2,HEIGHT/2,40,earth_mass,0,0)
moon = Planet(WIDTH/2,60,earth.r/(earth_radius/moon_radius),moon_mass,1.8,0)

circleX1 = 400
circleY1 = 400

radius = 20
delta_t = 0.3

def main():
    run = True
    clock1 = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 30)
    clock = pygame.time.Clock()
    elapsed_time = pygame.time.get_ticks()

    def redraw_window():
        WIN.blit(BG, (0, 0))
        days_passed = main_font.render(f"Days passed: {elapsed_time/1000}", 1, (255, 255, 255))
        WIN.blit(days_passed, (10, 10))
        earth.draw(WIN)
        moon.draw(WIN)
        pygame.draw.line(WIN,(255, 0, 0), (moon.x, moon.y), (moon.x+moon.accel_x*20, moon.y+moon.accel_y*20), 3)
        pygame.draw.line(WIN,(0, 255, 0), (moon.x, moon.y), (moon.x+moon.vel_y, moon.y+moon.vel_y), 3)
        pygame.draw.circle(WIN, (255, 0, 0), (WIDTH / 2, 60), moon.r)
        pygame.display.update()


    while run:
        clock.tick(FPS)

        elapsed_time = pygame.time.get_ticks()

        redraw_window()

        print(elapsed_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        dist = math.sqrt((earth.x - moon.x) ** 2 + (earth.y - moon.y) ** 2)

        f = (G * earth.mass * moon.mass) / (dist ** 2)
        print(dist, ", (",moon.x,", ",moon.y,")")

        if dist < 20:
            moon.vel_y = 0
            moon.vel_x = 0
            moon.accel_x = 0
            moon.accel_y = 0
        else:
            moon.accel_x = (f/moon.mass)*smooth*(earth.x - moon.x)/dist
            moon.accel_y = (f/moon.mass)*smooth*(earth.y - moon.y)/dist

            moon.vel_x +=moon.accel_x * delta_t
            moon.vel_y +=moon.accel_y * delta_t

            moon.x +=moon.vel_x*delta_t + moon.accel_x*(delta_t**2)/2
            moon.y +=moon.vel_y*delta_t + moon.accel_y*(delta_t**2)/2

main()