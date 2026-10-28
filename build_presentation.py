"""
=============================================================================
PowerPoint Presentation Generator for College Project
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
=============================================================================
Generates a 13-slide 16:9 widescreen presentation:
- Dark navy modern academic aesthetic (#0F172A, #1E293B)
- Accent highlights (#10B981 Emerald, #38BDF8 Sky Blue, #EF4444 Coral)
- Embedded 3D renders and mathematical diagrams
- High-density comparison tables, architectural diagrams, and viva proofs
Saves file as: `Real_Time_3D_Optimization_BackFace_Culling.pptx`.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Theme Colors
C_DARK_BG   = RGBColor(15, 23, 42)     # #0F172A
C_CARD_BG   = RGBColor(30, 41, 59)     # #1E293B
C_CARD_LINE = RGBColor(51, 65, 85)     # #334155
C_ACCENT_BL = RGBColor(56, 189, 248)   # #38BDF8 (Sky Blue)
C_ACCENT_GR = RGBColor(16, 185, 129)   # #10B981 (Emerald Green)
C_ACCENT_RD = RGBColor(239, 68, 68)    # #EF4444 (Coral Red)
C_ACCENT_YL = RGBColor(251, 191, 36)   # #FBBF24 (Amber Gold)
C_TEXT_WH   = RGBColor(248, 250, 252)  # #F8FAFC
C_TEXT_MUT  = RGBColor(148, 163, 184)  # #94A3B8

FONT_HEADING = 'Arial'
FONT_BODY    = 'Arial'

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_DARK_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="REAL-TIME 3D GRAPHICS OPTIMIZATION"):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_HEADING
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_ACCENT_BL

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEXT_WH

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_CARD_LINE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    
    # Left Hero Box
    card1 = add_card(s1, Inches(0.8), Inches(1.2), Inches(7.5), Inches(5.1))
    tf1 = card1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "COMPUTER GRAPHICS & GAME ENGINE OPTIMIZATION"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT_BL
    p.space_after = Pt(16)
    
    p = tf1.add_paragraph()
    p.text = "Real-Time 3D Game Environment\nOptimization Using Back-Face Culling"
    p.font.name = FONT_HEADING
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WH
    p.space_after = Pt(16)
    
    p = tf1.add_paragraph()
    p.text = "An interactive hardware-accelerated 3D environment analyzing polygon culling algorithms, vector normal mathematics, screen winding determinants, and real-time GPU frame latency."
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = C_TEXT_MUT
    p.space_after = Pt(28)
    
    p = tf1.add_paragraph()
    p.text = "Tech Stack: Python 3.x | OpenGL 4.6 (PyOpenGL) | Pygame | Blender 5.0"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT_GR
    
    # Right Image Preview
    if os.path.exists("render_aligned_0001.png"):
        s1.shapes.add_picture("render_aligned_0001.png", Inches(8.5), Inches(1.2), width=Inches(4.0))

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The 3D Graphics Bottleneck: Invisible Polygon Waste")
    
    c_w = Inches(3.7)
    c_h = Inches(5.2)
    
    # Card 1
    card_a = add_card(s2, Inches(0.8), Inches(1.6), c_w, c_h)
    tf_a = card_a.text_frame
    tf_a.word_wrap = True
    p = tf_a.paragraphs[0]
    p.text = "1. The Polygon Explosion"
    p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = C_ACCENT_BL; p.space_after = Pt(12)
    p = tf_a.add_paragraph()
    p.text = "• Modern 3D games render millions of triangles per second (buildings, terrain, props, characters).\n\n• Achieving 60+ FPS requires a frame budget under 16.6 milliseconds.\n\n• Processing non-visible geometry wastes GPU transform bandwidth and fill rate."
    p.font.size = Pt(13); p.font.color.rgb = C_TEXT_MUT
    
    # Card 2
    card_b = add_card(s2, Inches(4.8), Inches(1.6), c_w, c_h)
    tf_b = card_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "2. The ~50% Redundancy"
    p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = C_ACCENT_RD; p.space_after = Pt(12)
    p = tf_b.add_paragraph()
    p.text = "• In any closed 3D polyhedral mesh (building, tower, tree, cube), roughly 50% of surfaces face AWAY from the camera.\n\n• The observer can never see the rear walls of a closed structure from the outside.\n\n• Rendering back faces wastes rasterizer setup and pixel shading."
    p.font.size = Pt(13); p.font.color.rgb = C_TEXT_MUT
    
    # Card 3
    card_c = add_card(s2, Inches(8.8), Inches(1.6), c_w, c_h)
    tf_c = card_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "3. The Solution: Face Culling"
    p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = C_ACCENT_GR; p.space_after = Pt(12)
    p = tf_c.add_paragraph()
    p.text = "• Back-Face Culling detects surface orientation before rasterization.\n\n• Hardware discards back-facing primitives in the Primitive Assembly stage.\n\n• Eliminates ~50% of triangle setup and fragment shading without altering visual output."
    p.font.size = Pt(13); p.font.color.rgb = C_TEXT_MUT

    # =========================================================================
    # SLIDE 3: What is Back-Face Culling?
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "What is Back-Face Culling? Fundamental Concepts")
    
    # Left Big Card
    card_left = add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tf = card_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Core Definition"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = C_ACCENT_BL; p.space_after = Pt(10)
    p = tf.add_paragraph()
    p.text = "Back-Face Culling is an essential visibility determination algorithm implemented in GPU graphics hardware.\n\nIt evaluates each polygon's orientation relative to the camera viewpoint. Polygons facing away from the camera are discarded BEFORE pixel interpolation and fragment shading."
    p.font.size = Pt(14); p.font.color.rgb = C_TEXT_MUT; p.space_after = Pt(16)
    p = tf.add_paragraph()
    p.text = "Key Operational Rules:"
    p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = C_TEXT_WH; p.space_after = Pt(8)
    p = tf.add_paragraph()
    p.text = "✔ Front-Facing Polygon: Normal points toward camera (Rendered).\n✔ Back-Facing Polygon: Normal points away from camera (Culled).\n✔ Zero Visual Loss: Discarded faces are occluded by front surfaces on solid meshes."
    p.font.size = Pt(13); p.font.color.rgb = C_ACCENT_GR

    # Right Cards
    c1 = add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.4))
    tf1 = c1.text_frame; tf1.word_wrap = True
    p = tf1.paragraphs[0]; p.text = "WITHOUT Culling (glDisable(GL_CULL_FACE))"; p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = C_ACCENT_RD; p.space_after = Pt(8)
    p = tf1.add_paragraph()
    p.text = "• 100% of triangles pass through rasterization and pixel shading.\n• GPU renders back surfaces, only for them to be overwritten by the Z-Buffer.\n• Wastes fill-rate, memory bandwidth, and power."
    p.font.size = Pt(12); p.font.color.rgb = C_TEXT_MUT

    c2 = add_card(s3, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.5))
    tf2 = c2.text_frame; tf2.word_wrap = True
    p = tf2.paragraphs[0]; p.text = "WITH Culling (glEnable(GL_CULL_FACE))"; p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = C_ACCENT_GR; p.space_after = Pt(8)
    p = tf2.add_paragraph()
    p.text = "• Hardware discards ~50% of triangles before rasterization.\n• Zero fragment shader overhead for back-facing surfaces.\n• Results in lower frame latency (ms) and higher frame rates (FPS)."
    p.font.size = Pt(12); p.font.color.rgb = C_TEXT_MUT

    # =========================================================================
    # SLIDE 4: Mathematical Foundation & Algorithm
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Mathematical Foundation: Vectors & Winding Determinants")
    
    # Left text box
    c_math = add_card(s4, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    tf_m = c_math.text_frame; tf_m.word_wrap = True
    p = tf_m.paragraphs[0]; p.text = "The Mathematical Tests"; p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = C_ACCENT_BL; p.space_after = Pt(10)
    p = tf_m.add_paragraph()
    p.text = "1. Object Space (Dot Product):\n" \
             "• Surface Normal:  N = (V1 - V0) x (V2 - V0)\n" \
             "• View Vector:      V = CameraPos - Centroid\n" \
             "• Facing Test:\n" \
             "    N · V > 0  => Front Face (Render)\n" \
             "    N · V <= 0 => Back Face (Cull)\n\n" \
             "2. Screen Space (OpenGL Hardware):\n" \
             "• After 2D projection, OpenGL tests signed area:\n" \
             "  Area = 1/2 [(x1-x0)(y2-y0) - (y1-y0)(x2-x0)]\n\n" \
             "• Area > 0 => Counter-Clockwise (CCW)\n" \
             "• Area < 0 => Clockwise (CW) [Culled!]"
    p.font.size = Pt(12); p.font.color.rgb = C_TEXT_MUT
    
    # Right Image
    if os.path.exists("diagram_culling_math.png"):
        s4.shapes.add_picture("diagram_culling_math.png", Inches(5.6), Inches(1.6), width=Inches(6.9))

    # =========================================================================
    # SLIDE 5: OpenGL Pipeline Architecture
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Graphics Pipeline: Where Back-Face Culling Occurs")
    
    pipeline_steps = [
        ("1. Vertex Spec", "Vertex Arrays & VBOs\n(v, vn, vt indices)", C_CARD_BG, C_TEXT_MUT),
        ("2. Vertex Shader", "ModelView & Projection\nTransform to Clip Space", C_CARD_BG, C_TEXT_MUT),
        ("3. Primitive Assembly", "FACE CULLING STAGE!\nglCullFace(GL_BACK)\nDrops CW triangles!", RGBColor(6, 78, 59), C_ACCENT_GR),
        ("4. Rasterizer", "Scan-conversion of\nFRONT triangles only", C_CARD_BG, C_TEXT_MUT),
        ("5. Fragment Shader", "Lighting, texturing,\nshading visible pixels", C_CARD_BG, C_TEXT_MUT),
        ("6. Per-Sample Tests", "Depth Buffer (Z-Buffer)\n& Framebuffer blend", C_CARD_BG, C_TEXT_MUT),
    ]
    
    step_w = Inches(1.8)
    step_h = Inches(4.5)
    for idx, (title, desc, bg_col, text_col) in enumerate(pipeline_steps):
        left_pos = Inches(0.8 + idx * 1.95)
        card = add_card(s5, left_pos, Inches(1.8), step_w, step_h, bg_color=bg_col)
        tf = card.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.bold = True; p.font.size = Pt(14); p.font.color.rgb = text_col; p.space_after = Pt(12)
        p = tf.add_paragraph(); p.text = desc; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_WH if bg_col != C_CARD_BG else C_TEXT_MUT
        
    # Bottom Note
    nb = add_card(s5, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.7), bg_color=C_CARD_BG)
    tf = nb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "💡 CRITICAL ARCHITECTURAL POINT: Back-face culling drops triangles at Step 3, saving 100% of rasterization and pixel shading work at Steps 4 & 5!"
    p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = C_ACCENT_BL

    # =========================================================================
    # SLIDE 6: System Design & Implementation Architecture
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Software Architecture: Modular Python & OpenGL Engine")
    
    modules = [
        ("main.py", "Core Pipeline Coordinator", "• High-precision delta time clock\n• Viewport & OpenGL state initialization\n• Input event dispatcher & camera loop"),
        ("culling_manager.py", "Culling & Rasterizer State", "• Controls glEnable/glDisable(GL_CULL_FACE)\n• glCullFace(GL_BACK) & glFrontFace(GL_CCW)\n• glPolygonMode() wireframe switching"),
        ("scene.py", "3D Game Environment", "• Classical buildings, towers, trees, lamps\n• Inside-Out Inspection Chamber\n• Heavy-Poly Stress Grid (100K+ tris)"),
        ("camera.py", "6-DOF First-Person Camera", "• Smooth WASD flight & sprint boost\n• Mouse pitch/yaw look with angle clamping\n• gluLookAt view matrix update"),
        ("obj_loader.py", "Wavefront OBJ Parser", "• Parses vertices, normals, CCW faces\n• Compiles into OpenGL Display Lists\n• Zero runtime CPU parsing overhead"),
        ("hud.py", "2D Telemetry & UI Overlay", "• Real-time smoothed FPS & frame time (ms)\n• Live triangle discard counter (~50%)\n• Antialiased Pygame-to-OpenGL overlay"),
    ]
    
    for idx, (filename, subtitle, bullets) in enumerate(modules):
        col_idx = idx % 3
        row_idx = idx // 3
        left_pos = Inches(0.8 + col_idx * 3.95)
        top_pos  = Inches(1.6 + row_idx * 2.7)
        card = add_card(s6, left_pos, top_pos, Inches(3.7), Inches(2.4))
        tf = card.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = filename; p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = C_ACCENT_GR
        p = tf.add_paragraph(); p.text = subtitle; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = C_ACCENT_BL; p.space_after = Pt(6)
        p = tf.add_paragraph(); p.text = bullets; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_MUT

    # =========================================================================
    # SLIDE 7: 3D Environment Design & Blender 5.0 Pipeline
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "3D Environment Design & Blender 5.0 Asset Pipeline")
    
    card_bld = add_card(s7, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2))
    tf = card_bld.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Asset Pipeline & Face Orientation"; p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = C_ACCENT_BL; p.space_after = Pt(10)
    p = tf.add_paragraph()
    p.text = "1. Blender 5.0 Integration:\n" \
             "• Automated headless script builds and exports all modular assets.\n" \
             "• Saved complete scene to `game_environment.blend`.\n\n" \
             "2. The Face Orientation Rule:\n" \
             "• In Blender's Viewport Overlays, Face Orientation must be BLUE (front-facing CCW normals).\n" \
             "• Inward RED normals cause OpenGL to cull front faces mistakenly!\n\n" \
             "3. Architectural Elements:\n" \
             "• Hip roof townhouses with marble pillars and entrance porticos.\n" \
             "• Medieval corner watchtowers with crenellated observation rims.\n" \
             "• Upright coniferous pine trees with brown trunks & layered foliage.\n" \
             "• Street lamps with point lights and central plaza fountain."
    p.font.size = Pt(12); p.font.color.rgb = C_TEXT_MUT
    
    if os.path.exists("render_aligned_0001.png"):
        s7.shapes.add_picture("render_aligned_0001.png", Inches(6.9), Inches(1.6), width=Inches(5.6))

    # =========================================================================
    # SLIDE 8: Key Features & Interactive Controls
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Interactive Controls & Demonstration Modes")
    
    card_ctrl = add_card(s8, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf = card_ctrl.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Interactive Keyboard Shortcuts"; p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = C_ACCENT_BL; p.space_after = Pt(12)
    
    controls_data = [
        ("Key / Input", "Action", "Demonstration Purpose"),
        ("W, A, S, D + Mouse", "6-DOF First Person Flight", "Freely inspect buildings, plaza, and fly inside demo rooms"),
        ("[C] Key", "Toggle Back-Face Culling", "Instantly compare ENABLED (Optimized) vs DISABLED (Wasteful)"),
        ("[M] Key", "Toggle Mesh Mode (Solid / Wireframe)", "Wireframe mode exposes back surfaces for visual proof"),
        ("[T] Key", "Toggle Heavy-Poly Stress Grid", "Spawns 50,000+ triangles to show real frame latency differences"),
        ("[U] Key", "Toggle Uncapped FPS Benchmark", "Removes 60 FPS cap to benchmark raw hardware throughput"),
        ("[F] Key", "Toggle Cull Target (GL_BACK / GL_FRONT)", "Educational test showing inverted inside-out geometry"),
        ("[Tab] / [Esc]", "Lock / Unlock Mouse Cursor", "Frees mouse cursor to point on screen during presentation"),
    ]
    
    # Add Table
    rows = len(controls_data)
    cols = 3
    table_shape = s8.shapes.add_table(rows, cols, Inches(1.0), Inches(2.3), Inches(11.3), Inches(4.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(4.2)
    table.columns[2].width = Inches(4.5)
    
    for r_idx, row in enumerate(controls_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_ACCENT_BL
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
            else:
                p.font.color.rgb = C_TEXT_WH if c_idx == 0 else C_TEXT_MUT
                cell.fill.solid(); cell.fill.fore_color.rgb = C_CARD_BG

    # =========================================================================
    # SLIDE 9: Visual Verification: The Three Proofs
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Examiner Verification: 3 Indisputable Proofs")
    
    # Left Card
    card_prf = add_card(s9, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))
    tf = card_prf.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "How to Prove Culling Is Real"; p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = C_ACCENT_BL; p.space_after = Pt(10)
    p = tf.add_paragraph()
    p.text = "Proof 1: Wireframe Mode Test ([M] Key):\n" \
             "• Solid mode masks back faces behind the Z-Buffer.\n" \
             "• Wireframe mode removes surface occlusion!\n" \
             "• Culling OFF: All rear wireframes visible (cluttered mesh).\n" \
             "• Culling ON: Rear wireframes vanish instantly!\n\n" \
             "Proof 2: Inside-Out Chamber ([C] Inside Room):\n" \
             "• Walk inside the red building at X: -25, Z: -15.\n" \
             "• Walls were built with outward normals.\n" \
             "• From inside, all walls face AWAY from camera.\n" \
             "• Culling ON: Walls turn invisible (see through to outside)!\n" \
             "• Culling OFF: Walls reappear immediately.\n\n" \
             "Proof 3: Hardware Geometry Counters:\n" \
             "• Real-time HUD proves ~50% triangles discarded."
    p.font.size = Pt(12); p.font.color.rgb = C_TEXT_MUT
    
    if os.path.exists("render_birdseye_0001.png"):
        s9.shapes.add_picture("render_birdseye_0001.png", Inches(7.1), Inches(1.6), width=Inches(5.4))

    # =========================================================================
    # SLIDE 10: Performance Benchmarks & Experimental Results
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Performance Benchmarks & Experimental Results")
    
    if os.path.exists("diagram_benchmark_chart.png"):
        s10.shapes.add_picture("diagram_benchmark_chart.png", Inches(0.8), Inches(1.6), width=Inches(11.7))

    # =========================================================================
    # SLIDE 11: Comparison: Back-Face vs Frustum vs Occlusion Culling
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Comparative Visibility Analysis: Culling Techniques")
    
    comp_data = [
        ("Culling Technique", "Granularity", "Pipeline Stage", "Algorithmic Mechanism", "What It Removes"),
        ("Back-Face Culling\n(Our Project)", "Polygon-level\n(Individual Triangles)", "Primitive Assembly\n(Hardware Rasterizer)", "Normal · View Vector <= 0\nScreen Winding Det < 0", "Surfaces pointing away on visible objects (~50%)"),
        ("View Frustum Culling", "Object / Bounding Box\nlevel (AABB/Sphere)", "CPU Pre-Pass /\nCompute Shader", "6 Frustum Plane clipping\nequations", "Entire objects outside the camera FOV"),
        ("Occlusion Culling", "Object or Fragment\nlevel", "Early-Z / Hardware\nOcclusion Queries", "Hierarchical Z-Buffer\n(HZB) / Depth bounding", "Front-facing objects hidden behind large walls"),
    ]
    
    table_shape2 = s11.shapes.add_table(len(comp_data), 5, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.0))
    table2 = table_shape2.table
    table2.columns[0].width = Inches(2.4)
    table2.columns[1].width = Inches(2.2)
    table2.columns[2].width = Inches(2.3)
    table2.columns[3].width = Inches(2.5)
    table2.columns[4].width = Inches(2.3)
    
    for r_idx, row in enumerate(comp_data):
        for c_idx, val in enumerate(row):
            cell = table2.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_ACCENT_BL
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
            else:
                p.font.color.rgb = C_ACCENT_GR if (r_idx == 1 and c_idx == 0) else (C_TEXT_WH if c_idx == 0 else C_TEXT_MUT)
                cell.fill.solid(); cell.fill.fore_color.rgb = C_CARD_BG

    # =========================================================================
    # SLIDE 12: Conclusion & Key Takeaways
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Conclusion & Key Takeaways")
    
    c_conc = add_card(s12, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf = c_conc.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Summary of Project Achievements"; p.font.bold = True; p.font.size = Pt(17); p.font.color.rgb = C_ACCENT_BL; p.space_after = Pt(12)
    p = tf.add_paragraph()
    p.text = "✔ Genuine Hardware Culling: Implemented authentic OpenGL pipeline face culling (`glEnable(GL_CULL_FACE)`, `glCullFace(GL_BACK)`, `glFrontFace(GL_CCW)`), not superficial object-hiding."
    p.font.size = Pt(13); p.font.color.rgb = C_TEXT_WH; p.space_after = Pt(10)
    p = tf.add_paragraph()
    p.text = "✔ ~50% Fill-Rate Protection: Confirmed that closed polyhedral meshes achieve a consistent ~50% primitive drop before rasterization, directly lowering frame latency under heavy polygon loads."
    p.font.size = Pt(13); p.font.color.rgb = C_TEXT_WH; p.space_after = Pt(10)
    p = tf.add_paragraph()
    p.text = "✔ Multi-Disciplinary Pipeline: Successfully bridged 3D digital content creation (Blender 5.0) with real-time rendering code (Python/PyOpenGL) enforcing strict Counter-Clockwise vertex winding."
    p.font.size = Pt(13); p.font.color.rgb = C_TEXT_WH; p.space_after = Pt(10)
    p = tf.add_paragraph()
    p.text = "✔ Complete Viva-Ready Suite: Equipped with live wireframe inspection, inside-out chamber demonstration, high-density stress tests, and automated telemetry overlays."
    p.font.size = Pt(13); p.font.color.rgb = C_TEXT_WH

    # =========================================================================
    # SLIDE 13: Thank You & Viva Q&A
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    
    card_ty = add_card(s13, Inches(2.0), Inches(1.5), Inches(9.33), Inches(4.5))
    tf = card_ty.text_frame; tf.word_wrap = True
    
    p = tf.paragraphs[0]; p.text = "THANK YOU!"; p.font.bold = True; p.font.size = Pt(36); p.font.color.rgb = C_ACCENT_GR; p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(14)
    p = tf.add_paragraph(); p.text = "Real-Time 3D Game Environment Optimization Using Back-Face Culling"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = C_TEXT_WH; p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(20)
    p = tf.add_paragraph(); p.text = "Ready for Questions & Live Demonstration"; p.font.size = Pt(16); p.font.color.rgb = C_ACCENT_BL; p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(24)
    p = tf.add_paragraph(); p.text = "Interactive Demo Controls: [M] Wireframe | [C] Toggle Culling | [T] Stress Grid | [U] Uncapped FPS"; p.font.size = Pt(12); p.font.color.rgb = C_TEXT_MUT; p.alignment = PP_ALIGN.CENTER

    # Save Presentation
    output_path = os.path.abspath("Real_Time_3D_Optimization_BackFace_Culling.pptx")
    prs.save(output_path)
    print(f"[PPTX GENERATOR] Presentation saved successfully to: {output_path}")

if __name__ == '__main__':
    create_deck()
