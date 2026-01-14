# Lorenz Attractor: The Butterfly Effect
**COMP 342 - Computer Graphics Mini Project**

## Overview
This project visualizes the **Lorenz Attractor**, a chaotic dynamical system that demonstrates the butterfly effect—how infinitesimal changes in initial conditions lead to vastly different outcomes.

## What It Does
- Simulates two Lorenz systems with nearly identical initial conditions
- **System A**: Starts at (1.0, 1.0, 1.0) with rainbow coloring
- **System B**: Starts at (1.0, 1.0, 1.0 + ε) with white coloring to show divergence
- Renders 3D trajectories in real-time using OpenGL
- Demonstrates sensitivity to initial conditions and chaotic behavior

## Key Features
✓ **Real-time 3D visualization** using OpenGL 3.3  
✓ **Configurable parameters**: Epsilon (initial condition difference) & simulation speed  
✓ **Interactive camera**: Rotate and zoom with mouse  
✓ **Pause/Resume**: SPACE key to pause the simulation  
✓ **Anti-aliasing**: 8x MSAA for smooth rendering  

## Requirements
```
glfw
numpy
PyOpenGL
```

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

### Controls
| Input | Action |
|-------|--------|
| **Left Mouse Drag** | Rotate camera |
| **Mouse Wheel** | Zoom in/out |
| **SPACE** | Pause/Resume simulation |

## Parameters
When prompted:
- **Epsilon**: Difference in initial Z coordinate (e.g., `0.00001`)
- **Simulation Speed**: Steps per frame (e.g., `2` or `5`)

## Project Structure
- `main.py` - Main application loop and rendering
- `lorenz.py` - Lorenz system solver (RK4 integration)
- `graphics_utils.py` - OpenGL utilities (shaders, buffers, matrices)
- `requirements.txt` - Python dependencies

## Demo
![(Lorenz_demo](lorenz_gif.gif)
## Theory
The Lorenz system is defined by:
```
dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz
```

Where σ=10, ρ=28, β=8/3 (standard chaotic parameters).

---
*Created for COMP 342 - Computer Graphics*
