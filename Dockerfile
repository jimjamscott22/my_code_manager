# Use Ubuntu as base for GTK4/Libadwaita support
FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-4.0 \
    gir1.2-adwaita-1 \
    libgtk-4-1 \
    libadwaita-1-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/
COPY data/ ./data/

# Install the application
RUN pip3 install -e .

# Create directory for application data
RUN mkdir -p /root/.local/share/my-code-organizer

# Set environment variables for GUI
ENV DISPLAY=:0
ENV GDK_BACKEND=x11

# Run the application
CMD ["my-code-organizer"]
