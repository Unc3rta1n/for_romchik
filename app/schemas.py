from typing import Optional

from pydantic import BaseModel


class DefaultResponse(BaseModel):
    error: bool
    message: str
    payload: Optional[str]
