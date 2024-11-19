import random
import math

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