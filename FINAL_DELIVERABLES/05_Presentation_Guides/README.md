# Real-Time 3D Game Environment Optimization Using Back-Face Culling

A complete, beginner-friendly interactive 3D game environment built with **Python**, **OpenGL (PyOpenGL)**, **Pygame**, and **Blender 5.0**. This project demonstrates genuine hardware-level **Polygon Back-Face Culling** and provides real-time performance metrics (FPS, frame latency, polygon counts, wireframe inspection, and high-density stress testing).

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [The Science Behind Back-Face Culling](#the-science-behind-back-face-culling)
4. [OpenGL Implementation Details](#opengl-implementation-details)
5. [Installation & Requirements](#installation--requirements)
6. [How to Run on Windows](#how-to-run-on-windows)
7. [Controls & Keybindings](#controls--keybindings)
8. [How to Observe & Demonstrate the Optimization](#how-to-observe--demonstrate-the-optimization)
9. [Blender 5.0 Asset Pipeline](#blender-50-asset-pipeline)
10. [Project File Architecture](#project-file-architecture)
11. [Troubleshooting & FAQ](#troubleshooting--faq)

---

## Project Overview

In 3D video games, every character, building, wall, and landscape feature is constructed out of polygons (predominantly triangles). In any closed, opaque 3D solid—such as a building, column, or cube—**approximately 50% of all polygon surfaces face away from the player's camera at any moment**.

Without optimization:
- The GPU transforms, rasterizes, and shades pixels on polygons that are pointing backwards and will never be seen.
- This creates massive redundant memory bandwidth and shader overhead.

**Back-Face Culling** is a standard computer graphics optimization technique that detects whether a polygon faces toward or away from the camera. If it faces away, the graphics pipeline **discards the polygon immediately before rasterization and pixel shading**, cutting redundant rendering work by nearly half!

---

## Key Features

- **Attractive 3D Virtual World**: Contains medieval watchtowers, multi-story buildings, perimeter walls, cobblestone/grass terrain, avenues, lamp posts, and stylized pine trees.
- **Blender 5.0 Integration**: Uses high-quality 3D assets exported directly from Blender with consistent Counter-Clockwise (CCW) face normals.
- **Genuine OpenGL Face Culling**: Implements hardware pipeline back-face culling via `glEnable(GL_CULL_FACE)`, `glCullFace(GL_BACK)`, and `glFrontFace(GL_CCW)`.
- **First-Person 6-DOF Camera**: Full keyboard (WASD + Space/Ctrl flight) and smooth mouse-look controls with pitch clamping and cursor grabbing.
- **Interactive On-Demand Optimization**: Starts with Culling **OFF by default**. Optimization ONLY executes when the user explicitly asks for it!
- **Clickable UI Buttons & Free Cursor**: Press **`Tab`** to free your mouse cursor and click on-screen buttons (`[ ⚡ ASK FOR CULLING ]`, `[Wireframe]`, `[Stress Grid]`, `[Uncap FPS]`) with hover glow effects!
- **Animated Notification Toasts**: Instant animated banner notifications appear whenever the user triggers optimization or toggles rendering modes.
- **Live 2D Heads-Up Display (HUD)**: Displays real-time FPS, frame latency (ms), optimization status badge, polygon counters, and active coordinates.
- **Wireframe Inspection Mode (`M` key)**: Instantly reveals the mesh structure, showing how back-facing triangles disappear when culling is enabled.
- **Inside-Out Demonstration Chamber**: An enclosed room where walking inside reveals how outward-facing walls become invisible when culling is active.
- **Heavy-Poly Stress Grid (`T` key)**: Spawns a massive urban grid with tens of thousands of triangles to benchmark real-world GPU performance.
- **Uncapped Benchmark Mode (`U` key)**: Disables V-Sync/framerate capping for benchmarking raw hardware throughput.

---

## The Science Behind Back-Face Culling

### 1. The Vector Dot-Product Test (Object/World Space)
For any polygon triangle with vertices $V_0, V_1, V_2$ arranged in Counter-Clockwise (CCW) order:

1. **Calculate two edge vectors**:
   $$\vec{E}_1 = V_1 - V_0$$
   $$\vec{E}_2 = V_2 - V_0$$

2. **Compute the Surface Normal ($\vec{N}$)** using the cross product:
   $$\vec{N} = \vec{E}_1 \times \vec{E}_2$$

3. **Determine the View Vector ($\vec{V}$)** from the surface toward the camera:
   $$\vec{V} = \text{CameraPosition} - \text{TriangleCentroid}$$

4. **Evaluate the Dot Product ($\vec{N} \cdot \vec{V}$)**:
   - **If $\vec{N} \cdot \vec{V} > 0$**: The angle between the normal and camera ray is $< 90^\circ$. The polygon faces **toward** the camera $\rightarrow$ **FRONT-FACING (Rendered)**.
   - **If $\vec{N} \cdot \vec{V} \le 0$**: The angle between the normal and camera ray is $\ge 90^\circ$. The polygon faces **away from** the camera $\rightarrow$ **BACK-FACING (Culled / Discarded)**.

```
       Camera (V)                           Camera (V)
          \                                    /
           \  Angle < 90°                     /  Angle > 90°
            \                                /
             v                              v
      [Front Surface] ---> N         [Back Surface] <--- N
       (N · V > 0 => KEEP)            (N · V <= 0 => CULL)
```

---

### 2. Screen-Space Winding Order Test (OpenGL Hardware Rasterizer)
In modern graphics hardware, the test is performed after vertices are projected into 2D Screen Space (Normalized Device Coordinates).

Vertices $(x_0, y_0)$, $(x_1, y_1)$, $(x_2, y_2)$ form a 2D triangle. OpenGL computes the signed area (determinant):
$$\text{Area} = \frac{1}{2} \Big[ (x_1 - x_0)(y_2 - y_0) - (y_1 - y_0)(x_2 - x_0) \Big]$$

- **If $\text{Area} > 0$**: Vertices appear in **Counter-Clockwise (CCW)** order $\rightarrow$ Front Face.
- **If $\text{Area} < 0$**: Vertices appear in **Clockwise (CW)** order $\rightarrow$ Back Face.

When a 3D object turns around, the order in which its vertices appear on the 2D screen reverses from CCW to CW. OpenGL uses this property to discard back-facing triangles without needing expensive trigonometric functions!

---

## OpenGL Implementation Details

In this project, face culling is managed in `culling_manager.py`:

```python
from OpenGL.GL import glEnable, glDisable, glCullFace, glFrontFace, GL_CULL_FACE, GL_BACK, GL_CCW

# Enable hardware back-face culling
if self.culling_enabled:
    glEnable(GL_CULL_FACE)      # Enable face culling test in rasterizer
    glCullFace(GL_BACK)         # Specify that back faces must be discarded
    glFrontFace(GL_CCW)         # Define Counter-Clockwise vertex ordering as front-facing
else:
    glDisable(GL_CULL_FACE)     # Draw all faces (front and back)
```

---

## Installation & Requirements

### Prerequisites
- **Operating System**: Windows 10 or Windows 11 (64-bit)
- **Python**: Version 3.10 to 3.13
- **Graphics**: Any OpenGL 3.3+ capable GPU (Intel HD/Iris Xe, Nvidia GeForce, AMD Radeon)
- **Blender (Optional)**: Blender 5.0 (Pre-generated models are already included in `models/`, but Blender can be used to generate or export new models).

### Setup Commands
Open Command Prompt or PowerShell in the project directory:

```powershell
# 1. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt
```

---

## How to Run on Windows

### Method 1: One-Click Batch Launcher (Recommended)
Double-click `run_project.bat` in the project root folder. It automatically verifies Python, installs dependencies if missing, checks models, and launches the application.

### Method 2: Command Line
```powershell
python main.py
```

---

## Controls & Keybindings

| Key / Input | Action | Description |
| :--- | :--- | :--- |
| **`W` / `S`** | Move Forward / Backward | Camera movement along viewing direction |
| **`A` / `D`** | Strafe Left / Right | Camera movement perpendicular to view |
| **`Space`** | Fly Upward | Elevate camera position |
| **`Left Ctrl`** | Fly Downward | Lower camera position |
| **`Left Shift`** | Sprint Boost | Increases movement speed from 12 to 28 units/sec |
| **Mouse Motion** | Look Around | Smooth pitch and yaw first-person camera control |
| **`Tab` / `Esc`** | Lock / Unlock Mouse | Frees the mouse cursor to interact outside the window |
| **`C`** | **Toggle Back-Face Culling** | Switches culling **ON** (Optimized) vs **OFF** (Redundant) |
| **`M`** | **Toggle Mesh Mode** | Switches between **Solid Shading** and **Wireframe Mode** |
| **`F`** | **Toggle Cull Target** | Toggles between `GL_BACK` (Normal) and `GL_FRONT` (Inverted) |
| **`T`** | **Toggle Stress Test Grid** | Spawns a massive 100K+ triangle city grid |
| **`U`** | **Toggle FPS Benchmark** | Toggles between capped 60 FPS and uncapped frame rate |
| **`R`** | **Reset Camera** | Snaps the camera back to starting position |

---

## How to Observe & Demonstrate the Optimization

Here are the **three primary ways** to visually observe and demonstrate Back-Face Culling in this project:

### 1. Wireframe Mode Demonstration (The Visual Proof)
1. Launch the program and press **`M`** to enter **Wireframe Mode**.
2. Look at any building or watchtower.
3. Press **`C`** to turn Culling **OFF**:
   - You can see *all* the rear wireframe triangles through the front walls. The mesh appears cluttered, dense, and tangled.
4. Press **`C`** to turn Culling **ON**:
   - The rear triangles instantly vanish! Only the front-facing silhouette and front facets are drawn.
   - This provides visual proof that the GPU is skipping back-facing geometry.

### 2. Inside-Out Inspection Chamber (The Camera Perspective Test)
1. Turn left toward the **red building with the floating yellow beacon** located at coordinates `(-25, 4, -15)`.
2. Fly through the doorway to enter the interior of the chamber.
3. Turn **Culling ON (`C`)**:
   - Because the walls have outward-facing normals, looking from the inside makes them back-facing!
   - The walls become completely invisible—you see straight through them to the open world outside!
4. Turn **Culling OFF (`C`)**:
   - The walls immediately appear, trapping you inside a solid colored room.

### 3. Stress Test & Benchmark Mode (The Performance Proof)
1. Press **`U`** to switch to **UNCAPPED FPS** mode.
2. Press **`T`** to activate the **High-Poly Stress Test Grid** (spawns 100+ buildings with tens of thousands of triangles).
3. Compare the numbers on the HUD:
   - **Culling ON**: Discards ~50% of triangles before rasterization. Frame time is lower and FPS is higher.
   - **Culling OFF**: The GPU must process and shade 100% of triangles, increasing frame latency.

---

## Blender 5.0 Asset Pipeline

This project includes a dedicated script (`export_blender_assets.py`) that uses Blender 5.0's Python API (`bpy`) to model and export assets.

### Face Orientation in Blender
In 3D modeling, vertex winding determines which way a face points:
- In Blender: In the **Viewport Overlays** menu, enable **Face Orientation**.
  - **Blue Faces**: Front-facing (Normals point outward, Counter-Clockwise winding).
  - **Red Faces**: Back-facing (Normals point inward, Clockwise winding).
- For Back-Face Culling to work correctly in games, all exterior surfaces must be **Blue**!

### How to Export Your Own Blender Models
If you want to create custom 3D models in Blender and use them in this project:
1. Model your object in Blender.
2. Ensure outward normals: Select all in Edit Mode (`A`), then press **`Shift + N`** (*Recalculate Normals Outside*).
3. Triangulate faces: Press **`Ctrl + T`** (*Triangulate Faces*).
4. Export as Wavefront OBJ:
   - Go to **File $\rightarrow$ Export $\rightarrow$ Wavefront (.obj)**.
   - Set **Forward Axis**: `-Z Forward`.
   - Set **Up Axis**: `Y Up`.
5. Save the `.obj` file inside the `models/` directory.
### Opening the Entire Project in Blender 5.0
You can open and view the **entire 3D game environment** directly inside Blender:
1. Double-click [**`open_in_blender.bat`**](file:///c:/Users/panch/Downloads/3D%20game%20environment%20optimisation/open_in_blender.bat) or open [**`game_environment.blend`**](file:///c:/Users/panch/Downloads/3D%20game%20environment%20optimisation/game_environment.blend).
2. Switch to **Material Preview** by clicking the 3rd sphere at the top-right of the 3D Viewport (or press **`Z`** -> **Material Preview**).
3. To test **Backface Culling** in Blender:
   - Click the dropdown arrow next to the Viewport Shading spheres (top-right).
   - Check the **Backface Culling** checkbox.
4. To test **Face Orientation**:
   - Click **Viewport Overlays** (two overlapping circles icon).
   - Check **Face Orientation** (Blue = Front faces, Red = Back faces).
5. To walk through the scene in first-person in Blender:
   - Press **`Shift + ~`** (Tilde key) or go to **View -> Navigation -> Walk Navigation**.
   - Use **`W, A, S, D`** and your mouse to walk around the scene just like a video game!

---

## Project File Architecture

```
3D game environment optimisation/
│
├── game_environment.blend    # Complete 3D game environment ready to open in Blender 5.0
├── open_in_blender.bat        # 1-click launcher to open the scene directly in Blender
├── build_blender_scene.py     # Script that constructed game_environment.blend
├── export_blender_assets.py   # Headless Blender 5.0 script that modeled & exported assets
│
├── requirements.txt           # Python package dependencies (PyOpenGL, pygame, numpy)
├── run_project.bat            # Windows 1-click launcher script
├── main.py                    # Application entry point, game loop, and input handling
├── config.py                  # Display constants, colors, speeds, lighting
├── camera.py                  # 6-DOF first-person camera with mouse-look and vectors
├── culling_manager.py         # OpenGL face culling state and mathematical logic
├── obj_loader.py              # Wavefront OBJ parser and OpenGL Display List compiler
├── scene.py                   # 3D game environment, layout, walls, and inspection room
├── hud.py                     # Antialiased 2D OpenGL HUD overlay (FPS, stats, badges)
│
├── models/                    # 3D assets exported from Blender 5.0
│   ├── building.obj           # Multi-story classical building
│   ├── watchtower.obj         # Medieval stone watchtower
│   ├── tree.obj               # Stylized pine tree
│   └── lamp_post.obj          # Urban streetlamp
│
├── README.md                  # Comprehensive project documentation
└── COLLEGE_PROJECT_GUIDE.md   # Presentation script, viva Q&A, and benchmark table
```

---

## Troubleshooting & FAQ

**Q: PyOpenGL throws `NullFunctionError` or OpenGL fails to initialize.**  
*A:* Ensure your graphics drivers are up to date. Run `pip install --force-reinstall PyOpenGL PyOpenGL-accelerate`.

**Q: The mouse cursor is locked and I cannot click outside the window.**  
*A:* Press **`Tab`** or **`Escape`** to unlock the mouse cursor. Click back inside the window to re-lock.

**Q: Can I run this without Blender installed?**  
*A:* Yes! The `.obj` models are already pre-generated and stored in the `models/` directory. Blender is only needed if you want to run `export_blender_assets.py` to regenerate or modify assets.

**Q: Why is my FPS capped at 60?**  
*A:* By default, the simulation caps the frame rate at 60 FPS for smooth rendering. Press **`U`** to toggle **Uncapped FPS Benchmark Mode**.
