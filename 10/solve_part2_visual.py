"""
Advent of Code 2025 - Day 10 Part 2 - Visual Solver
Joltage Configuration Problem with Terminal Visualization

Shows:
- Current machine being solved with button/target info
- Live counter values vs targets during solution search
- Progress bar and statistics
"""

import re
import time
import sys
from fractions import Fraction

# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'

def clear_screen():
    print('\033[2J\033[H', end='')

def move_cursor(row, col):
    print(f'\033[{row};{col}H', end='')

def hide_cursor():
    print('\033[?25l', end='')

def show_cursor():
    print('\033[?25h', end='')


class Visualizer:
    def __init__(self, total_machines):
        self.total_machines = total_machines
        self.current_machine = 0
        self.solutions_found = 0
        self.total_presses = 0
        self.start_time = time.time()
        
    def draw_header(self):
        move_cursor(1, 1)
        print(f"{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.BOLD}🔧 ADVENT OF CODE 2025 - DAY 10 PART 2: JOLTAGE CONFIGURATION{Colors.RESET}              {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
    
    def draw_progress_bar(self, progress, width=60):
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        pct = progress * 100
        return f"[{bar}] {pct:.1f}%"
    
    def draw_machine_info(self, machine_num, buttons, targets, row=5):
        move_cursor(row, 1)
        elapsed = time.time() - self.start_time
        
        # Machine header
        print(f"{Colors.BOLD}{Colors.YELLOW}┌─────────────────────────────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.YELLOW}│{Colors.RESET} Machine {Colors.BOLD}{machine_num}/{self.total_machines}{Colors.RESET}  │  Elapsed: {elapsed:.1f}s  │  Found: {self.solutions_found}  │  Total: {self.total_presses:,}    {Colors.YELLOW}│{Colors.RESET}")
        print(f"{Colors.YELLOW}└─────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        
        # Progress bar
        progress = machine_num / self.total_machines
        print(f"\n  Progress: {self.draw_progress_bar(progress)}")
        
        # Targets display
        print(f"\n  {Colors.BOLD}Targets:{Colors.RESET} ", end='')
        for i, t in enumerate(targets[:12]):  # Show first 12
            print(f"{Colors.CYAN}{t:3}{Colors.RESET}", end=' ')
        if len(targets) > 12:
            print(f"... (+{len(targets)-12} more)", end='')
        print()
        
        # Buttons info
        print(f"\n  {Colors.BOLD}Buttons:{Colors.RESET} {len(buttons)} available")
    
    def draw_solution_attempt(self, current_values, targets, presses, row=15):
        move_cursor(row, 1)
        print(f"\n  {Colors.BOLD}Current Solution Attempt:{Colors.RESET}                                              ")
        print(f"  Button presses: {Colors.MAGENTA}{presses}{Colors.RESET}                                              ")
        
        print(f"\n  {Colors.BOLD}Counter Values vs Targets:{Colors.RESET}                                             ")
        
        # Show counter comparison (first 10)
        max_show = min(10, len(targets))
        for i in range(max_show):
            current = int(current_values[i]) if current_values[i].denominator == 1 else float(current_values[i])
            target = targets[i]
            
            if current == target:
                status = f"{Colors.GREEN}✓{Colors.RESET}"
                color = Colors.GREEN
            elif current < target:
                status = f"{Colors.YELLOW}↑{Colors.RESET}"
                color = Colors.YELLOW
            else:
                status = f"{Colors.RED}↓{Colors.RESET}"
                color = Colors.RED
            
            bar_width = 20
            if target > 0:
                fill = min(bar_width, int(bar_width * abs(current) / target))
            else:
                fill = 0
            bar = '▓' * fill + '░' * (bar_width - fill)
            
            print(f"    [{i:2}] {color}{current:6.0f}{Colors.RESET} / {target:3} {status}  [{bar}]              ")
        
        if len(targets) > max_show:
            print(f"    ... and {len(targets) - max_show} more counters                                     ")
    
    def draw_found_solution(self, machine_num, presses, row=30):
        move_cursor(row, 1)
        print(f"  {Colors.GREEN}✓ Machine {machine_num} solved with {presses} presses{Colors.RESET}                              ")
    
    def finalize(self, total):
        move_cursor(35, 1)
        elapsed = time.time() - self.start_time
        print(f"\n{Colors.BOLD}{Colors.GREEN}╔══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.GREEN}║{Colors.RESET}  {Colors.BOLD}🎉 COMPLETE! Total minimum button presses: {total:,}{Colors.RESET}                         {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}║{Colors.RESET}     Time elapsed: {elapsed:.2f}s                                                     {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        print()


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
    """Compute Reduced Row Echelon Form using exact fraction arithmetic."""
    if not matrix or not matrix[0]:
        return matrix, []
    
    m = len(matrix)
    n = len(matrix[0])
    
    mat = [[Fraction(matrix[i][j]) for j in range(n)] for i in range(m)]
    
    pivot_cols = []
    pivot_row = 0
    
    for col in range(n - 1):
        max_row = None
        for row in range(pivot_row, m):
            if mat[row][col] != 0:
                max_row = row
                break
        
        if max_row is None:
            continue
        
        mat[pivot_row], mat[max_row] = mat[max_row], mat[pivot_row]
        pivot_cols.append(col)
        
        scale = mat[pivot_row][col]
        for j in range(n):
            mat[pivot_row][j] /= scale
        
        for row in range(m):
            if row != pivot_row and mat[row][col] != 0:
                factor = mat[row][col]
                for j in range(n):
                    mat[row][j] -= factor * mat[pivot_row][j]
        
        pivot_row += 1
        if pivot_row >= m:
            break
    
    return mat, pivot_cols


def solve_machine_visual(buttons: list, targets: list, viz: Visualizer, machine_num: int) -> int:
    """Solve with visualization."""
    n_buttons = len(buttons)
    n_counters = len(targets)
    
    if n_buttons == 0:
        return 0 if all(t == 0 for t in targets) else -1
    
    # Build augmented matrix
    aug = [[0] * (n_buttons + 1) for _ in range(n_counters)]
    for i, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < n_counters:
                aug[counter_idx][i] = 1
    for j in range(n_counters):
        aug[j][n_buttons] = targets[j]
    
    # Get RREF
    mat, pivot_cols = rref(aug)
    
    # Check for inconsistency
    for i in range(len(mat)):
        all_zero = all(mat[i][j] == 0 for j in range(n_buttons))
        if all_zero and mat[i][n_buttons] != 0:
            return -1
    
    # Identify free variables
    free_vars = [i for i in range(n_buttons) if i not in pivot_cols]
    n_free = len(free_vars)
    
    # Build pivot expressions
    pivot_expressions = {}
    for i, pcol in enumerate(pivot_cols):
        if i >= len(mat):
            break
        constant = mat[i][n_buttons]
        coeffs = {}
        for fv in free_vars:
            if mat[i][fv] != 0:
                coeffs[fv] = -mat[i][fv]
        pivot_expressions[pcol] = (constant, coeffs)
    
    def evaluate_solution(free_values):
        x = [Fraction(0)] * n_buttons
        for i, fv in enumerate(free_vars):
            x[fv] = Fraction(free_values[i])
        for pcol, (const, coeffs) in pivot_expressions.items():
            val = const
            for fv, coef in coeffs.items():
                val += coef * x[fv]
            x[pcol] = val
        return x
    
    def compute_counters(x):
        """Compute resulting counter values from button presses."""
        counters = [Fraction(0)] * n_counters
        for i, button in enumerate(buttons):
            for counter_idx in button:
                if counter_idx < n_counters:
                    counters[counter_idx] += x[i]
        return counters
    
    def is_valid_solution(x):
        for val in x:
            if val < 0 or val.denominator != 1:
                return False
        return True
    
    def solution_cost(x):
        return sum(int(val) for val in x)
    
    if n_free == 0:
        x = evaluate_solution([])
        if is_valid_solution(x):
            counters = compute_counters(x)
            viz.draw_solution_attempt(counters, targets, solution_cost(x))
            return solution_cost(x)
        return -1
    
    max_target = max(targets) if targets else 0
    max_free = max_target + 1
    
    best = float('inf')
    iteration = 0
    
    def search(depth, current_values, current_min_cost):
        nonlocal best, iteration
        
        if depth == n_free:
            x = evaluate_solution(current_values)
            if is_valid_solution(x):
                cost = solution_cost(x)
                if cost < best:
                    best = cost
                    # Visualize found solution
                    counters = compute_counters(x)
                    viz.draw_solution_attempt(counters, targets, cost)
                    time.sleep(0.01)  # Brief pause to see updates
            return
        
        fv = free_vars[depth]
        current_free_sum = sum(current_values)
        if current_free_sum >= best:
            return
        
        for val in range(0, max_free + 1):
            if current_free_sum + val >= best:
                break
            
            current_values.append(val)
            
            # Periodic visualization update
            iteration += 1
            if iteration % 1000 == 0:
                x = evaluate_solution(current_values + [0] * (n_free - depth - 1))
                counters = compute_counters(x)
                viz.draw_solution_attempt(counters, targets, solution_cost(x))
            
            possibly_valid = True
            partial_cost = current_free_sum + val
            
            for pcol, (const, coeffs) in pivot_expressions.items():
                partial_val = const
                for fv_idx, fv in enumerate(free_vars[:depth + 1]):
                    if fv in coeffs:
                        partial_val += coeffs[fv] * current_values[fv_idx]
                
                remaining_min = Fraction(0)
                remaining_max = Fraction(0)
                for fv_idx, fv in enumerate(free_vars[depth + 1:], depth + 1):
                    if fv in coeffs:
                        coef = coeffs[fv]
                        if coef > 0:
                            remaining_max += coef * max_free
                        else:
                            remaining_min += coef * max_free
                
                potential_max = partial_val + remaining_max
                
                if potential_max < 0:
                    possibly_valid = False
                    break
                
                if partial_val >= 0 and partial_val.denominator == 1:
                    partial_cost += int(partial_val)
            
            if possibly_valid and partial_cost < best:
                search(depth + 1, current_values, partial_cost)
            
            current_values.pop()
    
    search(0, [], 0)
    
    return best if best < float('inf') else -1


def main():
    with open('10/input.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    viz = Visualizer(len(lines))
    
    clear_screen()
    hide_cursor()
    
    try:
        viz.draw_header()
        
        total = 0
        for i, line in enumerate(lines):
            buttons, targets = parse_line(line)
            
            viz.draw_machine_info(i + 1, buttons, targets)
            
            min_presses = solve_machine_visual(buttons, targets, viz, i + 1)
            
            if min_presses >= 0:
                total += min_presses
                viz.solutions_found += 1
                viz.total_presses = total
                viz.draw_found_solution(i + 1, min_presses)
        
        viz.finalize(total)
        
    finally:
        show_cursor()


if __name__ == "__main__":
    main()
