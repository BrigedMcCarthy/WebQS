# Q.S.E.R.F RPG v2.0 - Quick Start Guide

## Getting Started

### Launch the Game
```bash
cd /workspaces/WebQS
python3 rpg_improved.py
```

### Character Creation
1. Enter your character name
2. Select personnel classification (1-4)
3. Read facility briefing

## Game Phases

### Phase 1: Introduction
- Facility briefing and welcome

### Phase 2: Normal Operations  
- Learn DMR controls
- Optionally interact with reactor systems
- Adjust power, coolant, and thermal parameters

### Phase 3: Emergency Detection
- System failures cascade
- Make critical decisions (3 options)

### Phase 4: Final Countdown
- Watch the inevitable unfold
- Atmospheric crisis sequence

### Phase 5: Epilogue
- Historical aftermath
- Consequences revealed

## DMR Control Interface

**Available Commands During Normal Operations:**
```
1 = Adjust power laser level (0-5)
2 = Adjust coolant pump speed (50-150%)
3 = Adjust thermal system efficiency (50-100%)
4 = Check fuel cell status
5 = View support reactor status
6 = Continue shift (triggers safety test)
```

## Quick Technical Reference

| System | Normal | Min | Max |
|--------|--------|-----|-----|
| Power Laser | 3-5 | 0 | 5 |
| Coolant Pump | 100% | 50% | 150% |
| Thermal Eff. | 100% | 50% | 100% |
| Temperature | 3800K | 1800K | 8000K+ |
| Pressure | 98% | 50% | 150%+ |

## Tips

- ✓ Interact with controls to learn systems before emergency
- ✓ Pay attention to fuel cell degradation
- ✓ Listen to narrative carefully
- ✓ Each decision has consequences
- ✓ Play multiple times for different perspectives

## Game Duration

**Total playtime:** 10-15 minutes
- Intro: 1-2 min
- Operations: 3-5 min
- Emergency: 2-3 min
- Countdown: 2-3 min
- Epilogue: 2-3 min

## Troubleshooting

**No audio?** 
- Game works without sound, optional feature

**Colors not showing?**
- Try different terminal emulator

**Game crashes?**
- Ensure Python 3.6+ installed
- Check file permissions

## Key Story Context

**Date:** August 18, 1985
**Location:** Madison Research Institute, Connecticut
**Depth:** 3000 meters underground
**Personnel:** ~230 night shift operators
**Reactor:** Dark Matter Reactor (DMR), 30 GW nominal

## Files Included

- `rpg_improved.py` - Main game executable
- `DMR_OPERATIONS_MANUAL.md` - Technical specifications
- `README_GAME.md` - Complete documentation
- `Audio/` - Sound effects (optional)

---

**Ready?** Run: `python3 rpg_improved.py`
