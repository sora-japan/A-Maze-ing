# A-Maze-ing ファイルごとの役割（叩き台）

## 全体のルール

**依存の向きは一方通行にする：`a_maze_ing.py` → `app/` → `mazegen/`**

- `mazegen/` から `app/` を import しない。
- `mazegen/` の中では `print`、ファイル操作、`sys.exit` を使わない。

これを守ることで、第VI章の「別のプロジェクトで再利用できるモジュール」が自然に満たされる。

## ディレクトリ構成

```
a_maze_ing.py              # B  エントリーポイント
config.txt                 # B  デフォルト設定
mazegen/                   # A  再利用パッケージ（wheel に入るのはここだけ）
  __init__.py
  maze.py
  generator.py
  pattern.py               # 追加
  solver.py
app/                       # B
  __init__.py              # 追加
  config.py
  writer.py
  display.py
  menu.py                  # display から分離
tests/
  checker.py               # B7
  test_*.py
pyproject.toml             # A
MAZEGEN.md                 # A  パッケージのドキュメント（追加）
Makefile                   # B
.gitignore                 # B（追加）
README.md                  # 共同
LICENSE.md                 # 共同
mazegen-1.0.0-py3-none-any.whl
```

## ファイルごとの役割

### `mazegen/`（Aさん）

| ファイル | 役割 | やらないこと |
|---|---|---|
| `__init__.py` | 外に見せるものだけを公開する（`MazeGenerator`、`Maze`、例外クラス、`__version__`） | ロジックを書く |
| `maze.py` | `Maze` クラス。4bit のグリッド、幅と高さ、入口と出口、パターンのセルを持つ。壁の取得・追加・削除（隣のセルも同時に更新）、範囲判定、隣接セルの取得 | 乱数を使う、16進数の文字列を作る |
| `pattern.py` | 「42」のビットマップの定義と、配置位置の計算。置けないサイズなら「置けない」と返す | 迷路の生成 |
| `generator.py` | `MazeGenerator` クラス。引数の検証、`random.Random(seed)` の管理、パターンの配置、DFS による生成、PERFECT=False のときのループ追加。完成した `Maze` を返す | `print` する（パターンを省略したことは属性などで伝える） |
| `solver.py` | BFS で最短経路を求め、`"NESW..."` 形式の文字列を返す関数 | 迷路を変更する |

### `app/` とトップレベル（Bさん）

| ファイル | 役割 | やらないこと |
|---|---|---|
| `a_maze_ing.py` | 引数のチェック、全体の流れ（設定を読む → 生成 → 書き出し → メニュー）、例外を捕まえてメッセージを出し、終了コードを返す | 細かいロジックを持つ（各モジュールを呼ぶだけ） |
| `app/config.py` | `ConfigError`、`MazeConfig`、パーサー。文法、必須キー、型、範囲、「入口と出口が範囲内で、互いに異なる」の検証 | パターンとの重なりの判定（パターンの位置を知らないため） |
| `app/writer.py` | `Maze` を16進数の行に変換し、空行、入口、出口、経路を書き出す。ファイルは `with` で開く | 表示、生成 |
| `app/display.py` | `Maze` と表示の設定（経路の表示/非表示、色）から、表示用の**文字列を返す** | `input` や `print` を使う |
| `app/menu.py` | 対話ループ。再生成、経路の切り替え、色の変更、終了。Ctrl-C と EOF の処理 | 描画の中身を作る |
| `tests/checker.py` | メモリ上の `Maze` を直接チェックする（壁の整合性、3x3 の開放エリア、連結性、行き止まり、ループ） | 提出物の動作に関わる（`app/` には置かない） |

## 未決事項と、この案での置き場所

| | 論点 | この案での扱い | 状態 |
|---|---|---|---|
| (a) | 「42」パターンを中央に置くこと（A2）と、PERFECT=False で中央を通路にすること（A5、課題 IV.4）が衝突する | 解決するのは `pattern.py` | **未決**（二人で検討） |
| (b) | パターンを省略したときのエラーメッセージ（課題 IV.4）を誰が出すか | `generator.py` が「省略した」という情報を持ち、`a_maze_ing.py` が表示する | 案 |
| (c) | 16進数への変換をどこに置くか | `writer.py`（課題 VI：パッケージの構造は出力形式と同じでなくてよい） | 案 |
| (d) | ENTRY と EXIT のチェックをどこでやるか | 範囲内か・異なるかは `config.py` と `generator.py` の両方で確認（`mazegen` を直接使う人がいるため）。パターンとの重なりは `generator.py` だけで確認 | 案 |
| (e) | 課題 VI の「a unique class」をどう満たすか | 利用者の入口は `MazeGenerator` の1つだけ。`Maze` は生成結果として返ってくるオブジェクトという位置づけ | 案 |

合意できたものから「状態」を「決定」に変え、README の技術的な判断の節に理由と一緒に書く。

## ビルドまわりで確認すること

- [ ] `pyproject.toml` で、パッケージに含めるものを `mazegen` だけと明示する（`[tool.setuptools] packages = ["mazegen"]`）
- [ ] ビルド後に `unzip -l mazegen-*.whl` を実行し、`app/` が wheel に入っていないことを確認する
- [ ] `MAZEGEN.md` を `pyproject.toml` の `readme` に指定し、wheel 内の `METADATA` ファイルにその内容が入っていることを確認する
- [ ] 新しい venv で wheel を `pip install` し、`from mazegen import MazeGenerator` が通ることを確認する
- [ ] `.gitignore` に `__pycache__/`、`.mypy_cache/`、`build/`、`dist/`、`*.egg-info/`、venv のディレクトリを入れる
