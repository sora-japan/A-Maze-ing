from dataclasses import dataclass, field


@dataclass
class DummyMaze:
    """開発用のダミー迷路。Aの Maze 完成までの代用品"""
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    grid: list[list[int]]
    pattern_cells: set[tuple[int, int]] = field(default_factory=set)
    path: str = ""

    def cell(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        bit = {"N": 0, "E": 1, "S": 2, "W": 3}[direction]
        return bool(self.cell(x, y) & (1 << bit))

    def solve(self) -> str:
        return self.path


def make_small_maze() -> DummyMaze:
    """3*3"""
    grid = [
        [0b1101, 0b0101, 0b0011],
        [0b1001, 0b0101, 0b0110],
        [0b1100, 0b0101, 0b0111]
    ]
    return DummyMaze(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(2, 2),
        grid=grid,
        path="EESWWSEE"
    )


def make_medium_maze() -> DummyMaze:
    """5*5"""
