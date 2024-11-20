import random
import math
import time

clock = 20

def code_gen(n):
  code = ''
  for i in range(n):
    code = " ".join([code, str(random.randint(1,9))]).lstrip()
  return code

print("You log into the mainframe and attempt to recover the shutdown code")

print("=============")

fail_chance = random.randint(1, 100) #fail_chance number choosen by @katsumi143 on discord

if fail_chance < math.pi:
#redundant because fail_chance can only be a int, use < 4
  print(str(code_gen(5)))
  print("ERROR RECOVERING DATA")
else:
  print(str(code_gen(7)))

print("=============")

print("Get sometime to write the shutdown code down on. Ill give you 20 seconds")
for i in range(21):
    print(clock)
    clock -= 1
    time.sleep(0)
yesno = "yes"

while yesno == "yes" or "Yes":
  if yesno == "no" or "No":
    yesno = input("Did you write it down?: ")
  elif yesno == "yes" or "Yes":
    print("hello world")
    break