"""
=============================================================================
Main Application Entry Point & Game Loop
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================

Controls:
---------
  W, A, S, D       : Move Forward / Left / Backward / Right
  Space / L-Ctrl   : Fly Upward / Downward
  Left Shift       : Sprint boost
  Mouse            : Look around (pitch & yaw)
  Tab / Esc        : Unlock / Lock mouse cursor
  C                : Toggle Back-Face Culling (ON / OFF)
  M                : Toggle Mesh Mode (Solid / Wireframe)
  F                : Toggle Culling Face Target (GL_BACK / GL_FRONT)
  T                : Toggle High-Density Stress Test Grid (100,000+ Triangles)
  U                : Toggle Uncapped FPS (Benchmark Mode)
  R                : Reset Camera Position
"""

import sys
import time
import pygame
from OpenGL.GL import (
    glEnable, glDisable, glClear, glClearColor, glViewport,
    glMatrixMode, glLoadIdentity, glDepthFunc, glShadeModel,
    glLightfv, glColorMaterial,
    GL_DEPTH_TEST, GL_LEQUAL, GL_LIGHTING, GL_LIGHT0,
    GL_POSITION, GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR,
    GL_COLOR_MATERIAL, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    GL_NORMALIZE, GL_SMOOTH, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
    GL_PROJECTION, GL_MODELVIEW
)
from OpenGL.GLU import gluPerspective

import config
from camera import Camera
from culling_manager import CullingManager
from scene import Scene
from hud import HUD


def setup_opengl():
    """Configures global OpenGL 3D rendering pipeline state."""
    # Background clear color (sky blue)
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

    # 5. Lock mouse into first-person view
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
    print("   [W, A, S, D]       : Move camera")
    print("   [Mouse]            : Look around (pitch & yaw)")
    print("   [Space / L-Ctrl]   : Fly up / Fly down")
    print("   [Left Shift]       : Sprint boost")
    print("   [C]                : Toggle Back-Face Culling (ON / OFF)")
    print("   [M]                : Toggle Wireframe / Solid mode")
    print("   [F]                : Toggle Cull Face (GL_BACK / GL_FRONT)")
    print("   [T]                : Toggle Heavy-Poly Stress Grid (100K+ Triangles)")
    print("   [U]                : Toggle Uncapped FPS (Benchmark mode)")
    print("   [Tab]              : Unlock / Lock mouse cursor")
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
                        hud.show_notification("🖱️ MOUSE LOCKED: LOOK MODE", "First-person camera view active. Press [Tab] to free cursor and click buttons.", (56, 189, 248), 2.5)
                    else:
                        hud.show_notification("🖱️ MOUSE UNLOCKED: CURSOR FREE", "You can now click any on-screen button with your mouse!", (251, 191, 36), 3.5)

                elif event.key == pygame.K_c:
                    state = culling_mgr.toggle_culling()
                    if state:
                        hud.show_notification(
                            "⚡ USER REQUEST RECEIVED: CULLING ACTIVATED!",
                            "OpenGL is now discarding ~50% of triangles before rasterization!",
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
                    print(f"[CULL TARGET] Face: {culling_mgr.get_cull_face_str()}")

                elif event.key == pygame.K_o:
                    winding = culling_mgr.toggle_winding_order()
                    hud.show_notification(f"🔄 WINDING ORDER: {culling_mgr.get_winding_str()}", "Toggled Counter-Clockwise (CCW) vs Clockwise (CW) definition.", (56, 189, 248), 3.0)
                    print(f"[WINDING] Order: {culling_mgr.get_winding_str()}")

                elif event.key == pygame.K_t:
                    stress = culling_mgr.toggle_stress_test()
                    if stress:
                        hud.show_notification("🏙️ HIGH-POLY STRESS TEST: ACTIVE", "Loaded massive city grid (50,000+ triangles) to benchmark GPU fill-rate!", (245, 158, 11), 3.5)
                    else:
                        hud.show_notification("🏙️ STANDARD TOWN SCENE RESTORED", "Base environment loaded (~4,600 triangles).", (148, 163, 184), 2.5)
                    print(f"[STRESS TEST] Heavy Grid: {'ACTIVE (50K+ Polygons)' if stress else 'OFF'}")

                elif event.key == pygame.K_u:
                    uncapped = culling_mgr.toggle_fps_cap()
                    if uncapped:
                        hud.show_notification("🚀 UNCACHED BENCHMARK MODE: ACTIVE", "Frame rate limiter disabled! Benchmarking raw GPU throughput.", (168, 85, 247), 3.0)
                    else:
                        hud.show_notification("🔒 60 FPS VSYNC CAP RESTORED", "Frame rate locked to 60 FPS for smooth simulation.", (148, 163, 184), 2.5)
                    print(f"[BENCHMARK] FPS Cap: {'UNCAPPED' if uncapped else 'CAPPED (60 FPS)'}")

                elif event.key == pygame.K_r:
                    camera.reset_position()
                    hud.show_notification("📍 CAMERA RESET", "Viewpoint snapped back to starting position.", (56, 189, 248), 2.0)
                    print("[CAMERA] Viewpoint reset to starting position.")

            elif event.type == pygame.MOUSEMOTION:
                if camera.mouse_locked:
                    camera.process_mouse(event.rel[0], event.rel[1])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not camera.mouse_locked:
                        clicked_action = hud.handle_click(event.pos, culling_mgr, camera)
                        if not clicked_action:
                            # User clicked on 3D viewport outside buttons: re-lock mouse!
                            camera.set_mouse_lock(True)

        # Process continuous keyboard inputs for camera flight
        keys = pygame.key.get_pressed()
        camera.process_keyboard(keys, dt)

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

        # Render 3D Environment Geometry
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
