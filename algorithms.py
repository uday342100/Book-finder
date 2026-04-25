"""Pathfinding algorithms for Smart Library Navigator."""

from __future__ import annotations

from collections import deque
import heapq
from typing import Dict, Optional

from map import get_neighbors


def reconstruct_path(
    came_from: Dict[tuple[int, int], Optional[tuple[int, int]]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    """Reconstruct path from parent references."""
    if goal not in came_from:
        return []

    path = [goal]
    current = goal
    while current != start:
        parent = came_from[current]
        if parent is None:
            return []
        path.append(parent)
        current = parent
    path.reverse()
    return path


def bfs(
    grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
) -> list[tuple[int, int]]:
    """Breadth-First Search for shortest path in unweighted grid."""
    queue = deque([start])
    came_from: Dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        for neighbor in get_neighbors(current, grid):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    return reconstruct_path(came_from, start, goal)


def dfs(
    grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
) -> list[tuple[int, int]]:
    """
    Depth-First Search path.

    DFS does not guarantee shortest path but is included for comparison.
    """
    stack = [start]
    came_from: Dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            break

        for neighbor in get_neighbors(current, grid):
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)

    return reconstruct_path(came_from, start, goal)


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(
    grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
) -> list[tuple[int, int]]:
    """A* algorithm for shortest path in grid."""
    frontier: list[tuple[int, tuple[int, int]]] = []
    heapq.heappush(frontier, (0, start))

    came_from: Dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}
    cost_so_far: Dict[tuple[int, int], int] = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break

        for neighbor in get_neighbors(current, grid):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + manhattan(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, goal)


def run_algorithm(
    algorithm_name: str,
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    """Dispatch selected algorithm."""
    algorithm_name = algorithm_name.strip().upper()
    if algorithm_name == "BFS":
        return bfs(grid, start, goal)
    if algorithm_name == "DFS":
        return dfs(grid, start, goal)
    if algorithm_name in {"A*", "A-STAR", "ASTAR"}:
        return a_star(grid, start, goal)
    raise ValueError(f"Unsupported algorithm: {algorithm_name}")
