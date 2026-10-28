"""
=============================================================================
Configuration & Constants
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================
This file centralizes all configuration parameters such as screen dimensions,
camera speed, rendering settings, materials, and lighting colors.
"""

# Window and Display Settings
WINDOW_TITLE = "Real-Time 3D Game Environment Optimization | Back-Face Culling Demo"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DEFAULT_FPS_CAP = 60          # Standard capped frame rate
UNCAPPED_FPS = 0             # 0 in Pygame allows uncapped frame rate for benchmarking

# 3D Projection Settings
FOV = 60.0                   # Field of view in degrees
NEAR_PLANE = 0.1             # Near clipping plane distance
FAR_PLANE = 600.0            # Far clipping plane distance

# Camera Control Settings
CAMERA_MOVE_SPEED = 12.0     # Units per second
CAMERA_SPRINT_SPEED = 28.0   # Sprint speed with Left Shift
MOUSE_SENSITIVITY = 0.12     # Degrees per pixel of mouse motion
CAMERA_INITIAL_POS = [0.0, 3.5, 25.0]  # Starting position [X, Y, Z]
CAMERA_INITIAL_YAW = -90.0   # Facing negative Z forward
CAMERA_INITIAL_PITCH = -5.0  # Slight downward tilt

# Color Palette (RGB 0.0 - 1.0 for OpenGL)
COLOR_SKY = (0.55, 0.72, 0.95, 1.0)       # Clear daylight blue
COLOR_GROUND_A = (0.22, 0.45, 0.22, 1.0)  # Forest grass green
COLOR_GROUND_B = (0.28, 0.52, 0.28, 1.0)  # Lighter grass checker
COLOR_ROAD = (0.25, 0.25, 0.28, 1.0)      # Asphalt grey
COLOR_ROAD_MARK = (0.9, 0.85, 0.2, 1.0)   # Yellow road divider
COLOR_WALL = (0.68, 0.65, 0.60, 1.0)      # Stone wall
COLOR_ROOF = (0.75, 0.25, 0.20, 1.0)      # Terracotta red roof
COLOR_ACCENT = (0.20, 0.60, 0.90, 1.0)    # Blue accent
COLOR_WOOD = (0.45, 0.28, 0.15, 1.0)      # Wood / Tree trunk
COLOR_FOLIAGE = (0.15, 0.55, 0.18, 1.0)   # Tree leaves

# Lighting Configuration (OpenGL Fixed-Function Pipeline)
LIGHT_POSITION = [50.0, 80.0, 50.0, 1.0]  # Directional / Positional sun
LIGHT_AMBIENT = [0.35, 0.35, 0.38, 1.0]   # Ambient base illumination
LIGHT_DIFFUSE = [0.90, 0.88, 0.82, 1.0]   # Direct sunlight color
LIGHT_SPECULAR = [0.5, 0.5, 0.5, 1.0]     # Highlights

# UI and HUD Color Palette (Pygame RGB 0 - 255)
UI_BG_COLOR = (20, 24, 34, 210)           # Dark semi-transparent slate
UI_BORDER_COLOR = (60, 80, 110, 255)      # Cool steel border
UI_TEXT_PRIMARY = (240, 245, 255)         # Crisp bright white
UI_TEXT_MUTED = (160, 175, 195)           # Soft description grey
UI_ACCENT_ON = (46, 204, 113)             # Emerald Green for CULLING ON (Optimized)
UI_ACCENT_OFF = (231, 76, 60)             # Alizarin Red for CULLING OFF (Wasteful)
UI_ACCENT_INFO = (52, 152, 219)           # Blue info
UI_ACCENT_WARN = (241, 196, 15)           # Golden yellow warning
