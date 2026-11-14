from dataclasses import dataclass, field

@dataclass
class Maze:
    width: int
    height: int
    grid: list[list[int]] = field(init=False)
    def __post_init__(self) -> None:
        closed_maze = []
        ALL_WALLS = 0b1111
        for _ in range(self.height):
            closed_grid = [ALL_WALLS] * self.width
            closed_maze.append(closed_grid)
        self.grid = closed_maze
    def range_judge(self, coordinates: tuple[int, int]) -> bool:
        x, y = coordinates
        return (0 <= x < self.width) and (0 <= y < self.height)
        # if bit[0] == 1:
        # 3 * 2
        # 1111, 1111, 1111
        # 1111, 1111, 1111
        # 北東南西
        # (0, 0) (1, 0) (2, 0)
        # 2進数を左から読むなら西南東北


if __name__ == '__main__':
    maze = Maze(3, 2)
    result = maze.range_judge((0, 1))
    print(result)
    result = maze.range_judge((2, 1))
    print(result)
    result = maze.range_judge((3, 0))
    print(result) # False
    result = maze.range_judge((0, -1))
    print(result) # False
    result = maze.range_judge((0, 0))
    print(result)
    print(maze.grid)
# [
#     [1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1],
#     [],
#     [],
# ]
# 
# [1, 1, 1, 0]
