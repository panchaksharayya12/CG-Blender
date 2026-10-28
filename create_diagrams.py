"""
Generates high-resolution diagrams for the PowerPoint presentation:
1. diagram_culling_math.png - Visualizing Vector Dot Product & Screen Winding Order
2. diagram_benchmark_chart.png - Performance Benchmark comparison charts
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set dark theme styling
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'Arial'

def create_culling_math_diagram():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), facecolor='#0F172A')
    
    # --- SUBPLOT 1: Vector Dot Product Test ---
    ax1.set_facecolor('#1E293B')
    ax1.set_xlim(-1, 11)
    ax1.set_ylim(-1, 10)
    ax1.axis('off')
    ax1.set_title("1. Vector Dot Product Test (World Space)", color='#38BDF8', fontsize=14, weight='bold', pad=15)
    
    # Camera position
    ax1.plot(5, 8.5, marker='o', markersize=12, color='#FBBF24')
    ax1.text(5, 9.1, "Camera (Observer)", color='#FBBF24', fontsize=11, weight='bold', ha='center')
    
    # Front-facing surface (Left)
    ax1.plot([0.5, 4.0], [3.5, 3.5], color='#10B981', linewidth=4)
    ax1.text(2.25, 2.7, "Front-Facing Surface", color='#10B981', fontsize=10, weight='bold', ha='center')
    # Normal N
    ax1.annotate("", xy=(2.25, 5.5), xytext=(2.25, 3.5),
                 arrowprops=dict(arrowstyle="->", color='#38BDF8', lw=2.5))
    ax1.text(2.25, 5.8, "Normal (N)", color='#38BDF8', fontsize=10, weight='bold', ha='center')
    # View ray V
    ax1.annotate("", xy=(2.25, 3.5), xytext=(5, 8.5),
                 arrowprops=dict(arrowstyle="->", color='#FBBF24', lw=2, linestyle='--'))
    # Dot product label
    ax1.text(2.25, 1.4, "N · V > 0  (Angle < 90°)\n[ RENDER FRONT FACE ]",
             color='#10B981', fontsize=10, weight='bold', ha='center',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='#064E3B', edgecolor='#10B981', lw=1.5))
    
    # Back-facing surface (Right)
    ax1.plot([6.0, 9.5], [3.5, 3.5], color='#EF4444', linewidth=4)
    ax1.text(7.75, 2.7, "Back-Facing Surface", color='#EF4444', fontsize=10, weight='bold', ha='center')
    # Normal N (pointing downward away from camera)
    ax1.annotate("", xy=(7.75, 1.5), xytext=(7.75, 3.5),
                 arrowprops=dict(arrowstyle="->", color='#38BDF8', lw=2.5))
    ax1.text(7.75, 0.9, "Normal (N)", color='#38BDF8', fontsize=10, weight='bold', ha='center')
    # View ray V
    ax1.annotate("", xy=(7.75, 3.5), xytext=(5, 8.5),
                 arrowprops=dict(arrowstyle="->", color='#FBBF24', lw=2, linestyle='--'))
    # Dot product label
    ax1.text(7.75, 5.5, "N · V <= 0  (Angle >= 90°)\n[ CULL / DISCARD FACE ]",
             color='#EF4444', fontsize=10, weight='bold', ha='center',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='#7F1D1D', edgecolor='#EF4444', lw=1.5))
    
    # --- SUBPLOT 2: Screen-Space Winding Order ---
    ax2.set_facecolor('#1E293B')
    ax2.set_xlim(-1, 11)
    ax2.set_ylim(-1, 10)
    ax2.axis('off')
    ax2.set_title("2. Screen Winding Order Test (OpenGL Rasterizer)", color='#38BDF8', fontsize=14, weight='bold', pad=15)
    
    # Triangle 1: CCW (Front Face)
    tri1_pts = np.array([[2, 4], [4, 4], [3, 7.5]])
    tri1 = patches.Polygon(tri1_pts, closed=True, facecolor='#065F46', edgecolor='#10B981', lw=2.5)
    ax2.add_patch(tri1)
    ax2.text(2, 3.4, "V0", color='#FFFFFF', fontsize=10, weight='bold', ha='center')
    ax2.text(4, 3.4, "V1", color='#FFFFFF', fontsize=10, weight='bold', ha='center')
    ax2.text(3, 7.8, "V2", color='#FFFFFF', fontsize=10, weight='bold', ha='center')
    
    # Circular CCW arrow
    arc1 = patches.Arc((3, 5.1), 1.6, 1.6, angle=0, theta1=30, theta2=330, color='#34D399', lw=2)
    ax2.add_patch(arc1)
    ax2.annotate("", xy=(2.2, 5.5), xytext=(2.2, 5.0),
                 arrowprops=dict(arrowstyle="->", color='#34D399', lw=2))
    ax2.text(3, 1.4, "Counter-Clockwise (CCW)\nSigned Area > 0\n[ FRONT FACE => RENDER ]",
             color='#10B981', fontsize=10, weight='bold', ha='center',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='#064E3B', edgecolor='#10B981', lw=1.5))
    
    # Triangle 2: CW (Back Face)
    tri2_pts = np.array([[7, 4], [9, 4], [8, 7.5]])
    tri2 = patches.Polygon(tri2_pts, closed=True, facecolor='#881337', edgecolor='#EF4444', lw=2.5)
    ax2.add_patch(tri2)
    ax2.text(7, 3.4, "V0", color='#FFFFFF', fontsize=10, weight='bold', ha='center')
    ax2.text(9, 3.4, "V2", color='#FFFFFF', fontsize=10, weight='bold', ha='center')
    ax2.text(8, 7.8, "V1", color='#FFFFFF', fontsize=10, weight='bold', ha='center')
    
    # Circular CW arrow
    arc2 = patches.Arc((8, 5.1), 1.6, 1.6, angle=0, theta1=30, theta2=330, color='#F87171', lw=2)
    ax2.add_patch(arc2)
    ax2.annotate("", xy=(8.8, 5.5), xytext=(8.8, 5.0),
                 arrowprops=dict(arrowstyle="->", color='#F87171', lw=2))
    ax2.text(8, 1.4, "Clockwise (CW)\nSigned Area < 0\n[ BACK FACE => CULL ]",
             color='#EF4444', fontsize=10, weight='bold', ha='center',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='#7F1D1D', edgecolor='#EF4444', lw=1.5))
    
    plt.tight_layout()
    plt.savefig('diagram_culling_math.png', dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Created diagram_culling_math.png")

def create_benchmark_chart():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0F172A')
    
    categories = ['Base Scene (4.6K Tris)', 'Stress Grid (50K+ Tris)']
    
    # Chart 1: Frame Latency (ms) - Lower is better!
    ax1.set_facecolor('#1E293B')
    x = np.arange(len(categories))
    width = 0.35
    
    cull_off_latency = [3.8, 14.5]
    cull_on_latency  = [2.2, 7.8]
    
    rects1 = ax1.bar(x - width/2, cull_off_latency, width, label='Culling OFF (Wasteful)', color='#EF4444', edgecolor='#B91C1C')
    rects2 = ax1.bar(x + width/2, cull_on_latency, width, label='Culling ON (Optimized)', color='#10B981', edgecolor='#047857')
    
    ax1.set_ylabel('Frame Time / Latency (ms) [Lower is Better]', color='#F8FAFC', fontsize=11)
    ax1.set_title('Frame Latency Reduction (ms)', color='#38BDF8', fontsize=13, weight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, color='#E2E8F0', fontsize=10, weight='bold')
    ax1.legend(facecolor='#0F172A', edgecolor='#475569', labelcolor='#F8FAFC')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.tick_params(colors='#E2E8F0')
    
    # Data labels
    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(f'{h} ms', xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', color='#FCA5A5', weight='bold')
    for rect in rects2:
        h = rect.get_height()
        ax1.annotate(f'{h} ms', xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', color='#6EE7B7', weight='bold')
    
    # Chart 2: Geometry Pipeline Workload (Triangles Sent to Rasterizer)
    ax2.set_facecolor('#1E293B')
    workload_off = [4612, 50200]
    workload_on  = [2306, 25100]
    
    rects3 = ax2.bar(x - width/2, workload_off, width, label='Culling OFF (100% Rendered)', color='#EF4444', edgecolor='#B91C1C')
    rects4 = ax2.bar(x + width/2, workload_on, width, label='Culling ON (50% Culled)', color='#10B981', edgecolor='#047857')
    
    ax2.set_ylabel('Primitives Shaded & Rasterized [Lower is Better]', color='#F8FAFC', fontsize=11)
    ax2.set_title('Rasterizer & Pixel Shader Workload', color='#38BDF8', fontsize=13, weight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, color='#E2E8F0', fontsize=10, weight='bold')
    ax2.legend(facecolor='#0F172A', edgecolor='#475569', labelcolor='#F8FAFC')
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.tick_params(colors='#E2E8F0')
    
    for rect in rects3:
        h = rect.get_height()
        ax2.annotate(f'{h:,}', xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', color='#FCA5A5', weight='bold')
    for rect in rects4:
        h = rect.get_height()
        ax2.annotate(f'{h:,} (-50%)', xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', color='#6EE7B7', weight='bold')
                     
    plt.tight_layout()
    plt.savefig('diagram_benchmark_chart.png', dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Created diagram_benchmark_chart.png")

if __name__ == '__main__':
    create_culling_math_diagram()
    create_benchmark_chart()
