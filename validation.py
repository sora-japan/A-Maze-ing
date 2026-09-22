from pydantic import BaseModel

class Validation(BaseModel):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple
    EXIT: tuple
    OUTPUT_FILE: str
    PERFECT: bool
