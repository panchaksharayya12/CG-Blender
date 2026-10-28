"""
=============================================================================
Beautiful 3D Game Environment Builder for Blender 5.0 & OpenGL
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================

This script generates a visually rich, colorful, and architecturally accurate
3D game environment in Blender 5.0 and saves it as `game_environment.blend`.

Key Fixes & Architectural Improvements:
----------------------------------------
1. Roof Alignment: Custom hip roofs engineered to sit flush on top of building
   walls with precise eaves overhang (no skewed, diamond, or tilted roofs!).
2. Entrance Architecture: Classical porticos with white marble pillars, pediment
   canopy, oak double door, and reflective blue windows all parented cleanly.
3. Town Planning: Buildings arranged around the boulevard, each properly facing
   the central street and plaza.
4. Upright Coniferous Trees: Brown timber trunks and layered pine foliage.
5. Medieval Corner Watchtowers: Tower shafts, observation decks, blue slate spires.
6. Streetlamps with Actual Point Lights: Illuminates streets in Material/Rendered view.
7. Outliner Collections: Scene organized into logical collections for easy inspection.
8. Viewport Shading: Configured to launch immediately in colorful Material Preview!
"""

import os
import math
import bpy


# =============================================================================
# 1. Material Creation Helper
# =============================================================================
def create_mat(name, color, roughness=0.5, metallic=0.0, emission_strength=0.0):
    """
    Creates a material configured for BOTH Solid Mode (diffuse_color)
    and Material Preview / Rendered Mode (Principled BSDF).
    """
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)

    mat.diffuse_color = color

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if emission_strength > 0.0 and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = color
            bsdf.inputs["Emission Strength"].default_value = emission_strength

    mat.use_backface_culling = True
    return mat


def get_or_create_collection(name):
    """Gets an existing collection or creates a new one linked to scene."""
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


# =============================================================================
# 2. Main Scene Construction
# =============================================================================
def build_environment():
    print("[BLENDER BUILDER] Rebuilding environment with properly arranged architecture...")

    # Clear current scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # -------------------------------------------------------------------------
    # Material Library
    # -------------------------------------------------------------------------
    # Ground & Roads
    mat_grass_a  = create_mat("Mat_Grass_Dark",     (0.20, 0.58, 0.22, 1.0), roughness=0.85)
    mat_grass_b  = create_mat("Mat_Grass_Light",    (0.28, 0.68, 0.28, 1.0), roughness=0.85)
    mat_road     = create_mat("Mat_Road_Asphalt",   (0.22, 0.22, 0.25, 1.0), roughness=0.6)
    mat_stripe   = create_mat("Mat_Road_Stripe",    (0.95, 0.82, 0.15, 1.0), roughness=0.4)
    mat_plaza    = create_mat("Mat_Plaza_Cobble",   (0.50, 0.48, 0.46, 1.0), roughness=0.7)

    # Walls & Fortifications
    mat_wall     = create_mat("Mat_Stone_Wall",     (0.55, 0.52, 0.48, 1.0), roughness=0.8)
    mat_wall_cap = create_mat("Mat_Wall_Cap",       (0.72, 0.69, 0.64, 1.0), roughness=0.6)

    # Buildings & Architecture
    mat_bldg_cream = create_mat("Mat_Bldg_Cream",   (0.92, 0.88, 0.78, 1.0), roughness=0.6)
    mat_bldg_sand  = create_mat("Mat_Bldg_Sand",    (0.85, 0.78, 0.66, 1.0), roughness=0.6)
    mat_bldg_brick = create_mat("Mat_Bldg_Brick",   (0.75, 0.45, 0.38, 1.0), roughness=0.7)
    mat_roof_red   = create_mat("Mat_Roof_Red",     (0.82, 0.26, 0.18, 1.0), roughness=0.5)
    mat_roof_slate = create_mat("Mat_Roof_Slate",   (0.26, 0.36, 0.50, 1.0), roughness=0.5)
    mat_window     = create_mat("Mat_Window_Glass", (0.18, 0.45, 0.72, 1.0), roughness=0.1, metallic=0.3)
    mat_wood_door  = create_mat("Mat_Wood_Door",    (0.38, 0.22, 0.12, 1.0), roughness=0.7)
    mat_pillar     = create_mat("Mat_Pillar_Marble",(0.95, 0.95, 0.98, 1.0), roughness=0.3)

    # Watchtower
    mat_tower_stone = create_mat("Mat_Tower_Stone", (0.52, 0.52, 0.56, 1.0), roughness=0.8)
    mat_tower_wood  = create_mat("Mat_Tower_Wood",  (0.42, 0.26, 0.16, 1.0), roughness=0.7)
    mat_tower_spire = create_mat("Mat_Tower_Spire", (0.24, 0.34, 0.54, 1.0), roughness=0.4)

    # Trees
    mat_trunk       = create_mat("Mat_Tree_Trunk",   (0.36, 0.20, 0.10, 1.0), roughness=0.9)
    mat_leaves_dark = create_mat("Mat_Leaves_Dark",  (0.12, 0.48, 0.18, 1.0), roughness=0.7)
    mat_leaves_light= create_mat("Mat_Leaves_Light", (0.18, 0.62, 0.24, 1.0), roughness=0.7)

    # Streetlamps & Glowing Fixtures
    mat_lamp_iron   = create_mat("Mat_Lamp_Iron",    (0.18, 0.18, 0.20, 1.0), roughness=0.4, metallic=0.6)
    mat_lamp_glow   = create_mat("Mat_Lamp_Glow",    (1.00, 0.90, 0.40, 1.0), roughness=0.2, emission_strength=4.0)

    # Inside-Out Inspection Chamber & Beacon
    mat_chamber     = create_mat("Mat_Chamber_Red",  (0.85, 0.28, 0.22, 1.0), roughness=0.5)
    mat_beacon      = create_mat("Mat_Beacon_Gold",  (1.00, 0.85, 0.15, 1.0), roughness=0.2, emission_strength=5.0)

    # Central Plaza Fountain
    mat_water       = create_mat("Mat_Water_Azure",  (0.15, 0.60, 0.85, 1.0), roughness=0.1, metallic=0.1)

    # Setup Collections
    col_terrain  = get_or_create_collection("Terrain & Roads")
    col_walls    = get_or_create_collection("Fortress Walls")
    col_bldgs    = get_or_create_collection("Town Buildings")
    col_towers   = get_or_create_collection("Watchtowers")
    col_nature   = get_or_create_collection("Trees & Nature")
    col_lamps    = get_or_create_collection("Street Lamps")
    col_monument = get_or_create_collection("Plaza & Monument")
    col_chamber  = get_or_create_collection("Inside-Out Chamber")
    col_lighting = get_or_create_collection("Lighting & Camera")

    # -------------------------------------------------------------------------
    # 3. Terrain, Checkered Lawns & Roadways
    # -------------------------------------------------------------------------
    grid_range = 60
    tile_size = 6

    for gx in range(-grid_range, grid_range, tile_size):
        for gz in range(-grid_range, grid_range, tile_size):
            cx = gx + tile_size / 2.0
            cy = gz + tile_size / 2.0

            in_plaza = (-15 <= cx <= 15) and (-15 <= cy <= 15)
            is_road_x = (-4.0 <= cy <= 4.0)
            is_road_y = (-4.0 <= cx <= 4.0)

            if in_plaza:
                chosen_mat = mat_plaza
            elif is_road_x or is_road_y:
                chosen_mat = mat_road
            else:
                checker = ((gx + gz) // tile_size) % 2 == 0
                chosen_mat = mat_grass_a if checker else mat_grass_b

            bpy.ops.mesh.primitive_plane_add(size=tile_size, location=(cx, cy, 0.0))
            tile = bpy.context.active_object
            tile.name = f"Ground_{gx}_{gz}"
            tile.data.materials.append(chosen_mat)
            col_terrain.objects.link(tile)
            bpy.context.collection.objects.unlink(tile)

    # Road Centerline Stripes
    for sx in range(-54, 55, 6):
        if -15 <= sx <= 15:
            continue
        bpy.ops.mesh.primitive_plane_add(size=1.0, location=(sx, 0.0, 0.02))
        stripe = bpy.context.active_object
        stripe.scale = (3.5, 0.35, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        stripe.data.materials.append(mat_stripe)
        col_terrain.objects.link(stripe)
        bpy.context.collection.objects.unlink(stripe)

    for sy in range(-54, 55, 6):
        if -15 <= sy <= 15:
            continue
        bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, sy, 0.02))
        stripe = bpy.context.active_object
        stripe.scale = (0.35, 3.5, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        stripe.data.materials.append(mat_stripe)
        col_terrain.objects.link(stripe)
        bpy.context.collection.objects.unlink(stripe)

    # -------------------------------------------------------------------------
    # 4. Perimeter Fortress Walls & Defensive Battlement Caps
    # -------------------------------------------------------------------------
    for y_pos in [-56.0, 56.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_pos, 3.0))
        w = bpy.context.active_object
        w.name = f"Wall_H_{int(y_pos)}"
        w.scale = (112.0, 2.5, 6.0)
        bpy.ops.object.transform_apply(scale=True)
        w.data.materials.append(mat_wall)
        col_walls.objects.link(w)
        bpy.context.collection.objects.unlink(w)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_pos, 6.3))
        wc = bpy.context.active_object
        wc.scale = (114.0, 3.2, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        wc.data.materials.append(mat_wall_cap)
        col_walls.objects.link(wc)
        bpy.context.collection.objects.unlink(wc)

    for x_pos in [-56.0, 56.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, 3.0))
        w = bpy.context.active_object
        w.name = f"Wall_V_{int(x_pos)}"
        w.scale = (2.5, 112.0, 6.0)
        bpy.ops.object.transform_apply(scale=True)
        w.data.materials.append(mat_wall)
        col_walls.objects.link(w)
        bpy.context.collection.objects.unlink(w)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, 6.3))
        wc = bpy.context.active_object
        wc.scale = (3.2, 114.0, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        wc.data.materials.append(mat_wall_cap)
        col_walls.objects.link(wc)
        bpy.context.collection.objects.unlink(wc)

    # -------------------------------------------------------------------------
    # 5. ARCHITECTURALLY ACCURATE TOWN BUILDINGS
    # -------------------------------------------------------------------------
    def build_proper_building(b_id, world_x, world_y, rot_deg, body_mat, roof_mat):
        """
        Creates an architecturally aligned building with:
        - Foundation base (10.6 x 8.6 x 0.8)
        - Main body (10.0 x 8.0 x 7.0)
        - Flush hip roof (slopes matching width and depth, 0.4m eaves overhang)
        - Classical front entrance portico (marble columns, canopy, oak door)
        - Symmetrical windows
        All components are cleanly parented and rotated as a single unit!
        """
        # Root Empty to control position and rotation
        root = bpy.data.objects.new(f"Building_{b_id}_Root", None)
        root.location = (world_x, world_y, 0.0)
        root.rotation_euler.z = math.radians(rot_deg)
        col_bldgs.objects.link(root)

        parts = []

        # 1. Base Foundation
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.4))
        base = bpy.context.active_object
        base.name = f"Bldg_{b_id}_Base"
        base.scale = (10.6, 8.6, 0.8)
        bpy.ops.object.transform_apply(scale=True)
        base.data.materials.append(mat_wall_cap)
        parts.append(base)

        # 2. Main Wall Body
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 4.3))
        body = bpy.context.active_object
        body.name = f"Bldg_{b_id}_Body"
        body.scale = (10.0, 8.0, 7.0)
        bpy.ops.object.transform_apply(scale=True)
        body.data.materials.append(body_mat)
        parts.append(body)

        # 3. Mid-Floor Cornice Molding
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 4.5))
        molding = bpy.context.active_object
        molding.scale = (10.4, 8.4, 0.35)
        bpy.ops.object.transform_apply(scale=True)
        molding.data.materials.append(mat_wall_cap)
        parts.append(molding)

        # 4. Eaves Wall Crown
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 7.8))
        crown = bpy.context.active_object
        crown.scale = (10.5, 8.5, 0.3)
        bpy.ops.object.transform_apply(scale=True)
        crown.data.materials.append(mat_wall_cap)
        parts.append(crown)

        # 5. Flush Hip Roof (Engineered specifically to fit 10.0 x 8.0 walls!)
        # Base rectangle sits on Z = 7.8, eaves extend to 5.4 along X and 4.4 along Y
        roof_verts = [
            (-5.4, -4.4, 7.8),  # 0: Front-Left
            ( 5.4, -4.4, 7.8),  # 1: Front-Right
            ( 5.4,  4.4, 7.8),  # 2: Back-Right
            (-5.4,  4.4, 7.8),  # 3: Back-Left
            (-2.5,  0.0, 11.0), # 4: Ridge-Left
            ( 2.5,  0.0, 11.0), # 5: Ridge-Right
        ]
        roof_faces = [
            (0, 1, 5, 4),  # Front slope
            (1, 2, 5),     # Right slope
            (2, 3, 4, 5),  # Back slope
            (3, 0, 4),     # Left slope
            (0, 3, 2, 1),  # Bottom ceiling
        ]
        roof_mesh = bpy.data.meshes.new(f"Bldg_{b_id}_RoofMesh")
        roof_mesh.from_pydata(roof_verts, [], roof_faces)
        roof_mesh.update()
        roof = bpy.data.objects.new(f"Bldg_{b_id}_Roof", roof_mesh)
        col_bldgs.objects.link(roof)
        roof.data.materials.append(roof_mat)

        # Ensure CCW outward normals on roof
        bpy.context.view_layer.objects.active = roof
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.object.mode_set(mode='OBJECT')
        parts.append(roof)

        # 6. Front Entrance Portico (Facing local -Y)
        # Wooden Oak Double Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -4.05, 2.2))
        door = bpy.context.active_object
        door.scale = (1.8, 0.15, 2.8)
        bpy.ops.object.transform_apply(scale=True)
        door.data.materials.append(mat_wood_door)
        parts.append(door)

        # Marble Columns flanking entrance
        for col_x in [-2.0, 2.0]:
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=12, radius=0.32, depth=3.0, location=(col_x, -5.2, 2.3)
            )
            pillar = bpy.context.active_object
            pillar.data.materials.append(mat_pillar)
            parts.append(pillar)

        # Canopy Slab
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -4.7, 3.9))
        canopy = bpy.context.active_object
        canopy.scale = (5.2, 1.8, 0.3)
        bpy.ops.object.transform_apply(scale=True)
        canopy.data.materials.append(mat_wall_cap)
        parts.append(canopy)

        # Sloped Canopy Cap
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -4.7, 4.2))
        canopy_cap = bpy.context.active_object
        canopy_cap.scale = (5.0, 1.6, 0.3)
        bpy.ops.object.transform_apply(scale=True)
        canopy_cap.data.materials.append(roof_mat)
        parts.append(canopy_cap)

        # 7. Symmetrical Windows (Front & Side Facades)
        # Front Facade Windows (Y = -4.05)
        front_windows = [
            (-3.2, -4.05, 2.5), (3.2, -4.05, 2.5),  # Floor 1
            (-3.2, -4.05, 5.8), (0.0, -4.05, 5.8), (3.2, -4.05, 5.8),  # Floor 2
        ]
        for wx, wy, wz in front_windows:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, wy, wz))
            win = bpy.context.active_object
            win.scale = (1.4, 0.15, 1.6)
            bpy.ops.object.transform_apply(scale=True)
            win.data.materials.append(mat_window)
            parts.append(win)

        # Side Facade Windows (X = -5.05 and +5.05)
        side_windows = [
            (-5.05, 0.0, 2.5), (-5.05, -1.8, 5.8), (-5.05, 1.8, 5.8),
            ( 5.05, 0.0, 2.5), ( 5.05, -1.8, 5.8), ( 5.05, 1.8, 5.8),
        ]
        for wx, wy, wz in side_windows:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, wy, wz))
            win = bpy.context.active_object
            win.scale = (0.15, 1.4, 1.6)
            bpy.ops.object.transform_apply(scale=True)
            win.data.materials.append(mat_window)
            parts.append(win)

        # Link all parts into the collection and parent them to root
        for p in parts:
            if p.name not in col_bldgs.objects:
                col_bldgs.objects.link(p)
            if p.name in bpy.context.collection.objects:
                bpy.context.collection.objects.unlink(p)
            p.parent = root

        print(f"[BLENDER BUILDER] Building {b_id} created successfully with properly aligned roof!")

    # -------------------------------------------------------------------------
    # Layout Planning: Buildings facing the central avenues and plaza
    # -------------------------------------------------------------------------
    # Entrance is along local -Y.
    # To face North (+Y in world): rot_deg = 180
    # To face South (-Y in world): rot_deg = 0
    # To face East  (+X in world): rot_deg = 90
    # To face West  (-X in world): rot_deg = 270 (or -90)
    building_placements = [
        # (id, world_x, world_y, rot_deg, body_mat, roof_mat)
        (1,  22.0, -20.0, 270.0, mat_bldg_cream, mat_roof_red),    # SE Corner, faces West toward main avenue
        (2, -22.0, -20.0,  90.0, mat_bldg_sand,  mat_roof_slate),  # SW Corner, faces East toward main avenue
        (3,  22.0,  20.0, 270.0, mat_bldg_brick, mat_roof_red),    # NE Corner, faces West toward main avenue
        (4, -22.0,  20.0,  90.0, mat_bldg_cream, mat_roof_slate),  # NW Corner, faces East toward main avenue
        (5,  38.0,   0.0, 270.0, mat_bldg_sand,  mat_roof_red),    # East Grand Estate, faces West toward plaza
        (6, -38.0,   0.0,  90.0, mat_bldg_brick, mat_roof_red),    # West Manor, faces East toward plaza
    ]
    for b_id, wx, wy, r_deg, b_mat, r_mat in building_placements:
        build_proper_building(b_id, wx, wy, r_deg, b_mat, r_mat)

    # -------------------------------------------------------------------------
    # 6. Medieval Corner Watchtowers
    # -------------------------------------------------------------------------
    def build_watchtower(t_id, x, y):
        root = bpy.data.objects.new(f"Watchtower_{t_id}_Root", None)
        root.location = (x, y, 0.0)
        col_towers.objects.link(root)

        # 1. Octagonal stone tower shaft
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=3.2, depth=11.0, location=(0.0, 0.0, 5.5))
        shaft = bpy.context.active_object
        shaft.name = f"Tower_{t_id}_Shaft"
        shaft.data.materials.append(mat_tower_stone)

        # 2. Observation deck rim
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=4.2, depth=1.6, location=(0.0, 0.0, 11.5))
        rim = bpy.context.active_object
        rim.name = f"Tower_{t_id}_Rim"
        rim.data.materials.append(mat_tower_wood)

        # 3. Conical roof spire (royal blue slate)
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=4.4, depth=5.5, location=(0.0, 0.0, 14.8))
        spire = bpy.context.active_object
        spire.name = f"Tower_{t_id}_Spire"
        spire.data.materials.append(mat_tower_spire)

        # 4. Golden pinnacle spire ball
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45, location=(0.0, 0.0, 17.8))
        ball = bpy.context.active_object
        ball.data.materials.append(mat_beacon)

        for obj in [shaft, rim, spire, ball]:
            col_towers.objects.link(obj)
            bpy.context.collection.objects.unlink(obj)
            obj.parent = root

    tower_coords = [(-48.0, -48.0), (48.0, -48.0), (-48.0, 48.0), (48.0, 48.0)]
    for i, (tx, ty) in enumerate(tower_coords):
        build_watchtower(i + 1, tx, ty)

    # -------------------------------------------------------------------------
    # 7. Upright Coniferous Pine Trees
    # -------------------------------------------------------------------------
    def spawn_tree(tree_id, x, y, scale=1.0):
        root = bpy.data.objects.new(f"Tree_{tree_id}_Root", None)
        root.location = (x, y, 0.0)
        col_nature.objects.link(root)

        # Trunk (standing upright along Z)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=0.4 * scale, depth=2.8 * scale, location=(0.0, 0.0, 1.4 * scale)
        )
        trunk = bpy.context.active_object
        trunk.name = f"Tree_{tree_id}_Trunk"
        trunk.data.materials.append(mat_trunk)

        # Tiered foliage
        tiers = [
            (2.8 * scale, 3.0 * scale, 3.4 * scale, mat_leaves_dark),
            (2.2 * scale, 2.5 * scale, 5.2 * scale, mat_leaves_light),
            (1.5 * scale, 2.0 * scale, 6.8 * scale, mat_leaves_dark),
        ]
        parts = [trunk]
        for idx, (r, h, z, f_mat) in enumerate(tiers):
            bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=r, depth=h, location=(0.0, 0.0, z))
            tier = bpy.context.active_object
            tier.name = f"Tree_{tree_id}_Tier_{idx+1}"
            tier.data.materials.append(f_mat)
            parts.append(tier)

        for p in parts:
            col_nature.objects.link(p)
            bpy.context.collection.objects.unlink(p)
            p.parent = root

    tree_coords = [
        (-10.0, -10.0), (-10.0, -22.0), (-10.0, 10.0), (-10.0, 22.0),
        ( 10.0, -10.0), ( 10.0, -22.0), ( 10.0, 10.0), ( 10.0, 22.0),
        (-30.0, -35.0), (-38.0, -26.0), ( 32.0, 32.0), ( 40.0, 25.0),
        (  0.0, -38.0), (  0.0,  38.0)
    ]
    for i, (tx, ty) in enumerate(tree_coords):
        s = 0.9 + (i % 4) * 0.12
        spawn_tree(i + 1, tx, ty, scale=s)

    # -------------------------------------------------------------------------
    # 8. Street Lamps with Glowing Lanterns & Point Lights
    # -------------------------------------------------------------------------
    def spawn_lamp(lamp_id, x, y):
        root = bpy.data.objects.new(f"Lamp_{lamp_id}_Root", None)
        root.location = (x, y, 0.0)
        col_lamps.objects.link(root)

        # Pedestal
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.4))
        base = bpy.context.active_object
        base.scale = (0.8, 0.8, 0.8)
        bpy.ops.object.transform_apply(scale=True)
        base.data.materials.append(mat_lamp_iron)

        # Post
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.15, depth=4.6, location=(0.0, 0.0, 2.9))
        post = bpy.context.active_object
        post.data.materials.append(mat_lamp_iron)

        # Lantern cage
        bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0.0, 0.0, 5.3))
        cage = bpy.context.active_object
        cage.data.materials.append(mat_lamp_glow)

        # Lantern cap
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.7, depth=0.45, location=(0.0, 0.0, 5.85))
        cap = bpy.context.active_object
        cap.data.materials.append(mat_lamp_iron)

        # Point Light inside lantern
        bpy.ops.object.light_add(type='POINT', location=(0.0, 0.0, 5.3))
        pt = bpy.context.active_object
        pt.name = f"LampLight_{lamp_id}"
        pt.data.energy = 40.0
        pt.data.color = (1.0, 0.88, 0.55)

        for obj in [base, post, cage, cap, pt]:
            col_lamps.objects.link(obj)
            bpy.context.collection.objects.unlink(obj)
            obj.parent = root

    lamp_coords = [
        (-6.0, -12.0), (-6.0, 12.0),
        ( 6.0, -12.0), ( 6.0, 12.0),
        (-12.0, -6.0), ( 12.0, -6.0),
        (-12.0,  6.0), ( 12.0,  6.0),
    ]
    for i, (lx, ly) in enumerate(lamp_coords):
        spawn_lamp(i + 1, lx, ly)

    # -------------------------------------------------------------------------
    # 9. Central Plaza Monument & Fountain
    # -------------------------------------------------------------------------
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=5.0, depth=0.8, location=(0.0, 0.0, 0.4))
    basin = bpy.context.active_object
    basin.data.materials.append(mat_wall_cap)
    col_monument.objects.link(basin)
    bpy.context.collection.objects.unlink(basin)

    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=4.4, depth=0.6, location=(0.0, 0.0, 0.45))
    water = bpy.context.active_object
    water.data.materials.append(mat_water)
    col_monument.objects.link(water)
    bpy.context.collection.objects.unlink(water)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 2.5))
    monolith = bpy.context.active_object
    monolith.name = "Plaza_Monolith"
    monolith.scale = (1.4, 1.4, 3.8)
    bpy.ops.object.transform_apply(scale=True)
    monolith.data.materials.append(mat_pillar)
    col_monument.objects.link(monolith)
    bpy.context.collection.objects.unlink(monolith)

    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.9, depth=1.8, location=(0.0, 0.0, 5.0))
    crystal_top = bpy.context.active_object
    crystal_top.data.materials.append(mat_beacon)
    col_monument.objects.link(crystal_top)
    bpy.context.collection.objects.unlink(crystal_top)

    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.9, depth=1.8, location=(0.0, 0.0, 4.2))
    crystal_bot = bpy.context.active_object
    crystal_bot.rotation_euler.x = math.radians(180.0)
    crystal_bot.data.materials.append(mat_beacon)
    col_monument.objects.link(crystal_bot)
    bpy.context.collection.objects.unlink(crystal_bot)

    # -------------------------------------------------------------------------
    # 10. Educational Inside-Out Demonstration Chamber
    # -------------------------------------------------------------------------
    chamber_cx = -26.0
    chamber_cy = -15.0

    chamber_walls = [
        (chamber_cx, chamber_cy - 5.0, 4.0, 10.0, 0.8, 8.0),
        (chamber_cx - 5.0, chamber_cy, 4.0, 0.8, 10.0, 8.0),
        (chamber_cx + 5.0, chamber_cy, 4.0, 0.8, 10.0, 8.0),
        (chamber_cx, chamber_cy, 8.0, 10.0, 10.0, 0.8),
        (chamber_cx - 3.2, chamber_cy + 5.0, 4.0, 3.6, 0.8, 8.0),
        (chamber_cx + 3.2, chamber_cy + 5.0, 4.0, 3.6, 0.8, 8.0),
        (chamber_cx, chamber_cy + 5.0, 6.5, 2.8, 0.8, 3.0),
    ]
    for idx, (cx, cy, cz, sx, sy, sz) in enumerate(chamber_walls):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
        cw = bpy.context.active_object
        cw.name = f"Chamber_Wall_{idx+1}"
        cw.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(scale=True)
        cw.data.materials.append(mat_chamber)
        col_chamber.objects.link(cw)
        bpy.context.collection.objects.unlink(cw)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.9, location=(chamber_cx, chamber_cy, 10.0))
    beacon = bpy.context.active_object
    beacon.name = "Chamber_Beacon_Sphere"
    beacon.data.materials.append(mat_beacon)
    col_chamber.objects.link(beacon)
    bpy.context.collection.objects.unlink(beacon)

    # -------------------------------------------------------------------------
    # 11. Sun Light & Camera Setup
    # -------------------------------------------------------------------------
    bpy.ops.object.light_add(type='SUN', location=(30.0, -40.0, 60.0))
    sun = bpy.context.active_object
    sun.name = "Sun_Daylight"
    sun.data.energy = 4.5
    sun.data.color = (1.0, 0.96, 0.88)
    sun.rotation_euler = (math.radians(50.0), math.radians(15.0), math.radians(-35.0))
    col_lighting.objects.link(sun)
    bpy.context.collection.objects.unlink(sun)

    bpy.ops.object.camera_add(location=(0.0, -25.0, 4.0))
    cam = bpy.context.active_object
    cam.name = "Player_Camera"
    cam.rotation_euler = (math.radians(85.0), 0.0, 0.0)
    cam.data.lens = 32.0
    bpy.context.scene.camera = cam
    col_lighting.objects.link(cam)
    bpy.context.collection.objects.unlink(cam)

    # Sky background
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("World")
    world = bpy.context.scene.world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = (0.55, 0.72, 0.95, 1.0)
        bg_node.inputs["Strength"].default_value = 1.0

    # -------------------------------------------------------------------------
    # 12. Configure Viewport Shading to Material Preview
    # -------------------------------------------------------------------------
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    try:
                        space.shading.type = 'MATERIAL'
                    except Exception:
                        pass
                    try:
                        space.shading.color_type = 'MATERIAL'
                    except Exception:
                        pass
                    try:
                        space.shading.show_backface_culling = True
                    except Exception:
                        pass

    # Save to game_environment.blend
    blend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "game_environment.blend"))
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"\n[BLENDER BUILDER] COMPLETE! Scene rebuilt and saved cleanly to: {blend_path}\n")


if __name__ == "__main__":
    build_environment()
