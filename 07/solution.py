
import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            grid = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("input.txt not found")
        return

    # Find S
    sx, sy = -1, -1
    for r, row in enumerate(grid):
        if 'S' in row:
            sx = row.index('S')
            sy = r
            break
            
    if sx == -1:
        print("S not found")
        return

    # Part 1 Logic
    # beams = {sx}
    # total_splits = 0
    # height = len(grid)
    # width = len(grid[0])
    
    # for y in range(sy + 1, height):
    #     row = grid[y]
    #     next_beams = set()
    #     
    #     for x in beams:
    #         if x < 0 or x >= len(row):
    #             continue
    #             
    #         char = row[x]
    #         if char == '^':
    #             total_splits += 1
    #             next_beams.add(x - 1)
    #             next_beams.add(x + 1)
    #         else:
    #             next_beams.add(x)
    #     
    #     beams = next_beams

    # Part 2 Logic - Count Timelines
    from collections import defaultdict
    
    # Active timelines mapped by x-coordinate: {x: count}
    # Initial state: 1 timeline at S
    active_timelines = defaultdict(int) 
    active_timelines[sx] = 1
    
    completed_timelines = 0
    height = len(grid)
    width = len(grid[0])
    
    # Simulation:
    # process row y, determine where particles go in y+1 (or if they exit)
    # Beams start at S, which is at sy.
    # We iterate from sy. S acts like '.', so it just passes to next row.
    # Note: loop should handle "S" appropriately (handled as default case aka '.')
    
    for y in range(sy, height):
        next_active = defaultdict(int)
        row = grid[y]
        
        for x, count in active_timelines.items():
            # If x is currently in active_timelines, it is IN BOUNDS and valid for row y
            # (Check bounds just in case, though logically should be filtered)
            if not (0 <= x < width):
                # Should have been caught in previous iteration, but for safety:
                completed_timelines += count
                continue
                
            char = row[x]
            
            if char == '^':
                # Split: timelines go to x-1 and x+1 in the NEXT row (y+1)
                # Note: The split adds count to both branches.
                next_active[x - 1] += count
                next_active[x + 1] += count
            else:
                # '.' or 'S': continues downward to x in NEXT row (y+1)
                next_active[x] += count
        
        # Filter for valid bounds and update active_timelines for next iteration
        active_timelines = defaultdict(int)
        for x, count in next_active.items():
            if 0 <= x < width:
                active_timelines[x] = count
            else:
                # Exited the manifold sideways (or strictly, failed to enter next row)
                completed_timelines += count

    # Any particles still in active_timelines after processing the last row 
    # have effectively exited the bottom of the manifold
    completed_timelines += sum(active_timelines.values())

    print(f"Total timelines: {completed_timelines}")

if __name__ == '__main__':
    solve()
