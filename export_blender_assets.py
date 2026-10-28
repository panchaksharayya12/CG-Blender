"""
=============================================================================
Blender Asset Generator & Exporter
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================

This script uses Blender 5.0's Python API (`bpy`) to programmatically build
3D environment assets (Buildings, Watchtowers, Trees, Lamp Posts) and export
them as Wavefront (.obj) files with proper Counter-Clockwise (CCW) face normals.

How to Run:
-----------
1. Automatic from Windows PowerShell / Command Prompt:
   & "C:\\Program Files\\Blender Foundation\\Blender 5.0\\blender.exe" --background --python export_blender_assets.py

2. Inside Blender GUI:
   Open Blender -> Scripting workspace -> Open this file -> Run Script.
"""

import os
import sys

try:
    import bpy
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False


def reset_blender_scene():
    """Removes all default objects, meshes, and lights from the scene."""
    bpy.ops.wm.read_factory_settings(use_empty=True)


def finalize_mesh(objects, export_path):
    """
    Combines objects, ensures correct Counter-Clockwise outward normals,
    triangulates the mesh, and exports to Wavefront OBJ format.
    """
    for obj in bpy.data.objects:
        obj.select_set(False)

    for obj in objects:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = objects[0]
    if len(objects) > 1:
        bpy.ops.object.join()

    joined_obj = bpy.context.active_object

    # Switch to Edit Mode to clean and verify normals
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    # Remove duplicate vertices
    bpy.ops.mesh.remove_doubles(threshold=0.001)
    # Ensure all face normals point strictly outward (Counter-Clockwise winding)
    # Crucial for Back-Face Culling!
    bpy.ops.mesh.normals_make_consistent(inside=False)
    # Triangulate all faces for predictable OpenGL rasterization
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Export to OBJ using standard OpenGL coordinate convention (Y Up, -Z Forward)
    bpy.ops.wm.obj_export(
        filepath=export_path,
        export_selected_objects=True,
        up_axis='Y',
        forward_axis='NEGATIVE_Z'
    )
    print(f"[BLENDER EXPORTER] Successfully exported: {export_path}")


def create_building(output_dir):
    """Generates a modular classical multi-story building."""
    reset_blender_scene()
    parts = []

    # 1. Main building body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 4.0))
    body = bpy.context.active_object
    body.scale = (8.0, 6.0, 8.0)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(body)

    # 2. Base foundation
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.4))
    base = bpy.context.active_object
    base.scale = (8.8, 6.8, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(base)

    # 3. Middle floor ledge / cornice
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 4.5))
    ledge = bpy.context.active_object
    ledge.scale = (8.4, 6.4, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(ledge)

    # 4. Roof crown parapet
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 8.2))
    roof = bpy.context.active_object
    roof.scale = (8.6, 6.6, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(roof)

    # 5. Entrance pillars
    for x_offset in [-2.0, 2.0]:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12, radius=0.35, depth=3.0, location=(x_offset, -3.5, 1.5)
        )
        pillar = bpy.context.active_object
        parts.append(pillar)

    # 6. Entrance canopy
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -3.5, 3.2))
    canopy = bpy.context.active_object
    canopy.scale = (5.2, 1.8, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(canopy)

    filepath = os.path.join(output_dir, "building.obj")
    finalize_mesh(parts, filepath)


def create_watchtower(output_dir):
    """Generates a medieval defensive watchtower with battlements and roof spire."""
    reset_blender_scene()
    parts = []

    # 1. Main tower shaft (octagonal)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=2.5, depth=9.0, location=(0, 0, 4.5)
    )
    shaft = bpy.context.active_object
    parts.append(shaft)

    # 2. Overhanging observation deck
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=3.2, depth=1.5, location=(0, 0, 9.5)
    )
    deck = bpy.context.active_object
    parts.append(deck)

    # 3. Conical roof spire
    bpy.ops.mesh.primitive_cone_add(
        vertices=8, radius1=3.5, depth=4.0, location=(0, 0, 12.0)
    )
    spire = bpy.context.active_object
    parts.append(spire)

    filepath = os.path.join(output_dir, "watchtower.obj")
    finalize_mesh(parts, filepath)


def create_tree(output_dir):
    """Generates a stylized low-poly coniferous pine tree."""
    reset_blender_scene()
    parts = []

    # 1. Tree trunk
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=0.4, depth=2.5, location=(0, 0, 1.25)
    )
    trunk = bpy.context.active_object
    parts.append(trunk)

    # 2. Three foliage tiers
    tiers = [
        (2.6, 2.8, 3.2),  # (radius, depth, Z-center)
        (2.0, 2.3, 4.8),
        (1.3, 1.8, 6.0),
    ]
    for radius, depth, z in tiers:
        bpy.ops.mesh.primitive_cone_add(
            vertices=8, radius1=radius, depth=depth, location=(0, 0, z)
        )
        tier = bpy.context.active_object
        parts.append(tier)

    filepath = os.path.join(output_dir, "tree.obj")
    finalize_mesh(parts, filepath)


def create_lamp_post(output_dir):
    """Generates an urban streetlamp with pedestal and lantern cage."""
    reset_blender_scene()
    parts = []

    # 1. Pedestal base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.4))
    base = bpy.context.active_object
    base.scale = (0.9, 0.9, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(base)

    # 2. Vertical pole shaft
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=0.15, depth=4.5, location=(0, 0, 2.8)
    )
    pole = bpy.context.active_object
    parts.append(pole)

    # 3. Lamp lantern cage
    bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0, 0, 5.2))
    cage = bpy.context.active_object
    parts.append(cage)

    # 4. Lantern roof cap
    bpy.ops.mesh.primitive_cone_add(
        vertices=4, radius1=0.7, depth=0.4, location=(0, 0, 5.75)
    )
    cap = bpy.context.active_object
    parts.append(cap)

    filepath = os.path.join(output_dir, "lamp_post.obj")
    finalize_mesh(parts, filepath)


def generate_all_assets(output_dir):
    """Generates all 4 primary 3D environment assets into output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"[BLENDER EXPORTER] Generating assets in: {output_dir}")
    create_building(output_dir)
    create_watchtower(output_dir)
    create_tree(output_dir)
    create_lamp_post(output_dir)
    print("[BLENDER EXPORTER] All assets generated successfully!")


if __name__ == "__main__":
    if not IN_BLENDER:
        print("ERROR: This script must be executed via Blender.")
        print('Example: & "C:\\Program Files\\Blender Foundation\\Blender 5.0\\blender.exe" --background --python export_blender_assets.py')
        sys.exit(1)

    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "models"))
    generate_all_assets(target_dir)
