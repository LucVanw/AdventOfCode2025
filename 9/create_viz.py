
import json

def create_viz():
    # Read polygon points
    points = []
    try:
        with open('input.txt', 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    points.append({'x': int(parts[0]), 'y': int(parts[1])})
    except FileNotFoundError:
        print("input.txt not found")
        return

    # Solution rectangle from previous run
    # Rect: 5548,50137,94901,67598
    rect_min_x = 5548
    rect_min_y = 50137
    rect_max_x = 94901
    rect_max_y = 67598
    
    solution_rect = {
        'x': rect_min_x,
        'y': rect_min_y,
        'w': rect_max_x - rect_min_x,
        'h': rect_max_y - rect_min_y
    }

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advent of Code 2025 - Day 9 Visualization</title>
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1e1e1e;
            color: #d4d4d4;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            color: #61afef;
        }}
        #canvas-container {{
            background-color: #282c34;
            border: 1px solid #3e4451;
            padding: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            border-radius: 8px;
        }}
        canvas {{
            display: block;
        }}
        .legend {{
            margin-top: 15px;
            display: flex;
            gap: 20px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .color-box {{
            width: 16px;
            height: 16px;
            border-radius: 4px;
        }}
        .info {{
            margin-top: 10px;
            font-size: 0.9em;
            color: #abb2bf;
        }}
    </style>
</head>
<body>
    <h1>AoC 2025 Day 9: Polygon & Max Rectangle</h1>
    <div id="canvas-container">
        <canvas id="vizCanvas"></canvas>
    </div>
    <div class="legend">
        <div class="legend-item">
            <div class="color-box" style="background-color: rgba(97, 175, 239, 0.2); border: 2px solid #61afef;"></div>
            <span>Polygon Boundary</span>
        </div>
        <div class="legend-item">
            <div class="color-box" style="background-color: rgba(224, 108, 117, 0.5); border: 2px solid #e06c75;"></div>
            <span>Max Rectangle</span>
        </div>
    </div>
    <div class="info">
        Rectangle Area: {solution_rect['w'] * solution_rect['h']:,}<br>
        Coordinates: ({solution_rect['x']}, {solution_rect['y']}) to ({solution_rect['x'] + solution_rect['w']}, {solution_rect['y'] + solution_rect['h']})
    </div>

    <script>
        const points = {json.dumps(points)};
        const solution = {json.dumps(solution_rect)};

        const canvas = document.getElementById('vizCanvas');
        const ctx = canvas.getContext('2d');

        // Set canvas size
        const width = 800;
        const height = 600;
        canvas.width = width;
        canvas.height = height;

        // Calculate bounding box
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        points.forEach(p => {{
            minX = Math.min(minX, p.x);
            minY = Math.min(minY, p.y);
            maxX = Math.max(maxX, p.x);
            maxY = Math.max(maxY, p.y);
        }});

        // Add some padding
        const padding = 20;
        const dataWidth = maxX - minX;
        const dataHeight = maxY - minY;
        
        // Calculate scale to fit
        const scaleX = (width - 2 * padding) / dataWidth;
        const scaleY = (height - 2 * padding) / dataHeight;
        const scale = Math.min(scaleX, scaleY);
        
        const offsetX = padding + (width - 2 * padding - dataWidth * scale) / 2;
        const offsetY = padding + (height - 2 * padding - dataHeight * scale) / 2;

        function toScreen(x, y) {{
            // Flip Y axis because canvas Y increases downwards, but usually cartesian is upwards
            // But here the input coordinates likely mimic screen or map coords, let's keep Y as is but map to screen space.
            // If data Y increases upwards, we might want to flip.
            // Let's assume standard image coords (Y down).
            return {{
                x: offsetX + (x - minX) * scale,
                y: height - (offsetY + (y - minY) * scale) // Flip Y just in case to match standard math orientation if needed, or:
                // Actually usually graphics Y is down. Let's stick to simple mapping first.
                // y: offsetY + (y - minY) * scale
            }};
        }}
        
        // Wait, standard plots usually put (0,0) at bottom left.
        // Let's deduce from coords. They are all positive.
        // Let's map MinY to Bottom of canvas (Height - margin) and MaxY to Top (margin).
        function toScreenFlipped(x, y) {{
             return {{
                x: offsetX + (x - minX) * scale,
                y: height - (offsetY + (y - minY) * scale) 
            }};
        }}

        // Draw Grid/Axes (Optional - skipping for clarity)

        // Draw Solution Rectangle
        ctx.fillStyle = 'rgba(224, 108, 117, 0.5)';
        ctx.strokeStyle = '#e06c75';
        ctx.lineWidth = 2;

        const p1 = toScreenFlipped(solution.x, solution.y);
        const p2 = toScreenFlipped(solution.x + solution.w, solution.y + solution.h);
        
        // Screen coords for rect
        const rx = Math.min(p1.x, p2.x);
        const ry = Math.min(p1.y, p2.y);
        const rw = Math.abs(p1.x - p2.x);
        const rh = Math.abs(p1.y - p2.y);

        ctx.beginPath();
        ctx.rect(rx, ry, rw, rh);
        ctx.fill();
        ctx.stroke();

        // Draw Polygon
        ctx.strokeStyle = '#61afef';
        ctx.lineWidth = 2;
        ctx.beginPath();
        const start = toScreenFlipped(points[0].x, points[0].y);
        ctx.moveTo(start.x, start.y);
        
        for (let i = 1; i < points.length; i++) {{
            const p = toScreenFlipped(points[i].x, points[i].y);
            ctx.lineTo(p.x, p.y);
        }}
        ctx.closePath();
        ctx.stroke();
        
        // Draw points
        ctx.fillStyle = '#98c379';
        points.forEach(p => {{
            const sp = toScreenFlipped(p.x, p.y);
            ctx.beginPath();
            ctx.arc(sp.x, sp.y, 2, 0, Math.PI * 2);
            ctx.fill();
        }});

    </script>
</body>
</html>
"""

    with open('viz.html', 'w') as f:
        f.write(html_content)
    print("viz.html created successfully.")

if __name__ == "__main__":
    create_viz()
