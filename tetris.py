from math import *
from random import *
from kandinsky import fill_rect as rect, get_pixel as gpix, draw_string as ds, color
from ion import keydown as kd
from ion import *
from time import *

wh=color(255,255,255)
bl=color(0,0,0)

def init():
  rect(0,0,320,240,bl)
  global ikicks,bsys,dropspeed,kickdata,scoresys,scoretitles,keys,whiteline,tetraminos,matrix,colors,levelsys
  colors=[(0,255,255),(255,255,0),(200,0,255),(255,150,0),(0,0,255),(255,0,0),(0,255,0)]  
  tetraminos=[
  [[2,3,3,3,3],[0,0,1,2,0,0,1,2,0,0,1,2,0,0,3],[2,2,3,3,3,3],[0,1,2,0,1,2,0,1,2,0,3],0],
  [[0,1,1,2,0,3,3],1],
  [[0,1,2,3,3,3],[0,1,2,0,1,3,2,0,3],[2,3,1,3,2,0,3],[0,1,2,3,1,2,0,3],2],
  [[0,0,1,2,3,3,3],[0,1,2,0,1,2,0,3,3],[2,1,3,3,2,3],[3,1,2,0,1,2,0,3],3],
  [[1,2,3,3,3],[0,1,3,2,0,1,2,0,3],[2,3,3,1,2,0,0,3],[0,1,2,0,1,2,3,3],4],
  [[3,1,2,0,3,3],[0,0,1,2,0,1,3,2,0,3],[2,3,1,2,0,3,3],[0,1,2,1,3,2,3],5],
  [[0,1,3,2,3,3],[0,1,2,0,3,1,2,0,0,3],[2,0,1,3,2,3,3],[1,2,3,1,2,0,3],6]]
  kickdata=[[(-1,0),(-1,-1),(0,2),(-1,2)],[(1,0),(1,1),(0,-2),(1,-2)],[(1,0),(1,-1),(0,2),(1,2)],[(-1,0),(-1,1),(0,-2),(-1,-2)],
  [(-2,0),(1,0),(-2,1),(1,-2)],[(2,0),(-1,0),(2,-1),(-1,2)],[(-1,0),(2,0),(-1,-2),(2,1)],[(1,0),(-2,0),(1,2),(-2,-1)]]
  ikicks=[[0,5,0,7],[4,0,7,0],[0,6,0,4],[6,0,5,0]]
  scoresys=[[0,100,300,500,800],[100,400,1200,1600],[0,1200,1800,2400,1200],[100,200,400,1200],[0,0,600,2400]]
  levelsys=[0,1,3,5,8]
  bsys=[[0,0,0,0,1],[1,1,1,1],[1,1,1,1,1],[0,0,1,1],[0,0,1,1]]
  scoretitles=[["         ","Single","Double","Triple","Tetris"],["M T-S","T-S S","T-S D","T-S T"],
  ["","T-S B","T-S D B","T-S T B","Tetris B"],["M T-S","M T-S S","M T-S D","T-S T"],["","","T-S M D B","T-S T B"]]
  bt=(120,120,120)
  rect(110,0,100,230,wh)
  for ys in range(0,230,10):
    square(100,ys,bt)
    square(210,ys,bt)
  for xs in range(110,210,10):
    square(xs,220,bt)
  rect(110,19,100,1,(255,0,0))
  for ys in range(40,190,10):
    for xs in range(240,300,10):
      square(xs,ys,bt)
  for ys in range(80,140,10):
    for xs in range(240,300,10):
      square(xs-220,ys-40,bt)
  rect(250,50,40,130,bl)
  rect(30,50,40,40,bl)
  if mode%3!=1:
    ds("Score :",15,110,wh,bl)
    ds("0000000",15,130,wh,bl)
  else:
    ds("Lines :",15,110,wh,bl)
    ds("00/40",15,130,wh,bl)
  if mode%3==0:
    ds("Level :",15,160,wh,bl)
    ds("01",65,180,wh,bl)
  else:
    ds("Time :",15,160,wh,bl)
    ds("00:00.00",15,180,wh,bl)
  for tm in range(3):
    ds(str(3-tm),155,110)
    sleep(1)
  ds(" ",155,110)
  game()
  
def game():
  x,y,px,py=140,20,150,10
  t=randrange(0,7)
  wait=-1
  rot=0
  plowest=500
  next=[[0]*8,[-1]+[0]*7,[-1]]
  next[0]=randombag()
  next=nextt(next)
  hold,holdtemp,holdallowed=-1,0,True
  score,combo=0,0
  level= 1 if mode==0 else speed
  xp=0
  btob=0
  end=False
  mono=monotonic()
  mt=monotonic()
  coolr=0
  lines=0
  coolh=monotonic()
  arr=True
  while end==False:
    px,py,prot=x,y,rot
    move=[0]*4
    if kd(52):
      while kd(52):
        pass
      while not kd(52):
        ds("Paused",240,205,wh,bl)
        ds("7-Restart",5,5,wh,bl)
        ds("Menu-9",240,5,wh,bl)
        if kd(30):
          init()
        if kd(32):
          menu(mode,speed)
      ds("      ",240,205,wh,bl)
      ds("         ",5,5,wh,bl)
      ds("      ",240,5,wh,bl)
      while kd(52):
        pass
      for tm in range(3):
        ds(str(3-tm),10,200,wh,bl)
        sleep(1)
      ds(" ",10,200,wh,bl)
    if (mt+(0.8-(level-1)*0.007)**(level-1)<=monotonic() and not kd(2)) or (mt+0.03<=monotonic() and kd(2)):
      y+=10
      mt=monotonic()
      move[1]=1
      
    if kd(17) and holdallowed:
      if hold==-1:
        hold=next[0][0]
        next=nextt(next)
      refresh(t,px,py,prot)
      refresh(t,px,plowest,prot)
      holdtemp=hold
      hold=t
      rect(30,50,40,40,bl)
      tetra(30,60,hold,0)
      t=holdtemp
      holdallowed=False
      x,y,rot,px,py,prot,plowest=140,10,0,140,10,0,500
    if kd(0) and coolh<=monotonic():
      x-=10
      coolh=monotonic()+0.03+int(arr)*0.14
      arr=False
      move[0]=1
    if not (kd(3) or kd(0)):
      coolh=monotonic()
      arr=True
    if kd(3) and coolh<=monotonic():
      x+=10
      coolh=monotonic()+0.03+int(arr)*0.14
      arr=False
      move[0]=1
    if kd(42):
      move[3]=1
      y=plowest
      wait=monotonic()
      
    if kd(4):
      coolr+=1
    else:
      coolr=0
    if coolr==1:
      rot=(rot+(1-2*int(kd(12))))%(len(tetraminos[t])-1)
      move[2]=1
    timer=monotonic()-mono
    timems=str(int((timer-floor(timer))*100))
    timem=floor(int(timer)/60)
    times=str(int(timer)-60*timem)
    if mode!=0:
      ds(timems,75,180,wh,bl)
      ds(str(timem),25-len(str(timem)),180,wh,bl)
      ds(times,65-len(times)*10,180,wh,bl)
    if (mode==1 and lines>=40) or (mode==2 and timem>=3):
      while kd(4):
        pass
      ds("Victory",125,60)
      ds("[OK] Back to menu",75,80)
      while not kd(4):
        pass
      menu(mode,speed)
    if px!=x or py!=y or prot!=rot:
      refresh(t,px,py,prot)
      refresh(t,px,plowest,prot)
      rect(110,19,100,1,(255,0,0))
      x_,y_=x,y
      for tests in range(7-int(prot==rot)*4):
        cur=tetraminos[t][rot]
        tempx,tempy=x_,y_
        for i in range(len(cur)):
          if cur[i]==0:
            tempx+=10
          if cur[i]==1 or cur[i]==3:
            if not gpix(tempx,tempy)==wh:
              if tests==0:
                y,y_,move[1]=py,py,0
              elif tests==1:
                x,x_,move[0]=px,px,0
              elif 6>tests>=2 and prot!=rot:
                if tests<5:
                  iskicked=True
                else:
                  iskicked=False
                x_,y_=x,y
                if t==0:
                  ikick=ikicks[rot][prot]
                  x_+=kickdata[ikick][tests-2][0]*10
                  y_+=kickdata[ikick][tests-2][1]*10
                elif t>=2:
                  if prot==0 or prot==2:
                    x_+=kickdata[rot-1][tests-2][0]*10
                    y_+=kickdata[rot-1][tests-2][1]*10
                  else:
                    x_+=kickdata[prot][tests-2][0]*10
                    y_+=kickdata[prot][tests-2][1]*10
                elif t==1 or (prot==rot and t==2):
                  tests=6
              elif tests==6:
                rot,move[2]=prot,0
              break
            tempx+=10
          if cur[i]==2:
            tempy+=10
            tempx=x_
      if prot!=rot:
        x,y=x_,y_
      hasmoved=True
      if move[3]==1:
        lastmove=3
        hasmoved=False
      elif move[2]==1:
        lastmove=2
      elif move[1]==1:
        lastmove=1
      elif move[0]==1:
        lastmove=0
      else:
        #lastmove=-1
        hasmoved=False
      cur=tetraminos[t][rot]
      tempx,tempy=x+2,y+2
      for i in range(len(cur)):
        if cur[i]<=1:
          tempx+=10
        if cur[i]==3:
          if not gpix(tempx,tempy+10)==wh:
            if wait==-1 or hasmoved:
              wait=monotonic()+.5
            py=y
            if wait<=monotonic():
              wait=-1
              tetra(x,y,t,rot)
              holdallowed=True
              sline=0
              for ys_ in range(20):
                ys=20-ys_
                line=0
                for xs in range(112,212,10):
                  if gpix(xs,12+ys*10)!=wh:
                    line+=1
                if line==10:
                  pass
                  sline+=1
                  temp_y=10+ys*10
              scoring=0
              if sline==0:
                combo=0
              else:
                score+=combo*50*level
                combo+=1
              if t==2 and lastmove==2:
                c=0
                for adj in range(4):
                  ads=gpix(5+x+floor(adj%2)*20,5+y+floor(adj/2)*20)
                  if ads!=wh:
                    c+=1
                  else:
                    if (rot%2==0 and (adj==rot or adj==rot+1)) or (rot%2==1 and (adj==1-(rot-1)/2) or adj==3-(rot-1)/2):
                      scoring=3
                if c>=3:
                  if scoring!=3:
                    scoring=1
                  if iskicked:
                    scoring=3
                elif scoring==3:
                  scoring=0
              xp+=levelsys[sline]
              if xp>=10 and mode%3==0:
                if level<15:
                  level+=1
                xp=0
              if bsys[scoring][sline]==1:
                btob+=1
              elif sline!=0:
                btob=0
              if btob>=2:
                if scoring!=3:
                  scoring=2
                else:
                  scoring=4
              lines+=sline
              if mode==0:
                score+=scoresys[scoring][sline]*level
              else:
                score+=scoresys[scoring][sline]
              title=scoretitles[scoring][sline]
              if mode!=1:
                ds(str(score),85-ceil(len(str(score)))*10,130,wh,bl)
              else:
                ds(str(lines),35-ceil(len(str(lines)))*10,130,wh,bl)
              if mode==0:
                ds(str(level),85-ceil(len(str(level)))*10,180,wh,bl)
              ds(scoretitles[0][0],5,5,wh,bl)
              ds(title,5,5,wh,bl)
              if bsys[scoring][sline]==1:
                btob=1
              if sline != 0 or scoring != 0:
                sleep(0.5)
              for ys_ in range(20):
                ys=20-ys_
                line=0
                for xs in range(112,212,10):
                  if gpix(xs,12+ys*10)!=wh:
                    line+=1
                if line==10:
                  rect(110,10+ys*10,100,10,wh)
                if not line==0:
                  a=0
                  temp_y=10+ys*10
                  temp_line=[0,0,0,0,0,0,0,0,0,0]
                  for xs in range(10):
                    temp_line[xs]=gpix(114+10*xs,temp_y+4)
                  
                  while a<10:
                    a=0
                    for xs in range(10):
                      if not gpix(112+10*xs,temp_y+12)==wh:
                        a+=1
                    if a==0:
                      rect(110,temp_y,100,10,wh)
                      temp_y+=10
                    else:
                      for xs_ in range(10):
                        if not temp_line[xs_]==wh:
                          square(110+10*xs_,temp_y,temp_line[xs_])
                      a=10                         
              for xd in range(112,212,10):
                if gpix(xd,12)!=wh:
                  #ded
                  pass
                  #end=True
              x,y,rot=140,0,0
              t=next[0][0]
              iskicked=False
              px,py,prot=x,y,rot
              next=nextt(next)
              sleep(0.2)
              break
          tempx+=10
        if cur[i]==2:
          tempy+=10
          tempx=x    


      plowest=getlowest(x,y,t,rot)
      outline(x,plowest,t,rot)
      
    tetra(x,y,t,rot)
  ds("GAME OVER",115,60)
  ds("[OK] Back to menu",75,80)
  while not kd(4):
    pass

def menu(mm, sm):
  global mode,speed
  mode,speed=mm,sm
  modetext=["Marathon (default)","Sprint 40 lines   ","Ultra 3 min        "]
  i=0
  draw_logo()
  while True:
    if i==0:
      ds("Press [EXE] to start",60,170,wh,bl)
      ds("[0] Options",105,190,wh,bl)
      if kd(48):
        i=1
        rect(0,0,320,240,bl)
        while kd(48):
          pass
      if kd(52):
        init()
        draw_logo()
  

    if i==1:
      ds("[Options]",10,10,wh,bl)
      ds("Mode : ",30,40,wh,bl)
      if mm%3!=0:
        ds("Speed : ",30,60,wh,bl)
        ds(str(speed) +"   ",120,60,wh,bl)
      else:
        ds("               ",30,60,wh,bl)
      ds(modetext[mode%3],110,40,wh,bl)
      if kd(4):
        mm+=1
        mode=mm%3
        while kd(4):
          pass
      sm+=int(kd(1))*int(speed<15)-int(kd(2)*int(speed>1))
      speed=sm
      sleep(0.12)
      if kd(48):
        i=0
        draw_logo()
        while kd(48):
          pass
def draw_logo():
  logo=[
  [1,1,1,0,2,2,2,0,3,3,3,0,4,4,4,0,5,0,0,6,6],
  [0,1,0,0,2,0,0,0,0,3,0,0,4,0,4,0,0,0,6,0,0],
  [0,1,0,0,2,2,0,0,0,3,0,0,4,4,0,0,5,0,0,6,0],
  [0,1,0,0,2,0,0,0,0,3,0,0,4,0,4,0,5,0,0,0,6],
  [0,1,0,0,2,2,2,0,0,3,0,0,4,0,4,0,5,0,6,6,0],
  ]
  logocolors=[(0,0,100),(255,0,0),(255,150,0),(255,255,0),(0,255,0),(0,255,255),(255,0,255)]
  bc=(0,0,150)
  rect(0,0,320,240,bl)
  rect(55,20,210,70,bc)
  rect(125,90,70,70,bc)
  rect(60,25,200,60,(0,0,100))
  rect(130,75,60,80,(0,0,100))
  for ym in range(5):
    for xm in range(21):
      rect(65+xm*9,32+ym*9,9,9,logocolors[logo[ym][xm]])

def outline(xt,yt,t,r):
  cur=tetraminos[t][r]    
  xl=xt
  c=colors[tetraminos[t][len(tetraminos[t])-1]]
  cl=list(c)
  for i in range(3):
    cl[i]=(cl[i]+255*5)/6

  c=tuple(cl)
  for i in range(len(cur)):       
    if cur[i]==0:
      xl+=10
    if cur[i]==1 or cur[i]==3:
      square(xl,yt,c)
      xl+=10
    if cur[i]==2:
      yt+=10
      xl=xt

      
def refresh(t,px,py,prot):  
  cur=tetraminos[t][prot]
  xtemp=px
  for i in range(len(cur)):
    if cur[i]==0:
      px+=10
    if cur[i]==1 or cur[i]==3:
      rect(px,py,10,10,wh)
      px+=10
    if cur[i]==2:
      py+=10
      px=xtemp
def tetra(xt,yt,t,r):
  cur=tetraminos[t][r]
  xl=xt
  for i in range(len(cur)):       
    if cur[i]==0:
      xl+=10
    if cur[i]==1 or cur[i]==3:
      square(xl,yt,colors[tetraminos[t][len(tetraminos[t])-1]])
      xl+=10
    if cur[i]==2:
      yt+=10
      xl=xt

def square(x,y,c):
  cd=list(c)
  for i in range(3):
    cd[i]/=2
  cd=tuple(cd)
  cl=list(c)
  for i in range(3):
    cl[i]=(cl[i]+255)/2
  rect(x+1,y+1,8,8,c)
  rect(x,y,9,1,cl)
  rect(x,y,1,9,cl)
  rect(x,y+9,9,1,cd)
  rect(x+9,y,1,10,cd)


def getlowest(x,y,t,r):
  cur=tetraminos[t][r]
  for ys in range(y,230,10):
    py,px=ys+5,x+5
    calcdone=False
    for i in range(len(cur)):
      if cur[i]==0:
        px+=10
      if cur[i]==1 or cur[i]==3:
        if not gpix(px,py)==wh:
          calcdone=True
          break
        px+=10
      if cur[i]==2:
        py+=10
        px=x+5
    if calcdone==True:
      return ys-10

def nextt(l):
  if l[1][0]==-1:
    l[1]=randombag()
  for i in range(14):
    l[floor(i/7)][i%7]=l[floor((i+1)/7)][(i+1)%7]
  l[2][0]=-1
  rect(250,50,40,130,bl)
  for ns in range(4):
    tetra(250,60+30*ns,l[0][ns],0)
  return l

def randombag():
  bag=[0,0,0,0,0,0,0]
  inbag=[0,1,2,3,4,5,6]
  for i in range(7):
    rand=randrange(0,len(inbag))
    bag[i]=inbag[rand]
    inbag.pop(rand)
  return bag

def start_notice():
  print("Tetris C 1985-2025 Tetris Holding.\nTetris logos, Tetris theme song and Tetriminos are trademarks of Tetris Holding.\nThe Tetris trade dress is owned by Tetris Holding.\nLicensed to The Tetris Company.\nTetris Game Design by Alexey Pajitnov.\nTetris Logo Design by Roger Dean.\nAll Rights Reserved.")
  sleep(.5)

start_notice()
menu(0,2)
