"""
=============================================================================
3D Game Environment & Scene Renderer
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================

This module constructs an attractive 3D game world combining:
1. Blender-Exported 3D Models (Buildings, Medieval Watchtowers, Pine Trees, Lamp Posts)
2. Procedural Architectural Elements (Fortress Walls, Arches, Roads, Plazas)
3. Dedicated Educational Inspection Chamber ("Inside-Out Culling Room")
4. Rotating Plaza Monolith & Showcase Cubes
5. Heavy-Density Stress Test City Grid (100,000+ Triangles) for performance benchmarks

All geometry strictly enforces Counter-Clockwise (CCW) vertex winding and
accurate outward normals to guarantee precise OpenGL Back-Face Culling behavior.
"""

import os
import math
from OpenGL.GL import (
    glPushMatrix, glPopMatrix, glTranslatef, glRotatef, glScalef,
    glBegin, glEnd, GL_TRIANGLES, GL_QUADS,
    glVertex3f, glNormal3f, glColor4f,
    glMaterialfv, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, GL_SPECULAR, GL_SHININESS,
    glGenLists, glNewList, glEndList, glCallList, GL_COMPILE
)
import config
from obj_loader import OBJModel


class Scene:
    def __init__(self):
        self.rotation_angle = 0.0
        self.models = {}
        self.ground_list = None
        self.walls_list = None
        self.inside_out_cube_list = None

        # Triangle count trackers
        self.base_triangles = 0
        self.stress_triangles = 0

        self._load_blender_models()
        self._build_procedural_lists()

    def _load_blender_models(self):
        """Loads .obj models exported from Blender."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(base_dir, "models")

        model_files = {
            "building": ("building.obj", (0.80, 0.78, 0.74, 1.0)),
            "watchtower": ("watchtower.obj", (0.65, 0.65, 0.68, 1.0)),
            "tree": ("tree.obj", (0.20, 0.55, 0.22, 1.0)),
            "lamp_post": ("lamp_post.obj", (0.35, 0.38, 0.42, 1.0)),
        }

        for key, (filename, color) in model_files.items():
            path = os.path.join(models_dir, filename)
            self.models[key] = OBJModel(path, default_color=color)

    def _build_procedural_lists(self):
        """Compiles static terrain, walls, and inspection chamber into display lists."""
        self.ground_list = glGenLists(1)
        glNewList(self.ground_list, GL_COMPILE)
        self._render_ground_grid()
        glEndList()

        self.walls_list = glGenLists(1)
        glNewList(self.walls_list, GL_COMPILE)
        self._render_perimeter_walls()
        glEndList()

        self.inside_out_cube_list = glGenLists(1)
        glNewList(self.inside_out_cube_list, GL_COMPILE)
        self._render_inside_out_chamber()
        glEndList()

    @staticmethod
    def _draw_box(x, y, z, sx, sy, sz, color):
        """
        Draws a box centered at (x, y, z) with half-extents (sx, sy, sz)
        using strict Counter-Clockwise (CCW) face vertex winding.
        """
        glColor4f(*color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, color)

        x0, x1 = x - sx, x + sx
        y0, y1 = y - sy, y + sy
        z0, z1 = z - sz, z + sz

        glBegin(GL_TRIANGLES)

        # Front Face (Normal: 0, 0, 1) - CCW
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(x0, y0, z1); glVertex3f(x1, y0, z1); glVertex3f(x1, y1, z1)
        glVertex3f(x0, y0, z1); glVertex3f(x1, y1, z1); glVertex3f(x0, y1, z1)

        # Back Face (Normal: 0, 0, -1) - CCW
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(x1, y0, z0); glVertex3f(x0, y0, z0); glVertex3f(x0, y1, z0)
        glVertex3f(x1, y0, z0); glVertex3f(x0, y1, z0); glVertex3f(x1, y1, z0)

        # Left Face (Normal: -1, 0, 0) - CCW
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(x0, y0, z0); glVertex3f(x0, y0, z1); glVertex3f(x0, y1, z1)
        glVertex3f(x0, y0, z0); glVertex3f(x0, y1, z1); glVertex3f(x0, y1, z0)

        # Right Face (Normal: 1, 0, 0) - CCW
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(x1, y0, z1); glVertex3f(x1, y0, z0); glVertex3f(x1, y1, z0)
        glVertex3f(x1, y0, z1); glVertex3f(x1, y1, z0); glVertex3f(x1, y1, z1)

        # Top Face (Normal: 0, 1, 0) - CCW
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(x0, y1, z1); glVertex3f(x1, y1, z1); glVertex3f(x1, y1, z0)
        glVertex3f(x0, y1, z1); glVertex3f(x1, y1, z0); glVertex3f(x0, y1, z0)

        # Bottom Face (Normal: 0, -1, 0) - CCW
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(x0, y0, z0); glVertex3f(x1, y0, z0); glVertex3f(x1, y0, z1)
        glVertex3f(x0, y0, z0); glVertex3f(x1, y0, z1); glVertex3f(x0, y0, z1)

        glEnd()

    def _render_ground_grid(self):
        """Constructs checkered terrain and asphalt central boulevards."""
        glBegin(GL_TRIANGLES)
        glNormal3f(0.0, 1.0, 0.0)

        grid_range = 60
        tile_size = 6

        # Checkered grass plaza
        for gx in range(-grid_range, grid_range, tile_size):
            for gz in range(-grid_range, grid_range, tile_size):
                # Central boulevard check
                is_road = (-9 <= gx <= 9) or (-9 <= gz <= 9)
                if is_road:
                    col = config.COLOR_ROAD
                else:
                    checker = ((gx + gz) // tile_size) % 2 == 0
                    col = config.COLOR_GROUND_A if checker else config.COLOR_GROUND_B

                glColor4f(*col)
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, col)

                # Two CCW triangles per grid square
                glVertex3f(gx, 0.0, gz + tile_size)
                glVertex3f(gx + tile_size, 0.0, gz + tile_size)
                glVertex3f(gx + tile_size, 0.0, gz)

                glVertex3f(gx, 0.0, gz + tile_size)
                glVertex3f(gx + tile_size, 0.0, gz)
                glVertex3f(gx, 0.0, gz)

        glEnd()

    def _render_perimeter_walls(self):
        """Builds boundary defensive walls and battlements."""
        wall_col = (0.58, 0.55, 0.52, 1.0)
        cap_col = (0.70, 0.67, 0.63, 1.0)

        # North & South walls
        for z_pos in [-55.0, 55.0]:
            self._draw_box(0.0, 3.0, z_pos, 52.0, 3.0, 1.2, wall_col)
            # Wall cap
            self._draw_box(0.0, 6.3, z_pos, 53.0, 0.3, 1.5, cap_col)

        # East & West walls
        for x_pos in [-55.0, 55.0]:
            self._draw_box(x_pos, 3.0, 0.0, 1.2, 3.0, 52.0, wall_col)
            # Wall cap
            self._draw_box(x_pos, 6.3, 0.0, 1.5, 0.3, 53.0, cap_col)

    def _render_inside_out_chamber(self):
        """
        Educational Demo Chamber:
        An enclosed room located at (-25, 4, -15) with an entrance doorway.
        Vertices are wound CCW with normals facing OUTWARD.

        When you walk INSIDE this room:
        - Back-Face Culling ON: The outward-facing walls are culled! You see right through them!
        - Back-Face Culling OFF: The walls are rendered, showing the enclosure.
        """
        chamber_color = (0.85, 0.35, 0.25, 1.0)
        beacon_color = (0.95, 0.85, 0.20, 1.0)

        # Main room structure (North, South, East, West walls and ceiling)
        # Back wall (-Z)
        self._draw_box(-25.0, 4.0, -20.0, 5.0, 4.0, 0.4, chamber_color)
        # Left wall (-X)
        self._draw_box(-30.0, 4.0, -15.0, 0.4, 4.0, 5.0, chamber_color)
        # Right wall (+X)
        self._draw_box(-20.0, 4.0, -15.0, 0.4, 4.0, 5.0, chamber_color)
        # Ceiling (+Y)
        self._draw_box(-25.0, 8.0, -15.0, 5.0, 0.4, 5.0, chamber_color)
        # Front wall with entrance doorway (+Z)
        self._draw_box(-28.0, 4.0, -10.0, 2.0, 4.0, 0.4, chamber_color)
        self._draw_box(-22.0, 4.0, -10.0, 2.0, 4.0, 0.4, chamber_color)
        self._draw_box(-25.0, 6.5, -10.0, 1.0, 1.5, 0.4, chamber_color)

        # Floating yellow beacon over chamber
        self._draw_box(-25.0, 9.5, -15.0, 0.8, 0.8, 0.8, beacon_color)

    def update(self, dt):
        """Updates animation angles (such as rotating plaza monoliths)."""
        self.rotation_angle = (self.rotation_angle + 40.0 * dt) % 360.0

    def render(self, culling_mgr):
        """Renders the entire 3D scene."""
        total_triangles = 0

        # 1. Static Ground & Roads
        if self.ground_list:
            glCallList(self.ground_list)
            # 20 * 20 * 2 = 800 triangles
            total_triangles += 800

        # 2. Perimeter Walls
        if self.walls_list:
            glCallList(self.walls_list)
            # 8 boxes * 12 triangles = 96 triangles
            total_triangles += 96

        # 3. Inside-Out Educational Chamber
        if self.inside_out_cube_list:
            glCallList(self.inside_out_cube_list)
            total_triangles += 96

        # 4. Central Plaza Rotating Monolith (Shows dynamic face orientation)
        glPushMatrix()
        glTranslatef(0.0, 3.5, 0.0)
        glRotatef(self.rotation_angle, 0.0, 1.0, 0.0)
        glRotatef(self.rotation_angle * 0.5, 1.0, 0.0, 0.0)
        self._draw_box(0.0, 0.0, 0.0, 1.8, 1.8, 1.8, (0.2, 0.7, 0.9, 1.0))
        # Inner core cube
        self._draw_box(0.0, 0.0, 0.0, 0.9, 0.9, 0.9, (0.9, 0.8, 0.2, 1.0))
        glPopMatrix()
        total_triangles += 24

        # 5. Render Primary Blender Assets
        # Main avenue buildings
        bldg = self.models.get("building")
        tower = self.models.get("watchtower")
        tree = self.models.get("tree")
        lamp = self.models.get("lamp_post")

        # Placement layout for main town scene
        building_positions = [
            ( 18.0, 0.0, -20.0, 0.0, (0.85, 0.82, 0.78, 1.0)),
            (-18.0, 0.0, -32.0, 90.0, (0.75, 0.72, 0.70, 1.0)),
            ( 22.0, 0.0,  18.0, 180.0, (0.80, 0.75, 0.70, 1.0)),
            (-20.0, 0.0,  20.0, 270.0, (0.82, 0.80, 0.75, 1.0)),
            ( 35.0, 0.0, -10.0, 45.0, (0.78, 0.76, 0.72, 1.0)),
            (-35.0, 0.0,  10.0, -45.0, (0.84, 0.82, 0.78, 1.0)),
        ]

        if bldg:
            for x, y, z, rot, col in building_positions:
                glPushMatrix()
                glTranslatef(x, y, z)
                glRotatef(rot, 0.0, 1.0, 0.0)
                bldg.render(col)
                glPopMatrix()
                total_triangles += bldg.num_triangles

        # Corner Watchtowers
        tower_positions = [
            (-48.0, 0.0, -48.0),
            ( 48.0, 0.0, -48.0),
            (-48.0, 0.0,  48.0),
            ( 48.0, 0.0,  48.0),
        ]
        if tower:
            for x, y, z in tower_positions:
                glPushMatrix()
                glTranslatef(x, y, z)
                tower.render((0.62, 0.62, 0.66, 1.0))
                glPopMatrix()
                total_triangles += tower.num_triangles

        # Trees lining avenues and park zones
        tree_positions = [
            (-10.0, 0.0, -10.0), (-10.0, 0.0, -22.0), (-10.0, 0.0, 10.0), (-10.0, 0.0, 22.0),
            ( 10.0, 0.0, -10.0), ( 10.0, 0.0, -22.0), ( 10.0, 0.0, 10.0), ( 10.0, 0.0, 22.0),
            (-30.0, 0.0, -35.0), (-38.0, 0.0, -28.0), ( 32.0, 0.0,  32.0), ( 40.0, 0.0,  25.0),
            (  0.0, 0.0, -40.0), (  0.0, 0.0,  40.0)
        ]
        if tree:
            for i, (x, y, z) in enumerate(tree_positions):
                glPushMatrix()
                glTranslatef(x, y, z)
                # Slight scale & rotation variation for natural appearance
                s = 0.85 + (i % 4) * 0.1
                glScalef(s, s, s)
                glRotatef((i * 47) % 360, 0.0, 1.0, 0.0)
                tree.render((0.18, 0.52 + (i % 3) * 0.03, 0.20, 1.0))
                glPopMatrix()
                total_triangles += tree.num_triangles

        # Street Lamps along plaza
        lamp_positions = [
            (-6.0, 0.0, -12.0), (-6.0, 0.0, 12.0),
            ( 6.0, 0.0, -12.0), ( 6.0, 0.0, 12.0),
            (-12.0, 0.0, -6.0), ( 12.0, 0.0, -6.0),
            (-12.0, 0.0,  6.0), ( 12.0, 0.0,  6.0),
        ]
        if lamp:
            for x, y, z in lamp_positions:
                glPushMatrix()
                glTranslatef(x, y, z)
                lamp.render((0.30, 0.32, 0.36, 1.0))
                glPopMatrix()
                total_triangles += lamp.num_triangles

        # 6. Stress Test Mode: Spawns dense 12x12 grid of buildings and towers
        # Used for college demonstration to show measurable FPS and frame-time scaling!
        if culling_mgr.stress_test_mode and bldg:
            grid_count = 10
            spacing = 24.0
            offset = - (grid_count * spacing) / 2.0

            for gx in range(grid_count):
                for gz in range(grid_count):
                    # Skip center plaza
                    if 3 <= gx <= 6 and 3 <= gz <= 6:
                        continue
                    wx = offset + gx * spacing
                    wz = offset + gz * spacing

                    glPushMatrix()
                    glTranslatef(wx, 0.0, wz)
                    if (gx + gz) % 2 == 0:
                        bldg.render((0.75, 0.72, 0.68, 1.0))
                        total_triangles += bldg.num_triangles
                    else:
                        if tower:
                            tower.render((0.60, 0.60, 0.65, 1.0))
                            total_triangles += tower.num_triangles
                        else:
                            bldg.render((0.75, 0.72, 0.68, 1.0))
                            total_triangles += bldg.num_triangles
                    glPopMatrix()

        self.base_triangles = total_triangles
        return total_triangles
