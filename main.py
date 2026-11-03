"""
=============================================================================
Main Application Entry Point & Game Loop
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================

Controls:
---------
  W, A, S, D       : Walk & Move Camera (Real-Time Culling Updates While Walking!)
  Space / L-Ctrl   : Fly Upward / Downward
  Left Shift       : Sprint boost
  Mouse            : Look around (pitch & yaw)
  Tab / Esc        : Unlock / Lock mouse cursor (Click sections / buttons)
  I                : Toggle Culling Inspector (Green = Rendered, Red = Culled)
  1 - 6            : Select Specific Section (Buildings, Towers, Chamber, Plaza, Nature)
  C                : Toggle Back-Face Culling (ON / OFF)
  M                : Toggle Mesh Mode (Solid / Wireframe)
  T                : Toggle High-Density Stress Test Grid (50,000+ Triangles)
  U                : Toggle Uncapped FPS (Benchmark Mode)
  R                : Reset Camera Position
"""

import sys
import time
import math
import pygame
from OpenGL.GL import (
    glEnable, glDisable, glClear, glClearColor, glViewport,
    glMatrixMode, glLoadIdentity, glDepthFunc, glShadeModel,
    glLightfv, glColorMaterial, glGetIntegerv, glGetDoublev,
    GL_DEPTH_TEST, GL_LEQUAL, GL_LIGHTING, GL_LIGHT0,
    GL_POSITION, GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR,
    GL_COLOR_MATERIAL, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    GL_NORMALIZE, GL_SMOOTH, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
    GL_PROJECTION, GL_MODELVIEW, GL_VIEWPORT, GL_MODELVIEW_MATRIX, GL_PROJECTION_MATRIX
)
from OpenGL.GLU import gluPerspective, gluUnProject

import config
from camera import Camera
from culling_manager import CullingManager
from scene import Scene
from hud import HUD


def setup_opengl():
    """Configures global OpenGL 3D rendering pipeline state."""
    glClearColor(*config.COLOR_SKY)

    # Depth Buffer Testing (Z-buffer)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    # Normal Vector Normalization for lighting calculations
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    # Lighting setup
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, config.LIGHT_AMBIENT)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, config.LIGHT_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_SPECULAR, config.LIGHT_SPECULAR)

    # Material Color Tracking
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Perspective Projection Matrix setup
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = config.WINDOW_WIDTH / float(config.WINDOW_HEIGHT)
    gluPerspective(config.FOV, aspect_ratio, config.NEAR_PLANE, config.FAR_PLANE)
    glMatrixMode(GL_MODELVIEW)


def get_3d_ray_from_mouse(mx, my, camera):
    """
    Calculates 3D world-space picking ray origin and direction from screen mouse coordinates.
    Uses OpenGL gluUnProject to translate 2D screen pixels to 3D world space.
    """
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)

    win_y = viewport[3] - my
    near_pt = gluUnProject(mx, win_y, 0.0, modelview, projection, viewport)
    far_pt = gluUnProject(mx, win_y, 1.0, modelview, projection, viewport)

    dx = far_pt[0] - near_pt[0]
    dy = far_pt[1] - near_pt[1]
    dz = far_pt[2] - near_pt[2]
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length > 0.0:
        ray_dir = (dx / length, dy / length, dz / length)
    else:
        ray_dir = (0.0, 0.0, -1.0)

    return near_pt, ray_dir


def main():
    # 1. Initialize Pygame Video & Audio subsystem
    pygame.init()
    pygame.display.set_caption(config.WINDOW_TITLE)

    # 2. Configure OpenGL Framebuffer attributes (Double Buffered, 24-bit Depth)
    pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)

    screen = pygame.display.set_mode(
        (config.WINDOW_WIDTH, config.WINDOW_HEIGHT),
        pygame.OPENGL | pygame.DOUBLEBUF
    )

    # 3. Setup OpenGL fixed-function pipeline states
    setup_opengl()

    # 4. Instantiate subsystems
    camera = Camera(
        x=config.CAMERA_INITIAL_POS[0],
        y=config.CAMERA_INITIAL_POS[1],
        z=config.CAMERA_INITIAL_POS[2],
        yaw=config.CAMERA_INITIAL_YAW,
        pitch=config.CAMERA_INITIAL_PITCH
    )
    culling_mgr = CullingManager()
    scene = Scene()
    hud = HUD(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

    # 5. Lock mouse into first-person view initially
    camera.set_mouse_lock(True)

    clock = pygame.time.Clock()
    running = True

    # Performance benchmark timers
    last_time = time.perf_counter()
    frame_count = 0
    fps_timer = 0.0
    current_fps = 60.0
    current_frame_time = 16.6

    print("\n" + "=" * 70)
    print(" 3D GAME ENVIRONMENT OPTIMIZATION USING BACK-FACE CULLING")
    print("=" * 70)
    print(" Controls:")
    print("   [W, A, S, D]       : Walk & Move (Real-Time Culling Updates While Walking!)")
    print("   [Mouse]            : Look around (pitch & yaw)")
    print("   [Space / L-Ctrl]   : Fly up / Fly down")
    print("   [Left Shift]       : Sprint boost")
    print("   [I]                : Toggle Culling Inspector (Green = Rendered, Red = Culled)")
    print("   [1 - 6]            : Select Specific Section (Buildings, Towers, Chamber, Plaza, Nature)")
    print("   [C]                : Toggle Back-Face Culling (ON / OFF)")
    print("   [M]                : Toggle Wireframe / Solid mode")
    print("   [T]                : Toggle Heavy-Poly Stress Grid (50K+ Triangles)")
    print("   [U]                : Toggle Uncapped FPS (Benchmark mode)")
    print("   [Tab]              : Unlock / Lock mouse cursor (Click sections / 3D buildings)")
    print("   [R]                : Reset camera position")
    print("=" * 70 + "\n")

    # -----------------------------------------------------------------
    # Main Game Loop
    # -----------------------------------------------------------------
    while running:
        # High precision delta time calculation
        now = time.perf_counter()
        dt = now - last_time
        last_time = now
        current_frame_time = dt * 1000.0  # ms

        # Live FPS calculation
        frame_count += 1
        fps_timer += dt
        if fps_timer >= 0.25:  # Refresh FPS metric every 250ms
            current_fps = frame_count / fps_timer
            frame_count = 0
            fps_timer = 0.0

        # Cap frame rate if enabled, or uncap for performance benchmark
        target_cap = config.UNCAPPED_FPS if culling_mgr.uncapped_fps else config.DEFAULT_FPS_CAP
        clock.tick(target_cap)

        # -------------------------------------------------------------
        # Event Processing
        # -------------------------------------------------------------
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                    locked = camera.toggle_mouse_lock()
                    if locked:
                        hud.show_notification("🖱️ MOUSE LOCKED: LOOK MODE", "First-person camera view active. Walk with WASD!", (56, 189, 248), 2.5)
                    else:
                        hud.show_notification("🖱️ MOUSE UNLOCKED: CURSOR FREE", "Click any section button or click directly on 3D buildings with mouse!", (251, 191, 36), 3.5)

                elif event.key == pygame.K_c:
                    state = culling_mgr.toggle_culling()
                    if state:
                        hud.show_notification(
                            "⚡ USER REQUEST RECEIVED: CULLING ACTIVATED!",
                            "OpenGL is now discarding ~50% of primitives before rasterization!",
                            (16, 185, 129), 3.5
                        )
                        print("[OPTIMIZATION] Back-Face Culling: ENABLED ON USER REQUEST")
                    else:
                        hud.show_notification(
                            "⚠️ CULLING DEACTIVATED BY USER",
                            "GPU is now rendering all redundant front and back surfaces (100% workload).",
                            (239, 68, 68), 3.5
                        )
                        print("[OPTIMIZATION] Back-Face Culling: DISABLED BY USER")

                elif event.key == pygame.K_i:
                    insp = culling_mgr.toggle_inspector()
                    if insp:
                        hud.show_notification(
                            "🔍 CULLING INSPECTOR: ACTIVE",
                            "GREEN = Front Faces (Rendered) | RED = Back Faces (Culled). Walk with WASD to see dynamic changes!",
                            (34, 197, 94), 4.0
                        )
                    else:
                        hud.show_notification("🎨 STANDARD SHADING RESTORED", "Normal mesh material colors active.", (148, 163, 184), 2.5)
                    print(f"[INSPECTOR] Culling Diagnostics: {'ACTIVE' if insp else 'OFF'}")

                # Quick Section Hotkeys: 1 - 6
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    sec_map = {
                        pygame.K_1: "all",
                        pygame.K_2: "buildings",
                        pygame.K_3: "towers",
                        pygame.K_4: "chamber",
                        pygame.K_5: "plaza",
                        pygame.K_6: "nature"
                    }
                    target_sec = sec_map[event.key]
                    culling_mgr.set_section(target_sec)
                    meta = scene.sections_meta.get(target_sec, {})
                    hud.show_notification(f"🎯 SECTION SELECTED: {meta.get('name', target_sec)}", meta.get('desc', ''), (56, 189, 248), 3.5)

                elif event.key == pygame.K_m:
                    wf = culling_mgr.toggle_wireframe()
                    if wf:
                        hud.show_notification("🌐 WIREFRAME MODE: ENABLED", "Surface occlusion removed! You can see all wireframe polygon lines.", (56, 189, 248), 3.0)
                    else:
                        hud.show_notification("🟦 SOLID SHADING RESTORED", "Standard opaque surface rendering active.", (148, 163, 184), 2.5)
                    print(f"[RENDER MODE] Mesh Mode: {'WIREFRAME' if wf else 'SOLID'}")

                elif event.key == pygame.K_f:
                    face = culling_mgr.toggle_cull_face()
                    hud.show_notification(f"🔄 CULL TARGET: {culling_mgr.get_cull_face_str()}", "Educational test switching between front and back face culling.", (56, 189, 248), 3.0)

                elif event.key == pygame.K_t:
                    stress = culling_mgr.toggle_stress_test()
                    if stress:
                        hud.show_notification("🏙️ HIGH-POLY STRESS TEST: ACTIVE", "Loaded massive city grid (50,000+ triangles) to benchmark GPU fill-rate!", (245, 158, 11), 3.5)
                    else:
                        hud.show_notification("🏙️ STANDARD TOWN SCENE RESTORED", "Base environment loaded (~4,600 triangles).", (148, 163, 184), 2.5)

                elif event.key == pygame.K_u:
                    uncapped = culling_mgr.toggle_fps_cap()
                    if uncapped:
                        hud.show_notification("🚀 UNCACHED BENCHMARK MODE: ACTIVE", "Frame rate limiter disabled! Benchmarking raw GPU throughput.", (168, 85, 247), 3.0)
                    else:
                        hud.show_notification("🔒 60 FPS VSYNC CAP RESTORED", "Frame rate locked to 60 FPS for smooth simulation.", (148, 163, 184), 2.5)

                elif event.key == pygame.K_r:
                    camera.reset_position()
                    hud.show_notification("📍 CAMERA RESET", "Viewpoint snapped back to starting position.", (56, 189, 248), 2.0)

            elif event.type == pygame.MOUSEMOTION:
                if camera.mouse_locked:
                    camera.process_mouse(event.rel[0], event.rel[1])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not camera.mouse_locked:
                        clicked_action = hud.handle_click(event.pos, culling_mgr, camera, scene)
                        if not clicked_action:
                            # User clicked on 3D viewport: Perform 3D Ray Picking to detect clicked section!
                            ray_origin, ray_dir = get_3d_ray_from_mouse(event.pos[0], event.pos[1], camera)
                            hit_section = scene.ray_pick(ray_origin, ray_dir)

                            if hit_section:
                                culling_mgr.set_section(hit_section)
                                meta = scene.sections_meta.get(hit_section, {})
                                hud.show_notification(
                                    f"🎯 CLICKED 3D OBJECT: {meta.get('name', hit_section)}",
                                    "Section selected! Front faces (Green) and Back faces (Red) are now highlighted.",
                                    (251, 191, 36), 3.5
                                )
                                print(f"[3D RAY PICK] Clicked section: {hit_section}")
                            else:
                                # Clicked empty sky/ground: re-lock mouse for smooth walking!
                                camera.set_mouse_lock(True)

        # Process continuous keyboard inputs for camera walking/flight
        keys = pygame.key.get_pressed()
        camera.process_keyboard(keys, dt)

        # Update walking status for dynamic telemetry badge
        culling_mgr.is_walking = any([
            keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d],
            keys[pygame.K_SPACE], keys[pygame.K_LCTRL]
        ])

        # Update scene animations (such as rotating monoliths)
        scene.update(dt)

        # Update HUD animations and toast timers
        hud.update(dt)

        # -------------------------------------------------------------
        # 3D Scene Rendering Pass
        # -------------------------------------------------------------
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Apply First-Person Camera View
        camera.apply_view()

        # Update directional sunlight position in world coordinates
        glLightfv(GL_LIGHT0, GL_POSITION, config.LIGHT_POSITION)

        # Apply active Back-Face Culling and Wireframe settings
        culling_mgr.apply_settings()

        # Render 3D Environment Geometry (with dynamic section isolation & inspector)
        total_triangles = scene.render(culling_mgr)

        # -------------------------------------------------------------
        # 2D HUD Rendering Pass
        # -------------------------------------------------------------
        hud.update_metrics(current_fps, current_frame_time)
        hud.render(culling_mgr, camera, total_triangles, mouse_pos, camera.mouse_locked)

        # Swap front and back buffers
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
