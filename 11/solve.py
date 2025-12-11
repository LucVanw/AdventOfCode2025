#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 11
Count all paths from 'you' to 'out' in a directed graph.
"""

from collections import defaultdict
import sys

def parse_input(filename):
    """Parse the input file and build the graph."""
    graph = defaultdict(list)
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Format: "source: dest1 dest2 dest3"
            parts = line.split(': ')
            source = parts[0]
            destinations = parts[1].split() if len(parts) > 1 else []
            
            for dest in destinations:
                graph[source].append(dest)
    
    return graph

def count_paths(graph, start, end, memo=None):
    """Count all paths from start to end using memoization."""
    if memo is None:
        memo = {}
    
    if start == end:
        return 1
    
    if start in memo:
        return memo[start]
    
    if start not in graph:
        return 0
    
    total = 0
    for neighbor in graph[start]:
        total += count_paths(graph, neighbor, end, memo)
    
    memo[start] = total
    return total

def main():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    graph = parse_input(filename)
    
    # Count all paths from 'you' to 'out'
    path_count = count_paths(graph, 'you', 'out')
    
    print(f"Number of paths from 'you' to 'out': {path_count}")

if __name__ == '__main__':
    main()
