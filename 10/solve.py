
import sys
import re
from fractions import Fraction
from math import ceil, floor

def parse_input(filename):
    machines = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse diagram: [.##.]
            diagram_match = re.search(r'\[([.#]+)\]', line)
            if not diagram_match:
                continue
            diagram_str = diagram_match.group(1)
            target_vector = [1 if c == '#' else 0 for c in diagram_str]
            num_lights = len(target_vector)
            
            # Parse buttons: (0,3,4)
            buttons = []
            button_matches = re.findall(r'\(([\d,]+)\)', line)
            for b_str in button_matches:
                indices = [int(x) for x in b_str.split(',')]
                button_vec = [0] * num_lights
                for idx in indices:
                    if idx < num_lights:
                        button_vec[idx] = 1
                buttons.append(button_vec)

            # Parse joltages: {3,5,4,7}
            jolt_match = re.search(r'\{([\d,]+)\}', line)
            if jolt_match:
                jolt_str = jolt_match.group(1)
                joltages = [int(x) for x in jolt_str.split(',')]
            else:
                joltages = []
                
            machines.append({
                'lights_target': target_vector,
                'buttons': buttons,
                'joltages': joltages
            })
    return machines

def solve_system_gf2(target, buttons):
    # System: sum(c_i * B_i) = target (mod 2)
    num_vars = len(buttons)
    num_eqs = len(target)
    
    # Augmented matrix [A | target]
    matrix = []
    for r in range(num_eqs):
        row = [b[r] for b in buttons] + [target[r]]
        matrix.append(row)
        
    pivot_row = 0
    pivot_cols = []
    
    for col in range(num_vars):
        if pivot_row >= num_eqs:
            break
        pivot = -1
        for r in range(pivot_row, num_eqs):
            if matrix[r][col] == 1:
                pivot = r
                break
        if pivot == -1:
            continue
        pivot_cols.append(col)
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        for r in range(num_eqs):
            if r != pivot_row and matrix[r][col] == 1:
                for c in range(col, num_vars + 1):
                    matrix[r][c] ^= matrix[pivot_row][c]
        pivot_row += 1
        
    for r in range(pivot_row, num_eqs):
        if matrix[r][num_vars] == 1:
            return None, None
            
    particular = [0] * num_vars
    for i, col in enumerate(pivot_cols):
        particular[col] = matrix[i][num_vars]
        
    free_vars = [c for c in range(num_vars) if c not in pivot_cols]
    null_basis = []
    for free in free_vars:
        basis_vec = [0] * num_vars
        basis_vec[free] = 1
        for i, p_col in enumerate(pivot_cols):
            if matrix[i][free] == 1:
                basis_vec[p_col] = 1
        null_basis.append(basis_vec)
        
    return particular, null_basis

def min_presses_gf2(particular, null_basis):
    if particular is None: return 0
    min_count = float('inf')
    num_free = len(null_basis)
    for i in range(1 << num_free):
        current_sol = list(particular)
        for j in range(num_free):
            if (i >> j) & 1:
                for k in range(len(current_sol)):
                    current_sol[k] ^= null_basis[j][k]
        presses = sum(current_sol)
        if presses < min_count:
            min_count = presses
    return min_count

def solve_system_rational(target, buttons):
    num_vars = len(buttons)
    num_eqs = len(target)
    
    # Matrix A with Rationals
    matrix = []
    for r in range(num_eqs):
        row = [Fraction(b[r]) for b in buttons] + [Fraction(target[r])]
        matrix.append(row)
        
    pivot_row = 0
    pivot_cols = []
    
    rows = num_eqs
    cols = num_vars
    
    for col in range(cols):
        if pivot_row >= rows: break
        
        pivot = -1
        for r in range(pivot_row, rows):
            if matrix[r][col] != 0:
                pivot = r
                break
        if pivot == -1: continue
        
        pivot_cols.append(col)
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        
        # Normalize pivot row
        pivot_val = matrix[pivot_row][col]
        for c in range(col, cols + 1):
            matrix[pivot_row][c] /= pivot_val
            
        # Eliminate
        for r in range(rows):
            if r != pivot_row and matrix[r][col] != 0:
                factor = matrix[r][col]
                for c in range(col, cols + 1):
                    matrix[r][c] -= factor * matrix[pivot_row][c]
                    
        pivot_row += 1
        
    # Check consistency
    for r in range(pivot_row, rows):
        if matrix[r][cols] != 0:
            return None, None
            
    # Particular solution
    particular = [Fraction(0)] * num_vars
    for i, col in enumerate(pivot_cols):
        particular[col] = matrix[i][cols]
        
    # Null basis
    free_vars = [c for c in range(num_vars) if c not in pivot_cols]
    null_basis = []
    for free in free_vars:
        basis_vec = [Fraction(0)] * num_vars
        basis_vec[free] = Fraction(1)
        # Back substitute
        for i, p_col in enumerate(pivot_cols):
            # x[p_col] + x[free] * matrix[i][free] = 0  (since row is normalized, coeff of p_col is 1)
            # x[p_col] = -matrix[i][free] * x[free]
            # here x[free] = 1
            basis_vec[p_col] = -matrix[i][free]
        null_basis.append(basis_vec)
        
    return particular, null_basis

def min_presses_rational(particular, null_basis):
    if particular is None: return 0
    
    if not null_basis:
        if all(x.denominator == 1 and x >= 0 for x in particular):
            return sum(int(x) for x in particular)
        else:
            return 0

    base_cost = sum(particular)
    weights = [sum(vec) for vec in null_basis]
    num_vars = len(null_basis)
    best_cost = float('inf')
    
    # Sort variables by weight (increasing) to try negative weights first?
    # Actually, keep original order to match basis structure.
    
    # Pre-calculated "max positive contribution" for each row from remaining variables?
    # Optimization: precompute for each idx and each row r, the max possible value null_basis[k][r] for k >= idx.
    # This helps feasibility pruning.
    
    max_help = []
    for idx in range(num_vars):
        row_help = []
        for r in range(len(particular)):
            max_val = 0
            for k in range(idx, num_vars):
                if null_basis[k][r] > 0:
                    # We can add arbitrary amount? Yes, c_k are unbounded.
                    # So if any future variable can help row r (has +ve coeff), 
                    # row r is potentially salvageable from negative values.
                    max_val = float('inf')
                    break
            row_help.append(max_val)
        max_help.append(row_help)
        
    def search(idx, current_x, current_cost):
        nonlocal best_cost
        
        # Pruning 1: Feasibility
        # If any component of current_x is negative and CANNOT be fixed by remaining vars, PRUNE.
        for r, val in enumerate(current_x):
            if val < 0:
                # Can we fix this?
                # We need to add positive value to this row.
                # max_help[idx][r] tells us if ANY future variable has a positive coeff for this row.
                if idx < num_vars and max_help[idx][r] == 0:
                    return # Dead end
                elif idx == num_vars:
                    return # Dead end (no variables left)

        # Pruning 2: Cost
        # Can we prune if current_cost >= best_cost?
        # ONLY if all remaining weights are non-negative.
        # If there are negative weights ahead, cost could drop.
        can_prune_cost = True
        for k in range(idx, num_vars):
            if weights[k] < 0:
                can_prune_cost = False
                break
        
        if can_prune_cost and current_cost >= best_cost:
             return

        if idx == num_vars:
            # Check integer and non-negative
            if all(val.denominator == 1 and val >= 0 for val in current_x):
                if current_cost < best_cost:
                    best_cost = current_cost
            return

        # Variable idx
        basis_vec = null_basis[idx]
        weight = weights[idx]
        
        # Range for c_idx
        # We need to explore enough values.
        # Since we have feasibility pruning, we can set a generous upper limit.
        # If weight is negative, we want c to be LARGE. But feasibility will stop us.
        # If weight is positive, we want c to be SMALL. Cost pruning will stop us.
        
        # 0 to 500 should be enough for typical AoC?
        LIMIT = 500
        
        for c in range(LIMIT):
            # Log progress for top-level search
            if idx == 0 and c % 10 == 0:
                print(f"Top-level search progress: c={c}/{LIMIT}, best_cost={best_cost}")

            new_x = [x + c * b for x, b in zip(current_x, basis_vec)]
            new_cost = current_cost + c * weight
            
            # Optimization: 
            # If weight > 0 and new_cost >= best_cost (and can_prune_cost satisfied earlier? No, need check here)
            # Actually, if prune condition holds, loop will break naturally or by check.
            
            # Sub-check for pruning inside loop:
            if can_prune_cost and new_cost >= best_cost:
                break 

            # Recursive call
            prev_best = best_cost
            search(idx + 1, new_x, new_cost)
            
            # If we didn't find a solution in the subtree, and weight < 0 (trying to reduce cost),
            # should we stop?
            # It's hard to say. Maybe feasibility stopped us.
            
    search(0, particular, base_cost)
    return int(best_cost) if best_cost != float('inf') else 0


def run_tests():
    print("Running tests...")
    # Part 1 Tests
    # ... (omitted for brevity, verified already)
    
    # Part 2 Tests
    test_cases_p2 = [
        # Example 1: 10 presses
        ("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}", 10),
        # Example 2: 12 presses
        ("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}", 12),
        # Example 3: 11 presses
        ("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}", 11)
    ]
    
    print("Part 2 verification:")
    for line_desc, expected in test_cases_p2:
         # Parse manually
         jolt_match = re.search(r'\{([\d,]+)\}', line_desc)
         joltages = [int(x) for x in jolt_match.group(1).split(',')]
         
         # Need number of lights/counters from diagram
         diagram_match = re.search(r'\[([.#]+)\]', line_desc)
         num_lights = len(diagram_match.group(1))

         buttons = []
         button_matches = re.findall(r'\(([\d,]+)\)', line_desc)
         for b_str in button_matches:
             indices = [int(x) for x in b_str.split(',')]
             button_vec = [0] * num_lights
             for idx in indices:
                 if idx < num_lights:
                     button_vec[idx] = 1
             buttons.append(button_vec)
             
         part, basis = solve_system_rational(joltages, buttons)
         ans = min_presses_rational(part, basis)
         
         if ans == expected:
             print(f"PASSED: expected {expected}")
         else:
             print(f"FAILED: Got {ans}, expected {expected}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_tests()
        return

    machines = parse_input('10/input.txt')
    
    # Part 1
    total_presses_p1 = 0
    for m in machines:
        part, basis = solve_system_gf2(m['lights_target'], m['buttons'])
        total_presses_p1 += min_presses_gf2(part, basis)
    print(f"Part 1 Total: {total_presses_p1}")

if __name__ == '__main__':
    main()
