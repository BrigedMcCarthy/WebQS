#!/usr/bin/env python3
"""
RBMK-1000 Reactor Simulator - Full Simulation with ASCII Control Room Panel

A comprehensive simulation of the RBMK-1000 reactor with realistic graphite-moderated
boiling water reactor physics, emergency systems, and authentic control room interface.

Reference: Soviet-era RBMK (РБМК) design specifications
Power: 1000 MW thermal
Pressure tubes: 1661
Control rods: 211 (absorbing type)

WARNING: This reactor type has a POSITIVE VOID COEFFICIENT
An extremely dangerous characteristic that contributed to the Chernobyl disaster.

Date: January 13, 2026
"""

import time
import random
import os
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict
import sys
import shutil


# ============================================================================
# ANSI Color Codes
# ============================================================================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BG_RED = '\033[41m'
    BG_YELLOW = '\033[43m'
    BG_GREEN = '\033[42m'
    BLACK = '\033[30m'


# ============================================================================
# Enums
# ============================================================================
class ReactorState(Enum):
    COLD = "COLD"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    SCRAM = "SCRAM"
    SHUTDOWN = "SHUTDOWN"
    CRITICAL = "CRITICAL"


class TubeStatus(Enum):
    NORMAL = "OK"
    HOT = "HOT"
    CRITICAL = "CRIT"
    FAILED = "FAIL"


# ============================================================================
# Data Classes
# ============================================================================
@dataclass
class PressureTube:
    """Individual pressure tube in the RBMK core (1661 total)"""
    id: int
    power: float = 0.6  # MW each
    coolant_temp: float = 280.0  # Celsius
    coolant_pressure: float = 70.0  # Bar
    void_fraction: float = 0.0  # Vapor content (0-1)
    xenon_concentration: float = 0.0  # Fission product poisoning
    
    def get_status(self) -> TubeStatus:
        if self.coolant_temp > 320:
            return TubeStatus.CRITICAL
        elif self.coolant_temp > 300:
            return TubeStatus.HOT
        elif self.power <= 0:
            return TubeStatus.FAILED
        return TubeStatus.NORMAL


@dataclass
class ControlRod:
    """Individual control rod (211 total)"""
    id: int
    insertion: float = 0.0  # Percentage (0-100)
    manual: bool = False
    can_move: bool = True


# ============================================================================
# Main RBMK Reactor Simulation Class
# ============================================================================
class RBMKReactor:
    """RBMK-1000 Reactor Simulation with Full Physics"""
    
    def __init__(self):
        # === State Management ===
        self.state = ReactorState.COLD
        self.running_time = 0.0
        self.simulation_tick = 0
        
        # === Reactor Core ===
        self.pressure_tubes: List[PressureTube] = [
            PressureTube(i, power=0.6, coolant_temp=280.0, coolant_pressure=70.0)
            for i in range(1661)
        ]
        self.control_rods: List[ControlRod] = [
            ControlRod(i, insertion=0.0)
            for i in range(211)
        ]
        
        # === Bulk Parameters ===
        self.core_power = 0.0  # MW
        self.target_power = 1000.0  # MW
        self.core_neutron_flux = 0.0  # % relative to nominal
        self.xenon_buildup = 0.0  # Global xenon concentration
        self.iodine_131 = 0.0  # Fission product buildup
        
        # === Temperature System ===
        self.average_coolant_temp = 280.0
        self.steam_generator_temp = 270.0
        self.graphite_moderator_temp = 290.0
        
        # === Pressure System ===
        self.core_pressure = 70.0  # Bar (7 MPa)
        self.pressurizer_pressure = 70.0
        self.steam_drum_pressure = 70.0
        
        # === Control Rod Systems ===
        self.cr_auto_insertion = True
        self.cr_manual_enabled = False
        self.cr_speed = 0.8  # Cm per second
        self.cr_insertion_rate = 0.0
        
        # === Void Coefficient (DANGEROUS!) ===
        self.void_coefficient_enabled = True  # RBMK characteristic
        self.coolant_flow_rate = 100.0  # % of nominal
        
        # === Power Regulation System ===
        self.power_regulator_enabled = False
        self.turbine_load = 0.0  # MW
        self.steam_flow = 0.0  # kg/s
        
        # === Safety Systems ===
        self.reactor_safety_system_enabled = True
        self.emergency_cooling_active = False
        self.emergency_cooling_flow = 0.0  # kg/s
        self.scram_engaged = False
        self.auto_scram_triggered = False
        self.fast_scram = False  # AZ-5 system
        
        # === Alarms ===
        self.thermal_alarm = False
        self.pressure_alarm = False
        self.neutron_flux_alarm = False
        self.void_alarm = False
        self.xenon_alarm = False
        self.emergency_alarm = False
        
        # === Circuit Status ===
        self.main_circulating_pumps = [True, True, True, False]  # 4 pumps
        self.emergency_pump_engaged = False
        self.relief_valves_open = False
        
        # === Display Settings ===
        self.show_detailed_tubes = False
        self.active_alarm = None
        
    # ========================================================================
    # Control System Methods
    # ========================================================================
    
    def raise_all_rods(self):
        """Withdraw all control rods (decrease insertion)"""
        if not self.cr_manual_enabled or self.scram_engaged:
            return
        for rod in self.control_rods:
            if rod.can_move:
                rod.insertion = max(0.0, rod.insertion - 2.0)
    
    def lower_all_rods(self):
        """Insert all control rods (increase insertion)"""
        if not self.cr_manual_enabled or self.scram_engaged:
            return
        for rod in self.control_rods:
            if rod.can_move:
                rod.insertion = min(100.0, rod.insertion + 2.0)
    
    def az5_emergency_shutdown(self):
        """AZ-5 System: Rapid emergency shutdown (all rods to 100%)"""
        if self.scram_engaged:
            return
        self.fast_scram = True
        self.scram_engaged = True
        self.state = ReactorState.SCRAM
        for rod in self.control_rods:
            rod.insertion = 100.0
    
    def toggle_auto_regulation(self):
        """Toggle power regulation system"""
        if self.power_regulator_enabled:
            self.power_regulator_enabled = False
        else:
            self.power_regulator_enabled = True
    
    def toggle_manual_control(self):
        """Toggle manual rod control"""
        self.cr_manual_enabled = not self.cr_manual_enabled
    
    def toggle_circulating_pump(self, pump_idx: int):
        """Toggle main circulating pump"""
        if 0 <= pump_idx < 4 and not self.scram_engaged:
            self.main_circulating_pumps[pump_idx] = not self.main_circulating_pumps[pump_idx]
    
    def engage_emergency_cooling(self):
        """Activate emergency core cooling system"""
        self.emergency_cooling_active = True
        self.emergency_pump_engaged = True
    
    def toggle_relief_valve(self):
        """Toggle pressurizer relief valve"""
        self.relief_valves_open = not self.relief_valves_open
    
    def reduce_coolant_flow(self):
        """Reduce coolant flow rate"""
        self.coolant_flow_rate = max(20.0, self.coolant_flow_rate - 5.0)
    
    def increase_coolant_flow(self):
        """Increase coolant flow rate"""
        self.coolant_flow_rate = min(100.0, self.coolant_flow_rate + 5.0)
    
    def disable_safety_system(self):
        """Disable reactor safety system (DANGEROUS!)"""
        self.reactor_safety_system_enabled = False
    
    def enable_safety_system(self):
        """Re-enable reactor safety system"""
        self.reactor_safety_system_enabled = True
    
    def isolate_reactor(self):
        """Isolate reactor for emergency shutdown"""
        for pump in range(4):
            self.main_circulating_pumps[pump] = False
        self.emergency_cooling_active = True
    
    # ========================================================================
    # Physics Simulation
    # ========================================================================
    
    def calculate_avg_rod_insertion(self) -> float:
        """Calculate average control rod insertion"""
        return sum(rod.insertion for rod in self.control_rods) / len(self.control_rods)
    
    def update_core_power(self):
        """Calculate core power based on reactor parameters"""
        avg_insertion = self.calculate_avg_rod_insertion()
        
        # Base power from rod withdrawal
        rod_factor = (100.0 - avg_insertion) / 100.0
        base_power = 1000.0 * rod_factor
        
        # Xenon poisoning reduces power
        xenon_factor = 1.0 - (self.xenon_buildup * 0.003)
        
        # Void coefficient effect (POSITIVE - DANGEROUS!)
        # In RBMK, voids increase reactivity instead of reducing it
        avg_void = sum(tube.void_fraction for tube in self.pressure_tubes) / len(self.pressure_tubes)
        void_factor = 1.0 + (avg_void * 0.15)  # POSITIVE coefficient = amplification
        
        # Coolant flow affects power
        flow_factor = self.coolant_flow_rate / 100.0
        
        # Calculate final power
        self.core_power = base_power * xenon_factor * void_factor * flow_factor
        self.core_power = max(0.0, min(1000.0, self.core_power))
    
    def update_temperatures(self, delta_time: float = 1.0):
        """Update temperature throughout core"""
        for tube in self.pressure_tubes:
            # Heat generation from fission
            tube_power = self.core_power / 1661.0
            
            # Cool voids reduce effective cooling
            cooling_factor = 1.0 - (tube.void_fraction * 0.3)
            
            # Coolant flow affects temperature
            flow_effect = self.coolant_flow_rate / 100.0
            
            # Temperature change
            heat_added = tube_power * 0.05
            cooling = 2.5 * flow_effect * cooling_factor
            
            tube.coolant_temp += (heat_added - cooling) * delta_time / 50.0
            
            # Saturation temperature at this pressure (~280°C at 70 bar)
            if tube.coolant_temp > 285:
                tube.void_fraction = min(0.4, tube.void_fraction + 0.001)
            else:
                tube.void_fraction = max(0.0, tube.void_fraction - 0.005)
            
            tube.coolant_temp = max(270, min(350, tube.coolant_temp))
        
        # Bulk temperatures
        self.average_coolant_temp = sum(tube.coolant_temp for tube in self.pressure_tubes) / len(self.pressure_tubes)
        self.graphite_moderator_temp = self.average_coolant_temp + 15
        self.steam_generator_temp = self.average_coolant_temp - 5
    
    def update_xenon_buildup(self, delta_time: float = 1.0):
        """Simulate xenon fission product poisoning"""
        # Xenon builds up as fission product
        buildup_rate = self.core_power * 0.002
        self.xenon_buildup += buildup_rate * delta_time / 100.0
        
        # Xenon decays with half-life of ~9 hours (simulated as slow decay)
        decay_rate = self.xenon_buildup * 0.0001
        self.xenon_buildup = max(0.0, self.xenon_buildup - decay_rate * delta_time)
        
        # Iodine-131 buildup (precursor to xenon)
        self.iodine_131 += self.core_power * 0.001 * delta_time / 100.0
        self.iodine_131 = max(0.0, min(50.0, self.iodine_131))
    
    def update_pressure(self, delta_time: float = 1.0):
        """Update system pressure"""
        # Pressure increases with temperature
        temp_factor = (self.average_coolant_temp - 270.0) / 30.0
        pressure_from_temp = temp_factor * 15.0
        
        # Relief valve opens at ~86 bar
        relief_effect = 0.0
        if self.relief_valves_open or self.core_pressure > 86:
            relief_effect = -5.0
        
        # Calculate pressure change
        self.core_pressure = 70.0 + pressure_from_temp + relief_effect
        self.core_pressure = max(50.0, min(90.0, self.core_pressure))
        self.pressurizer_pressure = self.core_pressure
        self.steam_drum_pressure = self.core_pressure
    
    def update_alarms(self):
        """Check alarm conditions"""
        # Temperature alarm
        self.thermal_alarm = self.average_coolant_temp > 310
        
        # Pressure alarm
        self.pressure_alarm = self.core_pressure > 80
        
        # Neutron flux alarm
        avg_insertion = self.calculate_avg_rod_insertion()
        relative_power = (100.0 - avg_insertion) / 100.0
        self.neutron_flux_alarm = relative_power > 1.1  # Over 110% power
        
        # Void alarm
        avg_void = sum(tube.void_fraction for tube in self.pressure_tubes) / len(self.pressure_tubes)
        self.void_alarm = avg_void > 0.2
        
        # Xenon alarm
        self.xenon_alarm = self.xenon_buildup > 30
        
        # Emergency condition
        self.emergency_alarm = (self.thermal_alarm and self.pressure_alarm) or self.core_power > 1050
    
    def check_safety_conditions(self):
        """Check for SCRAM conditions"""
        if not self.reactor_safety_system_enabled:
            return
        
        # SCRAM on high temperature
        if self.average_coolant_temp > 325:
            self.auto_scram_triggered = True
            self.az5_emergency_shutdown()
        
        # SCRAM on high pressure
        if self.core_pressure > 87:
            self.auto_scram_triggered = True
            self.az5_emergency_shutdown()
        
        # SCRAM on core power exceeding limits
        if self.core_power > 1080:
            self.auto_scram_triggered = True
            self.az5_emergency_shutdown()
        
        # Criticality alarm
        if self.core_power > 1000:
            self.emergency_alarm = True
    
    def update_circulating_system(self):
        """Update main circulating pumps effect"""
        pumps_on = sum(self.main_circulating_pumps)
        if pumps_on == 0:
            self.coolant_flow_rate = 0.0
            self.emergency_cooling_active = True
        else:
            self.coolant_flow_rate = min(100.0, pumps_on * 30.0)
    
    def update_emergency_systems(self):
        """Update emergency cooling flow"""
        if self.emergency_cooling_active:
            self.emergency_cooling_flow = 50.0  # kg/s
        else:
            self.emergency_cooling_flow = 0.0
        
        # Emergency cooling helps reduce temperature
        if self.emergency_cooling_active and self.average_coolant_temp > 290:
            for tube in self.pressure_tubes:
                tube.coolant_temp -= 0.5
    
    # ========================================================================
    # Simulation Loop
    # ========================================================================
    
    def tick(self, delta_time: float = 1.0):
        """Execute one simulation cycle"""
        if self.state == ReactorState.SHUTDOWN:
            return
        
        self.simulation_tick += 1
        self.running_time += delta_time
        
        # Update systems in order
        self.update_core_power()
        self.update_temperatures(delta_time)
        self.update_xenon_buildup(delta_time)
        self.update_pressure(delta_time)
        self.update_circulating_system()
        self.update_emergency_systems()
        self.update_alarms()
        self.check_safety_conditions()
        
        # Update state
        if self.scram_engaged:
            self.state = ReactorState.SCRAM
        elif self.core_power > 100:
            self.state = ReactorState.RUNNING
        elif self.state == ReactorState.RUNNING and self.core_power < 50:
            self.state = ReactorState.SHUTDOWN


# ============================================================================
# ASCII Control Room Panel
# ============================================================================
class RBMKControlPanel:
    """ASCII-based RBMK control room panel with keyboard controls"""
    
    CONTROL_MAP = {
        'q': ('RAISE_RODS', 'Raise All Rods'),
        'w': ('LOWER_RODS', 'Lower All Rods'),
        'e': ('AZ5_SCRAM', 'AZ-5 Emergency SCRAM'),
        'r': ('TOGGLE_AUTO', 'Toggle Power Regulator'),
        't': ('TOGGLE_MANUAL', 'Toggle Manual Control'),
        'y': ('PUMP_1', 'Toggle Pump 1'),
        'u': ('PUMP_2', 'Toggle Pump 2'),
        'i': ('PUMP_3', 'Toggle Pump 3'),
        'o': ('PUMP_4', 'Toggle Pump 4'),
        'p': ('EMERGENCY_COOL', 'Engage Emergency Cooling'),
        '0': ('RELIEF_VALVE', 'Relief Valve'),
        '1': ('REDUCE_FLOW', 'Reduce Coolant Flow'),
        '2': ('INCREASE_FLOW', 'Increase Coolant Flow'),
        '3': ('DISABLE_SAFETY', 'Disable Safety System'),
        '4': ('ENABLE_SAFETY', 'Enable Safety System'),
        '5': ('ISOLATE', 'Isolate Reactor'),
        '6': ('TOGGLE_TUBES', 'Toggle Tube Display'),
    }
    
    def __init__(self, reactor: RBMKReactor):
        self.reactor = reactor
        self.running = True
    
    def get_terminal_width(self) -> int:
        """Get terminal width - scales from 24 to 100 columns"""
        width = shutil.get_terminal_size((80, 24)).columns
        if width < 24:
            width = 24
        elif width > 120:
            width = 120
        return width
    
    def draw_panel(self) -> str:
        """Draw simple vertical ASCII display - works on any device"""
        lines = []
        
        # Collect all data
        power_pct = (self.reactor.core_power / 1000.0) * 100
        power_color = Colors.RED if power_pct > 110 else Colors.YELLOW if power_pct > 100 else Colors.GREEN
        
        temp_pct = ((self.reactor.average_coolant_temp - 270) / 50) * 100
        temp_color = Colors.RED if self.reactor.average_coolant_temp > 310 else Colors.YELLOW if self.reactor.average_coolant_temp > 300 else Colors.GREEN
        
        pressure_pct = ((self.reactor.core_pressure - 50) / 40) * 100
        press_color = Colors.RED if self.reactor.core_pressure > 85 else Colors.YELLOW if self.reactor.core_pressure > 75 else Colors.GREEN
        
        avg_void = sum(tube.void_fraction for tube in self.reactor.pressure_tubes) / len(self.reactor.pressure_tubes)
        void_color = Colors.RED if avg_void > 0.2 else Colors.YELLOW if avg_void > 0.1 else Colors.GREEN
        
        avg_insertion = self.reactor.calculate_avg_rod_insertion()
        
        state_c = {
            'COLD': Colors.CYAN, 'STARTING': Colors.YELLOW, 'RUNNING': Colors.GREEN,
            'SCRAM': Colors.RED, 'SHUTDOWN': Colors.BLUE, 'CRITICAL': Colors.RED,
        }
        state = state_c.get(self.reactor.state.value, Colors.WHITE)
        
        # Simple vertical layout - fixed width bars, works on any screen
        lines.append("RBMK-1000 REACTOR")
        lines.append("")
        
        # Fixed 20-char bars for universal compatibility
        bar_width = 20
        
        pw_bar = self._make_compact_bar(power_pct, bar_width)
        lines.append(f"Power: {power_color}{pw_bar}{Colors.RESET} {self.reactor.core_power:6.1f} MW")
        
        tmp_bar = self._make_compact_bar(temp_pct, bar_width)
        lines.append(f"Temp:  {temp_color}{tmp_bar}{Colors.RESET} {self.reactor.average_coolant_temp:6.1f}°C")
        
        pr_bar = self._make_compact_bar(pressure_pct, bar_width)
        lines.append(f"Press: {press_color}{pr_bar}{Colors.RESET} {self.reactor.core_pressure:6.1f} Bar")
        
        vd_bar = self._make_compact_bar(avg_void * 100, bar_width)
        lines.append(f"Void:  {void_color}{vd_bar}{Colors.RESET} {avg_void*100:6.1f}%")
        
        rd_bar = self._make_compact_bar(avg_insertion, bar_width)
        lines.append(f"Rods:  {Colors.YELLOW}{rd_bar}{Colors.RESET} {avg_insertion:6.1f}%")
        
        lines.append("")
        
        # Status info
        state_str = self.reactor.state.value
        lines.append(f"State: {state}{state_str}{Colors.RESET}")
        lines.append(f"Time:  {self.reactor.running_time:7.1f}s")
        
        lines.append("")
        
        # System status - one per line
        pumps = "P1:" + ("ON " if self.reactor.main_circulating_pumps[0] else "OFF")
        pumps += " P2:" + ("ON " if self.reactor.main_circulating_pumps[1] else "OFF")
        pumps += " P3:" + ("ON " if self.reactor.main_circulating_pumps[2] else "OFF")
        pumps += " P4:" + ("ON " if self.reactor.main_circulating_pumps[3] else "OFF")
        lines.append(pumps)
        
        relief = "Relief: " + ("OPEN" if self.reactor.relief_valves_open else "CLOSED")
        lines.append(relief)
        
        reg = "Regulation: " + ("ON" if self.reactor.power_regulator_enabled else "OFF")
        lines.append(reg)
        
        safe = "Safety: " + ("ENABLED" if self.reactor.reactor_safety_system_enabled else "DISABLED")
        lines.append(safe)
        
        lines.append("")
        
        # Alarms
        alm = []
        if self.reactor.thermal_alarm:
            alm.append(f"{Colors.RED}THERMAL{Colors.RESET}")
        if self.reactor.pressure_alarm:
            alm.append(f"{Colors.RED}PRESSURE{Colors.RESET}")
        if self.reactor.void_alarm:
            alm.append(f"{Colors.YELLOW}VOID{Colors.RESET}")
        if self.reactor.auto_scram_triggered:
            alm.append(f"{Colors.RED}SCRAM{Colors.RESET}")
        
        if alm:
            alm_str = " | ".join(alm)
            lines.append(f"ALARMS: {alm_str}")
        else:
            lines.append(f"ALARMS: {Colors.GREEN}ALL NOMINAL{Colors.RESET}")
        
        return "\n".join(lines)
    
    def _make_compact_bar(self, percentage: float, width: int) -> str:
        """Create compact visual bar"""
        percentage = min(100, max(0, percentage))
        filled = int(width * percentage / 100)
        return f"[{'▓' * filled}{'░' * (width - filled)}]"
    
    def _make_compact_bar(self, percentage: float, width: int) -> str:
        """Create compact visual bar"""
        percentage = min(100, max(0, percentage))
        filled = int(width * percentage / 100)
        return f"[{'▓' * filled}{'░' * (width - filled)}]"
    
    def _make_ultra_compact_bar(self, percentage: float, width: int) -> str:
        """Create ultra-compact visual bar for tiny screens"""
        percentage = min(100, max(0, percentage))
        if width <= 3:
            # Single character indicator
            if percentage < 25:
                return "▁"
            elif percentage < 50:
                return "▂"
            elif percentage < 75:
                return "▃"
            else:
                return "█"
        filled = int(width * percentage / 100)
        return f"[{'▓' * filled}{'░' * (width - filled)}]"
    
    def draw_keyboard_guide(self) -> str:
        """Draw keyboard control guide - adaptive"""
        lines = []
        width = self.get_terminal_width()
        
        # Skip guide on very small screens
        if width < 30:
            return ""
        
        lines.append(f"{Colors.MAGENTA}┌{'─' * (width - 2)}┐{Colors.RESET}")
        lines.append(f"{Colors.MAGENTA}│ {Colors.BOLD}KEYS{Colors.RESET:<{width-4}} │{Colors.RESET}")
        lines.append(f"{Colors.MAGENTA}├{'─' * (width - 2)}┤{Colors.RESET}")
        
        if width < 50:
            # Minimal controls
            controls = [
                "Q:↑ W:↓ E:SCRAM R:RegOn T:RegOff",
                "Y/U/I/O:Pump1-4 P:Cool 0:Relief"
            ]
        else:
            # Full controls
            controls = [
                "Q:UP W:DN E:SCRAM R:RegOn T:RegOff",
                "Y/U/I/O:Pump1-4  P:EmCool  0:Relief",
                "1:↓Flow 2:↑Flow 3:SafeOff 4:SafeOn",
                "SPC:Auto ENT:Step  X:Exit"
            ]
        
        for ctrl in controls:
            if len(ctrl) > width - 4:
                ctrl = ctrl[:width - 5]
            lines.append(f"{Colors.MAGENTA}│{Colors.RESET} {ctrl:<{width-4}} │")
        
        lines.append(f"{Colors.MAGENTA}└{'─' * (width - 2)}┘{Colors.RESET}")
        
        return "\n".join(lines)
    
    def draw_display(self):
        """Render full display"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(self.draw_panel())
        print(self.draw_keyboard_guide())
    
    @staticmethod
    def _make_bar(percentage: float, width: int = 30) -> str:
        """Create a visual bar"""
        percentage = min(100, max(0, percentage))
        filled = int(width * percentage / 100)
        return f"[{'█' * filled}{'░' * (width - filled)}] {percentage:6.2f}%"
    
    @staticmethod
    def _make_compact_bar(percentage: float, width: int) -> str:
        """Create compact visual bar"""
        percentage = min(100, max(0, percentage))
        filled = int(width * percentage / 100)
        return f"[{'▓' * filled}{'░' * (width - filled)}]"
    
    def handle_input(self, key: str):
        """Handle keyboard input"""
        key = key.lower()
        
        if key in self.CONTROL_MAP:
            action, desc = self.CONTROL_MAP[key]
            
            if action == 'RAISE_RODS':
                self.reactor.raise_all_rods()
            elif action == 'LOWER_RODS':
                self.reactor.lower_all_rods()
            elif action == 'AZ5_SCRAM':
                self.reactor.az5_emergency_shutdown()
            elif action == 'TOGGLE_AUTO':
                self.reactor.toggle_auto_regulation()
            elif action == 'TOGGLE_MANUAL':
                self.reactor.toggle_manual_control()
            elif action == 'PUMP_1':
                self.reactor.toggle_circulating_pump(0)
            elif action == 'PUMP_2':
                self.reactor.toggle_circulating_pump(1)
            elif action == 'PUMP_3':
                self.reactor.toggle_circulating_pump(2)
            elif action == 'PUMP_4':
                self.reactor.toggle_circulating_pump(3)
            elif action == 'EMERGENCY_COOL':
                self.reactor.engage_emergency_cooling()
            elif action == 'RELIEF_VALVE':
                self.reactor.toggle_relief_valve()
            elif action == 'REDUCE_FLOW':
                self.reactor.reduce_coolant_flow()
            elif action == 'INCREASE_FLOW':
                self.reactor.increase_coolant_flow()
            elif action == 'DISABLE_SAFETY':
                self.reactor.disable_safety_system()
            elif action == 'ENABLE_SAFETY':
                self.reactor.enable_safety_system()
            elif action == 'ISOLATE':
                self.reactor.isolate_reactor()
            elif action == 'TOGGLE_TUBES':
                self.reactor.show_detailed_tubes = not self.reactor.show_detailed_tubes
        
        elif key == 'x':
            self.running = False
        
        elif key == ' ':
            # Auto-tick
            for _ in range(10):
                self.reactor.tick(1.0)
        
        elif key == '\n':
            # Manual tick
            self.reactor.tick(1.0)


# ============================================================================
# Main Control Room Interface
# ============================================================================
class RBMKControlRoom:
    """Interactive RBMK control room"""
    
    def __init__(self):
        self.reactor = RBMKReactor()
        self.panel = RBMKControlPanel(self.reactor)
        self.auto_tick = False
        self.tick_interval = 0.5
    
    def startup_sequence(self):
        """Run startup sequence"""
        print(f"\n{Colors.BOLD}{Colors.GREEN}INITIATING STARTUP SEQUENCE{Colors.RESET}")
        print("Setting reactor state to STARTING...")
        
        # Partially withdraw rods to critical
        for rod in self.reactor.control_rods:
            rod.insertion = 50.0
        
        self.reactor.state = ReactorState.STARTING
        
        for _ in range(50):
            self.reactor.tick(1.0)
            if self.reactor.core_power > 100:
                break
        
        self.reactor.state = ReactorState.RUNNING
        print(f"{Colors.GREEN}✓ Reactor in RUNNING state{Colors.RESET}\n")
    
    def run(self):
        """Main control room loop"""
        self.startup_sequence()
        
        # Enable interactive mode
        try:
            import tty
            import termios
            
            original_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
            
            while self.panel.running:
                # Display
                self.panel.draw_display()
                
                # Get input
                try:
                    ch = sys.stdin.read(1)
                    if ch:
                        self.panel.handle_input(ch)
                        if self.auto_tick:
                            self.reactor.tick(1.0)
                except:
                    pass
                
                time.sleep(self.tick_interval)
            
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)
        
        except ImportError:
            # Fallback for non-Unix systems
            print("Interactive mode not available on this platform")
            print("Running demonstration mode...\n")
            self._demo_mode()
    
    def _demo_mode(self):
        """Demonstration mode for non-Unix systems"""
        print("DEMONSTRATION MODE")
        for i in range(100):
            self.reactor.tick(1.0)
            if i % 10 == 0:
                self.panel.draw_display()
                time.sleep(0.5)


# ============================================================================
# Main Entry Point
# ============================================================================
if __name__ == "__main__":
    print(f"{Colors.BOLD}{Colors.MAGENTA}")
    print("╔════════════════════════════════════════════╗")
    print("║      RBMK-1000 REACTOR SIMULATOR v1.0      ║")
    print("║    Full Graphite-Moderated Reactor Model   ║")
    print("╚════════════════════════════════════════════╝")
    print(Colors.RESET)
    
    control_room = RBMKControlRoom()
    try:
        control_room.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Simulation terminated by user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
