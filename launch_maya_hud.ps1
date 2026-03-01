# Maya AI HUD Launcher Script
# This script sets up and launches the Maya AI HUD application

param(
    [switch]$Setup,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Test-Prerequisites {
    Write-ColorText "Checking prerequisites..." "Cyan"
    
    # Check Python
    try {
        $pythonVersion = python --version 2>$null
        Write-ColorText "✓ Python found: $pythonVersion" "Green"
    }
    catch {
        Write-ColorText "✗ Python not found. Please install Python 3.8 or higher." "Red"
        return $false
    }
    
    # Check pip
    try {
        pip --version >$null 2>&1
        Write-ColorText "✓ pip found" "Green"
    }
    catch {
        Write-ColorText "✗ pip not found. Please ensure pip is installed." "Red"
        return $false
    }
    
    return $true
}

function Initialize-VirtualEnv {
    Write-ColorText "Setting up virtual environment..." "Cyan"
    
    if (-not (Test-Path ".venv")) {
        python -m venv .venv
        Write-ColorText "✓ Virtual environment created" "Green"
    }
    else {
        Write-ColorText "✓ Virtual environment already exists" "Yellow"
    }
    
    # Activate virtual environment
    & .\.venv\Scripts\Activate.ps1
    Write-ColorText "✓ Virtual environment activated" "Green"
}

function Install-Dependencies {
    Write-ColorText "Installing dependencies..." "Cyan"
    
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt
        Write-ColorText "✓ Dependencies installed" "Green"
    }
    else {
        Write-ColorText "✗ requirements.txt not found" "Red"
        return $false
    }
}

function Start-Application {
    Write-ColorText "Starting Maya AI HUD..." "Cyan"
    Write-ColorText "Press ESC or Ctrl+Q to close the application" "Yellow"
    Write-Host ""
    
    try {
        python main.py
    }
    catch {
        Write-ColorText "✗ Application failed to start: $_" "Red"
        return $false
    }
    
    return $true
}

function Create-DesktopShortcut {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "Maya AI HUD.lnk"
    
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "powershell.exe"
    $shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$PSScriptRoot\launch_maya_hud.ps1`""
    $shortcut.WorkingDirectory = $PSScriptRoot
    $shortcut.IconLocation = "shell32.dll,13"
    $shortcut.Description = "Launch Maya AI HUD"
    $shortcut.Save()
    
    Write-ColorText "✓ Desktop shortcut created: $shortcutPath" "Green"
}

# Main execution
Write-ColorText "=== Maya AI HUD Launcher ===" "Cyan"
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

if ($Setup) {
    Write-ColorText "Running in setup mode..." "Yellow"
    
    if (-not (Test-Prerequisites)) {
        Write-ColorText "Prerequisites check failed. Exiting." "Red"
        exit 1
    }
    
    Initialize-VirtualEnv
    Install-Dependencies
    Create-DesktopShortcut
    
    Write-ColorText "Setup complete! You can now run the application or use the desktop shortcut." "Green"
    exit 0
}

# Normal execution
if (-not (Test-Prerequisites)) {
    Write-ColorText "Prerequisites check failed. Run with -Setup parameter to set up the environment." "Red"
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-ColorText "Virtual environment not found. Running setup..." "Yellow"
    Initialize-VirtualEnv
    Install-Dependencies
}

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Check if dependencies are installed
try {
    python -c "import PySide6, psutil, GPUtil, pynvml" >$null 2>&1
}
catch {
    if ($Force) {
        Write-ColorText "Installing missing dependencies..." "Yellow"
        Install-Dependencies
    }
    else {
        Write-ColorText "Dependencies missing. Run with -Force to install, or run with -Setup for full setup." "Red"
        exit 1
    }
}

# Start the application
Start-Application

Write-Host ""
Write-ColorText "Maya AI HUD closed." "Cyan"
