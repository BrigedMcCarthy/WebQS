# Used for testing parts of the main script
# Test code below


import time

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
    option1 = 1
else:
    print("*You press the alarm silence button on the main console*")
    option1 = 2