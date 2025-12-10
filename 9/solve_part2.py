
import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return

    poly_points = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            x, y = map(int, line.split(','))
            poly_points.append((x, y))
        except ValueError:
            continue

    if not poly_points:
        return

    n_poly = len(poly_points)
    
    # Pre-calculate edges
    edges = []
    for i in range(n_poly):
        p1 = poly_points[i]
        p2 = poly_points[(i + 1) % n_poly]
        edges.append((p1, p2))

    # Generate all candidate rectangles
    candidates = []
    for i in range(n_poly):
        for j in range(i + 1, n_poly):
            x1, y1 = poly_points[i]
            x2, y2 = poly_points[j]
            
            # Form rectangle
            rx1, rx2 = min(x1, x2), max(x1, x2)
            ry1, ry2 = min(y1, y2), max(y1, y2)
            
            w = rx2 - rx1 + 1
            h = ry2 - ry1 + 1
            area = w * h
            candidates.append({'area': area, 'rect': (rx1, rx2, ry1, ry2)})
    
    # Sort by area descending
    candidates.sort(key=lambda x: x['area'], reverse=True)
    
    def is_point_in_poly(x, y):
        # Ray casting algorithm
        inside = False
        j = n_poly - 1
        for k in range(n_poly):
            xi, yi = poly_points[k]
            xj, yj = poly_points[j]
            
            intersect = ((yi > y) != (yj > y)) and \
                        (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside
            j = k
        return inside

    def segments_intersect(p1, p2, q1, q2):
        # Check if segment p1-p2 intersects segment q1-q2
        # Standard vector cross product approach
        
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
            
        return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

    def is_segment_in_rect_interior(p1, p2, rect):
        rx1, rx2, ry1, ry2 = rect
        px1, py1 = p1
        px2, py2 = p2
        
        # If segment is vertical
        if px1 == px2:
             x = px1
             # Check if x is strictly between rx1 and rx2
             if rx1 < x < rx2:
                 # Check if overlap in Y
                 s_ymin, s_ymax = min(py1, py2), max(py1, py2)
                 if max(ry1, s_ymin) < min(ry2, s_ymax):
                     return True
        
        # If segment is horizontal
        elif py1 == py2:
            y = py1
            # Check if y is strictly between ry1 and ry2
            if ry1 < y < ry2:
                # Check if overlap in X
                s_xmin, s_xmax = min(px1, px2), max(px1, px2)
                if max(rx1, s_xmin) < min(rx2, s_xmax):
                    return True
        else:
             # Diagonal segments shouldn't happen based on problem desc ("same row or same column")
             # But if they did, we'd need full intersection test with rect interior
             pass
             
        return False

    for cand in candidates:
        area = cand['area']
        rect = cand['rect'] # rx1, rx2, ry1, ry2
        rx1, rx2, ry1, ry2 = rect
        
        # 1. Quick validation: Center point must be inside polygon
        cx = (rx1 + rx2) / 2
        cy = (ry1 + ry2) / 2
        
        # To avoid floating point issues with ray casting exactly on edges (though center shouldn't be on edge typically unless width=1),
        # let's pick a point slightly offset if needed or just use float. Ray cast usually handles float.
        # However, for width=1 or height=1, center is on boundary. If rect is single line, it is valid if that line is part of boundary or inside.
        # But wait, "rectangle uses red tiles for two of its opposite corners".
        # If area is width*height, and it's 1-wide, it's a line.
        # The prompt examples show proper 2D rectangles mainly, but "thin rectangle" is mentioned.
        # "thin rectangle with an area of only 6 between 7,3 and 2,3" -> (2,3) to (7,3). H=1, W=6.
        # In this case, center is on the line y=3.
        # Ray casting with point ON boundary is tricky.
        # Better heuristic: ALL 4 corners must be IsInside or OnBoundary.
        # AND Center IsInside or OnBoundary.
        # AND No edge intersects interior.
        
        # Actually simplest check:
        # A rectangle is inside if it doesn't intersect the polygon boundary strictly, and at least one point is inside.
        # STRICT intersection means an edge of the polygon goes THROUGH the rectangle.
        
        intersects_boundary = False
        for p1, p2 in edges:
            if is_segment_in_rect_interior(p1, p2, rect):
                intersects_boundary = True
                break
        
        if intersects_boundary:
            continue
            
        # Check if center is inside (or on boundary)
        # We need a robust point-in-poly.
        # Ray casting usually returns true for strictly inside.
        # If the rectangle is 1x1, or thin, center might be on edge.
        # Let's check center.
        if is_point_in_poly(cx, cy):
             print(f"Max area: {area}")
             print(f"Rect: {rx1},{ry1},{rx2},{ry2}")
             return

    print("No valid rectangle found")

if __name__ == "__main__":
    solve()
