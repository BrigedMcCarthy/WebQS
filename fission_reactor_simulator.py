#!/usr/bin/env python3
"""
QS-247 Stirling Converter Fission Reactor - Realistic Physics Simulator

A comprehensive simulation of the QS-247 Fission Reactor with realistic
thermodynamic modeling, multi-sector temperature distribution, and
safety system implementation.

Date: January 13, 2026
Certified by: QSST Devs and QAC
"""

import time
import random
import math
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple
from datetime import datetime


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


class CRPosition(Enum):
    UP = 1
    NEUTRAL = 0
    DOWN = -1


# ============================================================================
# Data Classes
# ============================================================================
@dataclass
class ReactorSector:
    """Represents a temperature sector in the reactor core"""
    name: str
    temperature: float = 75.0  # Celsius
    target_temperature: float = 750.0
    thermal_mass: float = 1000.0  # Heat capacity
    neutron_flux: float = 0.0  # Percentage


@dataclass
class ConversionSystem:
    """Represents a power converter"""
    name: str
    power_output: float = 0.0  # kW
    efficiency: float = 0.85
    connected: bool = True
    synchronized: bool = False


# ============================================================================
# Main Reactor Simulation Class
# ============================================================================
class FissionReactor:
    """Realistic QS-247 Stirling Converter Fission Reactor Simulation"""
    
    def __init__(self):
        # === State Management ===
        self.state = ReactorState.COLD
        self.running_time = 0.0  # Seconds
        self.simulation_tick = 0
        
        # === Core Temperature ===
        self.sectors: List[ReactorSector] = [
            ReactorSector("Sector A (North)", 75.0, 750.0, 1000.0),
            ReactorSector("Sector B (South)", 75.0, 750.0, 1000.0),
            ReactorSector("Sector C (East)", 75.0, 750.0, 1000.0),
            ReactorSector("Sector D (West)", 75.0, 750.0, 1000.0),
        ]
        
        self.core_average_temp = 75.0
        
        # === Pressure System ===
        self.pressure = 1000.0  # PSI
        self.pressure_relief_enabled = [False, False, False, False]  # Per sector
        self.vault_door_closed = True
        
        # === Control Rods ===
        self.cr_insertion = 0.0  # Percentage (0-100)
        self.cr_speed = 1  # 1x or 2x
        self.cr_continuous_transit = False
        self.cr_moving = False
        self.cr_movement_direction = CRPosition.NEUTRAL
        self.cr_stuck = False
        self.cr_stuck_at = 0.0
        
        # === Neutron Flux ===
        self.neutron_flux = 0.0  # Percentage
        self.neutron_flux_max_reached = 0.0
        
        # === Power Systems ===
        self.thermal_loop_enabled = False
        self.thermal_loop_inlet_open = False
        self.thermal_loop_outlet_open = False
        
        self.converters: List[ConversionSystem] = [
            ConversionSystem("Converter A"),
            ConversionSystem("Converter B"),
            ConversionSystem("Converter C"),
            ConversionSystem("Converter D"),
        ]
        self.total_power_output = 0.0
        self.grid_connected = False
        self.grid_type = "NONE"  # NONE, PRIMARY, AUXILIARY, EXTERNAL
        
        # === Thermal System ===
        self.coolant_pump_speed = 100.0  # Percentage (50-150)
        self.thermal_efficiency = 100.0  # Percentage (50-100)
        self.combustion_chamber_temp = 1800.0  # Kelvin
        
        # === Fission Support Reactors ===
        self.support_reactors = [100.0] * 6  # Health percentage
        
        # === Safety Systems ===
        self.reactor_safety_enabled = True
        self.scram_engaged = False
        self.auto_scram_triggered = False
        self.thermal_power_alarm = False
        self.overpressure_alarm = False
        self.temperature_alarm = False
        
        # === Synchroscope ===
        self.synchroscope_value = 0.0  # -100 to +100, 0 = synchronized
        self.synchroscope_same_speed = False
        
        # === Fuel Status ===
        self.fuel_burnup = 0.0  # Percentage consumed
        self.fuel_cell_status = [100.0, 100.0, 95.0]  # Three receptacles
        
        # === Physics Constants ===
        self.ambient_temp = 25.0
        self.pressure_loss_coefficient = 0.8
        self.thermal_conductivity = 0.15
        self.neutron_multiplication_factor = 1.5
        
        # === Failure Simulation ===
        self.random_seed = None
        self.force_rod_fault = False
        
    # ========================================================================
    # Control Systems
    # ========================================================================
    
    def enable_thermal_loop(self, inlet: bool, outlet: bool):
        """Enable/disable the thermal loop cooling system"""
        if not self.reactor_safety_enabled:
            self.thermal_loop_enabled = True
            self.thermal_loop_inlet_open = inlet
            self.thermal_loop_outlet_open = outlet
            return True
        return False
    
    def set_coolant_pump_speed(self, speed: float):
        """Set coolant pump speed (50-150%)"""
        self.coolant_pump_speed = max(50.0, min(150.0, speed))
    
    def set_thermal_efficiency(self, efficiency: float):
        """Set thermal system efficiency (50-100%)"""
        self.thermal_efficiency = max(50.0, min(100.0, efficiency))
    
    def set_cr_speed(self, speed: int):
        """Set control rod speed (1x or 2x)"""
        self.cr_speed = 1 if speed == 1 else 2
    
    def set_cr_continuous_transit(self, enabled: bool):
        """Enable/disable continuous control rod transit"""
        self.cr_continuous_transit = enabled
    
    def move_control_rods(self, direction: CRPosition):
        """Move control rods up or down"""
        if self.scram_engaged or self.state == ReactorState.SHUTDOWN:
            return
        
        self.cr_movement_direction = direction
        self.cr_moving = True
    
    def move_control_rods_neutral(self):
        """Stop control rod movement"""
        self.cr_movement_direction = CRPosition.NEUTRAL
        self.cr_moving = False
    
    def toggle_relief_valve(self, sector: int):
        """Toggle relief valve for a specific sector"""
        if 0 <= sector < 4:
            self.pressure_relief_enabled[sector] = not self.pressure_relief_enabled[sector]
    
    def toggle_converter(self, converter_idx: int):
        """Toggle a converter on/off"""
        if 0 <= converter_idx < len(self.converters):
            self.converters[converter_idx].connected = not self.converters[converter_idx].connected
    
    def synchronize_with_grid(self) -> bool:
        """Attempt to synchronize with grid"""
        if not self.synchroscope_same_speed or abs(self.synchroscope_value) > 2.0:
            return False
        
        if self.grid_type != "AUXILIARY":
            return False
        
        self.grid_connected = True
        self.synchroscope_value = 0.0
        return True
    
    def disconnect_from_grid(self):
        """Disconnect from grid"""
        self.grid_connected = False
    
    def set_reactor_safety(self, enabled: bool):
        """Set reactor safety system (QAC+ only)"""
        if enabled:
            self.reactor_safety_enabled = True
        else:
            self.reactor_safety_enabled = False
    
    def engage_scram(self):
        """Activate emergency shutdown (SCRAM)"""
        self.scram_engaged = True
        self.state = ReactorState.SCRAM
        self.cr_insertion = 100.0  # Insert all rods
    
    def reset_scram(self):
        """Reset SCRAM system after shutdown"""
        if self.pressure < 1200 and self.core_average_temp < 100:
            self.scram_engaged = False
            self.auto_scram_triggered = False
            self.state = ReactorState.COLD
            return True
        return False
    
    # ========================================================================
    # Physics Simulation
    # ========================================================================
    
    def update_control_rods(self, delta_time: float = 1.0):
        """Update control rod position based on movement"""
        if not self.cr_moving or not self.cr_continuous_transit:
            return
        
        if self.cr_stuck:
            self.cr_insertion = self.cr_stuck_at
            return
        
        # Calculate rod movement
        movement_speed = 5.0 * self.cr_speed  # Percentage per second
        movement = movement_speed * delta_time * self.cr_movement_direction.value
        
        new_insertion = self.cr_insertion + movement
        self.cr_insertion = max(0.0, min(100.0, new_insertion))
    
    def update_neutron_flux(self):
        """Update neutron flux based on control rod position"""
        if self.cr_movement_direction == CRPosition.UP and self.cr_moving:
            # Flux increases while raising rods
            flux_rate = (100 - self.cr_insertion) / 100 * 0.15
            self.neutron_flux = min(20.0, self.neutron_flux + flux_rate)
            self.neutron_flux_max_reached = max(self.neutron_flux_max_reached, self.neutron_flux)
        else:
            # Flux decays when not raising rods
            self.neutron_flux = max(0.0, self.neutron_flux - 0.5)
    
    def update_temperature(self, delta_time: float = 1.0):
        """Update core temperature based on physical parameters"""
        for sector in self.sectors:
            # === Heat Generation ===
            # Power generation from neutron flux
            heat_from_fission = (100 - self.cr_insertion) * self.neutron_flux * 0.15
            
            # Power laser equivalent (combustion chamber heating)
            heat_from_combustion = (self.combustion_chamber_temp - 1800) * 0.02
            
            # === Heat Removal ===
            # Cooling from thermal loop
            cooling_rate = 0.0
            if self.thermal_loop_enabled and self.thermal_loop_inlet_open and self.thermal_loop_outlet_open:
                cooling_rate = (self.coolant_pump_speed / 100.0) * (self.thermal_efficiency / 100.0) * 8.0
            
            # Thermal efficiency affects temperature
            efficiency_factor = self.thermal_efficiency / 100.0
            
            # === Temperature Change Equation ===
            temp_delta = (heat_from_fission + heat_from_combustion - cooling_rate) * delta_time * efficiency_factor
            
            # Damping with thermal mass
            sector.temperature += temp_delta / sector.thermal_mass
            
            # Temperature approaches equilibrium
            equilibrium = 600.0 + (100 - self.cr_insertion) * 2.0
            relaxation = (equilibrium - sector.temperature) * 0.01
            sector.temperature += relaxation
            
            # Prevent physically impossible temperatures
            sector.temperature = max(self.ambient_temp, min(2000.0, sector.temperature))
        
        # Calculate average temperature
        self.core_average_temp = sum(s.temperature for s in self.sectors) / len(self.sectors)
    
    def update_pressure(self, delta_time: float = 1.0):
        """Update system pressure based on temperature and rods"""
        # === Pressure from Fission Heat ===
        # Higher temperature = higher pressure
        pressure_from_temp = (self.core_average_temp - 75.0) * 2.5
        
        # === Pressure from Neutron Flux ===
        # Neutron flux creates significant pressure increase
        pressure_from_flux = self.neutron_flux * 150.0
        
        # === Pressure Reduction from Converters ===
        converter_pressure_reduction = 0.0
        if self.grid_connected:
            converter_pressure_reduction = 700.0  # Converters reduce pressure by 600-800 PSI
        
        # === Relief Valve Effect ===
        relief_reduction = 0.0
        for i, enabled in enumerate(self.pressure_relief_enabled):
            if enabled:
                relief_reduction += 200.0
        
        # === Calculate Total Pressure ===
        base_pressure = 1000.0  # Atmospheric + system pressure
        self.pressure = base_pressure + pressure_from_temp + pressure_from_flux - converter_pressure_reduction - relief_reduction
        
        # Prevent negative pressure
        self.pressure = max(800.0, self.pressure)
    
    def update_power_output(self, delta_time: float = 1.0):
        """Update electrical power generation"""
        # Base power from temperature differential
        power_per_converter = 0.0
        
        if self.core_average_temp > 400:
            # Temperature above 400°C allows power generation
            temp_factor = (self.core_average_temp - 400) / 400
            base_power = 12500.0 * temp_factor  # kW per converter
            
            # Control rod insertion affects available power
            rod_factor = 1.0 - (self.cr_insertion / 100.0) * 0.3
            
            power_per_converter = base_power * rod_factor * (self.thermal_efficiency / 100.0)
        
        # Update each converter
        for i, converter in enumerate(self.converters):
            if converter.connected:
                converter.power_output = power_per_converter * converter.efficiency
            else:
                converter.power_output = 0.0
        
        self.total_power_output = sum(c.power_output for c in self.converters)
    
    def update_synchroscope(self):
        """Update grid synchronization indicator"""
        if not self.grid_connected:
            # Synchroscope drifts when not connected
            drift = random.uniform(-0.5, 0.5)
            self.synchroscope_value += drift
            self.synchroscope_value = max(-100, min(100, self.synchroscope_value))
        else:
            # Synchroscope locks at zero when synchronized
            self.synchroscope_value = max(-2, min(2, self.synchroscope_value))
        
        # Check if synchronized
        self.synchroscope_same_speed = abs(self.synchroscope_value) < 0.5
    
    def update_combustion_chamber(self):
        """Update combustion chamber temperature (no power laser in fission reactor)"""
        # Combustion chamber cools when not active
        cooling = (self.combustion_chamber_temp - 1800.0) * 0.05
        self.combustion_chamber_temp = max(1800.0, self.combustion_chamber_temp - cooling)
    
    def update_fuel_consumption(self):
        """Update fuel cell status"""
        # Fuel cells consume during operation
        if self.state == ReactorState.RUNNING and self.core_average_temp > 400:
            for i in range(len(self.fuel_cell_status)):
                consumption_rate = 0.05 if i < 2 else 0.15  # Fuel cell 3 consumes faster (manufacturing flaw)
                self.fuel_cell_status[i] = max(0.0, self.fuel_cell_status[i] - consumption_rate)
    
    def update_support_reactors(self):
        """Update support reactor status"""
        if self.state == ReactorState.RUNNING:
            for i in range(len(self.support_reactors)):
                # Support reactors degrade slightly under load
                self.support_reactors[i] = max(0.0, self.support_reactors[i] - 0.01)
    
    def check_safety_conditions(self):
        """Check for safety violations and trigger alarms/SCRAM"""
        # === Temperature Alarms ===
        if self.core_average_temp > 850:
            self.thermal_power_alarm = True
        else:
            self.thermal_power_alarm = False
        
        if self.core_average_temp > 1200:
            self.temperature_alarm = True
        
        # === Pressure Alarms ===
        if self.pressure > 3500:
            self.overpressure_alarm = True
        else:
            self.overpressure_alarm = False
        
        # === Auto-SCRAM Conditions ===
        if self.reactor_safety_enabled:
            if (self.pressure > 3700 or self.core_average_temp > 850 or 
                self.neutron_flux > 20.0 or self.core_average_temp > 1200):
                self.auto_scram_triggered = True
                self.engage_scram()
                return True
        
        # === Catastrophic Failure ===
        if self.pressure > 4000:
            self.state = ReactorState.CRITICAL
            return True
        
        return False
    
    def update_sensor_noise(self):
        """Add realistic sensor noise to readings"""
        noise = random.gauss(0, 2)
        self.core_average_temp = max(0, self.core_average_temp + noise * 0.1)
        noise = random.gauss(0, 5)
        self.pressure = max(0, self.pressure + noise * 0.1)
    
    # ========================================================================
    # Simulation Loop
    # ========================================================================
    
    def tick(self, delta_time: float = 1.0):
        """Execute one simulation cycle"""
        if self.state == ReactorState.SHUTDOWN or self.state == ReactorState.COLD:
            return
        
        self.simulation_tick += 1
        self.running_time += delta_time
        
        # Update all systems in order
        self.update_control_rods(delta_time)
        self.update_neutron_flux()
        self.update_temperature(delta_time)
        self.update_pressure(delta_time)
        self.update_power_output(delta_time)
        self.update_synchroscope()
        self.update_combustion_chamber()
        self.update_fuel_consumption()
        self.update_support_reactors()
        self.check_safety_conditions()
        self.update_sensor_noise()
        
        # Update state
        if self.scram_engaged:
            self.state = ReactorState.SCRAM
        elif self.state == ReactorState.STARTING and self.core_average_temp > 400:
            self.state = ReactorState.RUNNING
        elif self.state == ReactorState.SCRAM and self.pressure < 1200 and self.core_average_temp < 100:
            self.state = ReactorState.SHUTDOWN
    
    def cold_start(self):
        """Initialize cold start procedure"""
        if self.state != ReactorState.COLD:
            return False
        
        # Reset state
        self.core_average_temp = 75.0
        for sector in self.sectors:
            sector.temperature = 75.0
        self.pressure = 1000.0
        self.cr_insertion = 0.0
        self.neutron_flux = 0.0
        self.scram_engaged = False
        self.state = ReactorState.STARTING
        return True
    
    # ========================================================================
    # Status Reporting
    # ========================================================================
    
    def get_status_brief(self) -> str:
        """Get brief reactor status"""
        status_color = {
            ReactorState.COLD: Colors.CYAN,
            ReactorState.STARTING: Colors.YELLOW,
            ReactorState.RUNNING: Colors.GREEN,
            ReactorState.SCRAM: Colors.RED,
            ReactorState.SHUTDOWN: Colors.BLUE,
            ReactorState.CRITICAL: f"{Colors.BG_RED}{Colors.WHITE}",
        }
        
        color = status_color.get(self.state, Colors.WHITE)
        return f"{color}{self.state.value}{Colors.RESET}"
    
    def get_pressure_bar(self, width: int = 30) -> str:
        """Get visual pressure bar"""
        # 0 PSI = 0%, 4000 PSI = 100%
        percentage = min(100, (self.pressure / 4000) * 100)
        filled = int(width * percentage / 100)
        
        color = Colors.GREEN
        if self.pressure > 3500:
            color = Colors.RED
        elif self.pressure > 3000:
            color = Colors.YELLOW
        
        bar = "█" * filled + "░" * (width - filled)
        return f"{color}[{bar}]{Colors.RESET} {self.pressure:.1f} PSI"
    
    def get_temperature_bar(self, width: int = 30) -> str:
        """Get visual temperature bar"""
        # 75°C = 0%, 850°C = 100%
        percentage = min(100, ((self.core_average_temp - 75) / 775) * 100)
        filled = int(width * percentage / 100)
        
        color = Colors.GREEN
        if self.core_average_temp > 850:
            color = Colors.RED
        elif self.core_average_temp > 750:
            color = Colors.YELLOW
        
        bar = "█" * filled + "░" * (width - filled)
        return f"{color}[{bar}]{Colors.RESET} {self.core_average_temp:.1f}°C"
    
    def get_system_status_panel(self) -> List[str]:
        """Get right-side system status panel"""
        lines = []
        lines.append(f"{Colors.BOLD}SYSTEM STATUS{Colors.RESET}")
        lines.append(f"{Colors.CYAN}{'─' * 28}{Colors.RESET}")
        
        # Core status
        lines.append(f"State: {self.get_status_brief()}")
        lines.append(f"Time:  {self.running_time:7.1f}s")
        lines.append("")
        
        # Temperature and pressure at a glance
        temp_status = "SAFE"
        if self.core_average_temp > 850:
            temp_status = f"{Colors.RED}CRITICAL{Colors.RESET}"
        elif self.core_average_temp > 750:
            temp_status = f"{Colors.YELLOW}HIGH{Colors.RESET}"
        
        pressure_status = "SAFE"
        if self.pressure > 3700:
            pressure_status = f"{Colors.RED}CRITICAL{Colors.RESET}"
        elif self.pressure > 3500:
            pressure_status = f"{Colors.YELLOW}HIGH{Colors.RESET}"
        
        lines.append(f"Temp:  {self.core_average_temp:6.1f}°C [{temp_status}]")
        lines.append(f"Press: {self.pressure:6.1f} PSI [{pressure_status}]")
        lines.append(f"Flux:  {self.neutron_flux:6.2f}%")
        lines.append("")
        
        # Control rods
        rod_status = "MOVING" if self.cr_moving else "STOPPED"
        if self.cr_stuck:
            rod_status = f"{Colors.RED}STUCK{Colors.RESET}"
        lines.append(f"Rods:  {self.cr_insertion:6.2f}% [{rod_status}]")
        lines.append("")
        
        # Power
        power_pct = min(100, (self.total_power_output / 50000) * 100)
        power_bar = "█" * int(power_pct / 10) + "░" * (10 - int(power_pct / 10))
        lines.append(f"Power: [{power_bar}]")
        lines.append(f"       {self.total_power_output:7.0f} kW")
        lines.append("")
        
        # Cooling
        lines.append(f"Coolant: {self.coolant_pump_speed:5.1f}%")
        lines.append(f"Eff:     {self.thermal_efficiency:5.1f}%")
        lines.append(f"Loop:    {'ON' if self.thermal_loop_enabled else 'OFF'}")
        lines.append("")
        
        # Safety indicators
        lines.append(f"{Colors.BOLD}SAFETY{Colors.RESET}")
        lines.append(f"{Colors.CYAN}{'─' * 28}{Colors.RESET}")
        
        safety_symbols = []
        if self.reactor_safety_enabled:
            safety_symbols.append("🔒 Safety Lock")
        else:
            safety_symbols.append(f"{Colors.RED}🔓 Safety DISABLED{Colors.RESET}")
        
        if not self.scram_engaged:
            safety_symbols.append("✓ SCRAM Ready")
        else:
            safety_symbols.append(f"{Colors.RED}⚠ SCRAM ACTIVE{Colors.RESET}")
        
        if not self.auto_scram_triggered:
            safety_symbols.append("✓ Auto-SCRAM OK")
        else:
            safety_symbols.append(f"{Colors.RED}⚠ Auto-SCRAM TRIG{Colors.RESET}")
        
        if self.vault_door_closed:
            safety_symbols.append("🚪 Vault Closed")
        else:
            safety_symbols.append(f"{Colors.YELLOW}🚪 Vault Open{Colors.RESET}")
        
        for symbol in safety_symbols:
            lines.append(symbol)
        
        lines.append("")
        
        # Alarms
        if self.thermal_power_alarm or self.overpressure_alarm or self.temperature_alarm or self.cr_stuck:
            lines.append(f"{Colors.BOLD}{Colors.RED}ALARMS{Colors.RESET}")
            lines.append(f"{Colors.CYAN}{'─' * 28}{Colors.RESET}")
            if self.thermal_power_alarm:
                lines.append(f"{Colors.YELLOW}⚠ THERMAL POWER{Colors.RESET}")
            if self.overpressure_alarm:
                lines.append(f"{Colors.RED}⚠ OVERPRESSURE{Colors.RESET}")
            if self.temperature_alarm:
                lines.append(f"{Colors.RED}⚠ TEMP CRITICAL{Colors.RESET}")
            if self.cr_stuck:
                lines.append(f"{Colors.RED}⚠ ROD FAULT{Colors.RESET}")
        else:
            lines.append(f"{Colors.BOLD}{Colors.GREEN}✓ ALL NOMINAL{Colors.RESET}")
        
        return lines
    
    def get_reactor_overview(self) -> str:
        """Get full reactor status overview with side panel"""
        left_lines = []
        left_lines.append(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════{Colors.RESET}")
        left_lines.append(f"{Colors.BOLD}QS-247 FISSION REACTOR - SYSTEM OVERVIEW{Colors.RESET}")
        left_lines.append(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════{Colors.RESET}\n")
        
        # === State ===
        left_lines.append(f"Reactor State: {self.get_status_brief()}")
        left_lines.append(f"Running Time: {self.running_time:.1f}s | Tick: {self.simulation_tick}")
        left_lines.append("")
        
        # === Core Parameters ===
        left_lines.append(f"{Colors.BOLD}Core Parameters:{Colors.RESET}")
        left_lines.append(f"  Temperature: {self.get_temperature_bar()}")
        left_lines.append(f"  Pressure:    {self.get_pressure_bar()}")
        left_lines.append(f"  Neutron Flux: {self.neutron_flux:.2f}%")
        left_lines.append("")
        
        # === Sector Temperatures ===
        left_lines.append(f"{Colors.BOLD}Sector Temperatures:{Colors.RESET}")
        for sector in self.sectors:
            bar_width = 20
            percentage = min(100, ((sector.temperature - 75) / 775) * 100)
            filled = int(bar_width * percentage / 100)
            bar = "█" * filled + "░" * (bar_width - filled)
            left_lines.append(f"  {sector.name:20s}: [{bar}] {sector.temperature:7.1f}°C")
        left_lines.append("")
        
        # === Control System ===
        left_lines.append(f"{Colors.BOLD}Control Systems:{Colors.RESET}")
        left_lines.append(f"  Control Rod Insertion: {self.cr_insertion:6.2f}% {'(STUCK)' if self.cr_stuck else ''}")
        left_lines.append(f"  Control Rod Speed: {self.cr_speed}x | Continuous Transit: {'ON' if self.cr_continuous_transit else 'OFF'}")
        left_lines.append(f"  Neutron Flux Max: {self.neutron_flux_max_reached:.2f}%")
        left_lines.append("")
        
        # === Power Systems ===
        left_lines.append(f"{Colors.BOLD}Power Generation:{Colors.RESET}")
        left_lines.append(f"  Total Output: {self.total_power_output:7.1f} kW (Target: 40-50k kW)")
        for i, converter in enumerate(self.converters):
            status = "ON" if converter.connected else "OFF"
            sync = "SYNC" if converter.synchronized else "----"
            left_lines.append(f"    {converter.name}: {converter.power_output:7.1f} kW [{status}] {sync}")
        left_lines.append("")
        
        # === Cooling System ===
        left_lines.append(f"{Colors.BOLD}Thermal Control:{Colors.RESET}")
        left_lines.append(f"  Thermal Loop: {'ENABLED' if self.thermal_loop_enabled else 'DISABLED'} (Inlet: {['CLOSED','OPEN'][self.thermal_loop_inlet_open]} | Outlet: {['CLOSED','OPEN'][self.thermal_loop_outlet_open]})")
        left_lines.append(f"  Coolant Pump Speed: {self.coolant_pump_speed:.1f}% (Range: 50-150%)")
        left_lines.append(f"  Thermal Efficiency: {self.thermal_efficiency:.1f}% (Range: 50-100%)")
        left_lines.append(f"  Combustion Chamber: {self.combustion_chamber_temp:.1f}K")
        left_lines.append("")
        
        # === Relief Valves ===
        left_lines.append(f"{Colors.BOLD}Relief Valves:{Colors.RESET}")
        for i, enabled in enumerate(self.pressure_relief_enabled):
            status = "OPEN" if enabled else "CLOSED"
            left_lines.append(f"  Sector {chr(65+i)}: {status}")
        left_lines.append("")
        
        # === Safety Status ===
        left_lines.append(f"{Colors.BOLD}Safety Status:{Colors.RESET}")
        left_lines.append(f"  Reactor Safety System: {'ENABLED' if self.reactor_safety_enabled else f'{Colors.RED}DISABLED{Colors.RESET}'}")
        left_lines.append(f"  SCRAM Engaged: {'YES' if self.scram_engaged else 'NO'}")
        left_lines.append(f"  Auto-SCRAM Triggered: {'YES' if self.auto_scram_triggered else 'NO'}")
        left_lines.append(f"  Vault Door: {['OPEN' if self.vault_door_closed else 'CLOSED']}")
        left_lines.append("")
        
        # === Alarms ===
        alarms = []
        if self.thermal_power_alarm:
            alarms.append(f"{Colors.YELLOW}THERMAL POWER ALARM{Colors.RESET}")
        if self.overpressure_alarm:
            alarms.append(f"{Colors.RED}OVERPRESSURE ALARM{Colors.RESET}")
        if self.temperature_alarm:
            alarms.append(f"{Colors.RED}TEMPERATURE ALARM{Colors.RESET}")
        if self.cr_stuck:
            alarms.append(f"{Colors.RED}CONTROL ROD FAULT{Colors.RESET}")
        
        if alarms:
            left_lines.append(f"{Colors.BOLD}{Colors.RED}Active Alarms:{Colors.RESET}")
            for alarm in alarms:
                left_lines.append(f"  ⚠️  {alarm}")
        else:
            left_lines.append(f"{Colors.BOLD}{Colors.GREEN}All Systems Nominal{Colors.RESET}")
        
        left_lines.append(f"{Colors.CYAN}═══════════════════════════════════════════{Colors.RESET}")
        
        # Get right panel
        right_lines = self.get_system_status_panel()
        
        # Combine left and right with proper spacing
        max_left = max(len(line) - len(self._strip_colors(line)) + len(self._strip_colors(line)) for line in left_lines)
        left_width = 46  # Approximate width for left column
        
        combined_output = ["\n"]
        max_lines = max(len(left_lines), len(right_lines))
        
        for i in range(max_lines):
            left = left_lines[i] if i < len(left_lines) else ""
            right = right_lines[i] if i < len(right_lines) else ""
            
            # Calculate padding needed
            stripped_left = self._strip_colors(left)
            padding = left_width - len(stripped_left)
            
            combined_output.append(left + " " * max(1, padding) + right)
        
        combined_output.append("")
        return "\n".join(combined_output)
    
    @staticmethod
    def _strip_colors(text: str) -> str:
        """Remove ANSI color codes from text"""
        import re
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        return ansi_escape.sub('', text)


# ============================================================================
# Interactive Simulator
# ============================================================================
class ReactorSimulation:
    """Interactive command-line interface for reactor simulation"""
    
    def __init__(self):
        self.reactor = FissionReactor()
        self.running = True
        self.auto_tick = False
        self.tick_delay = 0.1
        self.auto_start_running = False
        
    def print_menu(self):
        """Print main control menu"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}QS-247 REACTOR CONTROL MENU{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.RESET}")
        print("1. Raise Control Rods")
        print("2. Lower Control Rods")
        print("3. Stop Rod Movement")
        print("4. Toggle Continuous Transit")
        print("5. Set Coolant Pump Speed")
        print("6. Set Thermal Efficiency")
        print("7. Toggle Relief Valves")
        print("8. Toggle Converters")
        print("9. Synchronize with Grid")
        print("10. Disconnect from Grid")
        print("11. Enable Thermal Loop")
        print("12. Engage SCRAM")
        print("13. Reset SCRAM")
        print("14. Manual Tick (1 second)")
        print("15. Auto Tick (continuous)")
        print("16. Cold Start")
        print("17. Toggle Auto Tick")
        print("18. Show Full Status")
        print(f"{Colors.GREEN}19. Auto-Start Procedure{Colors.RESET}")
        print("0. Exit")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.RESET}")
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def run_auto_start(self):
        """Run automatic startup procedure"""
        print(f"\n{Colors.BOLD}{Colors.GREEN}INITIATING AUTO-START PROCEDURE{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.RESET}\n")
        
        self.auto_start_running = True
        
        # Step 1: Cold start
        print("[ STEP 1/5 ] Initiating cold start sequence...")
        if not self.reactor.cold_start():
            print(f"{Colors.RED}Cold start failed!{Colors.RESET}")
            self.auto_start_running = False
            return
        time.sleep(1.0)
        
        # Step 2: Enable thermal systems
        print("[ STEP 2/5 ] Enabling thermal loop and setting parameters...")
        self.reactor.set_reactor_safety(True)
        self.reactor.enable_thermal_loop(True, True)
        self.reactor.set_coolant_pump_speed(100.0)
        self.reactor.set_thermal_efficiency(100.0)
        self.reactor.set_cr_speed(1)
        self.reactor.set_cr_continuous_transit(True)
        for _ in range(5):
            self.reactor.tick(1.0)
        time.sleep(1.0)
        
        # Step 3: Raise control rods gradually
        print("[ STEP 3/5 ] Raising control rods and monitoring parameters...")
        self.reactor.move_control_rods(CRPosition.UP)
        
        target_cr = 35.0
        while self.reactor.cr_insertion < target_cr and self.auto_start_running:
            self.reactor.tick(1.0)
            
            # Safety check
            if self.reactor.neutron_flux > 8.0:
                self.reactor.move_control_rods_neutral()
                print(f"  → Neutron flux reached 8%, pausing rod movement")
                for _ in range(5):
                    self.reactor.tick(1.0)
                if self.reactor.neutron_flux < 1.0:
                    self.reactor.move_control_rods(CRPosition.UP)
            
            if self.reactor.pressure > 3200:
                self.reactor.move_control_rods_neutral()
                print(f"  → Pressure exceeded 3200 PSI, SCRAM triggered")
                self.reactor.engage_scram()
                self.auto_start_running = False
                return
            
            # Progress indicator
            if int(self.reactor.cr_insertion) % 5 == 0 and int(self.reactor.running_time) % 5 == 0:
                print(f"  → CR: {self.reactor.cr_insertion:.1f}% | Temp: {self.reactor.core_average_temp:.1f}°C | Pressure: {self.reactor.pressure:.1f} PSI")
        
        self.reactor.move_control_rods_neutral()
        time.sleep(1.0)
        
        # Step 4: Stabilize temperature
        print("[ STEP 4/5 ] Stabilizing reactor temperature...")
        stabilization_ticks = 0
        while self.reactor.core_average_temp < 700 and stabilization_ticks < 100 and self.auto_start_running:
            self.reactor.tick(1.0)
            stabilization_ticks += 1
        
        # Step 5: Enable converters and prepare for grid
        print("[ STEP 5/5 ] Enabling power converters...")
        for converter in self.reactor.converters:
            converter.connected = True
        
        for _ in range(20):
            self.reactor.tick(1.0)
        
        self.auto_start_running = False
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ AUTO-START PROCEDURE COMPLETE{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.RESET}")
        print(f"Reactor State: {self.reactor.get_status_brief()}")
        print(f"Temperature: {self.reactor.core_average_temp:.1f}°C")
        print(f"Pressure: {self.reactor.pressure:.1f} PSI")
        print(f"Power Output: {self.reactor.total_power_output:.1f} kW")
        print(f"\nReactor is now in RUNNING state and ready for operations.\n")
    
    def run(self):
        """Run the interactive simulation"""
        self.reactor.cold_start()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}QS-247 Fission Reactor Simulator Initialized{Colors.RESET}")
        print("Type 'help' for commands or '18' to see full status\n")
        
        while self.running:
            if self.auto_tick:
                self.reactor.tick(1.0)
                print(self.reactor.get_status_brief() + f" | T:{self.reactor.core_average_temp:.0f}°C | P:{self.reactor.pressure:.0f}PSI")
                time.sleep(self.tick_delay)
            else:
                print(self.reactor.get_status_brief())
                self.print_menu()
                choice = input(f"{Colors.BOLD}Enter command: {Colors.RESET}").strip()
                self._handle_command(choice)
    
    def _handle_command(self, choice: str):
        """Handle user command"""
        if choice == "0":
            self.running = False
            print(f"{Colors.GREEN}Shutting down simulation...{Colors.RESET}")
        elif choice == "1":
            self.reactor.move_control_rods(CRPosition.UP)
            print("Raising control rods...")
        elif choice == "2":
            self.reactor.move_control_rods(CRPosition.DOWN)
            print("Lowering control rods...")
        elif choice == "3":
            self.reactor.move_control_rods_neutral()
            print("Stopping rod movement")
        elif choice == "4":
            self.reactor.set_cr_continuous_transit(not self.reactor.cr_continuous_transit)
            print(f"Continuous Transit: {self.reactor.cr_continuous_transit}")
        elif choice == "5":
            speed = float(input("Enter coolant pump speed (50-150%): "))
            self.reactor.set_coolant_pump_speed(speed)
            print(f"Coolant pump set to {self.reactor.coolant_pump_speed:.1f}%")
        elif choice == "6":
            eff = float(input("Enter thermal efficiency (50-100%): "))
            self.reactor.set_thermal_efficiency(eff)
            print(f"Thermal efficiency set to {self.reactor.thermal_efficiency:.1f}%")
        elif choice == "7":
            sector = int(input("Enter sector (0-3): "))
            self.reactor.toggle_relief_valve(sector)
            status = "OPEN" if self.reactor.pressure_relief_enabled[sector] else "CLOSED"
            print(f"Relief valve Sector {chr(65+sector)}: {status}")
        elif choice == "8":
            conv = int(input("Enter converter (0-3): "))
            self.reactor.toggle_converter(conv)
            status = "ENABLED" if self.reactor.converters[conv].connected else "DISABLED"
            print(f"Converter {chr(65+conv)}: {status}")
        elif choice == "9":
            if self.reactor.synchronize_with_grid():
                print(f"{Colors.GREEN}Synchronized with AUXILIARY grid!{Colors.RESET}")
            else:
                print(f"{Colors.RED}Synchronization failed!{Colors.RESET}")
        elif choice == "10":
            self.reactor.disconnect_from_grid()
            print("Disconnected from grid")
        elif choice == "11":
            inlet = input("Open inlet? (y/n): ").lower() == 'y'
            outlet = input("Open outlet? (y/n): ").lower() == 'y'
            self.reactor.enable_thermal_loop(inlet, outlet)
            print(f"Thermal loop enabled")
        elif choice == "12":
            self.reactor.engage_scram()
            print(f"{Colors.RED}SCRAM ENGAGED - EMERGENCY SHUTDOWN{Colors.RESET}")
        elif choice == "13":
            if self.reactor.reset_scram():
                print("SCRAM reset successfully")
            else:
                print("Conditions not safe for SCRAM reset")
        elif choice == "14":
            self.reactor.tick(1.0)
            print(f"Tick executed | Reactor: {self.reactor.get_status_brief()}")
        elif choice == "15":
            # Run 10 ticks
            for _ in range(10):
                self.reactor.tick(1.0)
            print(f"10 ticks executed | Reactor: {self.reactor.get_status_brief()}")
        elif choice == "16":
            if self.reactor.cold_start():
                print("Cold start sequence initiated")
            else:
                print("Cold start failed - reactor not in COLD state")
        elif choice == "17":
            self.auto_tick = not self.auto_tick
            mode = "ENABLED" if self.auto_tick else "DISABLED"
            print(f"Auto-tick: {mode}")
        elif choice == "18":
            self.clear_screen()
            print(self.reactor.get_reactor_overview())
        elif choice == "19":
            self.run_auto_start()
        else:
            print(f"{Colors.RED}Unknown command{Colors.RESET}")


# ============================================================================
# Main Entry Point
# ============================================================================
if __name__ == "__main__":
    print(f"{Colors.BOLD}{Colors.MAGENTA}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   QS-247 STIRLING CONVERTER FISSION REACTOR v1.0       ║")
    print("║           Realistic Physics Simulator                  ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(Colors.RESET)
    
    sim = ReactorSimulation()
    try:
        sim.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Simulation interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
