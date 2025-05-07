from math import *
import random
from ion import *
from random import randint
from ion import keydown
from time import monotonic as mntnc,sleep
from kandinsky import fill_rect as rect, draw_string as text
from kandinsky import *
import time
projectiles={}
player={"default_hp":600,"hp":600,"x":200,"y":100,"size":25,"color":(255,50,50),"timeout":time.monotonic()+0.5}
boss={"default_hp":25000,"hp":25000,"x":0,"y":100,"size":50,"color":(255,50,50),"timeout":time.monotonic()+0.5}
def progression_bar(percent,fixedpercent):
  fill_rect(int(percent)*3-1 , 0, 300, 5, (0,0,0))
  fill_rect(0, 0, int(percent)*3, 5, (255,50,50))
  draw_string(percent,300,0,(0,0,0),(255,50,50))
  
def damaged():
  fill_rect(0, 0, 320, 230, color(255, 50, 50))
  draw_string("-200",player["x"],player["y"])
  time.sleep(0.1)
  blackout()
def level():
  blackout()
  draw_string("CHOOSE THE LEVEL",0,200)
  draw_string("[1] Easy",100,25)
  draw_string("[2] Medium",100,50)
  draw_string("[3] Hard",100,75)
  time.sleep(0.8)
  while True:
    if keydown(KEY_ONE):
      boss["hp"]=25000//2
      boss["default_hp"]=25000//2
      start()
    if keydown(KEY_TWO):
      boss["hp"]=25000
      boss["default_hp"]=25000
      start()
    if keydown(KEY_THREE):
      boss["hp"]=25000*2
      boss["default_hp"]=25000*2
      start()
def blackout():
  fill_rect(0, 0, 320, 230, color(0, 0, 0))
def start():
  blackout()
  draw_string("WELCOME TO BAD BOSS",0,200)
  draw_string("[OK] Start",100,75)
  draw_string("[EXE] Level",100,50)
  draw_string("[DEL] Exit",100,100)
  time.sleep(0.8)
  while True:
    if keydown(KEY_BACKSPACE):
      input()
      break
    if keydown(KEY_OK):
      game()
    if keydown(KEY_EXE):
      level()
def refresh():
  fixedpercent=100
  percent=str(int(boss["hp"]/boss["default_hp"]*100))
  if percent!="100":
    percent+=" "
  progression_bar(percent,fixedpercent)
  #draw_string(percent,0,0,(255,50,50))
  draw_char(boss)
  draw_char(player)
  fixedpercent-=1
def lose():
  for c in [(0,0,0),(255,255,255)]:
    for y in range(195,10):
      sleep(0.016)
      rect(0,y,295,10,c)
  draw_string("YOU DIED!",295//2-50,100, (0,0,0),(255,50,50))
  sleep(1.5)
  draw_string("[OK] Try again",295//2-50,150, (0,0,0),(255,50,50))
  draw_string("[EXE] Level",100,175,(0,0,0),(255,50,50))  
  while True:
    if keydown(KEY_OK):
      game()
      break
    if keydown(KEY_EXE):
      level()
      break
def win():
  for c in [(0,0,0),(255,255,255)]:
    for y in range(195,10):
      sleep(0.016)
      rect(0,y,295,10,c)
  draw_string("YOU WON!",295//2-50,100, (0,0,0),(50,255,50))
  sleep(1.5)
  draw_string("[EXE] Level",100,175,(0,0,0),(50,255,50))
  draw_string("[OK] Try again",295//2-50,150, (0,0,0),(50,255,50))
  while True:
    if keydown(KEY_OK):
      game()
      break
    if keydown(KEY_EXE):
      level()
      break
          
def game():
  blackout()
  started=True
  percent=str(boss["hp"]//boss["default_hp"]*100)
  draw_char(boss)
  draw_char(player)
  projcount=1
  while started:
    if player["hp"]<=200:
      blackout()
      
    if boss["timeout"]<=time.monotonic():
      boss["timeout"]=time.monotonic()+int(percent)/400
      projectiles[projcount]={"damage_hp":200,"target":[player["x"],player["y"]],"x":boss["x"]+boss["size"]//2,"y":boss["y"]+boss["size"]//2,"size":10,"color":(155,50,50)}
      projcount+=1
      
    if keydown(KEY_LEFT):
      if player["x"]<0:
        pass
        #boss["x"]+=1
        #fill_rect(boss["x"]-1, boss["y"],1, boss["size"], color(0, 0, 0))
      else:
        player["x"]-=2
      fill_rect(player["x"]+player["size"], player["y"],2, player["size"], color(0, 0, 0))
      fill_rect(player["x"]+player["size"]+5, player["y"]-20,2, player["size"], color(0, 0, 0))
      draw_char(player)
    if keydown(KEY_RIGHT):
      if player["x"]>295:
        pass
        #boss["x"]-=1
        #fill_rect(boss["x"]+boss["size"], boss["y"],1, boss["size"], color(0, 0, 0))
      else:
        player["x"]+=2
      fill_rect(player["x"]-2, player["y"], 2, player["size"], color(0, 0, 0))
      fill_rect(player["x"]-2, player["y"]-20,2, player["size"], color(0, 0, 0))
      draw_char(player)
    if keydown(KEY_UP):
      if player["y"]<0:
        pass
        #boss["y"]+=1
        #fill_rect(boss["x"], boss["y"]-1,boss["size"], 2, color(0, 0, 0))
      else:
        player["y"]-=2
      fill_rect(player["x"], player["y"]+player["size"], player["size"], 2, color(0, 0, 0))
      draw_char(player)
    if keydown(KEY_DOWN):
      if player["y"]>195:
        pass
        #boss["y"]-=1
        #fill_rect(boss["x"], boss["y"]+boss["size"],boss["size"], 1, color(0, 0, 0))
      else:
        player["y"]+=2
      fill_rect(player["x"], player["y"]-2, player["size"], 2, color(0, 0, 0))
      draw_char(player)
    handle_proj()
    handle_boss()
    refresh()
    if player["hp"]<=0:
      started=False
      for g,proj in projectiles.items():
        projectiles.pop(g)
      player["hp"]=player["default_hp"]
      boss["hp"]=boss["default_hp"]
      boss["x"]=0
      boss["y"]=100
      player["x"]=200
      player["y"]=100
      #projectiles={}
      #player={"default_hp":600,"hp":600,"x":200,"y":100,"size":25,"color":(255,50,50),"timeout":time.monotonic()+0.5}
      #boss={"default_hp":10000,"hp":10000,"x":100,"y":100,"size":50,"color":(255,50,50),"timeout":time.monotonic()+0.5}
      blackout()
      lose()
    if boss["hp"]<=0:
      started=False
      for g,proj in projectiles.items():
        projectiles.pop(g)
      player["hp"]=player["default_hp"]
      boss["hp"]=boss["default_hp"]
      boss["x"]=0
      boss["y"]=100
      player["x"]=200
      player["y"]=100
      blackout()
      win()
        

def draw_char(json):
  #rect(int(json["x"])-1,int(json["y"])-1,int(json["size"])+2,int(json["size"])+2,(0,0,0))
  rect(int(json["x"]),int(json["y"]),int(json["size"]),int(json["size"]),json["color"])
  
  if json["color"]!=(155,50,50):
    s_eye=json["size"]//4
    x_eye=int(json["x"])+json["size"]//2
    c_eyes=(0,0,0)
    
    rect(x_eye-s_eye-1,int(json["y"])+json["size"]//2-s_eye//2,int(s_eye),int(s_eye),c_eyes)
    rect(x_eye+1,int(json["y"])+json["size"]//2-s_eye//2,int(s_eye),int(s_eye),c_eyes)

    draw_string(str(json["hp"])+" ",json["x"],int(json["y"]-20),(255,50,50),(0,0,0))
def handle_boss():
  if boss["x"]<player["x"]:
    boss["x"]+=1
    fill_rect(boss["x"]-1, boss["y"], 1, boss["size"], color(0, 0, 0))
      
  if boss["x"]>player["x"]:
    boss["x"]-=1
    fill_rect(boss["x"]+boss["size"], boss["y"],1, boss["size"], color(0, 0, 0))

  if boss["y"]<player["y"]:
    boss["y"]+=1
    fill_rect(boss["x"], boss["y"]-1, boss["size"], 1, color(0, 0, 0))
      
  if boss["y"]>player["x"]:
    boss["y"]-=1
    fill_rect(boss["x"], boss["y"]+boss["size"], boss["size"], 1, color(0, 0, 0))
      
      
def handle_proj():
  for o,json in projectiles.items():
    rect(int(json["x"]),int(json["y"]),int(json["size"]),int(json["size"]),json["color"])
    
    #projectiles[o]["target"][0]=player["x"]
    #projectiles[o]["target"][1]=player["y"]
    if projectiles[o]["x"]<projectiles[o]["target"][0]:
      projectiles[o]["x"]+=1
      fill_rect(projectiles[o]["x"]-1, projectiles[o]["y"], 1, projectiles[o]["size"], color(0, 0, 0))
      
    if projectiles[o]["x"]>projectiles[o]["target"][0]:
      projectiles[o]["x"]-=1
      fill_rect(projectiles[o]["x"]+projectiles[o]["size"], projectiles[o]["y"],1, projectiles[o]["size"], color(0, 0, 0))

    if projectiles[o]["y"]<projectiles[o]["target"][1]:
      projectiles[o]["y"]+=1
      fill_rect(projectiles[o]["x"], projectiles[o]["y"]-1, projectiles[o]["size"], 1, color(0, 0, 0))
      
    if projectiles[o]["y"]>projectiles[o]["target"][1]:
      projectiles[o]["y"]-=1
      fill_rect(projectiles[o]["x"], projectiles[o]["y"]+projectiles[o]["size"], projectiles[o]["size"], 1, color(0, 0, 0))
      
    if projectiles[o]["x"]>=player["x"] and projectiles[o]["x"]<=player["x"]+player["size"] and projectiles[o]["y"]>=player["y"] and projectiles[o]["y"]<=player["y"]+player["size"]:
      player["hp"]-=projectiles[o]["damage_hp"]
      damaged()
      projectiles.pop(o)
      rect(int(json["x"]),int(json["y"]),int(json["size"]),int(json["size"]),(0,0,0))
    
    elif projectiles[o]["target"]==[projectiles[o]["x"],projectiles[o]["y"]]:
      boss["hp"]-=projectiles[o]["damage_hp"]
      projectiles.pop(o)
      rect(int(json["x"]),int(json["y"]),int(json["size"]),int(json["size"]),(0,0,0))
    
       
    #print(projectiles)        
start()
