from pydantic import BaseModel

class Config(BaseModel) -> None:
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple
    EXIT: tuple
    OUTPUT_FILE: str
    PERFECT: bool
