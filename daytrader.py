import sys
from random import randint 
import pygame
from pygame.locals import QUIT,Rect,KEYDOWN,K_SPACE,MOUSEBUTTONDOWN,MOUSEBUTTONUP

pygame.init()
pygame.key.set_repeat(5,5)
SURFACE=pygame.display.set_mode((800,600))
FPSCLOCK=pygame.time.Clock()
sysfont=pygame.font.SysFont(None,30)
sysfont2=pygame.font.SysFont(None,20)
sysfont3=pygame.font.SysFont(None,70)
stock=100
max=10
account=1000000
colors=[(100,100,100),(200,200,200),(200,50,50),(50,50,200),(255,255,255),(0,0,0),(0,255,50),(50,50,50)]
boom=True
recession=False
bubble=False
tradingprice=0

class Button:
    def __init__(self,name,rect,color,ispressed):
        self.name=name
        self.rect=rect
        self.color=color
        self.ispressed=ispressed
        self.handler = None

    def paint(self):
        pygame.draw.rect(SURFACE,self.color,self.rect)
        if self.ispressed:
            pygame.draw.rect(SURFACE,colors[0],self.rect)
        pygame.draw.rect(SURFACE,colors[1],self.rect,3)
        SURFACE.blit(sysfont.render("{}".format(self.name),True,(colors[1])),(self.rect.left+self.rect.width/2-45/2,self.rect.top+self.rect.height/2-15/2))
        
    def click(self,pos,theother,current):
        if self.rect.collidepoint(pos) and self.handler:
            self.handler(current)
    
def draw(current,account,buy,sell):
    global tradingprice
    SURFACE.fill(colors[5])
    gap=current%100
    upperline=current-gap+300
    for i in range(0,600,100):
        if upperline-i>=0:
            pygame.draw.line(SURFACE,colors[7],(0,i+gap),(800,i+gap),1)
            SURFACE.blit(sysfont2.render("{}".format((upperline-i)*stock),True,colors[4],colors[5]),(10,i+gap-5))
    SURFACE.blit(sysfont.render("{}".format(current*stock),True,colors[6],colors[5]),(540,310))
    SURFACE.blit(sysfont.render(" Account: {} ".format(account),True,colors[4],colors[5]),(550,65))
    SURFACE.blit(sysfont3.render("FTC Inc.",True,colors[4],colors[5]),(70,40))
    if buy.ispressed or sell.ispressed:
        SURFACE.blit(sysfont.render("Trade price: {}".format(tradingprice),True,colors[4]),(557,85))
        if buy.ispressed:
            Return=current*stock-tradingprice
        elif sell.ispressed:
            Return=-1*current*stock+tradingprice
        if Return>0:
            SURFACE.blit(sysfont.render("(+{})".format(Return),True,colors[2],colors[5]),(675,105))
        elif Return<0:
            SURFACE.blit(sysfont.render("({})".format(Return),True,colors[3],colors[5]),(675,105))
    buy.paint()
    sell.paint()
def drawchart(points):
    global max
    for j in range (max):
        if j != max-1:
            point1=(points[j].left,600-points[j].top)
            point2=(points[j+1].left,600-points[j+1].top)
            pygame.draw.line(SURFACE,colors[6],point1,point2)    
def buyaction(current):
    global account,boom,recession,tradingprice,framecount,sell,buy,changedframe
    if sell.ispressed:
        tradingprice=0
        sell.ispressed=False
        account-=stock*current
        boom=True
        recession=False
    else:
        buy.ispressed=True
        turn=randint(5,20)
        changedframe=framecount//13
        if account>current:
            if randint(1,3)==2:
                boom=True
                recession=False
            else:
                boom=False
                recession=True
            account-=current*stock
            tradingprice=current*stock
def sellaction(current):
    global account,boom,recession,tradingprice,turn,framecount,sell,buy,changedframe
    if buy.ispressed:
            buy.ispressed=False
            account+=stock*current
            boom=True
            recession=False
            tradingprice=0
    else:
        sell.ispressed=True
        turn=randint(3,9)
        changedframe=framecount//13
        if account>current:
            if randint(1,3)==2:
                recession=True
                boom=False
        else:
                recession=False
                boom=True
        tradingprice=current*stock
        account+=current*stock
def drawgameover():
    SURFACE.blit(sysfont3.render("GAMEOVER",True,colors[7],colors[5]),(230,260))



def main():
    global account,boom,recession,bubble,tradingprice,turn,framecount,sell,buy
    points=[]
    game_over=False
    next=None
    mousepos=[]
    cg=0
    gs=0
    price=10000
    framecount=0
    turn=randint(5,12)
    changedframe=0
    buy=Button("Buy",Rect(400,500,200,100),colors[2],False)
    buy.handler = buyaction
    sell=Button("Sell",Rect(600,500,200,100),colors[3],False)
    sell.handler = sellaction
    for point in range(max):
        points.append(Rect(point*60,randint(1300,1500),0,0))
    cg=points[-1].top-300
    points=[x.move(0,-cg) for x in points]
    gs=cg
    current=gs+300
    start=current

    while True:
        framecount+=1
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.quit()
            if  event.type==MOUSEBUTTONDOWN:
                buy.click(event.pos,sell,current)
                sell.click(event.pos,buy,current)
                  
        if not game_over and framecount%13==0:
            if framecount//13==turn+changedframe:
                if bubble:
                    bubble=False
                    boom=True
                    recession=False
                if randint(1,4)==2:
                    boom = not boom
                    recession = not recession
                    turn=randint(1,10)
                if randint(1,20)==7:
                    bubble=True
                    boom=False
                    recession=False
                    turn=randint(12,20)
                changedframe=framecount//13
            if boom:
                if randint(1,5)==1:
                    next=randint(current-20,current)
                else:
                    next=randint(current,current+80)
            elif recession:
                if randint(1,5)==1:
                    next=randint(current,current+20)
                else:
                    next=randint(current-80,current)
            elif bubble:
                if randint(1,5)==1:
                    next=randint(current-20,current)
                else:
                    next=randint(current,current+800)
            next-=gs
            points.append(Rect(600,next,0,0))
            del points[0]
            cg=points[-1].top-300
            gs+=cg
            points=[x.move(-600/max,-cg) for x in points]  
            current=gs+300
        if current<=0 or account<=0:
            game_over=True
            drawgameover()
        else:
            draw(current,account,buy,sell)
            drawchart(points)
        pygame.display.update()
        FPSCLOCK.tick(10)

if __name__=='__main__':
    main()