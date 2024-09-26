from pydantic import BaseModel

class Prompt(BaseModel):
    value: str