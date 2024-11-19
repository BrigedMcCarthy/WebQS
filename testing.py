# Used for testing parts of the main script
# Test code below


import time
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


option1 = 0

uname = input("please enter your name: ")

print("Hello " + uname + ", your shift will begin at the bell")
time.sleep(2)
print("*BELL*")
time.sleep(2)
print("later that night...")
time.sleep(2)
print("ATTENTION: DARK MATTER REACTOR INTEGRITY DROPPING! ENGAGE THERMAL SYSTEMS!")
usr = int(input("Do you: 1,Engage coolant to slow the loss of integrity. or 2, disregard the alert and continue operations: "))

if usr == 1:
    print("Activating coolant")
    time.sleep(2)
    print("coolant systems failure!")
    option1 = 1
else:
    print("*You press the alarm silence button on the main console*")
    option1 = 2
time.sleep(4)
print("Attention all reactor operations personel, we have discovered a fracture in the reactor coolant system")
time.sleep(2)
print("Attention! Dark matter reactor integrity at 75% Engage thermal systems!")
time.sleep(3)
print("Attention! Dark matter reactor integrity at 50% Engage thermal systems!")
time.sleep(2)
print("Attention! Dark matter reactor integrity at 25%")
time.sleep(3)
print("Dark matter reactor integrity monitering systems failure, attempting to reboot!")
time.sleep(4)
print("Reboot: Failure! integrity status UNKNOWN!")
time.sleep(2)
print("Pressure monitering systems failure! Pressure status UNKNOWN")
time.sleep(4)
print("All facility scientific personel please evacuate immediately! You have 11 minutes to reach minimum safe distance!")
time.sleep(4)
print("Attention all personel, a code red has been issues by the facility automated managment system, lockdown code has been overridden by the designated code bravo niner, please procede to the tarturus door for evacuation immediately, this is not a drill I repeat this is not a drill")
time.sleep(4)
print("ATTENTION! DARK MATTER REACTOR INTEGRITY MONTERING SYSTEM PREEMPTION PROTOCAL INITIATED, ENGAGING CODE RED EMERGENCY!")
time.sleep(5)
print("Attention reactor operations control room personel, you are instructed to attempt a reactor shutdown before evacuation the facility, attempting to flee will have you terminated on sight, this is your only warning.")
time.sleep(3)
print("Estimating time of reactor destruction...")
time.sleep(4)
print("Dark matter reactor explosion will occur in T-10 minutes! the option to shut down the reactor core will expire in t-5 minutes")
time.sleep(2)
thermal_choice = int(input("Where do you want to look for the shutdown code? Option 1: Break room Option 2: Attempt to recover deleted shutdown code from mainframe Option 3: Dont look for code "))

#thermal shutdown code options 

if thermal_choice == 1:
    print("You go into the break room and see a sticky note on the fridge with the numbers ")
    thermal_purge_code()
if thermal_choice == 2:
    print("You log into the mainframe and attempt to recover the shutdown code")
    fail_chance = random.randint(1, 100) #fail_chance number choosen by discord
    if fail_chance < 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482:
        thermal_purge_code_corrupt()
    if fail_chance > 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482:
        thermal_purge_code()