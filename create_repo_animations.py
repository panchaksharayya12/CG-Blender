"""
Generate optimized animated GIFs from PROJECT_DEMO_VIDEO.mp4 for the GitHub README.
"""

import os
import imageio
from PIL import Image

def extract_gif(video_path, output_gif, start_sec, duration_sec, fps_out=12, width=640):
    print(f"Generating {output_gif} from {start_sec}s for {duration_sec}s...")
    reader = imageio.get_reader(video_path)
    fps_in = reader.get_meta_data().get('fps', 30.0)
    
    start_frame = int(start_sec * fps_in)
    total_frames = int(duration_sec * fps_in)
    step = max(1, int(fps_in / fps_out))
    
    frames = []
    for idx in range(start_frame, start_frame + total_frames, step):
        try:
            frame_arr = reader.get_data(idx)
            img = Image.fromarray(frame_arr)
            # Resize preserving aspect ratio
            h = int(img.height * (width / img.width))
            img = img.resize((width, h), Image.Resampling.LANCZOS)
            # Quantize with adaptive palette for crisp small GIFs
            img_quantized = img.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
            frames.append(img_quantized)
        except (IndexError, StopIteration):
            break
            
    reader.close()
    
    if frames:
        os.makedirs(os.path.dirname(output_gif), exist_ok=True)
        # Duration per frame in milliseconds
        frame_duration = int(1000 / fps_out)
        frames[0].save(
            output_gif,
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=frame_duration,
            loop=0
        )
        size_kb = os.path.getsize(output_gif) / 1024
        print(f" -> Created {output_gif} ({len(frames)} frames, {size_kb:.1f} KB)")
    else:
        print(f" -> Failed to extract frames for {output_gif}")

def main():
    video_file = "PROJECT_DEMO_VIDEO.mp4"
    if not os.path.exists(video_file):
        print(f"Error: {video_file} not found!")
        return
        
    out_dir = "assets/animations"
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Environment Flythrough
    extract_gif(video_file, os.path.join(out_dir, "01_environment_flythrough.gif"), 6.0, 6.0, fps_out=12, width=640)
    
    # 2. Proof #1: Wireframe Occlusion Test (showing culling toggle)
    extract_gif(video_file, os.path.join(out_dir, "02_wireframe_culling_proof.gif"), 26.0, 7.0, fps_out=12, width=640)
    
    # 3. Proof #2: Inside-Out Demonstration Chamber
    extract_gif(video_file, os.path.join(out_dir, "03_inside_out_chamber.gif"), 38.0, 7.0, fps_out=12, width=640)
    
    # 4. Proof #3: High-Poly Stress Grid Benchmark
    extract_gif(video_file, os.path.join(out_dir, "04_stress_benchmark.gif"), 50.0, 7.0, fps_out=12, width=640)
    
    print("\nAll animated GIFs successfully generated for GitHub README!")

if __name__ == "__main__":
    main()
