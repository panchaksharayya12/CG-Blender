"""
=============================================================================
Wavefront (.obj) 3D Model Loader
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================

This module parses standard Wavefront OBJ files exported from 3D modeling
software like Blender 5.0 and compiles them into high-performance OpenGL
Display Lists.

Preserving Winding Order:
-------------------------
Back-Face Culling strictly relies on Counter-Clockwise (CCW) face vertex ordering.
This loader ensures that triangular and quadrilateral faces maintain their CCW
winding order so that OpenGL correctly distinguishes front faces from back faces.
"""

import os
import math
from OpenGL.GL import (
    glGenLists, glNewList, glEndList, glCallList,
    GL_COMPILE, glBegin, glEnd, GL_TRIANGLES,
    glVertex3f, glNormal3f, glColor4f,
    glMaterialfv, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, GL_SPECULAR, GL_SHININESS
)


class OBJModel:
    """
    Loads, parses, and caches a 3D Wavefront OBJ model for OpenGL rendering.
    """

    def __init__(self, filepath, default_color=(0.8, 0.8, 0.8, 1.0)):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.default_color = default_color
        self.display_list = None
        self.num_triangles = 0

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []  # List of tuples: [(v_idx, vt_idx, vn_idx), ...]

        self.load(filepath)
        self.compile_display_list()

    def load(self, filepath):
        """Parses the .obj file and extracts vertices, normals, and face indices."""
        if not os.path.exists(filepath):
            print(f"[OBJ LOADER] Warning: File not found: {filepath}. Generating fallback geometry.")
            self._generate_fallback_cube()
            return

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    tokens = line.split()
                    prefix = tokens[0]

                    if prefix == "v":
                        # Geometric Vertex: v x y z
                        self.vertices.append([float(tokens[1]), float(tokens[2]), float(tokens[3])])
                    elif prefix == "vn":
                        # Vertex Normal: vn x y z
                        self.normals.append([float(tokens[1]), float(tokens[2]), float(tokens[3])])
                    elif prefix == "vt":
                        # Texture Coordinate: vt u v
                        self.texcoords.append([float(tokens[1]), float(tokens[2])])
                    elif prefix == "f":
                        # Polygon Face: f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3 ...
                        face_vertices = []
                        for token in tokens[1:]:
                            indices = token.split("/")
                            v_idx = int(indices[0]) - 1 if indices[0] else None
                            vt_idx = int(indices[1]) - 1 if len(indices) > 1 and indices[1] else None
                            vn_idx = int(indices[2]) - 1 if len(indices) > 2 and indices[2] else None
                            face_vertices.append((v_idx, vt_idx, vn_idx))

                        # Fan triangulation to support both triangles and quads while preserving CCW winding
                        for i in range(1, len(face_vertices) - 1):
                            self.faces.append((face_vertices[0], face_vertices[i], face_vertices[i + 1]))
                            self.num_triangles += 1

            print(f"[OBJ LOADER] Loaded '{self.filename}': {len(self.vertices)} vertices, {self.num_triangles} triangles.")
        except Exception as e:
            print(f"[OBJ LOADER] Error loading {filepath}: {e}. Using fallback geometry.")
            self._generate_fallback_cube()

    def _generate_fallback_cube(self):
        """Creates a unit cube if an OBJ file fails to load."""
        self.vertices = [
            [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1],
            [-1, -1, -1], [-1,  1, -1], [ 1,  1, -1], [ 1, -1, -1]
        ]
        self.normals = [
            [ 0,  0,  1], [ 0,  0, -1], [-1,  0,  0],
            [ 1,  0,  0], [ 0,  1,  0], [ 0, -1,  0]
        ]
        # CCW winding faces
        quads = [
            ([0, 1, 2, 3], 0),  # Front
            ([7, 4, 5, 6], 1),  # Back
            ([4, 0, 3, 5], 2),  # Left
            ([1, 7, 6, 2], 3),  # Right
            ([3, 2, 6, 5], 4),  # Top
            ([4, 7, 1, 0], 5),  # Bottom
        ]
        for q, n_idx in quads:
            v0, v1, v2, v3 = q
            self.faces.append(((v0, None, n_idx), (v1, None, n_idx), (v2, None, n_idx)))
            self.faces.append(((v0, None, n_idx), (v2, None, n_idx), (v3, None, n_idx)))
            self.num_triangles += 2

    def compile_display_list(self):
        """
        Compiles the parsed mesh into an OpenGL Display List.
        This provides maximum hardware performance and minimizes Python-to-C overhead.
        """
        self.display_list = glGenLists(1)
        glNewList(self.display_list, GL_COMPILE)
        glBegin(GL_TRIANGLES)

        for tri in self.faces:
            # Each triangle consists of 3 vertices (CCW winding)
            # If vertex normals are missing, calculate face normal using cross product
            face_normal = None
            if tri[0][2] is None or tri[0][2] >= len(self.normals):
                v0 = self.vertices[tri[0][0]]
                v1 = self.vertices[tri[1][0]]
                v2 = self.vertices[tri[2][0]]
                face_normal = self._calculate_normal(v0, v1, v2)

            for vertex_data in tri:
                v_idx, _, vn_idx = vertex_data

                # Normal vector
                if vn_idx is not None and vn_idx < len(self.normals):
                    norm = self.normals[vn_idx]
                    glNormal3f(norm[0], norm[1], norm[2])
                elif face_normal is not None:
                    glNormal3f(face_normal[0], face_normal[1], face_normal[2])

                # Position vertex
                vert = self.vertices[v_idx]
                glVertex3f(vert[0], vert[1], vert[2])

        glEnd()
        glEndList()

    @staticmethod
    def _calculate_normal(v0, v1, v2):
        """
        Calculates the unit surface normal via cross product of edges:
        Edge1 = V1 - V0,  Edge2 = V2 - V0,  Normal = Edge1 x Edge2
        """
        ax, ay, az = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
        bx, by, bz = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]

        nx = ay * bz - az * by
        ny = az * bx - ax * bz
        nz = ax * by - ay * bx

        length = math.sqrt(nx * nx + ny * ny + nz * nz)
        if length > 0.00001:
            return (nx / length, ny / length, nz / length)
        return (0.0, 1.0, 0.0)

    def render(self, color=None):
        """Executes the pre-compiled OpenGL Display List with material settings."""
        mat_color = color if color is not None else self.default_color
        glColor4f(*mat_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, mat_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.3, 0.3, 0.3, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 32.0)

        if self.display_list:
            glCallList(self.display_list)
