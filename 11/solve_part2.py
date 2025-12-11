#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 11 Part 2
Count all paths from 'svr' to 'out' that visit both 'dac' and 'fft'.
"""

from collections import defaultdict
from functools import lru_cache
import sys

def parse_input(filename):
    """Parse the input file and build the graph."""
    graph = defaultdict(list)
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(': ')
            source = parts[0]
            destinations = parts[1].split() if len(parts) > 1 else []
            
            for dest in destinations:
                graph[source].append(dest)
    
    return graph

def count_paths_with_requirements(graph, start, end, required):
    """
    Count paths from start to end that visit all required nodes.
    Uses memoization with state = (current_node, visited_required_bitmask)
    """
    required = tuple(sorted(required))
    req_to_bit = {r: 1 << i for i, r in enumerate(required)}
    full_mask = (1 << len(required)) - 1
    
    # Convert graph to tuple for hashability
    graph_tuple = {k: tuple(v) for k, v in graph.items()}
    
    memo = {}
    
    def dfs(node, visited_mask):
        """Return count of paths from node to end with given visited state."""
        if node == end:
            # Only count if all required nodes have been visited
            return 1 if visited_mask == full_mask else 0
        
        state = (node, visited_mask)
        if state in memo:
            return memo[state]
        
        if node not in graph_tuple:
            memo[state] = 0
            return 0
        
        total = 0
        for neighbor in graph_tuple[node]:
            new_mask = visited_mask
            if neighbor in req_to_bit:
                new_mask |= req_to_bit[neighbor]
            total += dfs(neighbor, new_mask)
        
        memo[state] = total
        return total
    
    # Check if start is a required node
    initial_mask = req_to_bit.get(start, 0)
    return dfs(start, initial_mask)

def main():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    graph = parse_input(filename)
    
    # Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'
    required_nodes = {'dac', 'fft'}
    path_count = count_paths_with_requirements(graph, 'svr', 'out', required_nodes)
    
    print(f"Number of paths from 'svr' to 'out' visiting both 'dac' and 'fft': {path_count}")

if __name__ == '__main__':
    main()
