from math import *
from random import *
from kandinsky import *
seeed=int(hash(input("seed: ")))
seed(seeed)
#print(seeed)
leng = 300//int(input("len :"))  
def reverse(s):
  return "".join(reversed(s))
pswd=""
maxx=300
chars=["a","b","c","d","e","f","A","B","C","D","E","F","1","2","3","4","5","6","7","8","9"]
for o in range(300//leng) :
  for x in range(0,maxx,1):
    for y in range(0,200,1):
      char=choice(chars)
      draw_string(char,x,y)
  pswd+=char
  
  maxx-=leng
oo=reverse(pswd)
print(oo)
