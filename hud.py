"""
=============================================================================
Interactive 2D Heads-Up Display (HUD) & Telemetry Dashboard
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================

This module renders an interactive 2D control center on top of the 3D OpenGL viewport:
- Interactive Clickable UI Buttons with hover effects:
    [ ⚡ ASK FOR BACK-FACE CULLING ]
    [ 🌐 WIREFRAME MODE ]
    [ 🏙️ HIGH-POLY STRESS TEST ]
    [ 🚀 UNCAP FPS BENCHMARK ]
    [ 🖱️ CURSOR FREE / LOCK ]
- Dynamic On-Demand Optimization:
    Culling is OFF by default. Only when the user asks for culling (by pressing
    [C] or clicking the UI button) does the GPU face culling activate!
- Interactive Notification Banners (Toasts) showing instant feedback when the user
    triggers culling, switches wireframe, or enables stress tests.
- Real-time Smoothed FPS & Frame Latency (ms) metrics.
- Hardware Triangle Counters (100% Rendered vs ~50% Culled).
"""

import math
import pygame
from OpenGL.GL import (
    glGenTextures, glBindTexture, glTexImage2D, glTexParameteri,
    glPushAttrib, glPopAttrib, glMatrixMode, glPushMatrix, glPopMatrix,
    glLoadIdentity, glOrtho, glEnable, glDisable, glBlendFunc,
    glBegin, glEnd, glTexCoord2f, glVertex2f, glColor4f, glPolygonMode,
    GL_TEXTURE_2D, GL_RGBA, GL_UNSIGNED_BYTE, GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER, GL_LINEAR, GL_ALL_ATTRIB_BITS, GL_DEPTH_TEST,
    GL_LIGHTING, GL_CULL_FACE, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
    GL_PROJECTION, GL_MODELVIEW, GL_QUADS, GL_FRONT_AND_BACK, GL_FILL
)
import config


class HUD:
    def __init__(self, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT):
        self.width = width
        self.height = height

        # Initialize Typography
        pygame.font.init()
        font_name = "Segoe UI" if "segoeui" in pygame.font.get_fonts() else "Arial"
        mono_name = "Consolas" if "consolas" in pygame.font.get_fonts() else "Courier New"

        self.font_title = pygame.font.SysFont(font_name, 19, bold=True)
        self.font_btn   = pygame.font.SysFont(font_name, 14, bold=True)
        self.font_bold  = pygame.font.SysFont(font_name, 15, bold=True)
        self.font_reg   = pygame.font.SysFont(font_name, 13)
        self.font_mono  = pygame.font.SysFont(mono_name, 13, bold=True)
        self.font_toast = pygame.font.SysFont(font_name, 15, bold=True)
        self.font_keys  = pygame.font.SysFont(mono_name, 12)

        # Pygame 2D canvas for overlay
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # OpenGL 2D texture allocation
        self.tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Performance timing smoothing
        self.fps_smoothed = 60.0
        self.frame_time_smoothed = 16.6

        # Interactive Notification System (Toast)
        self.notification_title = ""
        self.notification_sub = ""
        self.notification_color = (16, 185, 129)
        self.notification_timer = 0.0
        self.notification_max_time = 4.0

        # Animation Pulse Timer
        self.anim_time = 0.0

        # Define Interactive UI Button Rectangles (Interactive Click Targets)
        # 1. Main Culling Request Button
        self.btn_cull_rect = pygame.Rect(32, 82, 440, 38)
        # 2. Secondary Mini-Buttons
        self.btn_wf_rect     = pygame.Rect(32, 168, 140, 28)
        self.btn_stress_rect = pygame.Rect(178, 168, 145, 28)
        self.btn_uncap_rect  = pygame.Rect(329, 168, 143, 28)

        # Default start banner
        self.show_notification(
            "⚡ WELCOME! CULLING IS CURRENTLY OFF",
            "Press [C] or click the button below to ASK FOR CULLING and optimize the scene!",
            (245, 158, 11),
            6.0
        )

    def show_notification(self, title, subtitle="", color=(16, 185, 129), duration=3.5):
        """Triggers an animated interactive on-screen notification toast."""
        self.notification_title = title
        self.notification_sub = subtitle
        self.notification_color = color
        self.notification_timer = float(duration)
        self.notification_max_time = float(duration)

    def update_metrics(self, fps, frame_time_ms):
        """Smoothes frame rate and frame time."""
        alpha = 0.15
        self.fps_smoothed = (1.0 - alpha) * self.fps_smoothed + alpha * fps
        self.frame_time_smoothed = (1.0 - alpha) * self.frame_time_smoothed + alpha * frame_time_ms

    def update(self, dt):
        """Advances animation clocks and toast timers."""
        self.anim_time += dt
        if self.notification_timer > 0.0:
            self.notification_timer = max(0.0, self.notification_timer - dt)

    def handle_click(self, mouse_pos, culling_mgr, camera):
        """
        Handles mouse clicks on interactive UI buttons when cursor is free.
        Returns the action name if a button was clicked, or None.
        """
        # 1. Clicked Main Culling Toggle Button
        if self.btn_cull_rect.collidepoint(mouse_pos):
            state = culling_mgr.toggle_culling()
            if state:
                self.show_notification(
                    "⚡ USER REQUEST GRANTED: CULLING ACTIVATED!",
                    "OpenGL is now discarding ~50% of triangles before rasterization!",
                    (16, 185, 129), 3.5
                )
            else:
                self.show_notification(
                    "⚠️ CULLING DEACTIVATED BY USER",
                    "GPU is now rasterizing all redundant back-facing geometry (100% load).",
                    (239, 68, 68), 3.5
                )
            return "cull"

        # 2. Clicked Wireframe Toggle Button
        if self.btn_wf_rect.collidepoint(mouse_pos):
            wf = culling_mgr.toggle_wireframe()
            if wf:
                self.show_notification(
                    "🌐 WIREFRAME MODE: ENABLED",
                    "Surface occlusion removed! You can see all wireframe polygon lines.",
                    (56, 189, 248), 3.0
                )
            else:
                self.show_notification(
                    "🟦 SOLID SHADING RESTORED",
                    "Standard opaque surface rendering active.",
                    (148, 163, 184), 2.5
                )
            return "wireframe"

        # 3. Clicked Stress Test Button
        if self.btn_stress_rect.collidepoint(mouse_pos):
            stress = culling_mgr.toggle_stress_test()
            if stress:
                self.show_notification(
                    "🏙️ HIGH-POLY STRESS TEST: ACTIVE",
                    "Loaded massive city grid (50,000+ triangles) to benchmark GPU fill-rate!",
                    (245, 158, 11), 3.5
                )
            else:
                self.show_notification(
                    "🏙️ STANDARD TOWN SCENE RESTORED",
                    "Base environment loaded (~4,600 triangles).",
                    (148, 163, 184), 2.5
                )
            return "stress"

        # 4. Clicked Benchmark Button
        if self.btn_uncap_rect.collidepoint(mouse_pos):
            uncapped = culling_mgr.toggle_fps_cap()
            if uncapped:
                self.show_notification(
                    "🚀 UNCACHED BENCHMARK MODE: ACTIVE",
                    "Frame rate limiter disabled! Benchmarking raw GPU throughput.",
                    (168, 85, 247), 3.0
                )
            else:
                self.show_notification(
                    "🔒 60 FPS VSYNC CAP RESTORED",
                    "Frame rate locked to 60 FPS for smooth simulation.",
                    (148, 163, 184), 2.5
                )
            return "uncap"

        return None

    def render(self, culling_mgr, camera, total_triangles, mouse_pos=(0, 0), mouse_locked=True):
        """Composes and renders the 2D interactive HUD overlay."""
        self.surface.fill((0, 0, 0, 0))

        # -----------------------------------------------------------------
        # Panel 1: Top-Left Interactive Optimization Control Center
        # -----------------------------------------------------------------
        panel_w = 490
        panel_h = 248
        panel_rect = pygame.Rect(18, 16, panel_w, panel_h)

        pygame.draw.rect(self.surface, (15, 23, 42, 225), panel_rect, border_radius=10)
        pygame.draw.rect(self.surface, (51, 65, 85, 255), panel_rect, width=2, border_radius=10)

        # Title Banner
        title_surf = self.font_title.render("3D GRAPHICS OPTIMIZATION CONTROLLER", True, (255, 255, 255))
        self.surface.blit(title_surf, (32, 26))

        sub_surf = self.font_reg.render("Technique: OpenGL Hardware Back-Face Culling", True, (148, 163, 184))
        self.surface.blit(sub_surf, (32, 50))

        pygame.draw.line(self.surface, (45, 60, 80), (32, 72), (panel_w + 4, 72), 1)

        # -----------------------------------------------------------------
        # THE PRIMARY INTERACTIVE BUTTON: "ASK FOR CULLING"
        # -----------------------------------------------------------------
        is_culled = culling_mgr.culling_enabled
        is_hover_cull = (not mouse_locked) and self.btn_cull_rect.collidepoint(mouse_pos)

        # Pulse animation when culling is OFF to invite user action!
        pulse = (math.sin(self.anim_time * 5.0) + 1.0) * 0.5 if not is_culled else 0.0

        if is_culled:
            btn_bg = (16, 185, 129, 230) if not is_hover_cull else (20, 205, 140, 250)
            btn_border = (52, 211, 153)
            btn_txt = "🟢 [C] CULLING: ACTIVE ON USER REQUEST  (Click to Turn OFF)"
            expl_txt = "Optimized: Back faces discarded in Primitive Assembly stage!"
            expl_col = (187, 247, 208)
        else:
            r = int(220 + pulse * 25)
            g = int(120 + pulse * 40)
            btn_bg = (r, g, 20, 235) if not is_hover_cull else (245, 158, 11, 255)
            btn_border = (251, 191, 36)
            btn_txt = "⚡ [C] ASK FOR BACK-FACE CULLING  (Click or Press 'C')"
            expl_txt = "Status: Culling is OFF. Drawing all redundant back-faces!"
            expl_col = (254, 215, 170)

        pygame.draw.rect(self.surface, btn_bg, self.btn_cull_rect, border_radius=6)
        pygame.draw.rect(self.surface, btn_border, self.btn_cull_rect, width=2 if not is_hover_cull else 3, border_radius=6)

        btn_surf = self.font_btn.render(btn_txt, True, (255, 255, 255) if is_culled else (15, 23, 42))
        btn_x = self.btn_cull_rect.x + (self.btn_cull_rect.width - btn_surf.get_width()) // 2
        btn_y = self.btn_cull_rect.y + (self.btn_cull_rect.height - btn_surf.get_height()) // 2
        self.surface.blit(btn_surf, (btn_x, btn_y))

        expl_surf = self.font_reg.render(expl_txt, True, expl_col)
        self.surface.blit(expl_surf, (32, 126))

        # Mode explanation line
        mode_txt = "Winding: Counter-Clockwise (CCW) | Cull Target: GL_BACK"
        mode_surf = self.font_reg.render(mode_txt, True, (148, 163, 184))
        self.surface.blit(mode_surf, (32, 146))

        # -----------------------------------------------------------------
        # Secondary Interactive Mini-Buttons (Wireframe, Stress, Benchmark)
        # -----------------------------------------------------------------
        # 1. Wireframe Button
        wf_active = culling_mgr.wireframe_mode
        hover_wf = (not mouse_locked) and self.btn_wf_rect.collidepoint(mouse_pos)
        wf_bg = (56, 189, 248, 200) if wf_active else (30, 41, 59, 220)
        pygame.draw.rect(self.surface, wf_bg, self.btn_wf_rect, border_radius=5)
        pygame.draw.rect(self.surface, (56, 189, 248) if hover_wf or wf_active else (71, 85, 105), self.btn_wf_rect, width=1, border_radius=5)
        wf_txt = "[M] Wireframe: ON" if wf_active else "[M] Wireframe: OFF"
        wf_surf = self.font_reg.render(wf_txt, True, (15, 23, 42) if wf_active else (226, 232, 240))
        self.surface.blit(wf_txt_surf := wf_surf, (self.btn_wf_rect.x + 8, self.btn_wf_rect.y + 6))

        # 2. Stress Grid Button
        st_active = culling_mgr.stress_test_mode
        hover_st = (not mouse_locked) and self.btn_stress_rect.collidepoint(mouse_pos)
        st_bg = (245, 158, 11, 200) if st_active else (30, 41, 59, 220)
        pygame.draw.rect(self.surface, st_bg, self.btn_stress_rect, border_radius=5)
        pygame.draw.rect(self.surface, (245, 158, 11) if hover_st or st_active else (71, 85, 105), self.btn_stress_rect, width=1, border_radius=5)
        st_txt = "[T] Stress: ON" if st_active else "[T] Stress: OFF"
        st_surf = self.font_reg.render(st_txt, True, (15, 23, 42) if st_active else (226, 232, 240))
        self.surface.blit(st_surf, (self.btn_stress_rect.x + 14, self.btn_stress_rect.y + 6))

        # 3. Benchmark Button
        uc_active = culling_mgr.uncapped_fps
        hover_uc = (not mouse_locked) and self.btn_uncap_rect.collidepoint(mouse_pos)
        uc_bg = (168, 85, 247, 200) if uc_active else (30, 41, 59, 220)
        pygame.draw.rect(self.surface, uc_bg, self.btn_uncap_rect, border_radius=5)
        pygame.draw.rect(self.surface, (168, 85, 247) if hover_uc or uc_active else (71, 85, 105), self.btn_uncap_rect, width=1, border_radius=5)
        uc_txt = "[U] FPS: Uncapped" if uc_active else "[U] FPS: Capped 60"
        uc_surf = self.font_reg.render(uc_txt, True, (15, 23, 42) if uc_active else (226, 232, 240))
        self.surface.blit(uc_surf, (self.btn_uncap_rect.x + 12, self.btn_uncap_rect.y + 6))

        # Camera Coordinate Telemetry
        cam_str = f"Camera: X:{camera.x:.1f} Y:{camera.y:.1f} Z:{camera.z:.1f} | Look: Yaw {camera.yaw:.0f}° Pitch {camera.pitch:.0f}°"
        cam_surf = self.font_mono.render(cam_str, True, (56, 189, 248))
        self.surface.blit(cam_surf, (32, 208))

        # Mouse Lock Status line
        mouse_txt = "🖱️ Mouse Locked (Look Mode). Press [Tab] to free cursor and click buttons!" if mouse_locked else "🖱️ Cursor Free! Click any button with mouse, or click 3D world to re-lock."
        mouse_surf = self.font_reg.render(mouse_txt, True, (251, 191, 36) if not mouse_locked else (148, 163, 184))
        self.surface.blit(mouse_surf, (32, 226))

        # -----------------------------------------------------------------
        # Panel 2: Top-Right Real-Time Telemetry & Hardware Workload
        # -----------------------------------------------------------------
        perf_w = 340
        perf_h = 220
        perf_x = self.width - perf_w - 18
        perf_rect = pygame.Rect(perf_x, 16, perf_w, perf_h)

        pygame.draw.rect(self.surface, (15, 23, 42, 225), perf_rect, border_radius=10)
        pygame.draw.rect(self.surface, (51, 65, 85, 255), perf_rect, width=2, border_radius=10)

        perf_title = self.font_title.render("PERFORMANCE METRICS", True, (255, 255, 255))
        self.surface.blit(perf_title, (perf_x + 16, 26))

        pygame.draw.line(self.surface, (45, 60, 80), (perf_x + 16, 50), (perf_x + perf_w - 16, 50), 1)

        # FPS
        fps_val = int(round(self.fps_smoothed))
        fps_color = (16, 185, 129) if fps_val >= 55 else ((245, 158, 11) if fps_val >= 30 else (239, 68, 68))
        self.surface.blit(self.font_bold.render("Frame Rate (FPS):", True, (226, 232, 240)), (perf_x + 16, 60))
        self.surface.blit(self.font_title.render(f"{fps_val} FPS", True, fps_color), (perf_x + 210, 58))

        # Frame Latency (ms)
        self.surface.blit(self.font_bold.render("Frame Latency:", True, (226, 232, 240)), (perf_x + 16, 86))
        self.surface.blit(self.font_mono.render(f"{self.frame_time_smoothed:.2f} ms", True, (56, 189, 248)), (perf_x + 210, 86))

        # FPS Limiter State
        cap_str = "UNCAPPED (Benchmark)" if culling_mgr.uncapped_fps else "CAPPED (60 FPS V-Sync)"
        self.surface.blit(self.font_reg.render(f"Framerate Cap: {cap_str}", True, (168, 85, 247) if culling_mgr.uncapped_fps else (148, 163, 184)), (perf_x + 16, 112))

        pygame.draw.line(self.surface, (45, 60, 80), (perf_x + 16, 134), (perf_x + perf_w - 16, 134), 1)

        # Total Triangles
        self.surface.blit(self.font_reg.render("Total Scene Triangles:", True, (226, 232, 240)), (perf_x + 16, 142))
        self.surface.blit(self.font_mono.render(f"{total_triangles:,}", True, (255, 255, 255)), (perf_x + 210, 142))

        # Discarded vs Rendered Triangles
        if is_culled:
            culled_count = int(total_triangles * 0.50)
            drawn_count = total_triangles - culled_count
            cull_stat_str = f"Hardware Discarded: ~{culled_count:,} (50%)"
            drawn_stat_str = f"Hardware Rendered:  ~{drawn_count:,} (50%)"
            col_stat = (16, 185, 129)
        else:
            cull_stat_str = "Hardware Discarded: 0 (0%)"
            drawn_stat_str = f"Hardware Rendered:  {total_triangles:,} (100%)"
            col_stat = (239, 68, 68)

        self.surface.blit(self.font_mono.render(cull_stat_str, True, col_stat), (perf_x + 16, 166))
        self.surface.blit(self.font_mono.render(drawn_stat_str, True, (148, 163, 184)), (perf_x + 16, 188))

        # -----------------------------------------------------------------
        # Panel 3: Center-Top Floating Interactive Toast / Notification
        # -----------------------------------------------------------------
        if self.notification_timer > 0.0:
            toast_w = 640
            toast_h = 58
            toast_x = (self.width - toast_w) // 2
            toast_y = 16
            toast_rect = pygame.Rect(toast_x, toast_y, toast_w, toast_h)

            # Alpha fade out during last 0.8s
            fade_alpha = min(240, int((self.notification_timer / min(0.8, self.notification_max_time)) * 240)) if self.notification_timer < 0.8 else 240
            t_surface = pygame.Surface((toast_w, toast_h), pygame.SRCALPHA)
            pygame.draw.rect(t_surface, (15, 23, 42, fade_alpha), (0, 0, toast_w, toast_h), border_radius=8)
            pygame.draw.rect(t_surface, (*self.notification_color, fade_alpha), (0, 0, toast_w, toast_h), width=2, border_radius=8)

            # Draw Toast Title & Subtitle
            t_title = self.font_toast.render(self.notification_title, True, self.notification_color)
            t_sub   = self.font_reg.render(self.notification_sub, True, (241, 245, 249))

            t_surface.blit(t_title, ((toast_w - t_title.get_width()) // 2, 8))
            t_surface.blit(t_sub, ((toast_w - t_sub.get_width()) // 2, 31))

            self.surface.blit(t_surface, (toast_x, toast_y))

        # -----------------------------------------------------------------
        # Panel 4: Bottom Navigation Bar
        # -----------------------------------------------------------------
        bar_h = 36
        bar_y = self.height - bar_h - 12
        bar_rect = pygame.Rect(18, bar_y, self.width - 36, bar_h)

        pygame.draw.rect(self.surface, (15, 23, 42, 225), bar_rect, border_radius=8)
        pygame.draw.rect(self.surface, (51, 65, 85, 255), bar_rect, width=1, border_radius=8)

        shortcuts = (
            "[W,A,S,D] Move | [Mouse] Look | [Space/Ctrl] Fly | [Shift] Sprint | "
            "[C] Ask For Culling | [M] Wireframe | [T] Stress Grid | [U] Uncap FPS | [Tab] Free Cursor"
        )
        bar_surf = self.font_keys.render(shortcuts, True, (226, 232, 240))
        text_x = 18 + (bar_rect.width - bar_surf.get_width()) // 2
        self.surface.blit(bar_surf, (text_x, bar_y + 9))

        # -----------------------------------------------------------------
        # Blit 2D Pygame Canvas to OpenGL Texture & Screen Quad
        # -----------------------------------------------------------------
        tex_data = pygame.image.tostring(self.surface, "RGBA", False)

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)

        glColor4f(1.0, 1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex2f(0, 0)
        glTexCoord2f(1.0, 0.0); glVertex2f(self.width, 0)
        glTexCoord2f(1.0, 1.0); glVertex2f(self.width, self.height)
        glTexCoord2f(0.0, 1.0); glVertex2f(0, self.height)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopAttrib()
