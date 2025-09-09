from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginathionParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=15)]


PaginathionDep = Annotated[PaginathionParams, Depends()]
