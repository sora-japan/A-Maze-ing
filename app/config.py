from pydantic import BaseModel, field_validator, model_validator, ValidationError


class MazeConfig(BaseModel):
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
        if v <= 0:
            raise ValueError(f"must be positive (got {v})")
        return v

    @field_validator("output_file")
    @classmethod
    def output_file_empty_check(cls, v: str) -> str:
        if not v:
            raise ValueError(f"must not be empty (got {v!r})")
        return v

    @model_validator(mode="after")
    def entry_check(self) -> "MazeConfig":
        x, y = self.entry
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"entry {self.entry} is out of range")
        return self

    @model_validator(mode="after")
    def exit_check(self) -> "MazeConfig":
        x, y = self.exit
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"exit {self.exit} is out of range")
        return self

    @model_validator(mode="after")
    def entry_not_exit(self) -> "MazeConfig":
        if self.entry == self.exit:
            raise ValueError("entry and exit must be different value")
        return self


class ConfigError(Exception):
    """設定ファイルの読み込みや検証で発生するエラー"""


def parse_config(path: str) -> "MazeConfig":
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
