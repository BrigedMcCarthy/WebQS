#!/usr/bin/env python3
"""
Q.S.E.R.F TEXT RPG - Madison Research Institute Emergency Simulation
Set in the Quantum Universe - August 18th, 1985

Based on the lore of The Quantum Corporation by Briged McCarthy
A text-based survival game set during the catastrophic failure of the 
Dark Matter Reactor at the Madison Research Institute (Quantum Science 
Energy Research Facility).
"""

import os
import time
import random
import math
import sys
from typing import Optional

# ============================================================================
# AUDIO SYSTEM
# ============================================================================

try:
    from playsound import playsound as _playsound
    AUDIO_ENABLED = True
    def play_sound(sound: str) -> None:
        """Play audio file with error handling"""
        try:
            _playsound(sound)
        except Exception:
            pass
except (ImportError, ModuleNotFoundError):
    AUDIO_ENABLED = False
    def play_sound(sound: str) -> None:
        pass


# ============================================================================
# DISPLAY & FORMATTING
# ============================================================================

RESET = "\x1b[1;0;0m"
RED = "\x1b[1;31m"
YELLOW = "\x1b[1;33m"
WHITE = "\x1b[1;37m"
CYAN = "\x1b[1;36m"
GREEN = "\x1b[1;32m"
MAGENTA = "\x1b[1;35m"
BLUE = "\x1b[1;34m"
ALERT = "\x1b[1;31;44m"
DARK_ALERT = "\x1b[1;30;41m"

def clear_screen() -> None:
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def sprint(text: str, delay: float = 0.01) -> None:
    """Print text character by character"""
    for c in text + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)

def sprint_fast(text: str) -> None:
    """Print text quickly"""
    sprint(text, delay=0.005)

def sprint_slow(text: str) -> None:
    """Print text slowly"""
    sprint(text, delay=0.05)

def print_header(title: str) -> None:
    """Print formatted header"""
    print(f"\n{CYAN}{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}{RESET}\n")

def print_alert(message: str) -> None:
    """Print critical alert"""
    print(f"{DARK_ALERT} ⚠️  {message:^60} {RESET}")
    time.sleep(0.5)

def print_status(message: str) -> None:
    """Print status message"""
    print(f"{YELLOW}{message}{RESET}")

def print_success(message: str) -> None:
    """Print success message"""
    print(f"{GREEN}{message}{RESET}")

def print_error(message: str) -> None:
    """Print error message"""
    print(f"{RED}{message}{RESET}")

def print_system(message: str) -> None:
    """Print system message"""
    print(f"{BLUE}[SYSTEM] {message}{RESET}")

def print_reactor(message: str) -> None:
    """Print reactor status"""
    print(f"{MAGENTA}[DMR STATUS] {message}{RESET}")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def code_gen(n: int) -> str:
    """Generate random numeric code"""
    code = ''
    for i in range(n):
        code = "".join([code, str(random.randint(1, 9))]).lstrip()
    return code

def get_user_choice(prompt: str, valid_options: list) -> str:
    """Get validated user input"""
    while True:
        try:
            user_input = input(f"{CYAN}{prompt}{RESET}").strip().lower()
            if user_input in valid_options:
                return user_input
            print_error(f"Invalid choice. Valid options: {', '.join(valid_options)}")
        except (ValueError, KeyboardInterrupt):
            print_error("Invalid input. Please try again.")

def get_numeric_choice(prompt: str, min_val: int = 1, max_val: int = 3) -> int:
    """Get validated numeric input"""
    while True:
        try:
            choice = int(input(f"{CYAN}{prompt}{RESET}").strip())
            if min_val <= choice <= max_val:
                return choice
            print_error(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print_error("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            sys.exit(0)


# ============================================================================
# GAME STATE
# ============================================================================

class ReactorSystem:
    """Manages DMR (Dark Matter Reactor) operational parameters"""
    def __init__(self):
        # Core parameters
        self.power_output = 0.0  # Gigawatts
        self.target_power = 30.0  # GW
        self.temperature = 3800  # Kelvin
        self.pressure = 98.0  # Percentage
        
        # Fuel cells (3 receptacles)
        self.fuel_cell_1 = 100.0
        self.fuel_cell_2 = 100.0
        self.fuel_cell_3 = 95.0  # Defective receptacle
        
        # Systems
        self.coolant_pump_speed = 100.0  # Percentage
        self.thermal_system_efficiency = 100.0
        self.power_laser_level = 0  # 0-5 intervals
        self.combustion_chamber_temp = 1800  # Kelvin
        
        # Support systems
        self.fission_reactor_1 = 100.0
        self.fission_reactor_2 = 100.0
        self.fission_reactor_3 = 100.0
        self.fission_reactor_4 = 100.0
        self.fission_reactor_5 = 100.0
        self.fission_reactor_6 = 100.0
        
        # Safety systems
        self.emergency_stall_ready = True
        self.containment_field_strength = 100.0
        self.radiation_shield = 100.0
        self.pressure_seals = [100.0, 100.0, 100.0]  # One per quadrant
        
        self.operational = False
        self.critical_warning = False
        
    def update_systems(self):
        """Update reactor systems based on current parameters"""
        # Power laser affects combustion
        self.combustion_chamber_temp = 1800 + (self.power_laser_level * 400)
        
        # Coolant pump affects temperature stability
        if self.coolant_pump_speed < 50:
            self.temperature += 50
        elif self.coolant_pump_speed > 100:
            self.temperature -= 20
        else:
            self.temperature = 3800 + (self.power_output - 30) * 20
        
        # Fuel cell 3 degradation (manufacturing flaw)
        if self.operational:
            self.fuel_cell_3 -= random.uniform(0.1, 0.3)
        
        # Pressure affected by power output
        self.pressure = 98 + (self.power_output / 30) * 10
        
        # Check for critical conditions
        if self.temperature > 5000 or self.pressure > 120:
            self.critical_warning = True
        else:
            self.critical_warning = False


class GameState:
    """Manages game state and variables"""
    def __init__(self):
        self.player_name = ""
        self.player_title = ""
        self.dmr = ReactorSystem()
        self.dmr_online = False
        self.integrity = 100
        self.coolant_engaged = False
        self.thermal_choice = 0
        self.shutdown_code = "0"
        self.code_input = ""
        self.game_over = False
        self.success = False
        self.radiation_level = 0
        self.time_elapsed = 0
        self.emergency_active = False
        self.communications_online = True
        self.operational_decisions = []
        
    def reset(self):
        """Reset game state"""
        self.game_over = False
        self.success = False


# ============================================================================
# OPENING SEQUENCE
# ============================================================================

def show_opening() -> None:
    """Show game opening sequence"""
    print_header("Q.S.E.R.F - QUANTUM SCIENCE ENERGY RESEARCH FACILITY")
    
    sprint_slow("""
    Madison Research Institute
    New Haven, Connecticut - United States
    
    Operated by: The Quantum Corporation
    Director of Operations: Dr. Helene Kaiser
    Facility Clearance Level: CLASSIFIED (Level 9)
    """)
    
    time.sleep(1)
    
    sprint_fast("""
╔════════════════════════════════════════════════════════════════════╗
║                    Q.S.E.R.F TEXT RPG v2.0                         ║
║         Dark Matter Reactor Emergency Simulation - Aug 18, 1985     ║
║                  Based on the Quantum Universe Lore                 ║
║                      © Briged McCarthy, 2025                        ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    time.sleep(2)
    
    print_system("Initializing facility systems...")
    time.sleep(1)
    print_system("Loading personnel database...")
    time.sleep(1)
    print_system("Synchronizing reactor telemetry...")
    time.sleep(1)
    print_system("All systems nominal. Welcome to the Madison Research Institute.")
    time.sleep(1)

def get_player_info() -> tuple:
    """Get player name and title"""
    print_header("Personnel Classification")
    
    print("Welcome to the Madison Research Institute (QSERF)")
    print(f"{YELLOW}Current Date: August 18, 1985{RESET}")
    print(f"{YELLOW}Current Time: 8:30 PM Eastern Standard Time{RESET}")
    print(f"{YELLOW}Facility Status: NOMINAL{RESET}\n")
    
    name = input(f"{CYAN}Enter your name: {RESET}").strip()
    if not name:
        name = "Operator"
    
    print("\nSelect your personnel classification:")
    print("  1) Reactor Operations Technician")
    print("  2) Safety Systems Engineer")
    print("  3) Facility Maintenance Supervisor")
    print("  4) Junior Control Room Operator")
    
    titles = {
        1: "Reactor Operations Technician",
        2: "Safety Systems Engineer",
        3: "Facility Maintenance Supervisor",
        4: "Junior Control Room Operator"
    }
    
    choice = get_numeric_choice("Choose (1-4): ", 1, 4)
    title = titles[choice]
    
    return name, title

def show_facility_briefing(name: str, title: str) -> None:
    """Show facility briefing"""
    print_header("Facility Briefing")
    
    sprint_slow(f"""
Personnel: {name}
Classification: {title}
Clearance Level: 5 (Restricted)
Department: Reactor Operations
Facility: Madison Research Institute (QSERF)

FACILITY OVERVIEW:
The Madison Research Institute is a classified Quantum Corporation
facility housing the Dark Matter Reactor (DMR), one of humanity's
greatest technological achievements. Located 3000 meters underground
in New Haven, Connecticut, this facility operates as the primary
power station for the Eastern Seaboard.

KEY SYSTEMS:
- Dark Matter Reactor Unit 1 (Operational)
- Reactor Operations Control Room
- Thermal Management Systems
- Emergency Containment Protocol
- Communications Relay (Kaiser Diode)
- Structural Support Systems

CURRENT STATUS:
All systems nominal. Routine maintenance operations scheduled for
tomorrow. Tonight's shift is expected to be standard.

You are about to enter one of the most advanced research facilities
in the world. Your actions may determine the fate of thousands.
    """)
    
    time.sleep(2)

def show_control_room_arrival() -> None:
    """Show arrival at control room"""
    print_header("Reactor Operations Control Room")
    
    sprint("""
You enter the main control room at approximately 8:45 PM EST.

The control room is a state-of-the-art facility with holographic
displays showing real-time reactor parameters. Rows of monitors
display temperature, pressure, coolant flow, and radiation levels.

The Dark Matter Reactor hums with immense power below you, contained
in a massive underground chamber with 50-foot concrete walls.

Dr. Daniel Weldman, Deputy Director of Reactor Operations, turns
from his station and nods to you. The rest of the team - about 12
operators and engineers - are at their stations.

"Welcome to the night shift," Weldman says. "Should be a routine
evening. We have a safety test scheduled for later tonight. Dr.
Kaiser is monitoring from her office."

You settle into your station as the clock ticks forward...
    """, delay=0.02)
    
    time.sleep(2)


def show_reactor_dashboard(reactor: ReactorSystem) -> None:
    """Display real-time reactor status dashboard"""
    print(f"\n{MAGENTA}{'='*70}")
    print(f"  DARK MATTER REACTOR - OPERATIONAL DASHBOARD")
    print(f"{'='*70}{RESET}\n")
    
    # Power and temperature
    power_bar = "█" * int(reactor.power_output / 2) + "░" * (15 - int(reactor.power_output / 2))
    temp_bar = "█" * int(reactor.temperature / 500) + "░" * (8 - int(reactor.temperature / 500))
    
    print(f"{CYAN}CORE PARAMETERS:{RESET}")
    print(f"  Power Output:        {reactor.power_output:>5.1f} GW [{power_bar}]")
    print(f"  Target Output:       {reactor.target_power:>5.1f} GW")
    print(f"  Temperature:         {reactor.temperature:>6.0f} K  [{temp_bar}]")
    print(f"  Combustion Temp:     {reactor.combustion_chamber_temp:>6.0f} K")
    print(f"  Pressure:            {reactor.pressure:>6.1f} %")
    
    # Fuel cells
    print(f"\n{CYAN}FUEL CELL RECEPTACLES:{RESET}")
    fc1_bar = "█" * int(reactor.fuel_cell_1 / 10) + "░" * (10 - int(reactor.fuel_cell_1 / 10))
    fc2_bar = "█" * int(reactor.fuel_cell_2 / 10) + "░" * (10 - int(reactor.fuel_cell_2 / 10))
    fc3_bar = "█" * int(reactor.fuel_cell_3 / 10) + "░" * (10 - int(reactor.fuel_cell_3 / 10))
    
    status1 = "OPTIMAL" if reactor.fuel_cell_1 > 90 else "WARNING" if reactor.fuel_cell_1 > 50 else "CRITICAL"
    status2 = "OPTIMAL" if reactor.fuel_cell_2 > 90 else "WARNING" if reactor.fuel_cell_2 > 50 else "CRITICAL"
    status3 = f"{RED}DEGRADED{RESET}" if reactor.fuel_cell_3 < 80 else "OPTIMAL"
    
    print(f"  Receptacle 1:        {reactor.fuel_cell_1:>6.1f}% [{fc1_bar}] {status1}")
    print(f"  Receptacle 2:        {reactor.fuel_cell_2:>6.1f}% [{fc2_bar}] {status2}")
    print(f"  Receptacle 3:        {reactor.fuel_cell_3:>6.1f}% [{fc3_bar}] {status3}")
    
    # Support systems
    print(f"\n{CYAN}FISSION SUPPORT REACTORS:{RESET}")
    reactors_status = [reactor.fission_reactor_1, reactor.fission_reactor_2, reactor.fission_reactor_3,
                       reactor.fission_reactor_4, reactor.fission_reactor_5, reactor.fission_reactor_6]
    for i, status in enumerate(reactors_status, 1):
        bar = "█" * int(status / 10) + "░" * (10 - int(status / 10))
        print(f"  Reactor {i}:           {status:>6.1f}% [{bar}]")
    
    # Control systems
    print(f"\n{CYAN}CONTROL SYSTEMS:{RESET}")
    print(f"  Coolant Pump Speed:  {reactor.coolant_pump_speed:>6.1f} %")
    print(f"  Thermal Efficiency:  {reactor.thermal_system_efficiency:>6.1f} %")
    print(f"  Power Laser Level:   {reactor.power_laser_level:>6d} / 5")
    print(f"  Containment Field:   {reactor.containment_field_strength:>6.1f} %")
    print(f"  Radiation Shield:    {reactor.radiation_shield:>6.1f} %")
    
    # Safety status
    safety_status = "✓ READY" if reactor.emergency_stall_ready else "✗ OFFLINE"
    print(f"\n{CYAN}SAFETY SYSTEMS:{RESET}")
    print(f"  Emergency Stall:     {safety_status}")
    
    if reactor.critical_warning:
        print_alert("⚠️  CRITICAL PARAMETERS DETECTED - MONITOR CLOSELY")
    
    print()


def dmr_control_interface(game: GameState) -> None:
    """Interactive DMR operations control"""
    reactor = game.dmr
    reactor.operational = True
    
    while reactor.operational and not game.emergency_active:
        show_reactor_dashboard(reactor)
        
        print(f"{CYAN}OPERATIONAL COMMANDS:{RESET}")
        print("  1) Adjust power laser level (0-5)")
        print("  2) Adjust coolant pump speed")
        print("  3) Adjust thermal system efficiency")
        print("  4) Check fuel cell status")
        print("  5) View support reactor status")
        print("  6) Continue shift (triggers safety test)")
        
        choice = get_numeric_choice("Select command (1-6): ", 1, 6)
        
        if choice == 1:
            level = get_numeric_choice("Set laser level (0-5): ", 0, 5)
            reactor.power_laser_level = level
            reactor.power_output = level * 6.0
            print_status(f"Power laser level set to {level}")
            print_status(f"Power output now: {reactor.power_output:.1f} GW")
            
        elif choice == 2:
            speed = get_numeric_choice("Set coolant pump speed (50-150): ", 50, 150)
            reactor.coolant_pump_speed = speed
            print_status(f"Coolant pump speed set to {speed}%")
            
        elif choice == 3:
            efficiency = get_numeric_choice("Set thermal efficiency (50-100): ", 50, 100)
            reactor.thermal_system_efficiency = efficiency
            print_status(f"Thermal system efficiency set to {efficiency}%")
            
        elif choice == 4:
            print_header("Fuel Cell Status Report")
            print(f"Receptacle 1: {reactor.fuel_cell_1:.1f}% - Nominal")
            print(f"Receptacle 2: {reactor.fuel_cell_2:.1f}% - Nominal")
            print(f"Receptacle 3: {reactor.fuel_cell_3:.1f}% - Manufacturing flaw detected")
            print_error("  WARNING: Receptacle 3 shows degraded pressurization efficiency!")
            time.sleep(1)
            
        elif choice == 5:
            print_header("Support Fission Reactor Status")
            reactors_status = [reactor.fission_reactor_1, reactor.fission_reactor_2, reactor.fission_reactor_3,
                             reactor.fission_reactor_4, reactor.fission_reactor_5, reactor.fission_reactor_6]
            for i, status in enumerate(reactors_status, 1):
                print(f"Fission Reactor {i}: {status:.1f}% - Operational")
            time.sleep(1)
            
        else:  # choice == 6
            break
        
        reactor.update_systems()
        time.sleep(1)
    
    reactor.operational = False


# ============================================================================
# NORMAL OPERATIONS
# ============================================================================

def normal_operations_phase(game: GameState) -> None:
    """Normal operations before emergency"""
    print_header("Normal Operations - 8:45 PM to 10:30 PM")
    
    print_reactor(f"Power Output: 30.5 Gigawatts")
    print_reactor(f"Temperature: 3800 Kelvin")
    print_reactor(f"Pressure: 98%")
    print_reactor(f"Coolant Status: NOMINAL")
    print_system("All systems operating within normal parameters.")
    
    time.sleep(2)
    
    sprint("""
You enter the main control room at approximately 8:45 PM EST.

The control room is a state-of-the-art facility with holographic
displays showing real-time reactor parameters. Rows of monitors
display temperature, pressure, coolant flow, and radiation levels.

The Dark Matter Reactor hums with immense power below you, located
in a massive cylindrical concrete chamber with 50-foot-wide walls
built to contain the most powerful force on Earth.

The reactor is currently at nominal operating status. The dark matter
fuel cells are injecting exotic matter into the combustion chamber,
sustaining a nuclear-fusion reaction powered by dark matter itself.

Dr. Weldman approaches and says: "We have some time before the
safety test. Would you like to familiarize yourself with the reactor
control systems? It's good practice to know the parameters."

    """, delay=0.02)
    
    time.sleep(2)
    
    choice = get_user_choice("Familiarize yourself with reactor systems? (y/n): ", ['y', 'yes', 'n', 'no'])
    
    if choice in ['y', 'yes']:
        print_status("Initializing DMR Control Interface...")
        time.sleep(1)
        dmr_control_interface(game)
    
    time.sleep(2)
    
    sprint("""
The minutes tick by as you monitor the reactor. Everything is running
smoothly. Six supporting fission reactors provide power to the facility,
while the Dark Matter Reactor generates power for millions.

At 10:00 PM, Dr. Weldman announces the mandatory safety test that
Dr. Kaiser scheduled - simulating coolant pump failures to test the
emergency response protocols.

At 10:20 PM, an announcement comes over the facility intercom:

    "Attention all personnel: Lockdown Drill Level 1 commencing in
    10 minutes. All personnel report to assigned stations. The Tartarus
    seal will be engaged at 10:30 PM EST."

The Tartarus seal is the primary blast door - the only entry/exit to
the facility. Once engaged, no one can leave until the drill is
concluded. You settle back into your station as the countdown begins.

    """, delay=0.02)
    
    time.sleep(2)
    
    print_alert("LOCKDOWN DRILL COMMENCING - T-10 MINUTES")
    
    game.emergency_active = False


# ============================================================================
# EMERGENCY PHASE
# ============================================================================

def emergency_begins(game: GameState) -> None:
    """Emergency phase begins"""
    print_header("⚠️  EMERGENCY EVENT ⚠️  ")
    
    sprint_slow("""
10:30 PM EST - Tartarus Seal ENGAGED

The massive blast door grinds shut with a deafening roar. The facility
is now sealed. Nothing can enter or leave until the drill is lifted.

Dr. Weldman begins the safety test protocol. The procedure is routine:
simulate coolant pump failures, test emergency systems, measure response
times. The test parameters are established.

"Reducing coolant pumps to 75% efficiency," announces Control Technician
Marcus. "Power lasers set to interval level 3."

The reactor power begins to rise gradually. Temperature increases as
thermal systems operate at reduced efficiency. The holographic displays
show the reactor responding exactly as expected.

But at 11:23 PM, something goes wrong...
    """)
    
    time.sleep(3)
    
    print_alert("SENSORY SYSTEM FAILURE - QUADRANT 1")
    print_system("Sensory reading discontinued without explanation.")
    
    time.sleep(2)
    
    sprint("""
The system restart attempt fails. A second sensory system goes offline
at 11:45 PM, this time in Quadrant 2 - dangerously close to Fuel Cell
Receptacle Three.

"That's two system failures in twenty minutes," you say, concerned.
"We should shut down the reactor immediately for diagnostics."

Dr. Weldman looks troubled. He glances at the communication console,
then back at you. "Dr. Kaiser specifically authorized this test. She
insisted we not interrupt commercial power distribution tonight."

"But sir, the error margin is expanding. That's not normal," another
operator insists.

Before Weldman can respond, the pressure reading system in Quadrant 2
fails completely.
    """, delay=0.02)
    
    time.sleep(2)
    
    print_alert("CRITICAL PRESSURE LEAK - FUEL CELL RECEPTACLE THREE")
    print_error("Temperature rising beyond safety parameters")
    print_error("Pressure systems failing")
    
    sprint("""

An ear-splitting alarm blares throughout the control room. Red emergency
lights flood the space with crimson color. The holographic displays
frantically update with cascading system failures.

"Pressure is skyrocketing!" Marcus shouts. "Temperature at 5200 Kelvin
and climbing! The cooling systems can't keep up!"

"Try to engage the emergency stall protocol!" Weldman commands, his voice
steady but desperate. "Maximum coolant intake! Kill the power lasers!"

You rush to your console, fingers flying across the interface. But as
you attempt to access the emergency shutdown code, your screen goes blank.

"The code is deleted," you say, unable to believe what you're seeing.
"The Dark Matter Reactor Emergency Combustion Stall Protocol (DMRECSP) -
the entire code is gone. Someone purged it from the system."

Weldman's face goes pale. "That's not possible. That code is locked
behind multiple security layers..."

Temperature: 6200 Kelvin
Pressure: 150%
Coolant Efficiency: 5%
Radiation Spike: CRITICAL

An ominous hum fills the facility - a sound you've never heard before.
The reactor chamber begins to shake. Dust falls from the ceiling. The
monitors show something impossible: a gravitational anomaly forming
inside the reactor core.

The dark matter is compressing... collapsing in on itself...

"It's forming a black hole," whispers Dr. Klein, the senior reactor
engineer. "My God... it's actually forming a singularity..."
    """, delay=0.02)
    
    time.sleep(3)
    
    game.emergency_active = True


# ============================================================================
# CRISIS PHASE
# ============================================================================

def handle_crisis_choices(game: GameState) -> None:
    """Handle player choices during crisis"""
    print_header("CRISIS - Decision Time")
    
    print_alert("THE REACTOR IS FAILING - YOU HAVE SECONDS TO ACT")
    
    time.sleep(1)
    
    print("""
The facility is in chaos. Alarms scream. The reactor chamber groans
as gravitational forces tear at the containment field. The entire
underground complex shakes violently.

Dr. Weldman turns to you: "We have maybe five minutes before this
reactor tears itself apart. We need to:"
""")
    
    time.sleep(1)
    
    choice = get_numeric_choice("""
Choose your action:
  1) Attempt to restore the DMRECSP code from backup systems
  2) Organize immediate evacuation to secondary safe zones
  3) Contact the surface and request emergency assistance
  
Your choice (1-3): """, 1, 3)
    
    if choice == 1:
        print_status("Attempting to restore emergency shutdown code...")
        time.sleep(2)
        
        sprint("""
You race to the backup server terminal. Your hands shake as you input
the restoration sequence. The system begins searching archived backups.

5 seconds... 10 seconds... The reactor continues to deteriorate.

"Come on, come on..." you whisper.

At 15 seconds, the search completes. The files are corrupted. Someone
didn't just delete the code - they systematically destroyed every copy.

"The backups are destroyed," you report, your voice hollow. "Whoever
did this planned it perfectly. They wanted us trapped down here without
any way to stop the reactor."
        """, delay=0.02)
        time.sleep(1)
        
    elif choice == 2:
        print_status("Initiating evacuation protocol...")
        time.sleep(2)
        
        sprint("""
"All personnel, this is Control," Weldman commands, his voice steady
despite the chaos. "Initiate secondary evacuation. Move to Safe Zone
Delta, sub-level 2. This is not a drill."

Operators begin evacuating, but the facility tremor worsens. One of
the exit corridors collapses partially, blocking the primary route.

The evacuation is... compromised.
        """, delay=0.02)
        time.sleep(1)
        
    else:
        print_status("Attempting to reach the surface...")
        time.sleep(2)
        
        sprint("""
You grab the communication console and attempt to reach the Kaiser
Communications Diode - the primary relay station to the surface.

"Surface Control, this is QSERF Reactor Operations, we have a critical
emergency situation. Reactor is experiencing uncontrolled compression.
Requesting immediate assistance..."

Static.

"Surface Control, do you copy?"

More static.

Dr. Klein checks the communications logs. His eyes widen. "The
communications... they've been silenced. Someone engaged Lockdown
Code Bravo-9 - complete radio silence protocol. We're completely
cut off from the outside world."

The realization hits you like ice water. Whatever is happening down
here... no one on the surface knows about it.
        """, delay=0.02)
        time.sleep(1)
    
    time.sleep(2)


# ============================================================================
# FINAL CRISIS
# ============================================================================

def final_countdown(game: GameState) -> None:
    """Final countdown to catastrophe"""
    print_header("T-MINUS FINAL MINUTES")
    
    print_alert("REACTOR STRUCTURAL INTEGRITY CRITICAL")
    
    sprint("""
11:50 PM EST

The containment chamber groans under impossible pressures. The
gravitational anomaly at the reactor's core has reached critical
mass. Alarms have become one continuous scream of electronic distress.

Dr. Weldman makes the hardest decision of his life: "All personnel,
move to the maximum distance safe zones immediately. We're sealing
the reactor chamber. Everyone not in that sector - go NOW."

Most of the team evacuates. You watch as they run through the corridors.
But some operators remain, trying desperately to find any way to shut
down the reactor. You can see the determination in their eyes... and
the futility.

"I'm staying," announces Dr. Klein. "Someone needs to document what
happens. Someone needs to record the truth."

He moves toward the observation window that overlooks the reactor
chamber, camera in hand.

The temperature gauge exceeds 8000 Kelvin. The pressure reading is
off the scale. The holographic displays flicker and fail as systems
overload. The emergency lighting bathes everything in a hellish red.

11:53 PM EST...

An overwhelming sound - not a roar, not an explosion, but something
far worse. A sound that shouldn't exist in nature. A sound like reality
itself is tearing.

The reactor chamber... it collapses inward. All that immense power,
all that dark matter, compressed to a singularity no bigger than an
atom.

A blinding light fills the chamber. Through the sealed observation
windows, you see something impossible: a black hole, holding the power
of stars, consuming everything around it.

The facility shakes so violently you're thrown to the ground. The
lights flicker and die. Emergency power kicks in, casting the room in
eerie strobing red light.

Then... silence.

But above ground, the consequences are just beginning.
    """, delay=0.02)
    
    time.sleep(3)
    
    print_alert("STRUCTURAL FAILURE DETECTED - MULTIPLE SECTORS")
    print_error("REACTOR CORE CATASTROPHIC FAILURE - CONTAINMENT BREACH")
    
    time.sleep(2)
    
    game.success = False
    game.game_over = True


# ============================================================================
# EPILOGUE
# ============================================================================

def show_epilogue() -> None:
    """Show game epilogue"""
    print_header("EPILOGUE - THE WORLD ABOVE")
    
    sprint_slow("""
11:54 PM Pacific Standard Time
(August 18, 1985 - 2:54 AM EST, August 19)

Above the Madison Research Institute, the night sky erupts.

A massive explosion - the underground chambers collapsing, the
structural supports failing under gravitational stress. The ground
splits open. Black smoke and radioactive steam erupt from dozens of
ventilation shafts across the facility.

A mushroom cloud rises over New Haven, Connecticut.

Telephone lines around the world become clogged as thousands of
people report the explosion. Emergency sirens wail across Connecticut.
The National Guard mobilizes. The FBI is dispatched. 

Washington D.C. raises the DEFCON status to DEFCON 2.
They believe America is under nuclear attack.

News channels cut their programming with emergency broadcasts:

"...an explosion of unprecedented scale has occurred near New Haven,
Connecticut. The Quantum Corporation's Madison Research Institute has
been completely destroyed. Early reports suggest catastrophic failure
of the Dark Matter Reactor. Radiation levels in the area are critical.
All residents of southern Connecticut are being ordered to evacuate
immediately..."

Over 230 people working the night shift at QSERF.

All presumed lost.

Within hours, Dr. Helene Kaiser, Director of Reactor Operations, is
found dead at the bottom of a cliff near the facility. Her car shows
signs of tampering. The brakes had been cut.

The investigation will reveal that Dr. Kaiser deliberately sabotaged
the reactor in an act of revenge against the Quantum Corporation for
denying her promotion.

Over the following weeks and months:
- Congressional investigations begin
- Quantum's stock price plummets
- Public trust in the company evaporates
- Quantum's expansion plans are shelved indefinitely
- The company survives only through military contracts

The facility remains sealed. The radiation levels remain critical.

A monument will eventually be erected at the site, commemorating
the lives lost. It will stand as a warning about the dangers of
unchecked corporate power and the fragility of human technology.

The date: August 18, 1985

The event: The worst industrial disaster of the 20th century

The cause: One woman's rage and the corporation's arrogance

The lesson: Not learned for another 260 years, until the very
           civilization built on Quantum's power collapses entirely.
    """)
    
    time.sleep(3)
    
    print_header("END SCENARIO")
    print_error("SCENARIO COMPLETE - FACILITY DESTROYED")
    print(f"""
{RED}
All personnel are presumed dead.
The Madison Research Institute has been destroyed.
Radiation spreads across the Eastern Seaboard.
The Quantum Corporation's empire begins its slow collapse.

This is not a victory. This is not a failure.
This is the inexorable march of consequences.

This is the truth of August 18, 1985.
{RESET}
    """)
    
    time.sleep(3)


# ============================================================================
# MAIN GAME LOOP
# ============================================================================

def main() -> None:
    """Main game loop"""
    
    show_opening()
    
    game = GameState()
    
    # Get player info
    game.player_name, game.player_title = get_player_info()
    
    # Facility briefing
    show_facility_briefing(game.player_name, game.player_title)
    
    # Arrival
    show_control_room_arrival()
    
    # Normal operations
    normal_operations_phase(game)
    
    # Emergency
    emergency_begins(game)
    
    # Crisis response
    handle_crisis_choices(game)
    
    # Final countdown
    final_countdown(game)
    
    # Epilogue
    show_epilogue()
    
    print(f"{CYAN}Thank you for experiencing the Madison Research Institute Emergency Simulation.{RESET}")
    time.sleep(2)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Game interrupted by user.{RESET}")
        sys.exit(0)
