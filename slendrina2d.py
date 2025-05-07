from kandinsky import fill_rect as rect, draw_string as text
from ion import *
from random import *
from time import sleep
difficulty=1
player = {"x": 50, "y": 100, "size": 20, "hp": 100, "rotation": "r", "color": (50, 255, 50)}
slendrina = {"x": 200, "y": 100, "size": 20, "color": (0, 0, 0)}
flashlight_length = 80
flashlight_height = 30
slendrina_speed = 1
NUM_ITEMS=8
items=[{"x":randint(30,280),"y":randint(30,200),"collected":False}for _ in range(1)]
items_collected=0
def help():
  rect(0, 0, 320, 240, (255, 50, 50))
  text("""-Collect 8 keys to escape
-Do not look at slendrina"""
  ,0,100,(0,0,0),(255,40,40))
  text("[EXE] Back",100,75,(0,0,0),(255,40,40))
  sleep(0.8)
  while True:
    if keydown(KEY_EXE):
      start()
      break
def level():
  global difficulty
  rect(0, 0, 320, 240, (255, 50, 50))
  text("CHOOSE THE LEVEL",0,200,(0,0,0),(255,40,40))
  text("[1] Easy",100,25,(0,0,0),(255,40,40))
  text("[2] Medium",100,50,(0,0,0),(255,40,40))
  text("[3] Hard",100,75,(0,0,0),(255,40,40))
  text("[4] Extreme",100,100,(0,0,0),(255,40,40))
  text("[5] Impossible",100,125,(0,0,0),(255,40,40))
  sleep(0.8)
  while True:
    if keydown(KEY_ONE):
      difficulty=0.2
      break
      start()
    if keydown(KEY_TWO):
      difficulty=0.5
      break
      start()
    if keydown(KEY_THREE):
      difficulty=1
      break
      start()
    if keydown(KEY_FOUR):
      difficulty=2
      break
    if keydown(KEY_FIVE):
      difficulty=3
      break
      start()
def start():
  rect(0, 0, 320, 240, (255, 50, 50))
  text("SLENDRINA",0,200,(0,0,0),(255,40,40))
  text("[EXE] Start",100,75,(0,0,0),(255,40,40))
  text("[OK] Level",100,50,(0,0,0),(255,40,40))
  text("[DEL] Exit",100,100,(0,0,0),(255,40,40))
  text("[+] Help",100,125,(0,0,0),(255,40,40))
  sleep(0.8)
  while True:
    if keydown(KEY_EXE):
      break
    if keydown(KEY_BACKSPACE):
      hii 
    if keydown(KEY_OK):
      level()
      break
    if keydown(KEY_PLUS):
      help()
      break
        
def loading_screen():
    rect(0, 0, 320, 240, (255, 50, 50))
    text("SLENDRINA 2D", 100, 100, (255, 255, 255),(0,0,0))
    for x in range(17):
        rect(20 * x, 205, 20, 20, (0, 0, 0))
        sleep(0.1)

def draw_player():
    rect(player["x"], player["y"], player["size"], player["size"], player["color"])
    eye_offset = player["size"] // 4
    center_x = player["x"] + player["size"] // 2
    rect(center_x - eye_offset, player["y"] + 5, 3, 3, (0, 0, 0))
    rect(center_x + eye_offset, player["y"] + 5, 3, 3, (0, 0, 0))

def draw_slendrina():
    rect(slendrina["x"], slendrina["y"], slendrina["size"], slendrina["size"], slendrina["color"])

def draw_items():
  for item in items:
    if not item["collected"]:
      rect(item["x"],item["y"],5,10,(0,0,0))
      
def move_player():
    if keydown(KEY_LEFT):
        player["x"] -= 2
        player["rotation"] = "l"
    if keydown(KEY_RIGHT):
        player["x"] += 2
        player["rotation"] = "r"
    if keydown(KEY_UP):
        player["y"] -= 2
    if keydown(KEY_DOWN):
        player["y"] += 2

def slendrina_follow():
    if player["x"] > slendrina["x"]:
        slendrina["x"] += slendrina_speed
    elif player["x"] < slendrina["x"]:
        slendrina["x"] -= slendrina_speed

    if player["y"] > slendrina["y"]:
        slendrina["y"] += slendrina_speed
    elif player["y"] < slendrina["y"]:
        slendrina["y"] -= slendrina_speed

def draw_flashlight():
    if player["rotation"] == "r":
        rect(player["x"]+ player["size"], player["y"]-flashlight_height//2,
             flashlight_length, flashlight_height, (255, 255, 100))
    elif player["rotation"] == "l":
        rect(player["x"] - flashlight_length, player["y"]-flashlight_height//2,
             flashlight_length, flashlight_height, (255, 255, 100))

def is_slendrina_in_flashlight():
    if player["rotation"] == "r":
        in_x = slendrina["x"] >= player["x"] + player["size"] and slendrina["x"] <= player["x"] + player["size"] +flashlight_length
    else:
        in_x = slendrina["x"] + slendrina["size"] <= player["x"] and slendrina["x"] + slendrina["size"] >= player["x"] - flashlight_length
    in_y = slendrina["y"] + slendrina["size"] >= player["y"] - flashlight_height // 2 and slendrina["y"] <= player["y"] + player["size"]
    return in_x and in_y
def coll():
  return (player["x"]<slendrina["x"]+slendrina["size"] and player["x"] + player["size"]>slendrina["x"] and player["y"]<slendrina["y"]+slendrina["size"] and player["y"] + player["size"]>slendrina["y"])
def check_item_collected():
  global items_collected
  for item in items:
    if not item["collected"]:
      if player["x"] < item["x"]+5 and player["x"]+player["size"] > item["x"] and player["y"]<item["y"]+10 and player["y"]+player["size"]>item["y"]:
        item["collected"]=True
        items_collected+=1
        items.append({"x":randint(30,280),"y":randint(30,200),"collected":False})    
def game_over():
    global player,slendrina,items,items_collected
    rect(0, 0, 320, 240, (0, 0, 0))
    text("YOU DIED", 120, 100, (255, 50, 50),(0,0,0))
    sleep(2)
    text("[EXE] Retry?",100,125,(255,50,50),(0,0,0))
    text("[OK] Menu",100,150,(255,50,50),(0,0,0))
    player = {"x": 50, "y": 100, "size": 20, "hp": 100, "rotation": "r", "color": (50, 255, 50)}
    slendrina = {"x": 200, "y": 100, "size": 20, "color": (0, 0, 0)}
    items=[{"x":randint(30,280),"y":randint(30,200),"collected":False}for _ in range(1)]
    items_collected=0
    while True:
      if keydown(KEY_EXE):
        game_loop()
        break
      if keydown(KEY_OK):
        start()
        game_loop()
        break
def win():
  global player,slendrina,items,items_collected
  rect(0,0,320,240,(0,0,0))
  text("YOU ESCAPED",100,100,(50,255,50),(0,0,0))
  sleep(2)
  text("[EXE] Retry?",100,125,(50,255,50),(0,0,0))
  text("[OK] Menu",100,150,(50,255,50),(0,0,0))
  player = {"x": 50, "y": 100, "size": 20, "hp": 100, "rotation": "r", "color": (50, 255, 50)}
  slendrina = {"x": 200, "y": 100, "size": 20, "color": (0, 0, 0)}
  items=[{"x":randint(30,280),"y":randint(30,200),"collected":False}for _ in range(1)]
  items_collected=0
  while True:
    if keydown(KEY_EXE):
      game_loop()
      break
    if keydown(KEY_OK):
      start()
      game_loop()
      break
              
def game_loop():
    global items_collected,difficulty
    r=0
    while True:
        sleep(0.009)
        rect(10, 10, 310, 215, (0, 0, 0))
        rect(0, 0, 10, 240, (r, 0, 0))
        rect(0, 0, 320, 10, (r, 0, 0))
        rect(310, 0, 10, 240, (r, 0, 0))
        rect(0, 215, 320, 10, (r, 0, 0))
        draw_flashlight()
        draw_items()
        draw_player()
        draw_slendrina()
        text("HP: " + str(int(player["hp"])), 5, 5, (255, 255, 255),(0,0,0))
        text("Keys: {}/{}".format(items_collected,NUM_ITEMS),5,20,(255,255,255),(0,0,0))
        move_player()
        slendrina_follow()
        check_item_collected()
        if is_slendrina_in_flashlight() or coll():
            player["hp"] -= difficulty
            if r<255:
              r+=difficulty*3
        else:
          if r>0:
            r-=1    

        if player["hp"] <= 0:
            game_over()
            break
        if items_collected==NUM_ITEMS:
          win()
          break

loading_screen()
start()
game_loop()
