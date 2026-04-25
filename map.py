"""Grid map module for Smart Library Navigator."""

from __future__ import annotations

from typing import Iterable


# 0 = walkable, 1 = obstacle (racks/walls)
LIBRARY_GRID = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
]

ENTRANCE = (0, 0)


def in_bounds(coord: tuple[int, int], grid: list[list[int]]) -> bool:
    """Check whether coordinate is inside the grid."""
    r, c = coord
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def is_walkable(coord: tuple[int, int], grid: list[list[int]]) -> bool:
    """Check whether cell is walkable."""
    r, c = coord
    return in_bounds(coord, grid) and grid[r][c] == 0


def get_neighbors(coord: tuple[int, int], grid: list[list[int]]) -> Iterable[tuple[int, int]]:
    """Yield valid 4-directional neighbors."""
    r, c = coord
    candidates = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    for candidate in candidates:
        if is_walkable(candidate, grid):
            yield candidate
