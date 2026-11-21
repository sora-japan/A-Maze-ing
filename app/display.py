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


def _cell_row(maze: DummyMaze, y: int) -> str:
    """y 行目のセル中身ラインを生成する。

    各セルについて左の壁（西に壁があれば '|'、なければ ' '）と
    セル内部の 2 文字分を並べ、最後に右端の壁を付けて返す。

    Args:
        maze: 描画対象の迷路オブジェクト。
        y: 対象となるセル行のインデックス（0 始まり）。

    Returns:
        '|        |' のようなセル中身ラインの文字列。
    """
    row = ""
    for x in range(maze.width):
        row += "|" if maze.has_wall(x, y, "W") else " "
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


def to_text(maze: DummyMaze) -> str:
    """迷路を 2 文字/セル方式のテキスト表現に変換して返す。

    各 y 行について '壁ライン → セル中身ライン' の 2 行を並べ、
    最後に下辺の壁ラインを付加して 1 枚の絵として組み立てる。
    基本は ASCII 文字で描画するが、将来 ANSI カラーや Unicode 罫線を
    混ぜる拡張も見据えてテキスト全般を扱う想定。

    Args:
        maze: 描画対象の迷路オブジェクト。

    Returns:
        改行区切りで 1 枚にまとまった迷路のテキスト表現。
    """
    lines: list[str] = []
    for y in range(maze.height):
        lines.append(_wall_row(maze, y))
        lines.append(_cell_row(maze, y))
    lines.append(_bottom_row(maze))
    return "\n".join(lines)


if __name__ == "__main__":
    from tests.fixtures.dummy_maze import make_small_maze
    print(to_text(make_small_maze()))
