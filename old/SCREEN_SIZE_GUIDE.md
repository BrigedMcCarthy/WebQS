# RBMK Reactor Simulator - Screen Size Optimization Guide

## Overview

The RBMK-1000 Reactor Simulator has been optimized to run on screen sizes ranging from **24 columns** (ultra-compact) to **120+ columns** (full display). The display automatically adapts based on available terminal width.

## Supported Screen Sizes

### Ultra-Compact Mode (24-29 columns)
**Ideal for:** Mobile terminals, constrained SSH sessions, minimal terminals

**Features:**
- Single-character parameter labels (P, T, R, V, D)
- Ultra-compact 3-character wide bars using block characters (▁▂▃█)
- State abbreviation (3 chars: COL, STA, RUN, etc.)
- Single-character alarms (T=Thermal, P=Pressure, S=SCRAM, ◆=OK)
- Minimal spacing, no keyboard guide
- **Total display: 11 lines**

**Example (24 columns):**
```
┌──────────────────────┐
│         RBMK         │
├──────────────────────┤
│P█899W│
│T▁279C│
│R▃75B│
│V▁ 0%│
│D▁ 0%│
├──────────────────────┤
│RUN ◆  20s│
└──────────────────────┘
```

### Compact Mode (30-49 columns)
**Ideal for:** Split terminal panes, small terminal windows, retro computing

**Features:**
- 2-character parameter labels (P:, T:, R:, V:, D:)
- Compact 4-10 character wide bars with ▓░ characters
- Full state name (4 chars: RUNN, SCRA, COLD, etc.)
- Pump status shown as block symbols (█=ON, ░=OFF)
- Single-character alarm codes (T, P, V, S)
- Keyboard guide hidden
- **Total display: 13 lines**

**Example (32 columns):**
```
┌──────────────────────────────┐
│         RBMK REACTOR         │
├──────────────────────────────┤
│P:[▓▓▓▓▓▓▓░]  899│
│T:[▓░░░░░░░]  279│
│R:[▓▓▓▓░░░░] 74.6│
│V:[░░░░░░░░]  0.0│
│D:[░░░░░░░░]  0.0│
├──────────────────────────────┤
│ RUNN T: 20s         │
│ P1:█P2:█P3:█P4:░             │
│ OK                  │
└──────────────────────────────┘
```

### Standard/Full Mode (50+ columns)
**Ideal for:** Normal terminal windows, desktop displays, 80+ column terminals

**Features:**
- Full parameter names (Power:, Temp:, Pressure:, Void:, Rods:)
- Wide 15-60 character bars with detailed visuals
- Complete state names with full time displays
- Detailed pump status with ON/OFF labels
- Full relief/regulation/safety status lines
- Multi-line alarm display with color-coded warnings
- Keyboard control guide displayed
- **Total display: 15 lines**

**Example (60 columns):**
```
┌──────────────────────────────────────────────────────────┐
│                    RBMK-1000 REACTOR                     │
├──────────────────────────────────────────────────────────┤
│ Power:     [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░]  899.1 MW │
│ Temp:      [▓▓▓░░░░░░░░░░░░░░░░░]  279.1°C │
│ Pressure:  [▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░]  74.6 Bar │
│ Void:      [░░░░░░░░░░░░░░░░░░░░]   0.0% │
│ Rods:      [░░░░░░░░░░░░░░░░░░░░]    0.0% │
├──────────────────────────────────────────────────────────┤
│ RUNNING  | Time:    20.0s                       │
│ Pumps: P1:ON  P2:ON  P3:ON  P4:OFF Flow:  90.0%          │
│ Relief: CLOSED | Regulation: OFF | Safety: ENABLED       │
├──────────────────────────────────────────────────────────┤
│ Alarms: ✓ ALL NOMINAL                           │
└──────────────────────────────────────────────────────────┘
```

## Terminal Size Detection

The simulator automatically detects your terminal width using `shutil.get_terminal_size()` and selects the appropriate display mode:

```python
def get_terminal_width(self) -> int:
    """Get terminal width - scales from 24 to 120+ columns"""
    width = shutil.get_terminal_size((80, 24)).columns
    if width < 24:
        width = 24
    elif width > 120:
        width = 120
    return width
```

## Responsive Design Details

### Bar Graph Scaling
- **Ultra-compact:** 3-char blocks (▁▂▃█) - single character representation
- **Compact:** 4-10 character bars with filled/empty blocks
- **Standard:** 15-60 character bars for detailed visualization

### Data Truncation Strategy
- Parameter values are formatted to fit available space
- Long status lines are automatically truncated with safe margins
- Alarm text is condensed intelligently based on width

### Color Code Support
All modes maintain full ANSI color support:
- 🟢 Green: Normal/good status
- 🟡 Yellow: Warning conditions
- 🔴 Red: Critical/alarm conditions
- 🔵 Blue/Cyan: State indicators

## Minimum Viable Display (24 columns)

At 24 columns, the display still shows:
- Reactor state (COL, STA, RUN, SCRA, etc.)
- Power output
- Temperature
- Pressure
- Void fraction
- Control rod insertion
- Time running
- Alarm status

This represents a true minimum-viable display that maintains full situational awareness of the reactor.

## Usage

The display mode is automatically selected - no configuration needed:

```bash
# Terminal will auto-detect width
python3 rbmk_reactor_simulator.py

# Manually constrain width in SSH/tmux:
# The simulator will adapt to whatever width is available
```

## Testing Different Sizes

To test the simulator at a specific width in Python:

```python
import shutil
from unittest.mock import MagicMock
from rbmk_reactor_simulator import RBMKControlPanel

# Mock 24-column display
original = shutil.get_terminal_size
def mock_24(default):
    obj = MagicMock()
    obj.columns = 24
    return obj

shutil.get_terminal_size = mock_24
# ... simulator code ...
shutil.get_terminal_size = original
```

## Performance Notes

- Ultra-compact mode: Minimal CPU overhead (11 lines of output)
- Compact mode: Moderate overhead (13 lines)
- Standard mode: Full features (15 lines + keyboard guide)
- All modes update smoothly at interactive speeds

## Future Enhancements

Potential improvements:
- **Vertical scaling:** Optimize for very tall (50+ lines) terminals
- **Sideways scrolling:** For parameters that exceed current width
- **Mouse support:** Click-based control for wider displays
- **Split-screen:** Multiple displays side-by-side on ultra-wide terminals
