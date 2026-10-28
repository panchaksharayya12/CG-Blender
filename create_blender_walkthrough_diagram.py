from PIL import Image, ImageDraw, ImageFont

w, h = 1280, 720
img = Image.new('RGB', (w, h), (15, 23, 42))
draw = ImageDraw.Draw(img)

font_title = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 28)
font_h2 = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 17)
font_body = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 14)
font_mono = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 13)

# Header
draw.rounded_rectangle((30, 20, w - 30, 95), radius=10, fill=(30, 41, 59), outline=(56, 189, 248), width=2)
draw.text((w // 2, 45), 'HOW TO DEMONSTRATE & EXPLAIN IN BLENDER 5.0', fill=(255, 255, 255), font=font_title, anchor='mm')
draw.text((w // 2, 75), 'Step-by-Step Examiner Walkthrough: Normal Auditing, Real-Time Culling & Walk Navigation', fill=(148, 163, 184), font=font_body, anchor='mm')

# 4 Step Cards
cards = [
    ('STEP 1: Viewport Shading', 'Press [Z] -> Material Preview', 
     ['Switch Viewport Shading to MATERIAL PREVIEW.',
      'Allows real-time inspection of PBR materials,',
      'colors, and reflections without rendering delay.',
      'Shortcut: Press Z -> Material Preview (Sphere 3).'], 
     (59, 130, 246)),
     
    ('STEP 2: Face Orientation', 'Overlays -> Face Orientation', 
     ['Click Overlays dropdown (top-right rings icon).',
      'Check [x] Face Orientation.',
      '* BLUE = Front faces (CCW normals -> Rendered)',
      '* RED  = Back faces (CW normals -> Culled)',
      'Audits normal consistency across all meshes.'], 
     (16, 185, 129)),
     
    ('STEP 3: Backface Culling', 'Shading -> Backface Culling', 
     ['Click Shading dropdown arrow (next to spheres).',
      'Check [x] Backface Culling.',
      'Watch rear surfaces immediately disappear!',
      'Replicates exact hardware behavior of OpenGL',
      'glEnable(GL_CULL_FACE) in real time.'], 
     (245, 158, 11)),
     
    ('STEP 4: First-Person Walk', 'Press [Shift + ~] Walk Nav', 
     ['Activates game-style camera in Blender:',
      '* [W, A, S, D] : Walk through town streets',
      '* [Mouse] : Look around pitch and yaw',
      '* [Space] : Teleport / Jump | [V] : Gravity',
      'Walk inside the Inside-Out Chamber live!'], 
     (168, 85, 247))
]

cw = 280
ch = 405
y0 = 115
for i, (title, sub, lines, col) in enumerate(cards):
    x0 = 40 + i * (cw + 25)
    draw.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=8, fill=(30, 41, 59), outline=col, width=2)
    # Header box inside card
    draw.rounded_rectangle((x0, y0, x0 + cw, y0 + 62), radius=8, fill=col)
    draw.text((x0 + cw//2, y0 + 22), title, fill=(255, 255, 255), font=font_h2, anchor='mm')
    draw.text((x0 + cw//2, y0 + 46), sub, fill=(241, 245, 249), font=font_mono, anchor='mm')
    # Body text
    ly = y0 + 80
    for line in lines:
        if line.startswith('* BLUE'):
            draw.text((x0 + 12, ly), line, fill=(96, 165, 250), font=font_body)
        elif line.startswith('* RED'):
            draw.text((x0 + 12, ly), line, fill=(248, 113, 113), font=font_body)
        elif line.startswith('*'):
            draw.text((x0 + 12, ly), line, fill=(226, 232, 240), font=font_body)
        else:
            draw.text((x0 + 12, ly), line, fill=(203, 213, 225), font=font_body)
        ly += 26

# Bottom examiner speech card
draw.rounded_rectangle((30, 540, w - 30, 700), radius=10, fill=(15, 23, 42), outline=(100, 116, 139), width=2)
draw.text((50, 555), 'WHAT TO EXPLAIN TO THE EXAMINER WORD-FOR-WORD:', fill=(251, 191, 36), font=font_h2)
speech = (
    '"In modern game engines, 3D meshes are modeled with outward-facing normals and Counter-Clockwise (CCW) winding. '
    'Here in Blender 5.0, enabling Face Orientation proves all exterior surfaces are Blue (front-facing). '
    'When we enable Backface Culling in Blender, rear polygons are immediately skipped, identical to glEnable(GL_CULL_FACE) in our OpenGL engine. '
    'When we walk inside the Inside-Out Chamber, the walls face away from the camera and vanish, proving culling operates on surface orientation!"'
)

# word wrap speech
words = speech.split(' ')
cur_line = ''
sy = 585
for word in words:
    test_line = cur_line + (' ' if cur_line else '') + word
    bbox = draw.textbbox((50, sy), test_line, font=font_body)
    if bbox[2] > w - 60:
        draw.text((50, sy), cur_line, fill=(241, 245, 249), font=font_body)
        cur_line = word
        sy += 25
    else:
        cur_line = test_line
if cur_line:
    draw.text((50, sy), cur_line, fill=(241, 245, 249), font=font_body)

img.save('diagram_blender_walkthrough.png')
print('diagram_blender_walkthrough.png generated successfully!')
