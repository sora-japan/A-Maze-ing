from dataclasses import dataclass, field


ALL_WALLS = 0b1111

# 北東南西
DIRECTION_BITS = {
    'N': 0,
    'E': 1,
    'S': 2,
    'W': 3,
}

@dataclass
class Maze:
    """各マスの壁を4bitで持つ、長方形の迷路の盤面。

    ビット0が北、ビット1が東、ビット2が南、ビット3が西を表す。
    ビットが1なら壁が閉じている、0なら開いている。

    Attributes:
        width: 横方向（x）のマスの数。
        height: 縦方向（y）のマスの数。
        grid: 各マスの壁の値。grid[y][x] の順で参照する。
    """
    width: int
    height: int
    grid: list[list[int]] = field(init=False)
    def __post_init__(self) -> None:
        """すべてのマスを、4方向の壁が閉じた状態で初期化する。"""
        closed_maze = []
        for _ in range(self.height):
            closed_grid = [ALL_WALLS] * self.width
            closed_maze.append(closed_grid)
        self.grid = closed_maze
    def range_judge(self, coordinates: tuple[int, int]) -> bool:
        """座標が迷路の範囲内にあるかを判定する。

        Args:
            coordinates: マスの座標 (x, y)。

        Returns:
            範囲内なら True、範囲外なら False。
        """
        x, y = coordinates
        return (0 <= x < self.width) and (0 <= y < self.height)
    def has_wall(self, coordinates: tuple[int, int], direction: str) -> bool:
        """指定したマスの、指定した方向の壁が閉じているかを判定する。

        Args:
            coordinates: マスの座標 (x, y)。
            direction: 調べる方向。'N'、'E'、'S'、'W' のいずれか。

        Returns:
            壁が閉じていれば True、開いていれば False。
        """
        x, y = coordinates
        grid_num = self.grid[y][x]
        bit = DIRECTION_BITS[direction]
        mask = 1 << bit
        return (grid_num & mask) != 0


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
    bit = 1 << 3
    print(bit)
    print(0b1000)



# [
#     [1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1],
#     [],
#     [],
# ]
# 
# [1, 1, 1, 0]
