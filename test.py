import random

num1 = random.randint(1,9) 
num2 = random.randint(1,9) 
num3 = random.randint(1,9) 
num4 = random.randint(1,9) 
num5 = random.randint(1,9) 
num6 = random.randint(1,9)
num7 = random.randint(1,9)

def thermal_purge_code():
    print("=============")
    print(num1, + num2, + num3, + num4, + num4, + num6, + num7)
    print("=============")

def thermal_purge_code_corrupt():
    print("=============")
    print(num1, + num2, + num3, + num4, + num4, )
    print("ERROR RECOVERING DATA")
    print("=============")

print("You log into the mainframe and attempt to recover the shutdown code")
fail_chance = random.randint(1, 100) #fail_chance number choosen by @katsumi143 on discord
if fail_chance < 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482:
    thermal_purge_code_corrupt()
if fail_chance > 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482:
    thermal_purge_code()