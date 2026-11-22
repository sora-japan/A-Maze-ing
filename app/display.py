from tests.fixtures.dummy_maze import DummyMaze


def _wall_row(maze: DummyMaze, y: int) -> str:
    """y 行目のセルの北側に沿った壁ラインを生成する。

    各セルについて北に壁があれば '--'、通路なら '  ' を並べ、
    '+' で区切った 1 本の文字列を返す。

    Args:
        maze: 描画対象の迷路オブジェクト。
        y: 対象となるセル行のインデックス（0 始まり）。

    Returns:
        '+--+--+--+' のような壁ラインの文字列。
    """
    row = ""
    for x in range(maze.width):
        row += "+"
        row += "--" if maze.has_wall(x, y, "N") else "  "
    row += "+"
    return row


def _cell_row(maze: DummyMaze, y: int, path_cells: set[tuple[int, int]] | None = None) -> str:
    """y 行目のセル中身ラインを生成する。

    各セルについて左の壁（西に壁があれば '|'、なければ ' '）と、
    セル内部の 2 文字分を並べ、最後に右端の壁を付けて返す。
    セル内部の優先順位:
        1. 入口 → 'S '
        2. 出口 → 'E '
        3. 経路（path_cells に含まれる）→ '. '
        4. それ以外 → 空白 2 文字

    Args:
        maze: 描画対象の迷路オブジェクト。
        y: 対象となるセル行のインデックス（0 始まり）。
        path_cells: 経路に含まれるセル座標の集合。None または空集合なら
            経路マークを表示しない。

    Returns:
        '|S       |' のようなセル中身ラインの文字列。
    """
    row = ""
    for x in range(maze.width):
        row += "|" if maze.has_wall(x, y, "W") else " "
        if (x, y) == maze.entry:
            row += "S "
        elif (x, y) == maze.exit:
            row += "E "
        elif path_cells and (x, y) in path_cells:
            row += ". "
        else:
            row += "  "
    row += "|"
    return row


def _bottom_row(maze: DummyMaze) -> str:
    """迷路の下辺となる壁ラインを生成する。

    最下段セル（y = height - 1）の南側の壁情報から 1 本の壁ラインを作る。

    Args:
        maze: 描画対象の迷路オブジェクト。

    Returns:
        '+--+--+--+' のような下辺の壁ライン文字列。
    """
    y = maze.height - 1
    row = ""
    for x in range(maze.width):
        row += "+"
        row += "--" if maze.has_wall(x, y, "S") else "  "
    row += "+"
    return row


def _path_cells(maze: DummyMaze) -> set[tuple[int, int]]:
    """入口から出口への経路に含まれるセル座標の集合を返す。

    maze.solve() が返す方向文字列 'EESWWSEE...' を 1 文字ずつ辿り、
    入口から順に通過したセル座標を集合に記録する。
    描画側は (x, y) in cells の高速判定だけで経路セルか判別できる。

    座標系の前提:
        画面座標系（原点は左上、y は下方向が正）を使用する。
        MOVE_MAP の (dx, dy) は 1 マス進む時の座標変化量。
            N (北・上方向) → (0, -1)  y が減る
            E (東・右方向) → (1, 0)   x が増える
            S (南・下方向) → (0, 1)   y が増える
            W (西・左方向) → (-1, 0)  x が減る

    Args:
        maze: 経路情報 (solve) と入口 (entry) を持つ迷路オブジェクト。

    Returns:
        経路上のセル座標 (x, y) の集合。入口セルも含む。
    """
    MOVE_MAP = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    x, y = maze.entry
    cells = {(x, y)}
    for direction in maze.solve():
        dx, dy = MOVE_MAP[direction]
        x += dx
        y += dy
        cells.add((x, y))
    return cells


def to_text(maze: DummyMaze, show_path: bool = False) -> str:
    """迷路を 2 文字/セル方式のテキスト表現に変換して返す。

    各 y 行について '壁ライン → セル中身ライン' の 2 行を並べ、
    最後に下辺の壁ラインを付加して 1 枚の絵として組み立てる。
    show_path が True の場合、入口から出口への経路を '. ' で重ね表示する。
    基本は ASCII 文字で描画するが、将来 ANSI カラーや Unicode 罫線を
    混ぜる拡張も見据えてテキスト全般を扱う想定。

    Args:
        maze: 描画対象の迷路オブジェクト。
        show_path: True の時、_path_cells で算出した経路セルに '. ' を
            重ねて表示する。入口 'S' と出口 'E' は経路より優先される。

    Returns:
        改行区切りで 1 枚にまとまった迷路のテキスト表現。
    """
    lines: list[str] = []
    path_cells = _path_cells(maze) if show_path else set()
    for y in range(maze.height):
        lines.append(_wall_row(maze, y))
        lines.append(_cell_row(maze, y, path_cells))
    lines.append(_bottom_row(maze))
    return "\n".join(lines)


if __name__ == "__main__":
    from tests.fixtures.dummy_maze import make_small_maze
    print(to_text(make_small_maze(), show_path=True))
