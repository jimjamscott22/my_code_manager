# My Code Organizer

A personal desktop app for Linux to organize and manage coding projects.

## Features

- Catalog and organize local coding projects
- Tag and group projects
- Quick access to projects (open in editor, terminal, file manager)
- Git status integration
- Project search and filtering

## Requirements

- Python 3.10+
- GTK4
- Libadwaita
- PyGObject

## Installation

### 1. Install system dependencies

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

### 2. Set up virtual environment

```bash
cd my_code_organizer

# Create venv with access to system GTK packages
python3 -m venv --system-site-packages venv

# Activate venv
source venv/bin/activate

# Install the application
pip install -e .

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

## Running

```bash
# Make sure venv is activated
source venv/bin/activate

# Run the application
my-code-organizer
```

## Development

This is Phase 1 - basic foundation with manual project management.

**Project database location:** `~/.local/share/my-code-organizer/projects.db`
