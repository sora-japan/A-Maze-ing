from pydantic import BaseModel, field_validator, model_validator, ValidationError


class MazeConfig(BaseModel):
    """迷路生成の設定値を表す、検証済みのデータモデル。

    フィールドに対する型・範囲・相互制約の検証を pydantic のバリデータで行う。
    インスタンス化に成功したら「全ての値が有効」と保証されている状態になる。

    Attributes:
        width: 迷路の幅（セル数、正の整数）。
        height: 迷路の高さ（セル数、正の整数）。
        entry: 入口の座標 (x, y)。範囲内かつ exit と異なる必要がある。
        exit: 出口の座標 (x, y)。範囲内かつ entry と異なる必要がある。
        output_file: 出力ファイル名（空文字不可）。
        perfect: 完全迷路フラグ。True なら唯一経路、False ならループ有り。
        seed: 乱数シード。省略時は None（生成器側でランダム）。
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None

    @field_validator("width", "height")
    @classmethod
    def positive_check(cls, v: int) -> int:
        """width / height が正の整数であることを検証する。

        Args:
            v: 検証対象の値（width または height）。

        Returns:
            検証を通過した値。

        Raises:
            ValueError: 値が 0 以下の場合。
        """
        if v <= 0:
            raise ValueError(f"must be positive (got {v})")
        return v

    @field_validator("output_file")
    @classmethod
    def output_file_empty_check(cls, v: str) -> str:
        """output_file が空文字列でないことを検証する。

        Args:
            v: 検証対象の文字列。

        Returns:
            検証を通過した文字列。

        Raises:
            ValueError: 空文字列が渡された場合。
        """
        if not v:
            raise ValueError(f"must not be empty (got {v!r})")
        return v

    @model_validator(mode="after")
    def entry_check(self) -> "MazeConfig":
        """entry 座標が迷路の範囲内に収まっているかを検証する。

        Returns:
            検証を通過した自身のインスタンス。

        Raises:
            ValueError: entry が width / height の範囲を外れている場合。
        """
        x, y = self.entry
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"entry {self.entry} is out of range")
        return self

    @model_validator(mode="after")
    def exit_check(self) -> "MazeConfig":
        """exit 座標が迷路の範囲内に収まっているかを検証する。

        Returns:
            検証を通過した自身のインスタンス。

        Raises:
            ValueError: exit が width / height の範囲を外れている場合。
        """
        x, y = self.exit
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"exit {self.exit} is out of range")
        return self

    @model_validator(mode="after")
    def entry_not_exit(self) -> "MazeConfig":
        """entry と exit が異なる座標であることを検証する。

        Returns:
            検証を通過した自身のインスタンス。

        Raises:
            ValueError: entry と exit が同じ座標の場合。
        """
        if self.entry == self.exit:
            raise ValueError("entry and exit must be different value")
        return self


class ConfigError(Exception):
    """設定ファイルの読み込みや検証で発生するエラー"""


def parse_config(path: str) -> "MazeConfig":
    """設定ファイルを読み込み、検証済みの MazeConfig を返す。

    KEY=VALUE 形式の各行を解析し、コメント行（'#' で始まる行）と空行を
    スキップする。キーは小文字化され、ENTRY / EXIT は tuple[int, int] に
    変換される。全キーの収集後、必須キーの欠落・値の型や範囲を検証する。

    Args:
        path: 設定ファイルのパス。

    Returns:
        検証を通過した MazeConfig インスタンス。

    Raises:
        ConfigError: 次のいずれかの異常が発生した場合、
            - ファイルを開けない（存在しない、権限なし、ディレクトリ指定等）
            - '=' を含まない行がある
            - キーが重複している
            - 必須キーが欠落している
            - ENTRY / EXIT が 'x,y' 形式でない、または整数に変換できない
            - MazeConfig のバリデーションに失敗した
    """
    data: dict[str, str] = {}
    try:
        with open(path, "r") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    continue
                try:
                    key, value = line.split("=", 1)
                    key = key.lower()
                except ValueError as e:
                    raise ConfigError(f"{path}:{line_no}: invalid line (no '='): {line!r}") from e
                if key in data:
                    raise ConfigError(f"{path}:{line_no}: duplicate key: {key!r}")
                data[key] = value
    except OSError as e:
        raise ConfigError(f"{path}: cannot open file: {e}") from e

    REQUIRED = ("width", "height", "entry", "exit", "output_file", "perfect")
    miss = [k for k in REQUIRED if k not in data]
    if miss:
        raise ConfigError(f"{path}: missing required keys: {miss}")

    for k in ("entry", "exit"):
        try:
            x_pos, y_pos = data[k].split(",", 1)
            data[k] = (int(x_pos), int(y_pos))
        except ValueError as e:
            raise ConfigError(f"{path}: invalid {k} format: {data[k]!r} (expected 'x,y')") from e

    try:
        return MazeConfig(**data)
    except ValidationError as e:
        raise ConfigError(f"{path}: invalid config: {e}") from e
