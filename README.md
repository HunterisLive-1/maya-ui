# Maya AI HUD - Futuristic Desktop Interface

A modern, futuristic HUD-style desktop monitoring application with real-time system metrics, audio visualization, and AI-themed interface.

## 🚀 Quick Start (One-Click Launch)

### Option 1: Batch File (Simple)

Double-click `Start_Maya_AI_HUD.bat` to launch the application.

### Option 2: PowerShell Script (Advanced)

Right-click `launch_maya_hud.ps1` and select "Run with PowerShell".

### First-Time Setup

Run the PowerShell script with setup parameter:

```powershell
.\launch_maya_hud.ps1 -Setup
```

## ✅ Latest Updates & Fixes

### 🔧 GPU & Temperature Monitoring - FIXED

- **NVIDIA External GPU Detection**: Now properly detects and prioritizes NVIDIA external GPU over AMD iGPU
- **Enhanced Temperature Monitoring**: Multiple detection methods including NVML, GPUtil, and WMI
- **Better Error Handling**: Graceful fallbacks when GPU detection fails
- **Added pynvml dependency**: For more reliable NVIDIA GPU monitoring

### 🎨 AI-Style UI Enhancement

- **Neural Network Mode**: Animated nodes with dynamic connections and wave motion
- **Holographic Waves**: Multi-layered wave interference patterns with color shifts
- **Quantum Field**: Floating particles with quantum entanglement effects and pulsing animations
- **Enhanced Borders**: Multi-layer glow with animated color-shifting and corner accents
- **Smooth Transitions**: All animations run at 60 FPS with improved performance

### 🖱️ One-Click Desktop Launcher

- **Batch File**: Simple double-click launcher for basic users
- **PowerShell Script**: Advanced launcher with automatic setup and dependency management
- **Desktop Shortcut**: Automatically created during setup
- **Error Recovery**: Automatic dependency installation and troubleshooting

## Features

### 🎨 Visual Design

- **AI-themed backgrounds** with three animated modes:
  - Neural network visualization with connected nodes
  - Holographic waves with interference patterns
  - Quantum field with floating particles
- **Multi-layer glow borders** with color-shifting animations
- **Smooth 60 FPS animations** throughout
- **Professional AI aesthetic** with modern gradients

### 🔮 Advanced Orb Visualization

- **Multi-layer glow effects** with pulsing animations
- **Segmentated rotating arcs** at different speeds
- **Circular waveform** reactive to speaker audio
- **Dynamic speaker detection** - works with headphones, Bluetooth, monitor speakers
- **High sensitivity** with smooth response
- **Clean shutdown** with no freezing

### 📊 System Monitoring Panel - ENHANCED

- **Large, bold metrics** display with improved accuracy:
  - CPU usage with animated progress bar
  - RAM usage with color-coded indicators
  - **GPU Usage**: NVIDIA external GPU properly detected and monitored
  - **Temperature**: Enhanced GPU/CPU temperature monitoring with multiple methods
  - Disk usage monitoring
  - Network upload/download speeds
- **Animated horizontal progress bars** with glowing effects
- **Color-coded status** (green → yellow → red based on usage)
- **Modern HUD typography**

### 🎤 Microphone Visualizer

- **Colorful gradient bars** with smooth animations
- **Idle animation** when no microphone input is detected
- **Wave effects** across the frequency spectrum
- **Neon-style glow effects**

### ✨ Signature Widget

- **Animated "HunterIsLive" signature** in bottom-right corner
- **Glowing neon effect** with pulse animations
- **Professional gamer aesthetic**

### ⌨️ Controls

- **ESC key** to close the application cleanly
- **Ctrl+Q** alternative close shortcut
- **Drag window** by clicking and holding anywhere
- **Proper thread shutdown** with no freezing

## Architecture

```
maya ui/
├── main.py                 # Application entry point
├── ui/                     # User interface components
│   ├── main_window.py      # Main window with background effects
│   ├── orb_widget.py       # Advanced audio-reactive orb
│   ├── left_panel.py       # System metrics panel
│   ├── right_panel.py      # Status and clock panel
│   └── mic_visualizer.py   # Microphone frequency visualizer
├── workers/                # Background threads
│   ├── audio_worker.py     # Speaker audio capture
│   ├── system_worker.py    # System monitoring
│   └── mic_worker.py       # Microphone input
├── effects/                # Visual effects
│   ├── particle_engine.py  # Background particle system
│   └── signature_widget.py # Animated signature
└── utils/                  # Utility functions
```

## Installation

### 🚀 One-Click Setup (Recommended)

1. Download and extract the project
2. Run the setup script:
   ```powershell
   .\launch_maya_hud.ps1 -Setup
   ```
3. Use the desktop shortcut or launchers to run

### 📦 Manual Installation

1. Install Python 3.8+ from python.org
2. Clone or download the project
3. Open Command Prompt in the project folder
4. Run:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

## Requirements

- Windows 10/11
- Python 3.8 or higher
- NVIDIA GPU (for GPU monitoring)
- 4GB RAM minimum
- DirectX 11 compatible graphics
- Audio output device for speaker visualization
- Microphone (optional, for mic visualizer)

## Dependencies

All dependencies are automatically installed by the setup script:

- **PySide6**: Qt6 GUI framework
- **numpy**: Numerical computations for audio processing
- **sounddevice**: Audio capture and playback
- **psutil**: System monitoring utilities
- **GPUtil**: GPU detection and monitoring
- **pynvml**: NVIDIA GPU management library
- **wmi**: Windows Management Instrumentation for temperature
- **setuptools**: Package management utilities

## Troubleshooting

### 🔧 GPU/Temperature Still Shows 0

1. **Install NVIDIA Drivers**: Download from https://www.nvidia.com/drivers/
2. **Run as Administrator**: Right-click launcher and "Run as administrator"
3. **Check NVIDIA GPU Detection**: Open Command Prompt and run:
   ```bash
   nvidia-smi
   ```
4. **Verify GPU is Active**: Ensure NVIDIA GPU is not in power-saving mode

### 🚀 Application Won't Start

1. **Run Setup Script**: `.\launch_maya_hud.ps1 -Setup`
2. **Check Python Installation**: Ensure Python 3.8+ is installed and in PATH
3. **Windows Defender**: Add exception for the project folder
4. **PowerShell Execution Policy**: Run as Administrator if needed

### 📦 Dependencies Issues

1. **Force Install**: Run `.\launch_maya_hud.ps1 -Force`
2. **Manual Install**: Activate venv and run `pip install -r requirements.txt`
3. **Update pip**: Run `python -m pip install --upgrade pip`

### 🎵 Audio Visualization Not Working

1. **Check Audio Devices**: Ensure speakers/headphones are connected
2. **Default Audio Device**: Set your desired speakers as default playback device
3. **Run as Administrator**: Some audio capture methods require elevated privileges

### ⚡ High CPU Usage

1. **Reduce Particles**: Edit `particle_engine.py` to reduce particle count
2. **Lower FPS**: Modify timer intervals in `main_window.py`
3. **Disable Backgrounds**: Comment out background animation calls

## Desktop Shortcut

The setup script automatically creates a desktop shortcut. To create manually:

1. Right-click on desktop → New → Shortcut
2. Location: `powershell.exe -ExecutionPolicy Bypass -File "C:\path\to\maya ui\launch_maya_hud.ps1"`
3. Name: "Maya AI HUD"
4. Finish

## Usage Tips

- **Window Movement**: The window is frameless - drag it by clicking anywhere
- **Background Modes**: AI backgrounds switch automatically every 25 seconds
- **Real-time Updates**: All system metrics update in real-time
- **Audio Detection**: Works with any default audio device automatically
- **Clean Exit**: Press ESC to exit cleanly at any time
- **Performance**: Optimized for 60 FPS smooth animations

## License

This project is provided as-is for educational and personal use.
