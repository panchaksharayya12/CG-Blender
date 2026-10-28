"""
=============================================================================
Blender Complete Scene Builder
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================

This script constructs the ENTIRE 3D game environment directly inside Blender 5.0:
- Ground terrain & checkered plaza road network
- Perimeter stone fortress walls & battlements
- Blender-imported classical buildings, watchtowers, trees, and streetlamps
- Educational Inside-Out Demonstration Chamber with doorway and glowing beacon
- Central plaza monument / showcase cubes
- Sun lighting & environment illumination
- Player Camera positioned at starting coordinates
- Materials configured with native Blender Backface Culling enabled!

Saves the complete scene as `game_environment.blend`.
"""

import os
import math
import bpy


def make_material(name, color, roughness=0.5, use_backface_culling=True):
    """Creates a Principled BSDF material with backface culling enabled."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness

    # Enable native Blender Backface Culling on the material
    mat.use_backface_culling = use_backface_culling
    return mat


def build_full_scene():
    print("[BLENDER BUILDER] Building complete 3D game environment...")

    # 1. Clear everything
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 2. Materials
    mat_grass_a = make_material("Mat_Grass_A", (0.22, 0.45, 0.22, 1.0), roughness=0.8)
    mat_grass_b = make_material("Mat_Grass_B", (0.28, 0.52, 0.28, 1.0), roughness=0.8)
    mat_road    = make_material("Mat_Road", (0.25, 0.25, 0.28, 1.0), roughness=0.6)
    mat_wall    = make_material("Mat_Wall", (0.58, 0.55, 0.52, 1.0), roughness=0.7)
    mat_wallcap = make_material("Mat_WallCap", (0.70, 0.67, 0.63, 1.0), roughness=0.6)
    mat_chamber = make_material("Mat_Chamber", (0.85, 0.35, 0.25, 1.0), roughness=0.4)
    mat_beacon  = make_material("Mat_Beacon", (0.95, 0.85, 0.20, 1.0), roughness=0.2)
    mat_core    = make_material("Mat_PlazaCore", (0.20, 0.70, 0.90, 1.0), roughness=0.3)
    mat_gold    = make_material("Mat_PlazaGold", (0.90, 0.80, 0.20, 1.0), roughness=0.2)

    # 3. Ground Grid (Checkered terrain & roads)
    grid_range = 60
    tile_size = 6
    for gx in range(-grid_range, grid_range, tile_size):
        for gz in range(-grid_range, grid_range, tile_size):
            is_road = (-9 <= gx <= 9) or (-9 <= gz <= 9)
            if is_road:
                chosen_mat = mat_road
            else:
                checker = ((gx + gz) // tile_size) % 2 == 0
                chosen_mat = mat_grass_a if checker else mat_grass_b

            # Create plane tile (OpenGL Z maps to Blender Y)
            bpy.ops.mesh.primitive_plane_add(
                size=tile_size,
                location=(gx + tile_size / 2.0, gz + tile_size / 2.0, 0.0)
            )
            tile = bpy.context.active_object
            tile.name = f"Tile_{gx}_{gz}"
            tile.data.materials.append(chosen_mat)

    # 4. Perimeter Defensive Walls
    # North & South walls
    for y_pos in [-55.0, 55.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_pos, 3.0))
        w = bpy.context.active_object
        w.scale = (104.0, 2.4, 6.0)
        bpy.ops.object.transform_apply(scale=True)
        w.data.materials.append(mat_wall)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_pos, 6.3))
        wc = bpy.context.active_object
        wc.scale = (106.0, 3.0, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        wc.data.materials.append(mat_wallcap)

    # East & West walls
    for x_pos in [-55.0, 55.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, 3.0))
        w = bpy.context.active_object
        w.scale = (2.4, 104.0, 6.0)
        bpy.ops.object.transform_apply(scale=True)
        w.data.materials.append(mat_wall)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, 6.3))
        wc = bpy.context.active_object
        wc.scale = (3.0, 106.0, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        wc.data.materials.append(mat_wallcap)

    # 5. Inside-Out Educational Chamber (Enclosed room at x=-25, y=-15)
    # Normals point outward, so inside it, faces are back-facing!
    chamber_parts = [
        # (x, y, z, sx, sy, sz)
        (-25.0, -20.0, 4.0, 10.0, 0.8, 8.0),   # Back wall
        (-30.0, -15.0, 4.0, 0.8, 10.0, 8.0),   # Left wall
        (-20.0, -15.0, 4.0, 0.8, 10.0, 8.0),   # Right wall
        (-25.0, -15.0, 8.0, 10.0, 10.0, 0.8),  # Ceiling
        (-28.0, -10.0, 4.0, 4.0, 0.8, 8.0),    # Front doorway left
        (-22.0, -10.0, 4.0, 4.0, 0.8, 8.0),    # Front doorway right
        (-25.0, -10.0, 6.5, 2.0, 0.8, 3.0),    # Front doorway lintel
    ]
    for x, y, z, sx, sy, sz in chamber_parts:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z))
        part = bpy.context.active_object
        part.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(scale=True)
        part.data.materials.append(mat_chamber)

    # Floating Yellow Beacon over chamber
    bpy.ops.mesh.primitive_cube_add(size=1.6, location=(-25.0, -15.0, 9.5))
    beacon = bpy.context.active_object
    beacon.data.materials.append(mat_beacon)

    # 6. Central Plaza Monument (Rotating Cube Showcase)
    bpy.ops.mesh.primitive_cube_add(size=3.6, location=(0.0, 0.0, 3.5))
    monolith = bpy.context.active_object
    monolith.name = "Plaza_Monolith"
    monolith.data.materials.append(mat_core)

    bpy.ops.mesh.primitive_cube_add(size=1.8, location=(0.0, 0.0, 3.5))
    inner = bpy.context.active_object
    inner.name = "Plaza_InnerCore"
    inner.data.materials.append(mat_gold)

    # 7. Import Blender Models & Place Them
    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "models"))

    def load_model(filename):
        path = os.path.join(models_dir, filename)
        bpy.ops.wm.obj_import(filepath=path)
        obj = bpy.context.active_object
        return obj

    # Template objects
    bldg_tpl  = load_model("building.obj")
    bldg_tpl.name = "Template_Building"
    bldg_tpl.hide_viewport = True
    bldg_tpl.hide_render = True

    tower_tpl = load_model("watchtower.obj")
    tower_tpl.name = "Template_Tower"
    tower_tpl.hide_viewport = True
    tower_tpl.hide_render = True

    tree_tpl  = load_model("tree.obj")
    tree_tpl.name = "Template_Tree"
    tree_tpl.hide_viewport = True
    tree_tpl.hide_render = True

    lamp_tpl  = load_model("lamp_post.obj")
    lamp_tpl.name = "Template_Lamp"
    lamp_tpl.hide_viewport = True
    lamp_tpl.hide_render = True

    # Place Buildings
    building_transforms = [
        ( 18.0, -20.0, 0.0, 0.0),
        (-18.0, -32.0, 0.0, 90.0),
        ( 22.0,  18.0, 0.0, 180.0),
        (-20.0,  20.0, 0.0, 270.0),
        ( 35.0, -10.0, 0.0, 45.0),
        (-35.0,  10.0, 0.0, -45.0),
    ]
    for i, (x, y, z, rot) in enumerate(building_transforms):
        dup = bldg_tpl.copy()
        dup.data = bldg_tpl.data.copy()
        dup.name = f"Building_{i+1}"
        dup.hide_viewport = False
        dup.hide_render = False
        dup.location = (x, y, z)
        dup.rotation_euler = (0.0, 0.0, math.radians(rot))
        bpy.context.collection.objects.link(dup)

    # Place Corner Watchtowers
    tower_positions = [
        (-48.0, -48.0, 0.0),
        ( 48.0, -48.0, 0.0),
        (-48.0,  48.0, 0.0),
        ( 48.0,  48.0, 0.0),
    ]
    for i, (x, y, z) in enumerate(tower_positions):
        dup = tower_tpl.copy()
        dup.data = tower_tpl.data.copy()
        dup.name = f"Watchtower_{i+1}"
        dup.hide_viewport = False
        dup.hide_render = False
        dup.location = (x, y, z)
        bpy.context.collection.objects.link(dup)

    # Place Trees
    tree_positions = [
        (-10.0, -10.0), (-10.0, -22.0), (-10.0, 10.0), (-10.0, 22.0),
        ( 10.0, -10.0), ( 10.0, -22.0), ( 10.0, 10.0), ( 10.0, 22.0),
        (-30.0, -35.0), (-38.0, -28.0), ( 32.0, 32.0), ( 40.0, 25.0),
        (  0.0, -40.0), (  0.0,  40.0)
    ]
    for i, (x, y) in enumerate(tree_positions):
        dup = tree_tpl.copy()
        dup.data = tree_tpl.data.copy()
        dup.name = f"PineTree_{i+1}"
        dup.hide_viewport = False
        dup.hide_render = False
        dup.location = (x, y, 0.0)
        s = 0.85 + (i % 4) * 0.1
        dup.scale = (s, s, s)
        dup.rotation_euler = (0.0, 0.0, math.radians((i * 47) % 360))
        bpy.context.collection.objects.link(dup)

    # Place Street Lamps
    lamp_positions = [
        (-6.0, -12.0), (-6.0, 12.0),
        ( 6.0, -12.0), ( 6.0, 12.0),
        (-12.0, -6.0), ( 12.0, -6.0),
        (-12.0,  6.0), ( 12.0,  6.0),
    ]
    for i, (x, y) in enumerate(lamp_positions):
        dup = lamp_tpl.copy()
        dup.data = lamp_tpl.data.copy()
        dup.name = f"StreetLamp_{i+1}"
        dup.hide_viewport = False
        dup.hide_render = False
        dup.location = (x, y, 0.0)
        bpy.context.collection.objects.link(dup)

    # 8. Setup Sun Light
    bpy.ops.object.light_add(type='SUN', location=(50.0, 50.0, 80.0))
    sun = bpy.context.active_object
    sun.name = "Daylight_Sun"
    sun.data.energy = 4.0
    sun.rotation_euler = (math.radians(45.0), math.radians(20.0), math.radians(-30.0))

    # 9. Setup Player Camera
    bpy.ops.object.camera_add(location=(0.0, 25.0, 3.5))
    cam = bpy.context.active_object
    cam.name = "Player_Camera"
    cam.rotation_euler = (math.radians(85.0), 0.0, math.radians(180.0))
    cam.data.lens = 35.0  # ~60 deg FOV
    bpy.context.scene.camera = cam

    # 10. Save as Blender project file
    blend_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "game_environment.blend"))
    bpy.ops.wm.save_as_mainfile(filepath=blend_filepath)
    print(f"\n[BLENDER BUILDER] COMPLETE! Entire project saved as: {blend_filepath}\n")


if __name__ == "__main__":
    build_full_scene()
