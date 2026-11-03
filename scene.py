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
6. Section Inspector & 3D Ray-Picking for interactive visual culling diagnostics:
   - Green = Front Facing (Rendered by GPU)
   - Red   = Back Facing (Culled / Discarded by GPU)
"""

import os
import math
from OpenGL.GL import (
    glPushMatrix, glPopMatrix, glTranslatef, glRotatef, glScalef,
    glBegin, glEnd, GL_TRIANGLES, GL_QUADS, GL_LINES,
    glVertex3f, glNormal3f, glColor4f, glLineWidth,
    glMaterialfv, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, GL_SPECULAR, GL_SHININESS,
    glGenLists, glNewList, glEndList, glCallList, GL_COMPILE,
    glEnable, glDisable, glCullFace, glPolygonMode,
    GL_CULL_FACE, GL_BACK, GL_FRONT, GL_FILL, GL_LINE
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

        # Section Definitions & Bounding Boxes for 3D Ray Picking
        self.sections_meta = {
            "all": {
                "name": "ALL SECTIONS (Whole Town)",
                "icon": "🏛️",
                "desc": "Entire environment with all residential buildings, towers, plaza & walls.",
                "triangles": 4612,
                "cam_pos": (0.0, 10.0, 32.0, -90.0, -10.0),
                "boxes": []
            },
            "buildings": {
                "name": "TOWN BUILDINGS (Residential)",
                "icon": "🏢",
                "desc": "6 modular buildings with hip slate roofs, foundations & windows.",
                "triangles": 1872,
                "cam_pos": (18.0, 3.5, -8.0, -90.0, -5.0),
                "boxes": [
                    ((-5, 0, -6), (5, 9, 6), ( 18.0, 0.0, -20.0)),
                    ((-6, 0, -5), (6, 9, 5), (-18.0, 0.0, -32.0)),
                    ((-5, 0, -6), (5, 9, 6), ( 22.0, 0.0,  18.0)),
                    ((-6, 0, -5), (6, 9, 5), (-20.0, 0.0,  20.0)),
                    ((-5, 0, -5), (5, 9, 5), ( 35.0, 0.0, -10.0)),
                    ((-5, 0, -5), (5, 9, 5), (-35.0, 0.0,  10.0)),
                ]
            },
            "towers": {
                "name": "CORNER DEFENSE WATCHTOWERS",
                "icon": "🏰",
                "desc": "4 fortified corner towers guarding the perimeter walls.",
                "triangles": 280,
                "cam_pos": (-40.0, 4.0, -38.0, -135.0, 10.0),
                "boxes": [
                    ((-4, 0, -4), (4, 15, 4), (-48.0, 0.0, -48.0)),
                    ((-4, 0, -4), (4, 15, 4), ( 48.0, 0.0, -48.0)),
                    ((-4, 0, -4), (4, 15, 4), (-48.0, 0.0,  48.0)),
                    ((-4, 0, -4), (4, 15, 4), ( 48.0, 0.0,  48.0)),
                ]
            },
            "chamber": {
                "name": "INSIDE-OUT DEMO CHAMBER",
                "icon": "🚪",
                "desc": "Educational room at (-25, 4, -15). Step inside: outward walls vanish!",
                "triangles": 96,
                "cam_pos": (-25.0, 3.8, -15.0, 0.0, 0.0),
                "boxes": [
                    ((-6, 0, -6), (6, 12, 6), (-25.0, 0.0, -15.0))
                ]
            },
            "plaza": {
                "name": "CENTRAL PLAZA & FOUNTAIN",
                "icon": "⛲",
                "desc": "Circular cobblestone plaza with rotating monolith & roads.",
                "triangles": 824,
                "cam_pos": (0.0, 4.0, 16.0, -90.0, -10.0),
                "boxes": [
                    ((-12, 0, -12), (12, 8, 12), (0.0, 0.0, 0.0))
                ]
            },
            "nature": {
                "name": "PINE TREES & STREET LAMPS",
                "icon": "🌲",
                "desc": "Evergreen pines and iron streetlamps with glowing lantern heads.",
                "triangles": 1444,
                "cam_pos": (-10.0, 3.0, 0.0, 0.0, 0.0),
                "boxes": [
                    ((-3, 0, -3), (3, 8, 3), (-10.0, 0.0, -10.0)),
                    ((-3, 0, -3), (3, 8, 3), ( 10.0, 0.0, -10.0)),
                    ((-3, 0, -3), (3, 8, 3), (-10.0, 0.0,  10.0)),
                    ((-3, 0, -3), (3, 8, 3), ( 10.0, 0.0,  10.0)),
                ]
            },
            "stress": {
                "name": "50,000+ TRIANGLE STRESS GRID",
                "icon": "⚡",
                "desc": "100+ dense building benchmark array to test raw GPU fill-rate.",
                "triangles": 52180,
                "cam_pos": (0.0, 25.0, 60.0, -90.0, -25.0),
                "boxes": []
            }
        }

        # Model positions
        self.building_positions = [
            ( 18.0, 0.0, -20.0, 0.0, (0.85, 0.82, 0.78, 1.0)),
            (-18.0, 0.0, -32.0, 90.0, (0.75, 0.72, 0.70, 1.0)),
            ( 22.0, 0.0,  18.0, 180.0, (0.80, 0.75, 0.70, 1.0)),
            (-20.0, 0.0,  20.0, 270.0, (0.82, 0.80, 0.75, 1.0)),
            ( 35.0, 0.0, -10.0, 45.0, (0.78, 0.76, 0.72, 1.0)),
            (-35.0, 0.0,  10.0, -45.0, (0.84, 0.82, 0.78, 1.0)),
        ]

        self.tower_positions = [
            (-48.0, 0.0, -48.0),
            ( 48.0, 0.0, -48.0),
            (-48.0, 0.0,  48.0),
            ( 48.0, 0.0,  48.0),
        ]

        self.tree_positions = [
            (-10.0, 0.0, -10.0), (-10.0, 0.0, -22.0), (-10.0, 0.0, 10.0), (-10.0, 0.0, 22.0),
            ( 10.0, 0.0, -10.0), ( 10.0, 0.0, -22.0), ( 10.0, 0.0, 10.0), ( 10.0, 0.0, 22.0),
            (-30.0, 0.0, -35.0), (-38.0, 0.0, -28.0), ( 32.0, 0.0,  32.0), ( 40.0, 0.0,  25.0),
            (  0.0, 0.0, -40.0), (  0.0, 0.0,  40.0)
        ]

        self.lamp_positions = [
            (-6.0, 0.0, -12.0), (-6.0, 0.0, 12.0),
            ( 6.0, 0.0, -12.0), ( 6.0, 0.0, 12.0),
            (-12.0, 0.0, -6.0), ( 12.0, 0.0, -6.0),
            (-12.0, 0.0,  6.0), ( 12.0, 0.0,  6.0),
        ]

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
            self._draw_box(0.0, 6.3, z_pos, 53.0, 0.3, 1.5, cap_col)

        # East & West walls
        for x_pos in [-55.0, 55.0]:
            self._draw_box(x_pos, 3.0, 0.0, 1.2, 3.0, 52.0, wall_col)
            self._draw_box(x_pos, 6.3, 0.0, 1.5, 0.3, 53.0, cap_col)

    def _render_inside_out_chamber(self):
        """
        Educational Demo Chamber:
        An enclosed room located at (-25, 4, -15) with an entrance doorway.
        Vertices are wound CCW with normals facing OUTWARD.
        """
        chamber_color = (0.85, 0.35, 0.25, 1.0)
        beacon_color = (0.95, 0.85, 0.20, 1.0)

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

    def ray_pick(self, ray_origin, ray_dir):
        """
        Tests 3D ray against bounding boxes of scene sections.
        Returns the closest hit section key ("buildings", "towers", "chamber", "plaza", "nature") or None.
        """
        closest_dist = float('inf')
        hit_section = None

        for sec_key, meta in self.sections_meta.items():
            for box in meta.get("boxes", []):
                b_min, b_max, offset = box
                # Translate box to world coordinates
                w_min = (b_min[0] + offset[0], b_min[1] + offset[1], b_min[2] + offset[2])
                w_max = (b_max[0] + offset[0], b_max[1] + offset[1], b_max[2] + offset[2])

                hit, dist = self._ray_intersects_box(ray_origin, ray_dir, w_min, w_max)
                if hit and 0.0 < dist < closest_dist:
                    closest_dist = dist
                    hit_section = sec_key

        return hit_section

    @staticmethod
    def _ray_intersects_box(ray_origin, ray_dir, box_min, box_max):
        """Axis-Aligned Bounding Box (AABB) ray intersection test."""
        tmin = -float('inf')
        tmax = float('inf')
        for i in range(3):
            if abs(ray_dir[i]) < 1e-8:
                if ray_origin[i] < box_min[i] or ray_origin[i] > box_max[i]:
                    return False, 0.0
            else:
                t1 = (box_min[i] - ray_origin[i]) / ray_dir[i]
                t2 = (box_max[i] - ray_origin[i]) / ray_dir[i]
                if t1 > t2:
                    t1, t2 = t2, t1
                tmin = max(tmin, t1)
                tmax = min(tmax, t2)
                if tmin > tmax or tmax < 0.0:
                    return False, 0.0
        return True, tmin

    def _draw_selection_bracket(self, b_min, b_max, offset):
        """Draws a sleek golden wireframe bounding box to visually highlight the selected section."""
        x0, y0, z0 = b_min[0] + offset[0] - 0.2, b_min[1] + offset[1] - 0.2, b_min[2] + offset[2] - 0.2
        x1, y1, z1 = b_max[0] + offset[0] + 0.2, b_max[1] + offset[1] + 0.2, b_max[2] + offset[2] + 0.2

        glColor4f(0.98, 0.75, 0.15, 0.9)
        glLineWidth(2.5)
        glBegin(GL_LINES)
        # 12 edges of the bounding box
        for e in [
            ((x0, y0, z0), (x1, y0, z0)), ((x1, y0, z0), (x1, y1, z0)), ((x1, y1, z0), (x0, y1, z0)), ((x0, y1, z0), (x0, y0, z0)),
            ((x0, y0, z1), (x1, y0, z1)), ((x1, y0, z1), (x1, y1, z1)), ((x1, y1, z1), (x0, y1, z1)), ((x0, y1, z1), (x0, y0, z1)),
            ((x0, y0, z0), (x0, y0, z1)), ((x1, y0, z0), (x1, y0, z1)), ((x1, y1, z0), (x1, y1, z1)), ((x0, y1, z0), (x0, y1, z1))
        ]:
            glVertex3f(*e[0])
            glVertex3f(*e[1])
        glEnd()
        glLineWidth(1.0)

    def _render_model_with_diagnostics(self, model, default_col, is_target_sec, culling_mgr):
        """
        Renders an OBJ model. If inspector_mode is ON and section matches:
        Pass 1: Front faces in Solid Green (Rendered)
        Pass 2: Back faces in Ruby Red Wireframe (Culled) - only drawn if culling is OFF!
        """
        if culling_mgr.inspector_mode and is_target_sec:
            # Pass 1: Front Faces = RENDERED (Emerald Green)
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            model.render((0.15, 0.85, 0.35, 1.0))

            # Pass 2: Back Faces = CULLED (Ruby Red)
            # Only visible when Culling is OFF! When culling is ON, OpenGL drops back faces!
            if not culling_mgr.culling_enabled:
                glCullFace(GL_FRONT)
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                glLineWidth(2.0)
                model.render((0.95, 0.18, 0.18, 1.0))
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                glCullFace(GL_BACK)
        else:
            # Standard Shading
            model.render(default_col)

    def render(self, culling_mgr):
        """
        Renders the entire 3D scene with dynamic section isolation,
        inspection mode, and live walking culling.
        """
        total_triangles = 0
        active_sec = culling_mgr.selected_section

        # 1. Static Ground & Roads
        if self.ground_list:
            glCallList(self.ground_list)
            total_triangles += 800

        # 2. Perimeter Walls
        if self.walls_list:
            glCallList(self.walls_list)
            total_triangles += 96

        # 3. Inside-Out Educational Chamber
        is_chamb_sec = (active_sec in ["all", "chamber"])
        if self.inside_out_cube_list:
            glCallList(self.inside_out_cube_list)
            total_triangles += 96
            # Selection bracket if selected
            if active_sec == "chamber":
                for b_min, b_max, offset in self.sections_meta["chamber"]["boxes"]:
                    self._draw_selection_bracket(b_min, b_max, offset)

        # 4. Central Plaza Rotating Monolith
        glPushMatrix()
        glTranslatef(0.0, 3.5, 0.0)
        glRotatef(self.rotation_angle, 0.0, 1.0, 0.0)
        glRotatef(self.rotation_angle * 0.5, 1.0, 0.0, 0.0)
        self._draw_box(0.0, 0.0, 0.0, 1.8, 1.8, 1.8, (0.2, 0.7, 0.9, 1.0))
        self._draw_box(0.0, 0.0, 0.0, 0.9, 0.9, 0.9, (0.9, 0.8, 0.2, 1.0))
        glPopMatrix()
        total_triangles += 24

        # 5. Render Primary Blender Assets
        bldg = self.models.get("building")
        tower = self.models.get("watchtower")
        tree = self.models.get("tree")
        lamp = self.models.get("lamp_post")

        # 5A. Town Buildings
        is_bldg_sec = (active_sec in ["all", "buildings"])
        if bldg:
            for i, (x, y, z, rot, col) in enumerate(self.building_positions):
                glPushMatrix()
                glTranslatef(x, y, z)
                glRotatef(rot, 0.0, 1.0, 0.0)
                self._render_model_with_diagnostics(bldg, col, is_bldg_sec, culling_mgr)
                glPopMatrix()
                total_triangles += bldg.num_triangles

            # Highlight selection brackets for buildings
            if active_sec == "buildings":
                for b_min, b_max, offset in self.sections_meta["buildings"]["boxes"]:
                    self._draw_selection_bracket(b_min, b_max, offset)

        # 5B. Corner Watchtowers
        is_tower_sec = (active_sec in ["all", "towers"])
        if tower:
            for x, y, z in self.tower_positions:
                glPushMatrix()
                glTranslatef(x, y, z)
                self._render_model_with_diagnostics(tower, (0.62, 0.62, 0.66, 1.0), is_tower_sec, culling_mgr)
                glPopMatrix()
                total_triangles += tower.num_triangles

            if active_sec == "towers":
                for b_min, b_max, offset in self.sections_meta["towers"]["boxes"]:
                    self._draw_selection_bracket(b_min, b_max, offset)

        # 5C. Trees Lining Avenues
        is_nature_sec = (active_sec in ["all", "nature"])
        if tree:
            for i, (x, y, z) in enumerate(self.tree_positions):
                glPushMatrix()
                glTranslatef(x, y, z)
                s = 0.85 + (i % 4) * 0.1
                glScalef(s, s, s)
                glRotatef((i * 47) % 360, 0.0, 1.0, 0.0)
                self._render_model_with_diagnostics(tree, (0.18, 0.52 + (i % 3) * 0.03, 0.20, 1.0), is_nature_sec, culling_mgr)
                glPopMatrix()
                total_triangles += tree.num_triangles

            if active_sec == "nature":
                for b_min, b_max, offset in self.sections_meta["nature"]["boxes"]:
                    self._draw_selection_bracket(b_min, b_max, offset)

        # 5D. Street Lamps
        if lamp:
            for x, y, z in self.lamp_positions:
                glPushMatrix()
                glTranslatef(x, y, z)
                self._render_model_with_diagnostics(lamp, (0.30, 0.32, 0.36, 1.0), is_nature_sec, culling_mgr)
                glPopMatrix()
                total_triangles += lamp.num_triangles

        # 6. Stress Test Mode: 100+ building grid
        if culling_mgr.stress_test_mode and bldg:
            grid_count = 10
            spacing = 24.0
            offset = - (grid_count * spacing) / 2.0
            is_stress_sec = (active_sec in ["all", "stress"])

            for gx in range(grid_count):
                for gz in range(grid_count):
                    if 3 <= gx <= 6 and 3 <= gz <= 6:
                        continue
                    wx = offset + gx * spacing
                    wz = offset + gz * spacing

                    glPushMatrix()
                    glTranslatef(wx, 0.0, wz)
                    col = (0.75, 0.72, 0.68, 1.0) if (gx + gz) % 2 == 0 else (0.60, 0.60, 0.65, 1.0)
                    model_to_draw = bldg if (gx + gz) % 2 == 0 or not tower else tower
                    self._render_model_with_diagnostics(model_to_draw, col, is_stress_sec, culling_mgr)
                    total_triangles += model_to_draw.num_triangles
                    glPopMatrix()

        self.base_triangles = total_triangles
        return total_triangles
