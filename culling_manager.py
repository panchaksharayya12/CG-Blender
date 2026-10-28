"""
=============================================================================
Culling Manager & Graphics Pipeline Controller
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================

What is Back-Face Culling?
---------------------------
When rendering a closed 3D solid (like a building, cube, or character),
roughly 50% of all polygon surfaces face away from the observer's camera at
any given moment.

Without Back-Face Culling:
    The GPU transforms all vertices, performs rasterization, calculates fragment
    interpolations, and runs pixel shading on surfaces that will immediately be
    overwritten by front surfaces or hidden behind the depth buffer. This wastes
    GPU vertex/fragment throughput, memory bandwidth, and power.

With Back-Face Culling Enabled:
    The graphics hardware tests the orientation of each triangle before rasterization.
    If a triangle faces away from the camera, it is instantly discarded (culled)
    BEFORE rasterization and pixel shading occur.

The Mathematical Foundation:
----------------------------
1. Vector Dot Product Test (Object / World Space):
   Given a triangle with vertices V0, V1, V2 in Counter-Clockwise (CCW) order:
       Edge 1: E1 = V1 - V0
       Edge 2: E2 = V2 - V0
       Surface Normal Vector: N = E1 x E2  (Cross Product)

   Let V be the View Vector from the triangle surface toward the Camera:
       V = Camera_Position - Triangle_Centroid

   The Dot Product (N . V) determines facing:
       If (N . V) > 0  => Surface faces TOWARD camera (Front-Facing => RENDER)
       If (N . V) <= 0 => Surface faces AWAY from camera (Back-Facing => CULL)

2. Screen-Space Winding Order Test (OpenGL Hardware Implementation):
   In the rasterization stage, after vertices are projected to screen coordinates
   (x0, y0), (x1, y1), (x2, y2), OpenGL computes the signed 2D area (determinant):
       Signed_Area = (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)

   - If Signed_Area > 0: Vertices appear Counter-Clockwise (Front-Face in GL_CCW).
   - If Signed_Area < 0: Vertices appear Clockwise (Back-Face in GL_CCW).
   - Back-facing triangles are dropped immediately before generating fragments!
"""

from OpenGL.GL import (
    glEnable, glDisable, glCullFace, glFrontFace, glPolygonMode,
    GL_CULL_FACE, GL_BACK, GL_FRONT, GL_CCW, GL_CW,
    GL_FRONT_AND_BACK, GL_LINE, GL_FILL
)


class CullingManager:
    """
    Manages the OpenGL Face Culling state, polygon modes, and optimization metrics.
    """

    def __init__(self):
        # Culling state: Starts FALSE by default so optimization only happens when requested by user!
        self.culling_enabled = False
        self.user_requested_culling = False

        # Target face to cull: GL_BACK discards back-facing polygons (standard optimization)
        # GL_FRONT is provided for educational demonstration (culls front faces, rendering inside-out)
        self.cull_face_mode = GL_BACK

        # Winding order: GL_CCW means Counter-Clockwise vertices indicate front faces.
        # This is the industry standard followed by Blender and OpenGL.
        self.front_face_mode = GL_CCW

        # Wireframe mode: GL_LINE allows visual inspection of polygon wireframes.
        # This is the easiest way to visually witness back-face culling in action!
        self.wireframe_mode = False

        # Stress test mode: Spawns hundreds of buildings to stress GPU and highlight FPS gains.
        self.stress_test_mode = False

        # Uncapped FPS mode: disables framerate limiter for benchmarking
        self.uncapped_fps = False

    def apply_settings(self):
        """
        Applies current culling and rasterization settings to the active OpenGL context.
        Must be called at the start of each frame before drawing scene geometry.
        """
        # 1. Back-Face Culling State
        if self.culling_enabled:
            glEnable(GL_CULL_FACE)
            glCullFace(self.cull_face_mode)
            glFrontFace(self.front_face_mode)
        else:
            glDisable(GL_CULL_FACE)

        # 2. Polygon Rasterization Mode (Solid Fill vs Wireframe Line)
        if self.wireframe_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def toggle_culling(self):
        """Toggle Back-Face Culling ON or OFF upon user request."""
        self.culling_enabled = not self.culling_enabled
        if self.culling_enabled:
            self.user_requested_culling = True
        return self.culling_enabled

    def toggle_wireframe(self):
        """Toggle Wireframe Mode ON or OFF."""
        self.wireframe_mode = not self.wireframe_mode
        return self.wireframe_mode

    def toggle_cull_face(self):
        """
        Toggle between culling GL_BACK and GL_FRONT.
        Demonstrates that culling the wrong face inverts visibility.
        """
        if self.cull_face_mode == GL_BACK:
            self.cull_face_mode = GL_FRONT
        else:
            self.cull_face_mode = GL_BACK
        return self.cull_face_mode

    def toggle_winding_order(self):
        """Toggle between GL_CCW and GL_CW."""
        if self.front_face_mode == GL_CCW:
            self.front_face_mode = GL_CW
        else:
            self.front_face_mode = GL_CCW
        return self.front_face_mode

    def toggle_stress_test(self):
        """Toggle Stress Test environment to benchmark heavy polygon loads."""
        self.stress_test_mode = not self.stress_test_mode
        return self.stress_test_mode

    def toggle_fps_cap(self):
        """Toggle between capped (60 FPS) and uncapped frame rate."""
        self.uncapped_fps = not self.uncapped_fps
        return self.uncapped_fps

    def get_cull_face_str(self):
        return "GL_BACK (Normal)" if self.cull_face_mode == GL_BACK else "GL_FRONT (Inverted)"

    def get_winding_str(self):
        return "GL_CCW (Counter-Clockwise)" if self.front_face_mode == GL_CCW else "GL_CW (Clockwise)"
