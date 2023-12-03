import pygame, sys, os, random, time
import win32api
from PIL import Image
from shaders import *
from pygame import gfxdraw
import gicon_keyboard as gk

pygame.init()

global group_list

window = pygame.display.set_mode((1030,865))
save = (1030,int(1030*210/297))
pygame.display.set_caption("자리 바꾸기")
pygame.display.set_icon(pygame.image.load('.\\data\\icon.jpg'))
ui_list = []

group_seat_count = [5,5,5,6,5,5]
seat_surf = pygame.Surface((len(group_seat_count)+2,max(group_seat_count)+2))
for x in range(len(group_seat_count)):
    for y in range(group_seat_count[x]):
        seat_surf.set_at((len(group_seat_count)-x,max(group_seat_count)-y),(255,255,255))
seats = [[[] for n in range(x_count)] for x_count in group_seat_count]
# print(seats)
Position = []
students = eval(open('.\\data\\students','r',encoding='utf-8').read())
Decided = eval(open('.\\data\\group.json','r',encoding='utf-8').read())
define = eval(open('.\\data\\define.json','r',encoding='utf-8').read())
seperate = eval(open('.\\data\\seperate.json','r',encoding='utf-8').read())
thing = pygame.mixer.Sound(".\\data\\thing.mp3")
# print(len(students))
Distributed = {}
for i, team in enumerate(Decided):
    for name in team:
        Distributed[name] = i

# print(Distributed)
# print(Decided)
global group_
group_ = {}

class color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 9, 9)

class textures:
    dusts = [
        pygame.transform.scale(pygame.image.load(f".\\textures\\dust0{n+1}.png"), (64, 64)) for n in range(7)
    ]

entities = 0

def font(fontname, size):
    return pygame.font.Font(f"C:\\Windows\\Fonts\\{fontname}.TTF",size)
def addlist(lists:list):
    result = []
    for lst in lists:
        result += lst

    return result

lastleft1 = 0
lastleft2 = 0
lastright2 = 0
lastright1 = 0
lastmiddle1 = 0

def distance(pos1:tuple, pos2:tuple) -> tuple:
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 )**0.5

class mouse:
    def middlebtdown():
        global lastmiddle1
        middle = win32api.GetKeyState(0x04)
        if int(lastmiddle1) >=0 and middle <0:
            lastmiddle1 = middle
            return True
        else:
            lastmiddle1 = middle
            return False
    def rightbtdown():
        global lastright1
        right = win32api.GetKeyState(0x02)
        if int(lastright1) >= 0 and right <0:
            lastright1 = right
            return True
        else:
            lastright1=right
            return False
    def rightbtup():
        global lastright2
        right = win32api.GetKeyState(0x02)
        if int(lastright2) < 0 and right >=0:
            lastright2 = right
            return True
        else:
            lastright2=right
            return False
    def leftbtdown():
        global lastleft1
        left = win32api.GetKeyState(0x01)
        if int(lastleft1) >=0 and left <0:
            lastleft1 = left
            return True
        else:
            lastleft1 = left
            return False
    def leftbtup():
        global lastleft2
        left = win32api.GetKeyState(0x01)
        if int(lastleft2) < 0 and left >= 0:
            lastleft2 = left
            return True
        
        else:
            lastleft2 = left
            return False
class seat:
    student = list(students)
    dum = list(students)
    def PlantSeed():
        global Position
        Position = []
        for i in range(len(Decided)):
            if str(i) not in define:
                x = random.randint(1,len(group_seat_count))
                y = random.randint(1,group_seat_count[x-1])

                Position.append((x-1,y-1))
            else:
                Position.append(eval(random.choice(define[str(i)])))
    
    def do():
        seat.PlantSeed()
        seat.student = list(students)
        global group_
        for group in group_list:
            for seatt in group.seats:
                seatt.set_text("")

        seat_num = []
        combined = addlist(Decided)
        random.shuffle(seat.student)
        result = {}

        for x in range(len(group_seat_count)):
            for y in range(group_seat_count[x]):
                seat_num.append((x,y))

        for student in combined:
            pos = Position[Distributed[student]]
            
            if (pos in seat_num):
                new_seat = pos
                seat_num.remove(new_seat)
                result[student] = new_seat
            else:
                x = random.randint(-1,1)
                y = random.randint(-1,1)

                new_seat = (pos[0]+x,pos[1]+y)
                n = 0

                while ((new_seat not in seat_num or (x != 0 and y != 0)) and n < 30):
                    n += 1
                    x = random.randint(-1,1)
                    y = random.randint(-1,1)
                    new_seat = (pos[0]+x,pos[1]+y)

                if (n >= 30):
                    break


                seat_num.remove(new_seat)
                result[student] = new_seat

        for student in seat.student:
            if (student not in combined):

                new_seat = random.sample(seat_num,1)[0]
                seat_num.remove(new_seat)
                result[student] = new_seat

        group_ = result
        seat.dum = seat.student
        if (len(result) < len(seat.student)):
            seat.do()

    def RunOne():
        if (len(seat.dum) > 0):
            student = random.sample(seat.dum,1)[0]
            seat.dum.remove(student)

            pos = group_[student]
            obj = group_list[pos[0]].seats[pos[1]]
            obj.set_text(student)
            
            ParticleHub((int(obj.x + obj.sx/2), int(obj.y + obj.sy/2)))
            # pygame.mixer.Sound.play(thing)

    def RunAll():
        seat.do()
        global group_
        
        loc = {}
        for student in group_:

            pos = group_[student]
            loc[student] = pos
            obj = group_list[pos[0]].seats[pos[1]]
            obj.set_text(student)
            ParticleHub((int(obj.x + obj.sx/2), int(obj.y + obj.sy/2)))
        
        # check valid
        valid = True
        for group in seperate:
            if distance(loc.get(group[0]), loc.get(group[1])) <= group[2]: valid = False
        if not valid: seat.RunAll()
        
class System:
    clock = pygame.time.Clock()
    bugged_icon = pygame.image.load(f'.\\data\\icon\\bug.png')

    def SavePNG():
        image = pygame.Surface(save)
        image.blit(window,(0,0),((0,50),save))
        pygame.image.save(image,f'.\\{time.strftime("%Y%m%d",time.localtime())}.png')
    
    def SavePDF():
        image = pygame.Surface(save)
        image.blit(window,(0,0),((0,50),save))
        pygame.image.save(image,f'.\\data\\dummy.png')

        image1 = Image.open('.\\data\\dummy.png')
        im1 = image1.convert('RGB')
        im1.save(f'.\\{time.strftime("%Y%m%d",time.localtime())}.pdf')

    def icon(name):
        icon_list = os.listdir('.\\data\\icon')

        if (f"{name}.png" in icon_list): return pygame.image.load(f'.\\data\\icon\\{name}.png')
        elif (f"{name}.jpg" in icon_list): return pygame.image.load(f'.\\data\\icon\\{name}.jpg')
        else: return System.bugged_icon

    class draw:
        def aacircle(surface, x, y, radius, color):
            gfxdraw.aacircle(surface, x, y, radius, color)
            gfxdraw.filled_circle(surface, x, y, radius, color)
        def rrect(surface,rect,color,radius=0.4):
            rect         = pygame.Rect(rect)
            color        = pygame.Color(*color)
            alpha        = color.a
            color.a      = 0
            pos          = rect.topleft
            rect.topleft = 0,0
            rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)
            circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
            pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
            circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)
            radius              = rectangle.blit(circle,(0,0))
            radius.bottomright  = rect.bottomright
            rectangle.blit(circle,radius)
            radius.topright     = rect.topright
            rectangle.blit(circle,radius)
            radius.bottomleft   = rect.bottomleft
            rectangle.blit(circle,radius)

            rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
            rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

            rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
            rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)
            return surface.blit(rectangle,pos)
        def trirect(surface,x,y,sx,sy,tri,color,edge=(1,1,1,1)):
            if sx < tri*2:
                sx = tri*2
            if sy < tri*2:
                sy = tri*2

            pygame.draw.rect(surface,color,[x+tri,y,sx-tri*2,sy])
            pygame.draw.rect(surface,color,[x,y+tri,sx,sy-tri*2])
            if edge[0] == 1:
                pygame.draw.polygon(surface,color,[[x,y+tri],[x+tri,y],[x+tri,y+tri]])
            else:
                pygame.draw.rect(surface,color,[x,y,tri,tri])
            if edge[1] == 1:
                pygame.draw.polygon(surface,color,[[x+sx-tri,y+1],[x+sx-1,y+tri],[x+sx-tri,y+tri]])
            else:
                pygame.draw.rect(surface,color,[x+sx-tri,y,tri,tri])
            if edge[2] == 1:
                pygame.draw.polygon(surface,color,[[x,y+sy-tri],[x+tri,y+sy-1],[x+tri,y+sy-tri]])
            else:
                pygame.draw.rect(surface,color,[x,y+sy-tri,tri,tri])
            if edge[3] == 1:
                pygame.draw.polygon(surface,color,[[x+sx-1,y+sy-tri],[x+sx-tri,y+sy-1],[x+sx-tri,y+sy-tri]])
            else:
                pygame.draw.rect(surface,color,[x+sx-tri,y+sy-tri,tri,tri])
        def textsize(text, font):
            text_obj = font.render(text, True, (0,0,0))
            text_rect=text_obj.get_rect()
            return text_rect.size
        def text(text, font, window, x, y, cenleft="center", color=(0,0,0)):
            text_obj = font.render(text, True, color)
            text_rect=text_obj.get_rect()
            if(cenleft == "center"):
                text_rect.centerx = x
                text_rect.centery = y
            elif(cenleft == "left"):
                text_rect.left=x
                text_rect.top=y
            elif(cenleft == "right"):
                text_rect.right=x
                text_rect.top=y
            elif(cenleft == "cenleft"):
                text_rect.left=x
                text_rect.centery=y
            elif(cenleft == "cenright"):
                text_rect.right=x
                text_rect.centery=y
            window.blit(text_obj, text_rect)
        def gettsize(text,font):
            return font.render(text,True,(0,0,0)).get_rect().size
    
    class ui:
        ui_tag = eval(open('.\\data\\ui.json','r',encoding='utf-8').read())

        def shadow(surface, amount, opacity):
            blured, x, y = blur(surface,amount)
            shadow = change_light_color(blured,(28, 32, 64))
            shadow.set_alpha(opacity)
            return shadow, x, y
        class line_shadow:
            def __init__(self,x,y,sx,sy,way,startvalue=150):
                global sshadow
                ui_list.append(self)
                self.x=x
                self.y=y
                self.sx=sx
                self.sy=sy
                self.way=way
                self.pointer=[0,0]
                self.startvalue=startvalue
                self.shadow = pygame.transform.smoothscale(pygame.transform.rotate(sshadow,(way-1)*90+180),(sx,sy))
                self.shadow.set_alpha(startvalue)
                self.mouse=pygame.SYSTEM_CURSOR_ARROW 
                if self.way >2:
                    self.startvalue = self.startvalue
            def draw(self,mx,my):
                window.blit(self.shadow,(self.x,self.y))
        class group:
            def __init__(self, surface:pygame.Surface,name:str,group_number:int, member_count:int,font_:font=font("LG_SMART_UI-SEMIBOLD",15)):
                ui_list.append(self)

                self.name = name
                self.font=font_
                self.group_number = group_number
                self.member_count = member_count
                self.surface = surface

                self.seats = []
                self.image = pygame.Surface((150,600),pygame.SRCALPHA,32).convert_alpha()
                self.hitbox = pygame.Surface(surface.get_size())
                self.nametag = pygame.Surface((60,20),pygame.SRCALPHA,32).convert_alpha()

                pygame.draw.rect(self.hitbox, (255,255,255),[1015-165*group_number, 75, 150,630])
                for i in range(member_count):
                    self.seats.append(System.ui.button(self.surface,1030-165*group_number,680-100*(i+1),120,85,color=(255,255,255),edge_thick=0,round=True,roundness=0.25,text_color=(28, 32, 64),font=font("LG_SMART_UI-SEMIBOLD",32)))

                System.draw.rrect(self.nametag,[0,0,60,20],(255,255,255),1)
                System.draw.text(self.name,self.font,self.nametag,30,10,color=(47,52,66))

                self.nametagshadow, self.correctionx,self.correctiony=System.ui.shadow(self.nametag,5,10)
            def draw(self,mx,my):
                if (self.hitbox.get_at((mx,my)) == (255,255,255)):
                    pygame.draw.rect(self.surface, (56,190,128),[1015-165*self.group_number, 75, 150,630],1) # <- hitbox line
                
                self.surface.blit(self.nametagshadow,(1060-165*self.group_number-self.correctionx,670-self.correctiony))
                self.surface.blit(self.nametag,(1060-165*self.group_number,670))
        class button:
            def __init__(self,surface:pygame.Surface, x:int, y:int, sx:int, sy:int, icon:pygame.Surface=False,
                            color=(255,255,255),edge_color=(0,0,0), edge_thick=1,opacity:int=255,round:bool=False, roundness=1.0,
                            text:str="",text_color=(0,0,0),font:font=font("LG_SMART_UI-SEMIBOLD",15),
                            addshadow=True, clickable=True,CustomCorrectionX=0,CustomCorrectionY=0,
                            showline=True,
                            tag=""
                        ):
                ui_list.append(self)

                self.surface=surface
                self.x=x
                self.y=y
                self.sx=sx
                self.sy=sy
                self.icon=icon
                self.color=color
                self.edge_color=edge_color
                self.edge_thick=edge_thick
                self.shape = round
                self.opacity = opacity
                self.text=text
                self.text_color = text_color
                self.font=font
                self.round=round
                self.roundness=roundness
                self.addshadow=addshadow
                self.clickable=clickable
                self.CustomCorrectionX=CustomCorrectionX
                self.CustomCorrectionY=CustomCorrectionY
                self.showline=showline
                self.tag=tag

                self.onmouse = False
                self.onmousecolor = (int(color[0]*0.9),int(color[1]*0.9),int(color[2]*0.9))

                self.image = pygame.Surface((sx,sy),pygame.SRCALPHA,32).convert_alpha()
                self.onmouseS = pygame.Surface((sx,sy),pygame.SRCALPHA,32).convert_alpha()
                self.omtexted = pygame.Surface((sx,sy),pygame.SRCALPHA,32).convert_alpha()
                self.texted = pygame.Surface((sx,sy),pygame.SRCALPHA,32).convert_alpha()
                self.hitbox = pygame.Surface(surface.get_size())

                if (round == False):
                    pygame.draw.rect(self.image,color,[0,0,sx,sy])
                    pygame.draw.rect(self.image,edge_color,[0,0,sx,sy],edge_thick)
                    pygame.draw.rect(self.hitbox,(255,255,255),[x,y,sx,sy])

                    pygame.draw.rect(self.onmouseS,self.onmousecolor,[0,0,sx,sy])
                    pygame.draw.rect(self.onmouseS,edge_color,[0,0,sx,sy],edge_thick)
                else:
                    System.draw.rrect(self.image,[0,0,sx,sy],edge_color,1)
                    System.draw.rrect(self.image,[edge_thick,edge_thick,sx-2*edge_thick,sy-2*edge_thick],color,roundness)
                    System.draw.rrect(self.hitbox,[x,y,sx,sy],(255,255,255),1)

                    System.draw.rrect(self.onmouseS,[0,0,sx,sy],edge_color,1)
                    System.draw.rrect(self.onmouseS,[edge_thick,edge_thick,sx-2*edge_thick,sy-2*edge_thick],self.onmousecolor,roundness)


                if (icon != False):
                    icon_size = icon.get_size()
                    self.image.blit(icon,(int((sx-icon_size[0])/2),int((sy-icon_size[1])/2)))
                    self.onmouseS.blit(icon,(int((sx-icon_size[0])/2),int((sy-icon_size[1])/2)))

                self.texted.blit(self.image,(0,0))
                self.omtexted.blit(self.onmouseS,(0,0))
                System.draw.text(text,font,self.texted,int(sx/2),int(sy/2),"center",self.text_color)
                System.draw.text(text,font,self.omtexted,int(sx/2),int(sy/2),"center",self.text_color)

                self.opacitied = self.texted
                self.omopacited = self.omtexted
                self.opacitied.set_alpha(opacity)
                self.omopacited.set_alpha(opacity)

                self.shadow, self.correctionx,self.correctiony=System.ui.shadow(self.opacitied,5,10)
            def draw(self, mx, my):
                
                if (self.addshadow == True):
                    if (self.CustomCorrectionX==0 and self.CustomCorrectionY ==0):
                        self.surface.blit(self.shadow,(self.x-self.correctionx,self.y-self.correctiony))
                    else:
                        self.surface.blit(self.shadow,(self.x+self.CustomCorrectionX,self.y+self.CustomCorrectionY))
                self.surface.blit(self.opacitied,(self.x,self.y))

                if (self.hitbox.get_at((mx,my)) == (255,255,255) and self.clickable==True):
                    self.onmouse = True
                    if (self.showline == True):
                        pygame.draw.rect(window,(56,190,128),[self.x,self.y,self.sx,self.sy],1)
                    else: self.surface.blit(self.omopacited,(self.x,self.y))

                    if (mouse.leftbtup() == True):
                        if (self.tag in System.ui.ui_tag['button']):
                            exec(f"{System.ui.ui_tag['button'][self.tag]}")
                else:
                    self.onmouse = False

                System.draw.text(self.text,self.font,window,self.x+int(self.sx/2),self.y+int(self.sy/2),"center",color=self.text_color)
            def set_text(self,text:str):
                self.text = text
                self.texted = pygame.Surface((self.sx,self.sy),pygame.SRCALPHA,32).convert_alpha()
                self.omtexted = pygame.Surface((self.sx,self.sy),pygame.SRCALPHA,32).convert_alpha()
                self.texted.blit(self.image,(0,0))
                self.omtexted.blit(self.onmouseS, (0,0))
                self.opacitied = self.texted
                self.opacitied.set_alpha(self.opacity)
                self.omopacited = self.omtexted
                self.omopacited.set_alpha(self.opacity)
            def set_opacity(self,opacity:int):
                self.opacity = opacity
                self.opacitied = self.texted
                self.opacitied.set_alpha(opacity)
        class textlistview:
            def __init__(self):
                pass
            def draw(self,mx,my):
                pass

    def display():
        window.fill((235, 241, 249))

        for ui in ui_list: 
            ui.draw(mx,my)
        for particle in ParticleHub.entities:
            particle.draw()

        # System.draw.rrect(window,[1055,25,360,200],(235, 241, 249),0.1)
        # window.blit(pygame.transform.scale(seat_surf,(seat_surf.get_size()[0]*3,seat_surf.get_size()[1]*3)),(1070,40))

    def event(events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

class ParticleHub:
    entities = []

    class SubParticle:
        def __init__(self, pos:tuple[int, int], speed:tuple[int, int]) -> None:
            self.pos = list(pos)
            self.speed = list(speed)
            self.scale = random.randint(0, 6)
            self.texture :pygame.Surface = textures.dusts[self.scale]
            # self.texture.set_alpha(100)

            return


        def draw(self):
            if ((fps := System.clock.get_fps()) > 0):
                self.speed[1] += 9.8/fps*50

                self.pos[0] += self.speed[0]/fps
                self.pos[1] += self.speed[1]/fps


            window.blit(self.texture, (self.pos[0]-32, self.pos[1]-32))

    def __init__(self, pos:tuple[int, int]) -> None:
        global entities
        self.pos = pos
        self.duration = 2.5
        self.summon = time.time()
        self.sub = []
        self.count = random.randint(2, 5)

        ParticleHub.entities.append(self)
        for i in range(self.count): self.sub.append(ParticleHub.SubParticle(self.pos, (random.randrange(-150, 150), random.randrange(-200, 30))))
        entities += self.count
        pass

    def draw(self):
        global entities
        for particle in self.sub:
            particle.draw()

        if (time.time() - self.summon >= self.duration):
            ParticleHub.entities.pop(ParticleHub.entities.index(self))
            entities -= self.count
        
        # pygame.draw.circle(window, color.red, self.pos, 3, 1)

#test_button = System.ui.button(window,100,100,25,25,round=True,edge_thick=1,opacity=255,icon=System.icon('plus'))

group_list = []
for i in range(6):group_list.append(System.ui.group(window,f"{i+1} 분단",i+1,group_seat_count[i])) # 분단
chalkboard = System.ui.button(window,365,730,300,20,color=(56,190,128),edge_thick=0,round=True,roundness=1,text="칠판",text_color=(255,255,255),edge_color=(56,190,128), addshadow=False,clickable=False)
setting_panel = System.ui.button(window,320,770,390,200,color=(255,255,255),edge_thick=0,round=True,roundness=0.1,clickable=False,CustomCorrectionX=-70, CustomCorrectionY=-35)
AtOnce = System.ui.button(window,1055-720,785,140,30,color=(56,190,128),edge_thick=0,text="한 번에 뽑기",text_color=(255,255,255),round=True,roundness=0.5,showline=False,tag="AtOnce")
OnlyOne = System.ui.button(window,1205-720,785,140,30,color=(56,190,128),edge_thick=0,text="하나 뽑기",text_color=(255,255,255),round=True,roundness=0.5,showline=False,tag="OnlyOne")
Reset = System.ui.button(window,1355-720,785,60,30,color=(253, 76, 54),edge_thick=0,text="초기화",text_color=(255,255,255),round=True,roundness=0.4,showline=False,tag="Reset")
PNGSave = System.ui.button(window,1055-720,825,175,30,color=(255,185,34),edge_thick=0,text="PNG로 저장",text_color=(255,255,255),round=True,roundness=0.4,showline=False,tag="SavePNG")
PDFSave = System.ui.button(window,1240-720,825,175,30,color=(255,185,34),edge_thick=0,text="PDF로 저장",text_color=(255,255,255),round=True,roundness=0.4,showline=False,tag="SavePDF")


seat.do()
while True:
    events = pygame.event.get()
    keyboard = gk.keyboard.get_input()

    mx, my = pygame.mouse.get_pos()

    System.display()
    System.event(events)
        
    pygame.display.update()

    System.clock.tick(144)