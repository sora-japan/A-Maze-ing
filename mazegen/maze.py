from dataclasses import dataclass, field

ALL_WALLS = 0b1111

# ビット番号 0 ~ 3 の順番 北東南西
# 2進数の桁([1, 1, 0, 1])に直した際は,西南東北
DIRECTION_BITS = {
    'N': 0,
    'E': 1,
    'S': 2,
    'W': 3,
}

DIRECTION_DELTAS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
}

OPPOSITE_DIRECTION = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E',
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

        Raises:
            ValueError: 座標が迷路の範囲外の場合。
        """
        if not self.range_judge(coordinates):
            raise ValueError(f'座標が範囲外です: {coordinates}')
        x, y = coordinates
        grid_num = self.grid[y][x]
        bit = DIRECTION_BITS[direction]
        mask = 1 << bit
        return (grid_num & mask) != 0

    def neighbor(
        self, coordinates: tuple[int, int], direction: str
    ) -> tuple[int, int]:
        """指定したマスから、指定した方向に1マス進んだ先の座標を返す。

        範囲の判定はしないため、盤面の外の座標を返すことがある。
        使う側で range_judge を呼び、範囲内かを確かめること。

        Args:
            coordinates: 元のマスの座標 (x, y)。
            direction: 進む方向。'N'、'E'、'S'、'W' のいずれか。

        Returns:
            隣のマスの座標 (x, y)。
        """
        x, y = coordinates
        dx, dy = DIRECTION_DELTAS[direction]
        new_coordinates = (x + dx, y + dy)
        return new_coordinates

    def remove_wall(
            self, coordinates: tuple[int, int], direction: str
    ) -> None:
        """指定したマスの、指定した方向の壁を消す。

        隣のマスの反対側の壁も同時に消し、2つのマスの情報を一致させる。
        外周の壁は消せない。範囲の確認は grid を書き換える前に行うため、
        例外が出たときは grid は変更されない。

        Args:
            coordinates: マスの座標 (x, y)。
            direction: 消す壁の方向。'N'、'E'、'S'、'W' のいずれか。

        Raises:
            ValueError: 座標が迷路の範囲外の場合、または
                指定した壁が外周の壁の場合。
        """
        if not self.range_judge(coordinates):
            raise ValueError(f'座標が範囲外です: {coordinates}')
        new_coordinates = self.neighbor(coordinates, direction)
        if not self.range_judge(new_coordinates):
            raise ValueError(
                f'外周の壁は消せません: {new_coordinates}'
            )
        self._clear_wall_bit(coordinates, direction)
        new_direction = OPPOSITE_DIRECTION[direction]
        self._clear_wall_bit(new_coordinates, new_direction)

    def _clear_wall_bit(
            self, coordinates: tuple[int, int], direction: str
    ) -> None:
        """1つのマスの、指定した方向のビットだけを 0 にする。

        隣のマスは更新せず、範囲の確認もしない。
        remove_wall の中だけで使う。

        Args:
            coordinates: マスの座標 (x, y)。範囲内であること。
            direction: 消す壁の方向。'N'、'E'、'S'、'W' のいずれか。
        """
        x, y = coordinates
        grid_num = self.grid[y][x]
        bit = DIRECTION_BITS[direction]
        mask = 1 << bit
        self.grid[y][x] = grid_num & ~mask


if __name__ == '__main__':
    maze = Maze(3, 2)
    result = maze.range_judge((0, 1))
    print(result)
    result = maze.range_judge((2, 1))
    print(result)
    result = maze.range_judge((3, 0))
    print(result)
    result = maze.range_judge((0, -1))
    print(result)
    result = maze.range_judge((0, 0))
    print(result)
    print(maze.grid)
    print('===has_wallメソッドの確認===')
    bit = 1 << 3
    print(bit)
    print(0b1000)
    print(maze.has_wall((0, 0), 'N'))
    print(maze.has_wall((2, 0), 'N'))
    print('===neighborメソッドの確認===')
    print(maze.neighbor((1, 1), 'N'))
    print(maze.neighbor((1, 1), 'E'))
    print(maze.neighbor((1, 1), 'S'))
    print(maze.neighbor((1, 1), 'W'))
    print('===remove_wallメソッドの確認===')
    maze.remove_wall((0, 0), 'E')
    print(maze.grid)
