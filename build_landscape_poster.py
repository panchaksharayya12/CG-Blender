"""
=============================================================================
Academic Landscape Poster Generator (Light Theme)
Project: Real-Time 3D Game Environment Optimization Using Back-Face Culling
Student: Panchaksharayya | Reg No: 2411021061321 | Dept of IT
Institution: Alliance School of Advanced Computing, Alliance University
=============================================================================
Generates:
1. PROJECT_POSTER_LANDSCAPE.png (4800 x 2700 pixels, Ultra-HD, 300 DPI, Light Theme)
2. PROJECT_POSTER_LANDSCAPE.pdf (Printable high-res PDF)
3. Real_Time_3D_Optimization_Poster.pptx (Editable widescreen presentation poster)
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------
POSTER_W = 4800
POSTER_H = 2700

# Color Palette (Crisp, High-Contrast Light Theme)
COLOR_BG_PAGE        = (248, 250, 252)   # Slate-50 off-white
COLOR_CARD_BG        = (255, 255, 255)   # Pure White
COLOR_CARD_BORDER    = (226, 232, 240)   # Slate-200 border
COLOR_CARD_SHADOW    = (203, 213, 225)   # Slate-300 shadow

# Branding Colors
COLOR_ALLIANCE_MAROON= (139, 0, 0)       # #8B0000 Alliance University Maroon
COLOR_ALLIANCE_CRIMSON=(153, 27, 27)     # #991B1B Dark Crimson
COLOR_NAVY_TITLE     = (15, 23, 42)      # Slate-900 Deep Navy
COLOR_NAVY_SUB       = (30, 41, 59)      # Slate-800
COLOR_BODY_TEXT      = (51, 65, 85)      # Slate-700
COLOR_MUTED_TEXT     = (100, 116, 139)   # Slate-500

# Accent Colors
COLOR_ACCENT_BLUE    = (37, 99, 235)     # #2563EB Primary Blue
COLOR_ACCENT_CYAN    = (14, 165, 233)    # Sky-500
COLOR_SUCCESS_GREEN  = (16, 185, 129)    # Emerald-500
COLOR_SUCCESS_BG     = (236, 253, 245)    # Emerald-50
COLOR_ALERT_RED      = (220, 38, 38)     # Red-600
COLOR_ALERT_BG       = (254, 242, 242)    # Red-50
COLOR_AMBER_BADGE    = (217, 119, 6)     # Amber-600
COLOR_AMBER_BG       = (254, 243, 199)    # Amber-50

# Fonts Loading
FONT_PATH_REG  = r"C:\Windows\Fonts\segoeui.ttf"
FONT_PATH_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_PATH_MONO = r"C:\Windows\Fonts\consola.ttf"

def get_font(size, bold=False, mono=False):
    path = FONT_PATH_MONO if mono else (FONT_PATH_BOLD if bold else FONT_PATH_REG)
    return ImageFont.truetype(path, size)

# Pre-allocated fonts
F_HEADER_TITLE = get_font(46, bold=True)
F_HEADER_SUB   = get_font(21, bold=False)
F_CARD_TITLE   = get_font(24, bold=True)
F_CARD_SUB     = get_font(17, bold=False)
F_BODY         = get_font(18, bold=False)
F_BODY_BOLD    = get_font(18, bold=True)
F_CAPTION      = get_font(15, bold=False)
F_CAPTION_BOLD = get_font(15, bold=True)
F_BADGE        = get_font(16, bold=True)
F_STUDENT_NAME = get_font(30, bold=True)
F_STUDENT_INFO = get_font(20, bold=True)
F_STAT_VAL     = get_font(32, bold=True)
F_STAT_LBL     = get_font(15, bold=False)

def draw_rounded_card(draw, x0, y0, x1, y1, radius=16, fill=COLOR_CARD_BG, border=COLOR_CARD_BORDER, border_width=2, shadow=True):
    """Draws a clean white card with soft drop shadow and subtle border."""
    if shadow:
        draw.rounded_rectangle((x0+3, y0+4, x1+3, y1+4), radius=radius, fill=(226, 232, 240))
        draw.rounded_rectangle((x0+1, y0+2, x1+1, y1+2), radius=radius, fill=(241, 245, 249))
    draw.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=fill, outline=border, width=border_width)

def draw_card_header(draw, x0, y0, width, title, icon="📌", accent_color=COLOR_ALLIANCE_CRIMSON):
    """Draws a professional card header with an accent pill and crisp title."""
    # Top accent bar
    draw.rounded_rectangle((x0, y0, x0 + width, y0 + 6), radius=3, fill=accent_color)
    # Header icon & title
    full_title = f"{icon}  {title.upper()}"
    draw.text((x0 + 24, y0 + 20), full_title, fill=COLOR_NAVY_TITLE, font=F_CARD_TITLE)
    # Divider line
    draw.line((x0 + 20, y0 + 64, x0 + width - 20, y0 + 64), fill=COLOR_CARD_BORDER, width=2)

def fit_image_inside(img_path, target_w, target_h, border_color=COLOR_CARD_BORDER):
    """Loads an image, crops/resizes cleanly with letterboxing/borders for neat presentation."""
    if not os.path.exists(img_path):
        placeholder = Image.new("RGB", (target_w, target_h), (241, 245, 249))
        d = ImageDraw.Draw(placeholder)
        d.text((target_w//2, target_h//2), f"Missing Image\n{os.path.basename(img_path)}", fill=COLOR_MUTED_TEXT, font=F_CAPTION, anchor="mm")
        return placeholder
        
    src = Image.open(img_path).convert("RGB")
    src_ratio = src.width / src.height
    dst_ratio = target_w / target_h
    
    # Resize maintaining aspect ratio
    if src_ratio > dst_ratio:
        new_w = target_w
        new_h = int(target_w / src_ratio)
    else:
        new_h = target_h
        new_w = int(target_h * src_ratio)
        
    resized = src.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Place on clean background
    canvas = Image.new("RGB", (target_w, target_h), (248, 250, 252))
    px = (target_w - new_w) // 2
    py = (target_h - new_h) // 2
    canvas.paste(resized, (px, py))
    
    # Subtle inner border
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, target_w-1, target_h-1), outline=border_color, width=2)
    return canvas

def draw_comparison_pair(poster_img, draw, x, y, total_w, img_h, img_left_path, img_right_path, label_left, label_right, caption):
    """Draws two comparison images side by side with colored status badges and shared caption."""
    single_w = (total_w - 20) // 2
    
    # Left image (Culling OFF - Alert Red badge)
    img_l = fit_image_inside(img_left_path, single_w, img_h, border_color=(254, 202, 202))
    poster_img.paste(img_l, (x, y))
    # Badge Left
    draw.rounded_rectangle((x + 10, y + 10, x + single_w - 10, y + 42), radius=6, fill=COLOR_ALERT_BG, outline=COLOR_ALERT_RED, width=2)
    draw.text((x + 20, y + 17), label_left, fill=COLOR_ALERT_RED, font=F_BADGE)
    
    # Right image (Culling ON - Success Green badge)
    img_r = fit_image_inside(img_right_path, single_w, img_h, border_color=(167, 243, 208))
    poster_img.paste(img_r, (x + single_w + 20, y))
    # Badge Right
    draw.rounded_rectangle((x + single_w + 30, y + 10, x + total_w - 10, y + 42), radius=6, fill=COLOR_SUCCESS_BG, outline=COLOR_SUCCESS_GREEN, width=2)
    draw.text((x + single_w + 40, y + 17), label_right, fill=COLOR_SUCCESS_GREEN, font=F_BADGE)
    
    # Shared Caption below
    draw.text((x + 10, y + img_h + 10), caption, fill=COLOR_BODY_TEXT, font=F_CAPTION)

def main():
    print("=" * 70)
    print(" GENERATING HIGH-RESOLUTION LANDSCAPE POSTER (LIGHT THEME)")
    print(f" Target Resolution: {POSTER_W} x {POSTER_H} pixels (16:9 Landscape)")
    print("=" * 70)
    
    poster = Image.new("RGB", (POSTER_W, POSTER_H), COLOR_BG_PAGE)
    draw = ImageDraw.Draw(poster)
    
    # -------------------------------------------------------------------------
    # 1. TOP HEADER & BRANDING BAR (y: 35 to 400)
    # -------------------------------------------------------------------------
    # Header container card
    draw_rounded_card(draw, 35, 35, POSTER_W - 35, 400, radius=18, fill=COLOR_CARD_BG, border=COLOR_CARD_BORDER)
    
    # Top decorative brand stripe (Alliance Crimson & Navy)
    draw.rounded_rectangle((35, 35, POSTER_W - 35, 47), radius=3, fill=COLOR_ALLIANCE_CRIMSON)
    draw.rounded_rectangle((35, 47, POSTER_W - 35, 52), radius=1, fill=COLOR_NAVY_TITLE)
    
    # Left: Alliance University Logo
    logo_path = "assets/alliance_university_logo.jpg"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).convert("RGB")
        # Resize logo nicely to height ~130 preserving aspect ratio
        logo_h = 130
        logo_w = int(logo_img.width * (logo_h / logo_img.height))
        logo_resized = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        # Logo frame
        draw.rounded_rectangle((65, 80, 65 + logo_w + 30, 80 + logo_h + 30), radius=12, fill=(255, 255, 255), outline=COLOR_CARD_BORDER, width=2)
        poster.paste(logo_resized, (80, 95))
        logo_end_x = 65 + logo_w + 60
    else:
        logo_end_x = 500
        draw.text((80, 130), "ALLIANCE UNIVERSITY", fill=COLOR_ALLIANCE_CRIMSON, font=F_CARD_TITLE)
        
    # Center: Project Title & Subtitle block
    title_x = logo_end_x + 30
    title_w = POSTER_W - title_x - 1280
    
    draw.text((title_x, 82), "ALLIANCE SCHOOL OF ADVANCED COMPUTING  •  ALLIANCE UNIVERSITY, BENGALURU", fill=COLOR_ALLIANCE_CRIMSON, font=get_font(22, bold=True))
    draw.text((title_x, 120), "REAL-TIME 3D GAME ENVIRONMENT OPTIMIZATION", fill=COLOR_NAVY_TITLE, font=F_HEADER_TITLE)
    draw.text((title_x, 180), "USING OPENGL HARDWARE BACK-FACE CULLING PIPELINE", fill=COLOR_ACCENT_BLUE, font=get_font(34, bold=True))
    draw.text((title_x, 240), "Eliminating Redundant Geometry in Primitive Assembly to Double Real-Time Rendering Frame Rates", fill=COLOR_BODY_TEXT, font=F_HEADER_SUB)
    
    # Tech pills
    pills = [
        ("Python 3.13 Engine", COLOR_ACCENT_BLUE),
        ("OpenGL Hardware Pipeline", (85, 134, 164)),
        ("Blender 5.0 Modeling", (245, 121, 42)),
        ("Pygame 2.6 Framework", (16, 185, 129)),
        ("6-DOF FPS Flight", COLOR_NAVY_TITLE),
        ("Real-Time Telemetry HUD", COLOR_ALLIANCE_CRIMSON)
    ]
    cur_px = title_x
    for p_txt, p_col in pills:
        pw = draw.textlength(p_txt, font=F_BADGE) + 26
        draw.rounded_rectangle((cur_px, 300, cur_px + pw, 335), radius=8, fill=(241, 245, 249), outline=p_col, width=2)
        draw.text((cur_px + 13, 307), p_txt, fill=p_col, font=F_BADGE)
        cur_px += pw + 16
        
    # Right: Student Details Card (Clean prominent student credentials box)
    stu_x0 = POSTER_W - 1220
    stu_y0 = 68
    stu_x1 = POSTER_W - 65
    stu_y1 = 368
    
    draw.rounded_rectangle((stu_x0, stu_y0, stu_x1, stu_y1), radius=14, fill=(255, 255, 255), outline=COLOR_CARD_BORDER, width=2)
    # Left accent vertical ribbon
    draw.rounded_rectangle((stu_x0, stu_y0, stu_x0 + 10, stu_y1), radius=4, fill=COLOR_ALLIANCE_CRIMSON)
    
    # Student Header Tag
    draw.rounded_rectangle((stu_x0 + 24, stu_y0 + 16, stu_x0 + 360, stu_y0 + 48), radius=6, fill=COLOR_AMBER_BG, outline=COLOR_AMBER_BADGE, width=1)
    draw.text((stu_x0 + 36, stu_y0 + 22), "🎓 CANDIDATE & PROJECT DETAILS", fill=COLOR_AMBER_BADGE, font=get_font(16, bold=True))
    
    # Details Fields
    draw.text((stu_x0 + 26, stu_y0 + 64), "STUDENT NAME:", fill=COLOR_MUTED_TEXT, font=get_font(15, bold=True))
    draw.text((stu_x0 + 26, stu_y0 + 88), "PANCHAKSHARAYYA", fill=COLOR_NAVY_TITLE, font=F_STUDENT_NAME)
    
    draw.text((stu_x0 + 26, stu_y0 + 138), "REGISTRATION NO:", fill=COLOR_MUTED_TEXT, font=get_font(15, bold=True))
    draw.text((stu_x0 + 26, stu_y0 + 162), "2411021061321", fill=COLOR_ALLIANCE_CRIMSON, font=get_font(26, bold=True))
    
    draw.text((stu_x0 + 26, stu_y0 + 208), "DEPARTMENT & SCHOOL:", fill=COLOR_MUTED_TEXT, font=get_font(15, bold=True))
    draw.text((stu_x0 + 26, stu_y0 + 230), "Dept. of Information Technology (IT)", fill=COLOR_ACCENT_BLUE, font=F_STUDENT_INFO)
    draw.text((stu_x0 + 26, stu_y0 + 262), "Alliance School of Advanced Computing", fill=COLOR_NAVY_SUB, font=get_font(18, bold=False))
    
    # -------------------------------------------------------------------------
    # 3-COLUMN MAIN BODY LAYOUT (y: 425 to 2665)
    # -------------------------------------------------------------------------
    # Column Coordinates
    col1_x0, col1_w = 35, 1530
    col2_x0, col2_w = 1600, 1600
    col3_x0, col3_w = 3235, 1530
    
    col1_x1 = col1_x0 + col1_w
    col2_x1 = col2_x0 + col2_w
    col3_x1 = col3_x0 + col3_w
    
    # =========================================================================
    # COLUMN 1: 3D Environment Architecture & Blender Modeling
    # =========================================================================
    # Card 1.1: Project Motivation & Problem Statement (y: 425 to 765, h: 340)
    c1_y0, c1_y1 = 425, 765
    draw_rounded_card(draw, col1_x0, c1_y0, col1_x1, c1_y1)
    draw_card_header(draw, col1_x0, c1_y0, col1_w, "Project Idea & Computer Graphics Motivation", icon="💡", accent_color=COLOR_ALLIANCE_CRIMSON)
    
    motivation_text = [
        ("THE PROBLEM IN 3D GRAPHICS:", COLOR_ALLIANCE_CRIMSON, True),
        ("In 3D video games, objects are modeled as closed, watertight solid meshes. At any viewpoint, exactly", COLOR_BODY_TEXT, False),
        ("~50% of triangle surfaces face AWAY from the camera. Without optimization, the GPU pipeline transforms,", COLOR_BODY_TEXT, False),
        ("interpolates, and evaluates fragment pixel shaders on invisible geometry, severely wasting fill-rate.", COLOR_BODY_TEXT, False),
        ("", COLOR_BODY_TEXT, False),
        ("THE SOLUTION: HARDWARE BACK-FACE CULLING", COLOR_ACCENT_BLUE, True),
        ("By testing vertex winding and surface normals in the early Primitive Assembly stage (glEnable(GL_CULL_FACE)),", COLOR_BODY_TEXT, False),
        ("OpenGL instantly drops ~50% of primitives BEFORE rasterization. Frame latency drops by 50% with ZERO visual artifacts!", COLOR_BODY_TEXT, False)
    ]
    my = c1_y0 + 82
    for m_line, m_col, m_bold in motivation_text:
        if m_line:
            draw.text((col1_x0 + 24, my), m_line, fill=m_col, font=F_BODY_BOLD if m_bold else F_BODY)
        my += 28
        
    # Card 1.2: 3D Environment Architecture (Blender 5.0 Modeling) (y: 785 to 1910, h: 1125)
    c2_y0, c2_y1 = 785, 1910
    draw_rounded_card(draw, col1_x0, c2_y0, col1_x1, c2_y1)
    draw_card_header(draw, col1_x0, c2_y0, col1_w, "3D Game Environment (Blender 5.0 Modeling)", icon="🏛️", accent_color=COLOR_NAVY_TITLE)
    
    # Aerial Image (Full Width of Column)
    aerial_w = col1_w - 48
    aerial_h = 420
    aerial_img = fit_image_inside("assets/renders/render_birdseye_0001.png", aerial_w, aerial_h)
    poster.paste(aerial_img, (col1_x0 + 24, c2_y0 + 80))
    draw.text((col1_x0 + 24, c2_y0 + 510), "Figure 1: Bird's-Eye Panoramic Layout — Modular town plaza, fountain basin, hip roof buildings & stone fortress perimeter", fill=COLOR_NAVY_TITLE, font=F_CAPTION_BOLD)
    
    # Dual Images Below: Street Level + Interactive Viewport
    sub_w = (aerial_w - 20) // 2
    sub_h = 360
    
    street_img = fit_image_inside("assets/renders/render_aligned_0001.png", sub_w, sub_h)
    poster.paste(street_img, (col1_x0 + 24, c2_y0 + 540))
    draw.text((col1_x0 + 24, c2_y0 + 910), "Figure 2: Ground-level perspective showing slate roofs,", fill=COLOR_BODY_TEXT, font=F_CAPTION)
    draw.text((col1_x0 + 24, c2_y0 + 932), "stone foundation arches, streetlamps, and pine trees.", fill=COLOR_MUTED_TEXT, font=F_CAPTION)
    
    game_img = fit_image_inside("assets/poster_shots/town_simulation_interactive.png", sub_w, sub_h)
    poster.paste(game_img, (col1_x0 + 24 + sub_w + 20, c2_y0 + 540))
    draw.text((col1_x0 + 24 + sub_w + 20, c2_y0 + 910), "Figure 3: Interactive real-time PyOpenGL simulation", fill=COLOR_BODY_TEXT, font=F_CAPTION)
    draw.text((col1_x0 + 24 + sub_w + 20, c2_y0 + 932), "with live 2D telemetry HUD and 60 FPS vsync cap.", fill=COLOR_MUTED_TEXT, font=F_CAPTION)
    
    # Highlights footer inside card
    draw.rounded_rectangle((col1_x0 + 24, c2_y0 + 970, col1_x1 - 24, c2_y1 - 20), radius=10, fill=(241, 245, 249), outline=COLOR_CARD_BORDER)
    draw.text((col1_x0 + 40, c2_y0 + 985), "• 6 Modular Collections in Blender 5.0: Architecture, Nature, Plaza Fountain, Perimeter Walls, Chamber & Camera", fill=COLOR_NAVY_SUB, font=get_font(16, bold=True))
    draw.text((col1_x0 + 40, c2_y0 + 1012), "• Strict Counter-Clockwise (CCW) face winding ensures outward surface normals for 100% reliable hardware culling", fill=COLOR_BODY_TEXT, font=get_font(16, bold=False))
    draw.text((col1_x0 + 40, c2_y0 + 1039), "• Wavefront OBJ & MTL exporter automatically compiles meshes into optimized display lists (glCallList)", fill=COLOR_BODY_TEXT, font=get_font(16, bold=False))

    # Card 1.3: Blender 5.0 Normal Auditing & Walk Navigation (y: 1930 to 2665, h: 735)
    c3_y0, c3_y1 = 1930, 2665
    draw_rounded_card(draw, col1_x0, c3_y0, col1_x1, c3_y1)
    draw_card_header(draw, col1_x0, c3_y0, col1_w, "Blender 5.0 Normal Auditing & Walkthrough", icon="🎨", accent_color=(245, 121, 42))
    
    blender_diag = fit_image_inside("assets/diagrams/diagram_blender_walkthrough.png", col1_w - 48, 560)
    poster.paste(blender_diag, (col1_x0 + 24, c3_y0 + 80))
    draw.text((col1_x0 + 24, c3_y0 + 655), "Figure 4: 4-Step Examiner Walkthrough — Material Preview Shading, Face Orientation (Blue=Front, Red=Back),", fill=COLOR_NAVY_TITLE, font=F_CAPTION_BOLD)
    draw.text((col1_x0 + 24, c3_y0 + 680), "real-time Backface Culling toggle, and interactive FPS Walk Navigation (Shift + ~) with WASD movement.", fill=COLOR_BODY_TEXT, font=F_CAPTION)

    # =========================================================================
    # COLUMN 2: The Core Concept & Visual Proofs (Working of the Project)
    # =========================================================================
    # Card 2.1: Mathematical Concept & GPU Pipeline (y: 425 to 1270, h: 845)
    c4_y0, c4_y1 = 425, 1270
    draw_rounded_card(draw, col2_x0, c4_y0, col2_x1, c4_y1)
    draw_card_header(draw, col2_x0, c4_y0, col2_w, "Core Mathematical Concept & OpenGL Pipeline", icon="📐", accent_color=COLOR_ACCENT_BLUE)
    
    # Math diagram image
    math_w = col2_w - 48
    math_h = 470
    math_img = fit_image_inside("assets/diagrams/diagram_culling_math.png", math_w, math_h)
    poster.paste(math_img, (col2_x0 + 24, c4_y0 + 80))
    draw.text((col2_x0 + 24, c4_y0 + 560), "Figure 5: Mathematical Foundations — 3D Vector Dot Product Test vs Screen-Space 2D Winding Determinant", fill=COLOR_NAVY_TITLE, font=F_CAPTION_BOLD)
    
    # 3 Math Explanatory Columns
    box_w = (math_w - 30) // 3
    box_y = c4_y0 + 595
    box_h = 240
    
    # Box 1: Vector Dot Product
    draw.rounded_rectangle((col2_x0 + 24, box_y, col2_x0 + 24 + box_w, box_y + box_h), radius=10, fill=(248, 250, 252), outline=COLOR_ACCENT_BLUE, width=2)
    draw.text((col2_x0 + 40, box_y + 14), "1. OBJECT SPACE TEST", fill=COLOR_ACCENT_BLUE, font=get_font(16, bold=True))
    draw.text((col2_x0 + 40, box_y + 44), "Normal N = (V1-V0) x (V2-V0)", fill=COLOR_NAVY_TITLE, font=get_font(15, bold=True, mono=True))
    draw.text((col2_x0 + 40, box_y + 74), "View V = CameraPos - Centroid", fill=COLOR_NAVY_TITLE, font=get_font(15, bold=True, mono=True))
    draw.text((col2_x0 + 40, box_y + 110), "N · V >= 0 => FRONT FACE", fill=COLOR_SUCCESS_GREEN, font=get_font(16, bold=True))
    draw.text((col2_x0 + 40, box_y + 138), "N · V <  0 => BACK FACE (CULL)", fill=COLOR_ALERT_RED, font=get_font(16, bold=True))
    draw.text((col2_x0 + 40, box_y + 175), "Determines orientation based on 3D", fill=COLOR_MUTED_TEXT, font=F_CAPTION)
    draw.text((col2_x0 + 40, box_y + 198), "angle relative to observer camera.", fill=COLOR_MUTED_TEXT, font=F_CAPTION)
    
    # Box 2: Screen-Space Winding
    bx2 = col2_x0 + 24 + box_w + 15
    draw.rounded_rectangle((bx2, box_y, bx2 + box_w, box_y + box_h), radius=10, fill=(248, 250, 252), outline=COLOR_AMBER_BADGE, width=2)
    draw.text((bx2 + 16, box_y + 14), "2. 2D SCREEN DETERMINANT", fill=COLOR_AMBER_BADGE, font=get_font(16, bold=True))
    draw.text((bx2 + 16, box_y + 44), "Area = (x1-x0)(y2-y0) -", fill=COLOR_NAVY_TITLE, font=get_font(15, bold=True, mono=True))
    draw.text((bx2 + 16, box_y + 70), "       (y1-y0)(x2-x0)", fill=COLOR_NAVY_TITLE, font=get_font(15, bold=True, mono=True))
    draw.text((bx2 + 16, box_y + 110), "Area > 0 => CCW (Front Face)", fill=COLOR_SUCCESS_GREEN, font=get_font(16, bold=True))
    draw.text((bx2 + 16, box_y + 138), "Area < 0 => CW (Back Face)", fill=COLOR_ALERT_RED, font=get_font(16, bold=True))
    draw.text((bx2 + 16, box_y + 175), "Fast hardware 2D determinant after", fill=COLOR_MUTED_TEXT, font=F_CAPTION)
    draw.text((bx2 + 16, box_y + 198), "perspective projection stage.", fill=COLOR_MUTED_TEXT, font=F_CAPTION)
    
    # Box 3: Pipeline Placement
    bx3 = bx2 + box_w + 15
    draw.rounded_rectangle((bx3, box_y, bx3 + box_w, box_y + box_h), radius=10, fill=(248, 250, 252), outline=COLOR_ALLIANCE_CRIMSON, width=2)
    draw.text((bx3 + 16, box_y + 14), "3. PIPELINE PLACEMENT", fill=COLOR_ALLIANCE_CRIMSON, font=get_font(16, bold=True))
    draw.text((bx3 + 16, box_y + 44), "Primitive Assembly Stage", fill=COLOR_NAVY_TITLE, font=get_font(17, bold=True))
    draw.text((bx3 + 16, box_y + 74), "BEFORE Rasterization!", fill=COLOR_ALLIANCE_CRIMSON, font=get_font(16, bold=True))
    draw.text((bx3 + 16, box_y + 110), "Saves 50% Fragment Fill-Rate", fill=COLOR_SUCCESS_GREEN, font=get_font(16, bold=True))
    draw.text((bx3 + 16, box_y + 138), "Zero Z-Buffer Contention", fill=COLOR_NAVY_SUB, font=get_font(16, bold=True))
    draw.text((bx3 + 16, box_y + 175), "Eliminates redundant pixel shading,", fill=COLOR_MUTED_TEXT, font=F_CAPTION)
    draw.text((bx3 + 16, box_y + 198), "texture fetches, and memory writes.", fill=COLOR_MUTED_TEXT, font=F_CAPTION)

    # Card 2.2: Proof #1 — The Wireframe Test (y: 1290 to 1960, h: 670)
    c5_y0, c5_y1 = 1290, 1960
    draw_rounded_card(draw, col2_x0, c5_y0, col2_x1, c5_y1)
    draw_card_header(draw, col2_x0, c5_y0, col2_w, "Proof #1: The Wireframe Occlusion Test (Visual Proof)", icon="🔬", accent_color=COLOR_SUCCESS_GREEN)
    
    wf_caption = "Figure 6: In wireframe mode ('M'), Z-buffer occlusion is removed. Turning Culling ON ('C') visually discards all rear wireframe triangles instantly."
    draw_comparison_pair(
        poster, draw,
        col2_x0 + 24, c5_y0 + 80, col2_w - 48, 480,
        "assets/poster_shots/wireframe_culling_off.png",
        "assets/poster_shots/wireframe_culling_on.png",
        "❌ CULLING OFF: Cluttered overlapping rear triangles visible",
        "✅ CULLING ON: Redundant rear triangles vanished! (50% dropped)",
        wf_caption
    )

    # Card 2.3: Proof #2 — Inside-Out Chamber (y: 1980 to 2665, h: 685)
    c6_y0, c6_y1 = 1980, 2665
    draw_rounded_card(draw, col2_x0, c6_y0, col2_x1, c6_y1)
    draw_card_header(draw, col2_x0, c6_y0, col2_w, "Proof #2: Inside-Out Chamber (Surface Orientation)", icon="🚪", accent_color=COLOR_ALLIANCE_CRIMSON)
    
    ch_caption = "Figure 7: Standing INSIDE the chamber at (X:-25, Z:-15). Outward walls face away (N · V < 0). Culling drops them, making walls fully transparent!"
    draw_comparison_pair(
        poster, draw,
        col2_x0 + 24, c6_y0 + 80, col2_w - 48, 480,
        "assets/poster_shots/chamber_culling_off.png",
        "assets/poster_shots/chamber_culling_on.png",
        "❌ CULLING OFF: Inside room — Outward walls rendered (Trapped)",
        "✅ CULLING ON: Inside room — Walls disappear! Outside world visible",
        ch_caption
    )

    # =========================================================================
    # COLUMN 3: High-Poly Benchmark, Analytics & Defense Summary
    # =========================================================================
    # Card 3.1: Proof #3 — 50,000+ Triangle Stress Grid (y: 425 to 1180, h: 755)
    c7_y0, c7_y1 = 425, 1180
    draw_rounded_card(draw, col3_x0, c7_y0, col3_x1, c7_y1)
    draw_card_header(draw, col3_x0, c7_y0, col3_w, "Proof #3: 50,000+ Polygon Benchmark Grid", icon="⚡", accent_color=COLOR_ALLIANCE_CRIMSON)
    
    st_caption = "Figure 8: High-density benchmark grid (100+ modular buildings). Culling cuts frame latency from 12.5 ms down to 6.2 ms (doubling FPS from 80 to 162)."
    draw_comparison_pair(
        poster, draw,
        col3_x0 + 24, c7_y0 + 80, col3_w - 48, 450,
        "assets/poster_shots/stress_culling_off.png",
        "assets/poster_shots/stress_culling_on.png",
        "❌ CULLING OFF: 12.5 ms (80 FPS) • 0% Discarded",
        "✅ CULLING ON: 6.2 ms (162 FPS) • 50.1% Discarded",
        st_caption
    )
    
    # 4 Quick Metric Badges Below
    mb_y = c7_y0 + 580
    mb_w = (col3_w - 48 - 30) // 4
    metrics = [
        ("50.4%", "Latency Drop", COLOR_SUCCESS_GREEN),
        ("2.02X", "FPS Speedup", COLOR_ACCENT_BLUE),
        ("26,140", "Primitives Culled", COLOR_ALLIANCE_CRIMSON),
        ("100%", "Lossless Fidelity", COLOR_NAVY_TITLE)
    ]
    for i, (m_val, m_lbl, m_col) in enumerate(metrics):
        mx = col3_x0 + 24 + i * (mb_w + 10)
        draw.rounded_rectangle((mx, mb_y, mx + mb_w, mb_y + 110), radius=10, fill=(248, 250, 252), outline=m_col, width=2)
        draw.text((mx + mb_w//2, mb_y + 24), m_val, fill=m_col, font=F_STAT_VAL, anchor="mm")
        draw.text((mx + mb_w//2, mb_y + 74), m_lbl, fill=COLOR_MUTED_TEXT, font=F_STAT_LBL, anchor="mm")

    # Card 3.2: Quantitative Benchmark Analytics & Graphs (y: 1200 to 1980, h: 780)
    c8_y0, c8_y1 = 1200, 1980
    draw_rounded_card(draw, col3_x0, c8_y0, col3_x1, c8_y1)
    draw_card_header(draw, col3_x0, c8_y0, col3_w, "Quantitative Benchmark Analytics & Scaling", icon="📊", accent_color=COLOR_ACCENT_BLUE)
    
    chart_w = col3_w - 48
    chart_h = 490
    chart_img = fit_image_inside("assets/diagrams/diagram_benchmark_chart.png", chart_w, chart_h)
    poster.paste(chart_img, (col3_x0 + 24, c8_y0 + 80))
    draw.text((col3_x0 + 24, c8_y0 + 580), "Figure 9: Latency Reduction & FPS Scaling Curves — Empirical GPU throughput under increasing polygon loads", fill=COLOR_NAVY_TITLE, font=F_CAPTION_BOLD)
    
    # Mini summary data table inside card
    table_y = c8_y0 + 615
    draw.rounded_rectangle((col3_x0 + 24, table_y, col3_x1 - 24, c8_y1 - 20), radius=10, fill=(241, 245, 249), outline=COLOR_CARD_BORDER)
    # Table headers
    draw.text((col3_x0 + 40, table_y + 14), "SCENARIO", fill=COLOR_MUTED_TEXT, font=get_font(14, bold=True))
    draw.text((col3_x0 + 440, table_y + 14), "TRIANGLES", fill=COLOR_MUTED_TEXT, font=get_font(14, bold=True))
    draw.text((col3_x0 + 720, table_y + 14), "CULLING OFF", fill=COLOR_ALERT_RED, font=get_font(14, bold=True))
    draw.text((col3_x0 + 1050, table_y + 14), "CULLING ON", fill=COLOR_SUCCESS_GREEN, font=get_font(14, bold=True))
    draw.text((col3_x0 + 1330, table_y + 14), "GAIN", fill=COLOR_ACCENT_BLUE, font=get_font(14, bold=True))
    
    # Row 1: Standard Town
    draw.text((col3_x0 + 40, table_y + 44), "Standard Medieval Town", fill=COLOR_NAVY_TITLE, font=get_font(16, bold=True))
    draw.text((col3_x0 + 440, table_y + 44), "4,612 tris", fill=COLOR_BODY_TEXT, font=get_font(15, bold=False))
    draw.text((col3_x0 + 720, table_y + 44), "16.6 ms (60 FPS)", fill=COLOR_BODY_TEXT, font=get_font(15, bold=False))
    draw.text((col3_x0 + 1050, table_y + 44), "16.6 ms (60 FPS)", fill=COLOR_BODY_TEXT, font=get_font(15, bold=False))
    draw.text((col3_x0 + 1330, table_y + 44), "50.1% culled", fill=COLOR_NAVY_TITLE, font=get_font(15, bold=True))
    
    # Row 2: 50K Stress Grid
    draw.text((col3_x0 + 40, table_y + 76), "Dense High-Poly Stress Grid", fill=COLOR_ALLIANCE_CRIMSON, font=get_font(16, bold=True))
    draw.text((col3_x0 + 440, table_y + 76), "52,180 tris", fill=COLOR_BODY_TEXT, font=get_font(15, bold=False))
    draw.text((col3_x0 + 720, table_y + 76), "12.5 ms (80 FPS)", fill=COLOR_ALERT_RED, font=get_font(15, bold=True))
    draw.text((col3_x0 + 1050, table_y + 76), "6.2 ms (162 FPS)", fill=COLOR_SUCCESS_GREEN, font=get_font(15, bold=True))
    draw.text((col3_x0 + 1330, table_y + 76), "2.02X BOOST", fill=COLOR_ACCENT_BLUE, font=get_font(15, bold=True))

    # Card 3.3: Conclusions & Academic Defense (y: 2000 to 2665, h: 665)
    c9_y0, c9_y1 = 2000, 2665
    draw_rounded_card(draw, col3_x0, c9_y0, col3_x1, c9_y1)
    draw_card_header(draw, col3_x0, c9_y0, col3_w, "Key Conclusions & Capstone Takeaways", icon="🎯", accent_color=COLOR_ALLIANCE_CRIMSON)
    
    takeaways = [
        ("1. Primitive Assembly Elimination:", "Back-face culling eliminates polygons BEFORE fragment rasterization,", COLOR_ALLIANCE_CRIMSON),
        ("", "saving ~50% of pixel fill-rate, fragment shading, and texture bandwidth with zero visual loss.", COLOR_BODY_TEXT),
        ("2. Surface Orientation Criterion:", "Visibility is governed strictly by surface normal orientation relative to", COLOR_ACCENT_BLUE),
        ("", "the camera view vector (N · V < 0), as demonstrated in the Inside-Out Chamber.", COLOR_BODY_TEXT),
        ("3. Industry Standard Foundation:", "Every major real-time 3D engine (Unreal Engine 5, Unity, Frostbite, Godot)", COLOR_NAVY_TITLE),
        ("", "relies on hardware face culling as the primary tier of rendering pipeline optimization.", COLOR_BODY_TEXT),
        ("4. Comprehensive Project Scope:", "Complete software pipeline integrating Blender 5.0 digital content creation,", COLOR_SUCCESS_GREEN),
        ("", "custom OBJ display list loaders, 6-DOF camera flight, and real-time interactive telemetry.", COLOR_BODY_TEXT),
    ]
    ty = c9_y0 + 82
    for t_head, t_body, t_col in takeaways:
        if t_head:
            draw.text((col3_x0 + 24, ty), t_head, fill=t_col, font=F_BODY_BOLD)
            ty += 28
        if t_body:
            draw.text((col3_x0 + 44, ty), t_body, fill=t_col, font=F_BODY)
            ty += 34
            
    # Bottom Defense Note Box
    draw.rounded_rectangle((col3_x0 + 24, c9_y1 - 105, col3_x1 - 24, c9_y1 - 20), radius=10, fill=COLOR_AMBER_BG, outline=COLOR_AMBER_BADGE, width=2)
    draw.text((col3_x0 + 40, c9_y1 - 92), "⭐ VIVA & DEFENSE SUMMARY STATEMENT:", fill=COLOR_AMBER_BADGE, font=get_font(15, bold=True))
    draw.text((col3_x0 + 40, c9_y1 - 65), "\"Back-Face Culling proves that software pipeline optimization can double 3D graphics rendering", fill=COLOR_NAVY_TITLE, font=F_CAPTION_BOLD)
    draw.text((col3_x0 + 40, c9_y1 - 42), "performance without requiring faster hardware or degrading visual quality on watertight models.\"", fill=COLOR_NAVY_TITLE, font=F_CAPTION_BOLD)

    # -------------------------------------------------------------------------
    # Save Image Outputs
    # -------------------------------------------------------------------------
    out_png = "PROJECT_POSTER_LANDSCAPE.png"
    poster.save(out_png, "PNG", dpi=(300, 300))
    print(f" -> Saved {out_png} ({os.path.getsize(out_png)/(1024*1024):.2f} MB)")
    
    # Generate high-resolution PDF
    out_pdf = "PROJECT_POSTER_LANDSCAPE.pdf"
    poster_rgb = poster.convert("RGB")
    poster_rgb.save(out_pdf, "PDF", resolution=300.0)
    print(f" -> Saved {out_pdf} ({os.path.getsize(out_pdf)/(1024*1024):.2f} MB)")
    
    # -------------------------------------------------------------------------
    # Generate PowerPoint Poster (.pptx)
    # -------------------------------------------------------------------------
    out_pptx = "Real_Time_3D_Optimization_Poster.pptx"
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions: 13.333 x 7.5 inches
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6] # Blank slide
    slide = prs.slides.add_slide(slide_layout)
    
    # Insert high-res poster image covering full slide
    slide.shapes.add_picture(out_png, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))
    prs.save(out_pptx)
    print(f" -> Saved {out_pptx} ({os.path.getsize(out_pptx)/(1024*1024):.2f} MB)")
    
    print("=" * 70)
    print(" POSTER GENERATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
