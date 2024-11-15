# QSERF text RPG
# Briged McCarthy 2024

# Project dependencies 
import os
import time




WHITE_CYAN = "\x1b[1;34;44m" # I know its not white cyan! im to lazy to change it
RESET = "\x1b[1;0;0m"

#DMR systems
dmr_online = 0
integrity = 100
coolant = 0
#option menu

usr = False

# Header
print("Todays date is: 8/18/85")
print("Topside temperture is: 95°F with an estimated high of 105°")

# Username prompt 
def getname():
    uname = input("please enter your name: ")
    return uname

uname = getname()

os.system("clear") # for some reason removing this breaks the ascii logo
print("Welcome " + uname + " to the Quantum Science Energy Reaserch Facility")
print( RESET + """                     """ + WHITE_CYAN + """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@""" + RESET + """
                    """ + WHITE_CYAN + """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@""" + RESET + """
          """ + WHITE_CYAN + """@@@@@@@@@@@@@"""+ RESET +"""                    """ + WHITE_CYAN + """@@@@@@@@@@@@@@@@@@@@@""" + RESET + """
         """ + WHITE_CYAN + """@@@""" + RESET + """      """ + WHITE_CYAN + """@@@@@@@""" + RESET + """                """ + WHITE_CYAN + """@@@@@@@@@@@@@@@@@@@@@@""" + RESET + """
         """+ WHITE_CYAN + """@@@""" + RESET + """     """ + WHITE_CYAN + """@@@@""" + RESET + """  """ + WHITE_CYAN + """@@@@@@@""" + RESET + """      """ + WHITE_CYAN + """@@@@@@@""" + RESET + """  """ + WHITE_CYAN + """@@@@@@@@@@@@@@@@@""" + RESET + """
          """ + WHITE_CYAN + """@@@""" + RESET + """   """ + WHITE_CYAN + """@@@@""" + RESET + """        """ + WHITE_CYAN + """@@@@@@@@@@""" + RESET + """        """ + WHITE_CYAN + """@@@@@@@@@@@@@@@""" + RESET + """
           """ + WHITE_CYAN + """@@@@@@@@""" + RESET + """          """ + WHITE_CYAN + """@@@@@@@@ """ + RESET + """          """ + WHITE_CYAN + """@@@@@@@@@@@@@""" + RESET + """
             """ + WHITE_CYAN + """@@@@@""" + RESET + """        """ + WHITE_CYAN + """@@@@@""" + RESET + """    """ + WHITE_CYAN + """@@@@@""" + RESET + """        """ + RESET + """ """ + WHITE_CYAN + """@@@@@@@@@@""" + RESET + """
             """ + WHITE_CYAN + """@@@@@""" + RESET + """     """ + WHITE_CYAN + """@@@@@""" + RESET + """          """ + WHITE_CYAN + """@@@@@""" + RESET + """     """ + WHITE_CYAN + """@@@@@@@@@""" + RESET + """
           """ + WHITE_CYAN + """@@@@@""" + RESET + """ """ + WHITE_CYAN + """@@@@@@@@""" + RESET + """       """ + WHITE_CYAN + """@@""" + RESET + """       """ + WHITE_CYAN + """@@@@@@@@""" + RESET + """ """ + WHITE_CYAN + """@@@@@@""" + RESET + """
          """ + WHITE_CYAN + """@@@@@""" + RESET + """   """ + WHITE_CYAN + """@@@@@""" + RESET + """        """ + WHITE_CYAN + """@@@@""" + RESET + """        """ + WHITE_CYAN + """@@@@@""" + RESET + """   """ + WHITE_CYAN + """@@@@""" + RESET + """
         """ + WHITE_CYAN + """@@@@@@@@@@@""" + RESET + """ """ + WHITE_CYAN + """@@@@@""" + RESET + """              """ + WHITE_CYAN + """@@@@@""" + RESET + """ """ + WHITE_CYAN + """@@@@@@@@""" + RESET + """
        """ + WHITE_CYAN + """@@@@@@@@@@""" + RESET + """      """ + WHITE_CYAN + """@@@@""" + RESET + """          """ + WHITE_CYAN + """@@@@""" + RESET + """      """ + WHITE_CYAN + """@@@@@""" + RESET + """
       """ + WHITE_CYAN + """@@@@@@@@@@@""" + RESET + """         """ + WHITE_CYAN + """@@@@@""" + RESET + """  """ + WHITE_CYAN + """@@@@@""" + RESET + """         """ + WHITE_CYAN + """@@@@@@""" + RESET + """
      """ + WHITE_CYAN + """@@@@@@@@@@@@@""" + RESET + """           """ + WHITE_CYAN + """@@@@@@""" + RESET + """           """ + WHITE_CYAN + """@@@@""" + RESET + """ """ + WHITE_CYAN + """@@@""" + RESET + """  
     """ + WHITE_CYAN + """@@@@@@@@@@@@@@@""" + RESET + """       """ + WHITE_CYAN + """@@@@@@@@@@@@""" + RESET + """       """ + WHITE_CYAN + """@@@@""" + RESET + """   """ + WHITE_CYAN + """@@@""" + RESET + """  
    """ + WHITE_CYAN + """@@@@@@@@@@@@@@@@@@@@@@@@@""" + RESET + """        """ + WHITE_CYAN + """@@@@@@@@@@@@""" + RESET + """     """ + WHITE_CYAN + """@@@""" + RESET + """
   """ + WHITE_CYAN + """@@@@@@@@@@@@@@@@@@@@@""" + RESET + """                  """ + WHITE_CYAN + """@@@@@@@@@@@@@@@""" + RESET + """
  """ + WHITE_CYAN + """@@@@@@@@@@@@@@@@@@@@@@""" + RESET + """                  """ + WHITE_CYAN + """@@@@@""" + RESET + """ """ + WHITE_CYAN + """@@@@@@@""" + RESET + """  
 """ + WHITE_CYAN + """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@""" + RESET + """
""" + WHITE_CYAN + """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@""" + RESET + """ """)
time.sleep(5)
print(RESET)
dmr_key = input("Turn the key to enable the DMR? ")
# DMR startup
if dmr_key == "yes" or "y" or "Yes":
    print("Reactor core ignition sequence primed, please vacate the core chamber immediately!")
    time.sleep(3)
    print("Gravitational lasers ONLINE, raising core superstructure to center position")
    time.sleep(2)
    print("Dark Matter reactor superstructure has been raised to center position")
    time.sleep(3)
    print("Activating power lasers...")
    time.sleep(2)
    print("Opening combustion intake valves...")
    time.sleep(1)
    print("Power lasers ONLINE.")
    time.sleep(2)
    print("Dark Matter reactor ONLINE, converting power back to main facility grid ")
    time.sleep(3)
    dmr_online = 1
# imported from testing 
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
print("ATTENTION! DARK MATTER REACTOR INTEGRITY MONTERING SYSTEM PREIMPTION PROTOCAL INITIATED, ENGAGING CODE RED EMERGENCY!")
time.sleep(5)
print("Attention reactor operations control room personel, you are instructed to attempt a reactor shutdown before evacuation the facility, attempting to flee will have you terminated on sight, this is your only warning.")
time.sleep(3)
print("Estimating time of reactor destruction...")