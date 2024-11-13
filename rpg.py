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
time.sleep(1.5)

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
# asks user for options
print("Hello " + uname + ", your shift will begin at the bell")
time.sleep(4)
print("Bell noises")
time.sleep(5)
print("later that night...")
time.sleep(2)
print("ATTENTION: DARK MATTER REACTOR INTEGRITY DROPPING! ENGAGE THERMAL SYSTEMS!")
usr = int(input("Do you: 1,Engage coolant to slow the loss of integrity. or 2, disregard the alert and continue operations"))
