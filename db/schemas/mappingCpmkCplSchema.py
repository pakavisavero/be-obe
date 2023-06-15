from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.cpmkSchema import CPMKSchema
from db.schemas.cplSchema import CPLSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseMappingCpmkCplSchema(BaseModel):
    id: Optional[int] = None
    cpmk_id: Optional[int] = None
    cpl_id: Optional[int] = None

    value: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class MappingCpmkCplSchema(BaseMappingCpmkCplSchema):
    cpmk: Optional[CPMKSchema] = None
    cpl: Optional[CPLSchema] = None

    class Config:
        orm_mode = True


class MappingCpmkCplCreateSchema(BaseMappingCpmkCplSchema):
    pass


class MappingCpmkCplUpdateSchema(BaseMappingCpmkCplSchema):
    id: int


class MappingCpmkCplDeleteSchema(BaseModel):
    id: int


class MappingCpmkCplResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[MappingCpmkCplSchema], MappingCpmkCplSchema] = None
    total: Optional[int] = None
