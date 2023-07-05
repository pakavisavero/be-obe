from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.perkuliahanSchema import PerkuliahanSchema

tz = pytz.timezone("Asia/Jakarta")


class BasePresentasePkSchema(BaseModel):
    id: Optional[int] = None
    perkuliahan_id: Optional[int] = None

    nilai_tugas: Optional[str] = None
    nilai_uts: Optional[str] = None
    nilai_uas: Optional[str] = None
    nilai_praktek: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class PresentasePkSchema(BasePresentasePkSchema):
    perkuliahan: Optional[PerkuliahanSchema] = None

    class Config:
        orm_mode = True


class PresentasePkCreateSchema(BasePresentasePkSchema):
    pass


class PresentasePkUpdateSchema(BasePresentasePkSchema):
    id: int


class PresentasePkDeleteSchema(BaseModel):
    id: int


class PresentasePkResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[PresentasePkSchema], PresentasePkSchema] = None
    total: Optional[int] = None
