# Q.S.E.R.F RPG v2.0 - Dark Matter Reactor Operations Simulator

## Game Overview

Q.S.E.R.F (Quantum Science Energy Research Facility) Text RPG v2.0 is an immersive interactive fiction game set in the Quantum Universe on August 18, 1985. Players take on the role of facility personnel during the catastrophic failure of the Dark Matter Reactor at the Madison Research Institute.

## What's New in v2.0

### ✨ DMR Operations System

The game now features a full **Dark Matter Reactor (DMR) Operations Control Interface** that allows players to:

- **Monitor Real-Time Parameters**
  - Power output (0-30 GW)
  - Temperature (Kelvin)
  - Pressure levels
  - Fuel cell status
  - Support reactor status
  - Safety system readiness

- **Control Critical Systems**
  - Adjust power laser levels (0-5 intervals)
  - Manage coolant pump speed (50-150%)
  - Control thermal system efficiency (50-100%)
  - Monitor fuel cell receptacles (3 units)
  - Track support fission reactors (6 units)

- **Check System Status**
  - Fuel cell receptacle health report
  - Support reactor operational status
  - Safety system diagnostics
  - Containment field integrity
  - Radiation shield status

### 🎮 Interactive Control Room

During normal operations (before the emergency), players can:

1. Familiarize themselves with reactor control systems
2. Adjust reactor parameters in real-time
3. Monitor operational dashboards
4. Learn about the facility's systems before the crisis

### 📊 Realistic Reactor Dynamics

The DMR system features:
- **Dynamic parameter relationships** - Power affects temperature, coolant affects pressure
- **Fuel cell degradation** - Receptacle 3 has a documented manufacturing flaw
- **Support reactor integration** - Six fission reactors provide facility power
- **Safety thresholds** - Critical alerts when parameters exceed safe ranges
- **System interdependencies** - Changes to one system affect others

## Gameplay Features

### Story Elements
- Character creation with multiple personnel classifications
- Authentic 1985 facility setting with period-accurate details
- Full lore integration from the Quantum Corporation universe
- Multiple decision points that affect gameplay
- Detailed narrative of the August 18, 1985 catastrophe

### Game Mechanics
1. **Normal Operations Phase** - Manage reactor systems, learn controls
2. **Emergency Detection** - System failures cascade realistically
3. **Crisis Response** - Make critical decisions under pressure
4. **Countdown Phase** - Watch the inevitable unfold
5. **Epilogue** - Historical aftermath and consequences

### Personnel Classifications
- **Reactor Operations Technician** - Direct reactor oversight
- **Safety Systems Engineer** - Emergency protocol specialist
- **Facility Maintenance Supervisor** - Support systems expert
- **Junior Control Room Operator** - Recent hire, learner role

## Technical Specifications

### DMR Operational Parameters

| System | Range | Normal | Warning | Critical |
|--------|-------|--------|---------|----------|
| Power Output | 0-30 GW | 30 GW | 20+ GW | N/A |
| Temperature | 1800-8000 K | 3800 K | 5000+ K | 6000+ K |
| Pressure | 50-150% | 98% | 110-120% | 120%+ |
| Fuel Cell 1 | 0-100% | 100% | <90% | <50% |
| Fuel Cell 2 | 0-100% | 100% | <90% | <50% |
| Fuel Cell 3 | 0-100% | 95%* | <85% | <50% |
| Coolant Speed | 50-150% | 100% | <75% | N/A |
| Thermal Efficiency | 50-100% | 100% | <75% | N/A |

*Fuel Cell 3: Degraded baseline due to manufacturing flaw

### Support Systems
- **6 Fission Reactors:** Provide primary facility power and DMR support
- **3 Pressure Seals:** Maintain atmospheric separation (Quadrants 1-3)
- **Containment Field:** Electromagnetic confinement (100% nominal)
- **Radiation Shield:** Absorbs laser particle emissions (100% nominal)
- **Emergency Stall Protocol:** DMRECSP (primary emergency shutdown)

## Lore Integration

The game is built on the extended Quantum Corporation lore, featuring:

- **Real historical figures** from the lore (Dr. Helene Kaiser, Dr. Daniel Weldman, Dr. Martin Miller, etc.)
- **Authentic facility details** (3000 meters underground, 50-foot concrete walls, etc.)
- **Technical accuracy** based on lore specifications
- **Historical context** (James McCarthy administration, Project Ignition, etc.)
- **Consequences** (Quantum's empire begins collapse, 230+ casualties, radiation spread)

## How to Play

### Starting the Game
```bash
python3 rpg_improved.py
```

### Character Creation
1. Enter your character name
2. Select personnel classification (1-4)
3. Read facility briefing

### Normal Operations Phase
1. Learn about the DMR control interface
2. Choose to familiarize yourself with systems (optional)
3. Adjust reactor parameters if desired
4. Observe system interactions and dynamics

### Emergency Phase
1. Experience cascading system failures
2. React to critical alerts
3. Make emergency decisions
4. Attempt recovery procedures

### Resolution
1. Final countdown sequence
2. Catastrophic failure cinematics
3. Epilogue describing world consequences
4. Game end credits

## File Structure

```
/workspaces/WebQS/
├── rpg_improved.py              # Main game executable (v2.0)
├── DMR_OPERATIONS_MANUAL.md     # Complete DMR technical manual
├── script.txt                   # Original story script
├── rpg.py                       # Original version (legacy)
└── Audio/                       # Sound effects directory
    ├── key is online.wav
    ├── gravity laser.wav
    ├── center position.wav
    ├── startupopen.wav
    ├── Dark-Matter-Core-Temp-safe-limits.mp3
    ├── Integrity-dropping.mp3
    ├── Integrity-Monitoring-Failure.mp3
    └── eme_shutdown.mp3
```

## System Requirements

- Python 3.6+
- `playsound` library (for audio, optional)
- Terminal/console with color support
- 120-150 seconds for complete playthrough

## Credits

**Game Design & Development:**
- Briged McCarthy (Original Concept & Lore)
- AI Assistant (v2.0 Enhancement & DMR Systems)

**Lore & Universe:**
- Series One: The Quantum Corporation
- Complete timeline and world-building
- Character backgrounds and technical specifications

**Audio:**
- Sound effects for immersive experience
- Gracefully degrades in headless environments

## Game Statistics

- **Play Time:** 10-15 minutes (normal playthrough)
- **Replay Value:** Multiple endings and decision paths
- **Difficulty:** Narrative/Low (focuses on experience over challenge)
- **Accessibility:** Terminal-based, no graphics required
- **Educational Value:** Learn about reactor operations and physics

## Known Features

✅ Dynamic DMR operations system
✅ Real-time parameter monitoring
✅ Interactive control interface
✅ Full lore integration
✅ Multiple character classes
✅ Realistic system cascading failures
✅ Period-accurate 1985 setting
✅ Audio support with graceful degradation
✅ Color-coded status displays
✅ Comprehensive epilogue

## Future Expansion Ideas

- Multiple facility layouts
- Different sabotage scenarios
- Success/survival paths
- More detailed system failures
- Save/load game state
- Difficulty levels
- Alternative timeline branches
- Extended lore sections
- Additional personnel interactions

## Support & Feedback

This game is a work in progress. For issues, suggestions, or feedback regarding:
- Gameplay mechanics
- Story elements
- Technical implementation
- Lore accuracy

Please contact the development team or submit issues to the project repository.

---

**Version:** 2.0
**Release Date:** January 13, 2026
**Status:** Production Ready
**Last Updated:** January 13, 2026
