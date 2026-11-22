class WriteError(Exception):
    """迷路のファイル書き出しで発生するエラー"""


def write_maze(maze, path: str) -> None:
    """迷路を課題指定のフォーマットでファイルに書き出す。

    出力形式（課題 IV.5）:
        1〜height 行目: 各セルの 4bit 壁情報を 16 進数 1 桁で並べた文字列。
            各桁のビット配置は N=bit0, E=bit1, S=bit2, W=bit3、1 で壁、0 で通路。
        空行 1 本
        入口座標 (x,y) 形式
        出口座標 (x,y) 形式
        最短経路 (N/E/S/W の文字列)

    全行末尾は '\\n' で終わる。既存ファイルは上書きされる。

    Args:
        maze: 書き出し対象の迷路オブジェクト。
            cell(x, y)、entry、exit、solve() を持つ必要がある。
        path: 出力ファイルのパス。

    Raises:
        WriteError: ファイルの書き出しに失敗した場合
            （パスが開けない、書き込み権限なし、ディレクトリ指定、
            ディスク容量不足、close 時のフラッシュ失敗など）。
    """
    try:
        with open(path, "w") as f:
            for y in range(maze.height):
                row = ""
                for x in range(maze.width):
                    row += f"{maze.cell(x, y):x}"
                f.write(row + "\n")

            f.write("\n")

            f.write(f"{maze.entry[0]},{maze.entry[1]}\n")

            f.write(f"{maze.exit[0]},{maze.exit[1]}\n")

            f.write(f"{maze.solve()}\n")
    except OSError as e:
        raise WriteError(f"{path}: cannot write file: {e}") from e
