"""
=============================================================================
First-Person 3D Camera System
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================
Provides a smooth 6-DOF (six degrees of freedom) first-person camera:
- Mouse look controls pitch (vertical tilt) and yaw (horizontal rotation)
- Keyboard controls:
    W / S : Move Forward / Backward
    A / D : Strafe Left / Right
    Space : Fly Upward
    Left Control / C : Fly Downward
    Left Shift : Sprint boost (faster flight speed)
- Automatic pitch clamping to prevent screen flips (-89° to +89°)
- Mouse grab/unlock toggle via TAB or ESC
"""

import math
import pygame
from OpenGL.GLU import gluLookAt
import config


class Camera:
    def __init__(self, x=0.0, y=3.5, z=25.0, yaw=-90.0, pitch=-5.0):
        # Camera 3D Position
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

        # Orientation Angles (in degrees)
        self.yaw = float(yaw)      # -90 deg points along -Z axis
        self.pitch = float(pitch)  # Vertical look angle

        # Direction Vectors
        self.front_x = 0.0
        self.front_y = 0.0
        self.front_z = -1.0

        self.right_x = 1.0
        self.right_y = 0.0
        self.right_z = 0.0

        self.up_x = 0.0
        self.up_y = 1.0
        self.up_z = 0.0

        # Speeds and sensitivity
        self.move_speed = config.CAMERA_MOVE_SPEED
        self.sprint_speed = config.CAMERA_SPRINT_SPEED
        self.sensitivity = config.MOUSE_SENSITIVITY

        # Mouse grab state
        self.mouse_locked = True

        self._update_vectors()

    def _update_vectors(self):
        """
        Calculates Cartesian unit vectors from spherical Euler angles (yaw, pitch).
        """
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        # Front Direction Vector
        fx = math.cos(yaw_rad) * math.cos(pitch_rad)
        fy = math.sin(pitch_rad)
        fz = math.sin(yaw_rad) * math.cos(pitch_rad)

        # Normalize Front
        length = math.sqrt(fx * fx + fy * fy + fz * fz)
        if length > 0.0:
            self.front_x = fx / length
            self.front_y = fy / length
            self.front_z = fz / length

        # Right Vector = Front x WorldUp (0, 1, 0)
        rx = self.front_z
        ry = 0.0
        rz = -self.front_x

        r_len = math.sqrt(rx * rx + rz * rz)
        if r_len > 0.0:
            self.right_x = rx / r_len
            self.right_y = 0.0
            self.right_z = rz / r_len

    def process_mouse(self, dx, dy):
        """
        Updates camera yaw and pitch based on relative mouse movements.
        """
        if not self.mouse_locked:
            return

        self.yaw += dx * self.sensitivity
        self.pitch -= dy * self.sensitivity

        # Constrain pitch to avoid gimbal flip
        if self.pitch > 89.0:
            self.pitch = 89.0
        elif self.pitch < -89.0:
            self.pitch = -89.0

        self._update_vectors()

    def process_keyboard(self, keys, dt):
        """
        Moves camera in 3D world space based on active keys and delta time (dt).
        """
        speed = self.sprint_speed if keys[pygame.K_LSHIFT] else self.move_speed
        velocity = speed * dt

        # Forward / Backward along horizontal viewing plane
        if keys[pygame.K_w]:
            self.x += self.front_x * velocity
            self.y += self.front_y * velocity
            self.z += self.front_z * velocity
        if keys[pygame.K_s]:
            self.x -= self.front_x * velocity
            self.y -= self.front_y * velocity
            self.z -= self.front_z * velocity

        # Strafe Left / Right
        if keys[pygame.K_a]:
            self.x -= self.right_x * velocity
            self.z -= self.right_z * velocity
        if keys[pygame.K_d]:
            self.x += self.right_x * velocity
            self.z += self.right_z * velocity

        # Vertical Up / Down
        if keys[pygame.K_SPACE]:
            self.y += velocity
        if keys[pygame.K_LCTRL] or keys[pygame.K_q]:
            self.y -= velocity

    def toggle_mouse_lock(self):
        """Toggles between locked mouse (look around) and unlocked (desktop cursor)."""
        self.mouse_locked = not self.mouse_locked
        pygame.mouse.set_visible(not self.mouse_locked)
        pygame.event.set_grab(self.mouse_locked)
        return self.mouse_locked

    def set_mouse_lock(self, locked):
        self.mouse_locked = locked
        pygame.mouse.set_visible(not locked)
        pygame.event.set_grab(locked)

    def reset_position(self):
        """Resets camera back to initial starting viewpoint."""
        self.x, self.y, self.z = config.CAMERA_INITIAL_POS
        self.yaw = config.CAMERA_INITIAL_YAW
        self.pitch = config.CAMERA_INITIAL_PITCH
        self._update_vectors()

    def apply_view(self):
        """Applies the View Matrix in OpenGL using gluLookAt."""
        target_x = self.x + self.front_x
        target_y = self.y + self.front_y
        target_z = self.z + self.front_z

        gluLookAt(
            self.x, self.y, self.z,
            target_x, target_y, target_z,
            self.up_x, self.up_y, self.up_z
        )
