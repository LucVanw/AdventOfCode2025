"""
Advent of Code 2025 - Day 10 Part 2
Joltage Configuration Problem - Pure Python Solution

This solves the Integer Linear Programming problem using:
- Gaussian elimination with exact fraction arithmetic
- Reduced Row Echelon Form (RREF) to find solution space
- Smart search for minimum non-negative integer solutions
"""

import re
from fractions import Fraction
from functools import lru_cache


def parse_line(line: str):
    """Parse a line to extract buttons and joltage requirements."""
    buttons = []
    for match in re.finditer(r'\(([^)]+)\)', line):
        indices = [int(x) for x in match.group(1).split(',')]
        buttons.append(indices)
    
    joltage_match = re.search(r'\{([^}]+)\}', line)
    targets = [int(x) for x in joltage_match.group(1).split(',')]
    
    return buttons, targets


def rref(matrix):
    """
    Compute Reduced Row Echelon Form using exact fraction arithmetic.
    Returns (rref_matrix, pivot_columns).
    """
    if not matrix or not matrix[0]:
        return matrix, []
    
    m = len(matrix)
    n = len(matrix[0])
    
    # Create a copy with Fractions
    mat = [[Fraction(matrix[i][j]) for j in range(n)] for i in range(m)]
    
    pivot_cols = []
    pivot_row = 0
    
    for col in range(n - 1):  # Don't pivot on augmented column
        # Find pivot
        max_row = None
        for row in range(pivot_row, m):
            if mat[row][col] != 0:
                max_row = row
                break
        
        if max_row is None:
            continue
        
        # Swap rows
        mat[pivot_row], mat[max_row] = mat[max_row], mat[pivot_row]
        
        pivot_cols.append(col)
        
        # Scale pivot row
        scale = mat[pivot_row][col]
        for j in range(n):
            mat[pivot_row][j] /= scale
        
        # Eliminate all other rows (both above and below for RREF)
        for row in range(m):
            if row != pivot_row and mat[row][col] != 0:
                factor = mat[row][col]
                for j in range(n):
                    mat[row][j] -= factor * mat[pivot_row][j]
        
        pivot_row += 1
        if pivot_row >= m:
            break
    
    return mat, pivot_cols


def solve_machine(buttons: list, targets: list) -> int:
    """
    Solve for minimum button presses using RREF and smart search.
    """
    n_buttons = len(buttons)
    n_counters = len(targets)
    
    if n_buttons == 0:
        return 0 if all(t == 0 for t in targets) else -1
    
    # Build augmented matrix [A | b]
    # A[j][i] = 1 if button i affects counter j
    aug = [[0] * (n_buttons + 1) for _ in range(n_counters)]
    for i, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < n_counters:
                aug[counter_idx][i] = 1
    for j in range(n_counters):
        aug[j][n_buttons] = targets[j]
    
    # Get RREF
    mat, pivot_cols = rref(aug)
    
    # Check for inconsistency (0 = non-zero in any row)
    for i in range(len(mat)):
        all_zero = all(mat[i][j] == 0 for j in range(n_buttons))
        if all_zero and mat[i][n_buttons] != 0:
            return -1  # No solution
    
    # Identify free variables
    free_vars = [i for i in range(n_buttons) if i not in pivot_cols]
    n_free = len(free_vars)
    
    # For each pivot variable, express it in terms of free variables
    # pivot_var = rhs - sum(coef * free_var)
    pivot_expressions = {}  # pivot_col -> (constant, {free_var: coef})
    
    for i, pcol in enumerate(pivot_cols):
        if i >= len(mat):
            break
        constant = mat[i][n_buttons]
        coeffs = {}
        for fv in free_vars:
            if mat[i][fv] != 0:
                coeffs[fv] = -mat[i][fv]  # Negate because we move to RHS
        pivot_expressions[pcol] = (constant, coeffs)
    
    def evaluate_solution(free_values):
        """Given values for free variables, compute full solution."""
        x = [Fraction(0)] * n_buttons
        
        # Set free variables
        for i, fv in enumerate(free_vars):
            x[fv] = Fraction(free_values[i])
        
        # Compute pivot variables
        for pcol, (const, coeffs) in pivot_expressions.items():
            val = const
            for fv, coef in coeffs.items():
                val += coef * x[fv]
            x[pcol] = val
        
        return x
    
    def is_valid_solution(x):
        """Check if solution has all non-negative integers."""
        for val in x:
            if val < 0 or val.denominator != 1:
                return False
        return True
    
    def solution_cost(x):
        """Total button presses."""
        return sum(int(val) for val in x)
    
    if n_free == 0:
        # Unique solution
        x = evaluate_solution([])
        if is_valid_solution(x):
            return solution_cost(x)
        return -1
    
    # For cases with free variables, we need to search
    # Key insight: free variables must be non-negative integers,
    # and they affect pivot variables linearly
    
    # Find bounds for free variables
    # For each pivot expression: constant + sum(coef * free_var) >= 0
    # This gives constraints on free variables
    
    # Estimate max value any free variable could take
    max_target = max(targets) if targets else 0
    max_free = max_target + 1
    
    # For small number of free variables, use iterative deepening
    best = float('inf')
    
    # Use branch and bound with pruning
    def search(depth, current_values, current_min_cost):
        nonlocal best
        
        if depth == n_free:
            x = evaluate_solution(current_values)
            if is_valid_solution(x):
                cost = solution_cost(x)
                if cost < best:
                    best = cost
            return
        
        fv = free_vars[depth]
        
        # Determine bounds for this free variable based on current partial solution
        # and constraints from pivot expressions
        
        min_val = 0
        max_val = max_free
        
        # Pruning: if current sum of free vars >= best, stop
        current_free_sum = sum(current_values)
        if current_free_sum >= best:
            return
        
        for val in range(min_val, max_val + 1):
            # Early pruning
            if current_free_sum + val >= best:
                break
            
            # Check if this value could lead to valid solution
            # by checking partial pivot evaluations
            current_values.append(val)
            
            # Quick validity check for already determined pivot vars
            possibly_valid = True
            partial_cost = current_free_sum + val
            
            for pcol, (const, coeffs) in pivot_expressions.items():
                # Compute partial value (only for free vars we've set)
                partial_val = const
                known_coeffs = True
                for fv_idx, fv in enumerate(free_vars[:depth + 1]):
                    if fv in coeffs:
                        partial_val += coeffs[fv] * current_values[fv_idx]
                
                # Check remaining free vars contribution
                remaining_min = Fraction(0)
                remaining_max = Fraction(0)
                for fv_idx, fv in enumerate(free_vars[depth + 1:], depth + 1):
                    if fv in coeffs:
                        coef = coeffs[fv]
                        if coef > 0:
                            remaining_max += coef * max_free
                        else:
                            remaining_min += coef * max_free
                
                # Check if any valid value is possible
                potential_min = partial_val + remaining_min
                potential_max = partial_val + remaining_max
                
                if potential_max < 0:
                    possibly_valid = False
                    break
                
                # Estimate minimum contribution to cost from this pivot
                if potential_min >= 0 and potential_min.denominator == 1:
                    partial_cost += int(potential_min)
            
            if possibly_valid and partial_cost < best:
                search(depth + 1, current_values, partial_cost)
            
            current_values.pop()
    
    # Start search
    search(0, [], 0)
    
    return best if best < float('inf') else -1


def main():
    with open('10/input.txt', 'r') as f:
        lines = f.readlines()
    
    total = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        buttons, targets = parse_line(line)
        min_presses = solve_machine(buttons, targets)
        
        if min_presses < 0:
            print(f"Machine {i+1}: No solution found!")
        else:
            total += min_presses
    
    print(f"Total minimum button presses: {total}")


if __name__ == "__main__":
    main()
