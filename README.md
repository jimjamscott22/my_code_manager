# My Code Organizer

A cross-platform desktop app to organize and manage coding projects.

## Features

### Implemented

- Catalog and organize local coding projects
- Add project metadata (name, language, description)
- Mark projects as favorites with star toggle
- Real-time search by name, path, or description
- Filter projects by language or favorites
- Delete projects from catalog

### Planned

- Tag and group projects (database ready)
- Quick access to projects (open in editor, terminal, file manager)
- Git status integration

## Requirements

- Python 3.10+
- GTK4
- Libadwaita
- PyGObject

## Installation

### 1. Install system dependencies

**Note:** These commands can be run from any directory.

**Windows:**

#### Option 1: Using MSYS2 (Recommended)

1. Download and install [MSYS2](https://www.msys2.org/)
2. Open the **MINGW64** terminal (not MSYS2 or UCRT64)
3. Update the package database:

```bash
pacman -Syu
```

4. Install Python, GTK4, and dependencies (all in one command):

```bash
pacman -S mingw-w64-x86_64-gtk4 mingw-w64-x86_64-libadwaita mingw-w64-x86_64-python mingw-w64-x86_64-python-gobject
```

5. Keep using the MINGW64 terminal for all subsequent commands

#### Option 2: If you already have Git for Windows with MINGW64

Git for Windows includes a minimal MSYS2 environment. You can try using it, but you'll need to check if `pacman` is available:

```bash
# Test if pacman is available
pacman --version
```

If pacman works, follow steps 3-5 above. If not, install full MSYS2 (Option 1) for access to GTK4 packages.

**Ubuntu/Debian:**
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adwaita-1
```

**Fedora:**
```bash
sudo dnf install python3-gobject gtk4 libadwaita
```

**Arch Linux:**
```bash
sudo pacman -S python-gobject gtk4 libadwaita
```

### 2. Set up virtual environment (Recommended)

Using a virtual environment isolates your project dependencies and is considered best practice.

**All platforms (including Windows MSYS2):**

```bash
# Navigate to the project directory (adjust path to match your location)
# In MSYS2/Git Bash, Windows paths look like: /c/Users/YourName/path/to/project
cd path/to/my_code_manager

# Create venv with access to system GTK packages
# Note: --system-site-packages is required to access GTK4/Libadwaita
python3 -m venv --system-site-packages venv

# Activate venv (Linux/macOS/MSYS2)
source venv/bin/activate

# Install the application
pip install -e .

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

**Why `--system-site-packages`?**
GTK4 and Libadwaita are installed via your system package manager (pacman/apt/dnf) and cannot be installed via pip. The `--system-site-packages` flag allows your virtual environment to access these system-installed packages while keeping other Python dependencies isolated.

## Running with Docker

**Linux only** (GUI applications in Docker require X11 forwarding, which works best on Linux):

```bash
# Allow Docker to access X server
xhost +local:docker

# Build and run with docker-compose
docker-compose up --build

# When done, revoke X server access
xhost -local:docker
```

Or using Docker directly:

```bash
# Build the image
docker build -t my-code-organizer .

# Run the container
xhost +local:docker
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v my-code-organizer-data:/root/.local/share/my-code-organizer \
  my-code-organizer

# Revoke X server access when done
xhost -local:docker
```

**Note:** Docker GUI applications on Windows/macOS require additional X server setup (like VcXsrv or XQuartz) and are not officially supported.

## Running Natively

**Note:** Run these commands from the project directory (where you created the venv).

**Linux/macOS:**

```bash
# Navigate to project directory if not already there
cd path/to/my_code_manager

# Activate venv
source venv/bin/activate

# Run the application
my-code-organizer
```

**Windows (MSYS2 MINGW64 or Git Bash):**

```bash
# Navigate to project directory if not already there
# Example: cd /c/Users/jimja/github_repos/Python/my_code_manager
cd /c/path/to/my_code_manager

# Activate venv
source venv/bin/activate

# Run the application
my-code-organizer
```

**Important for Windows users:**

- You must use MSYS2 MINGW64 or Git Bash terminal (not CMD or PowerShell)
- This is required because GTK4 libraries are installed via MSYS2

## Development

This is Phase 1 - basic foundation with manual project management.

**Project database location:** `~/.local/share/my-code-organizer/projects.db`
