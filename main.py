import pygame
from random import randint
import math

pygame.init()

step=10 #vzdálenost, kterou projde jeden opilec za tah
sizegoal=0 #velikost cíle
spawnopilec=3 #počet opilců
moves=10 #počet tahů za jeden snímek
mingoaldistance=100 #minimální vzdálenost cíle od (0,0)
maxfps=60 #maximální fps

screen = pygame.display.set_mode((1024, 1024))
clock = pygame.time.Clock()
vertical_spin=0
horizontal_spin=0
distance=1800
size = 500
half = size / 2
semioffsety=0
semioffsetx=0
oldoffsety=0
oldoffsetx=0
goalx=size
goaly=size
goalz=size
secondgoalx=size
secondgoaly=size
secondgoalz=size
runing=False
font = pygame.font.Font(None, 20)
last_frame_press=False

class opilec:
    def __init__(self, number):
        self.x = 0
        self.y = 0
        self.z = 0
        self.colour=(randint(0,255),randint(0,255),randint(0,255))
        self.trail=[]
        self.semi=[]
        self.number=number
        self.number_steps=0
        self.in_target=False
        self.ended=False
    def end(self):
        if self.in_target==False:
            self.trail=[]
            self.semi=[]
            self.ended=True

    def move(self):
        if self.ended==False:
            self.semi=[[self.x, self.y, self.z]]
            while True:
                direction = randint(0, 5)
                if direction == 0 and self.x > -half+step:
                    self.x -= step
                    break
                elif direction == 1 and self.x < half-step:
                    self.x += step
                    break
                elif direction == 2 and self.y > -half+step:
                    self.y -= step
                    break
                elif direction == 3 and self.y < half-step:
                    self.y += step
                    break
                elif direction == 4 and self.z > -half+step:
                    self.z -= step
                    break
                elif direction == 5 and self.z < half-step:
                    self.z += step
                    break
                else:
                    continue

            self.check()
            self.semi.append([self.x, self.y, self.z])
            self.trail.append(self.semi)
            self.number_steps+=1



    def check(self):
        if min(goalx, secondgoalx) <= self.x <= max(goalx, secondgoalx) and min(goaly, secondgoaly) <= self.y <= max(goaly, secondgoaly) and min(goalz, secondgoalz) <= self.z <= max(goalz, secondgoalz):
            print(f"opilec č.{self.number} došel do cíle za {self.number_steps} tahů")
            self.in_target=True
            return(True)


lines = [
    # Bottom Face (z = z_dist)
    [[-half, -half, -half], [half, -half, -half]],
    [[half, -half, -half], [half, half, -half]],
    [[half, half, -half], [-half, half, -half]],
    [[-half, half, -half], [-half, -half, -half]],

    # Top Face (z = z_dist + size)
    [[-half, -half, half], [half, -half, half]],
    [[half, -half, half], [half, half, half]],
    [[half, half, half], [-half, half,half]],
    [[-half, half, half], [-half, -half, half]],

    # Vertical Pillars
    [[-half, -half, -half], [-half, -half,half]],
    [[half, -half, -half], [half, -half, half]],
    [[half, half, -half], [half, half, half]],
    [[-half, half, -half], [-half, half, half]]
]
goal=opilec(0)
while True:
    for i in range(10000):
        goal.move()
    if abs(goal.x)>mingoaldistance and abs(goal.z)>mingoaldistance and abs(goal.y)>mingoaldistance: break

goalx=goal.x
goaly=goal.y
goalz=goal.z
if goalx <=0:secondgoalx=goalx + sizegoal
else: secondgoalx=goalx - sizegoal

if goaly <= 0:secondgoaly = goaly + sizegoal
else:secondgoaly = goaly - sizegoal

if goalz <= 0:secondgoalz = goalz + sizegoal
else:secondgoalz = goalz - sizegoal

x1, y1, z1 = goalx, goaly, goalz
x2, y2, z2 = secondgoalx, secondgoaly, secondgoalz
print(x1, y1, z1,x2, y2, z2)

cube_lines = [
    # Bottom Square (z1)
    [[x1, y1, z1], [x2, y1, z1]],
    [[x2, y1, z1], [x2, y2, z1]],
    [[x2, y2, z1], [x1, y2, z1]],
    [[x1, y2, z1], [x1, y1, z1]],

    # Top Square (z2)
    [[x1, y1, z2], [x2, y1, z2]],
    [[x2, y1, z2], [x2, y2, z2]],
    [[x2, y2, z2], [x1, y2, z2]],
    [[x1, y2, z2], [x1, y1, z2]],

    # Vertical Connectors
    [[x1, y1, z1], [x1, y1, z2]],
    [[x2, y1, z1], [x2, y1, z2]],
    [[x2, y2, z1], [x2, y2, z2]],
    [[x1, y2, z1], [x1, y2, z2]]
]

def renderlines(fov: int, vertical: bool, horizontal:bool, distance:int):
    cx, cy = 512, 512
    all=[]

    for g in opilci:
        for x in g.trail:
            all.append([list(x[0]), list(x[1]), g.colour])

    for x in lines:

        all.append([list(x[0]), list(x[1]), (0,255,0)])

    for x in cube_lines:
        all.append([list(x[0]), list(x[1]), (0, 255, 0)])

    for x in all:
        zs1=x[0][2]*math.cos(horizontal)+x[0][0]*math.sin(horizontal)
        zs2=x[1][2]*math.cos(horizontal)+x[1][0]*math.sin(horizontal)
        x[0][0]=x[0][0]*math.cos(horizontal)-x[0][2]*math.sin(horizontal)
        x[1][0]=x[1][0]*math.cos(horizontal)-x[1][2]*math.sin(horizontal)
        x[0][2]=x[0][1]*math.sin(vertical)+zs1*math.cos(vertical)+distance
        x[1][2]=x[1][1]*math.sin(vertical)+zs2*math.cos(vertical)+distance
        x[0][1]=x[0][1]*math.cos(vertical)-zs1*math.sin(vertical)
        x[1][1]=x[1][1]*math.cos(vertical)-zs2*math.sin(vertical)
    all.sort(key=lambda x: min(x[0][2],x[1][2]), reverse=True)
    for x in all:
        if x[0][2]>0 and x[1][2]>0:
            pygame.draw.line(screen, x[2], (((x[0][0] * fov) / x[0][2]) + cx, ((x[0][1] * fov) / x[0][2]) + cy), (((x[1][0] * fov) / x[1][2]) + cx, ((x[1][1] * fov) / x[1][2]) + cy), round(3500/((x[0][2]+x[1][2])/2)))
    number_of_lines = font.render(f"počet čar:{len(all)}", True, "red")
    screen.blit(number_of_lines, (0, 15))
opilci=[opilec(i) for i in range(spawnopilec)]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEWHEEL:
            distance+=event.y*50
        if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
            if runing:
                runing=False
            else:
                runing=True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        horizontal_spin -= 0.05
    if keys[pygame.K_RIGHT]:
        horizontal_spin += 0.05
    if keys[pygame.K_UP]:
        vertical_spin -= 0.05
    if keys[pygame.K_DOWN]:
        vertical_spin += 0.05

    keys=pygame.mouse.get_pressed()
    if keys[0]:
        if last_frame_press==False:
            new=pygame.mouse.get_pos()
            last_frame_press=True
        else:
            semioffsetx = (list(new)[0]-list(pygame.mouse.get_pos())[0])
            semioffsety = (list(new)[1] - list(pygame.mouse.get_pos())[1])
    else:
        oldoffsetx+=semioffsetx
        oldoffsety+=semioffsety
        semioffsetx,semioffsety=0,0
        last_frame_press=False

    if runing:
        for g in opilci:
            for i in range(moves):
                g.move()
                if g.in_target==True:
                    runing=False
                    for k in opilci:
                        k.end()
                    break

    screen.fill("black")
    renderlines(2500, (oldoffsety+semioffsety)*-0.005,(oldoffsetx+semioffsetx)*-0.005,distance)
    text=font.render(f"fps:{round(clock.get_fps())}", True, "red")
    screen.blit(text, (0, 0))
    pygame.display.update()
    clock.tick(maxfps)