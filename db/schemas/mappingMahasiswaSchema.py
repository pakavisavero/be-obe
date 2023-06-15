from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.perkuliahanSchema import PerkuliahanSchema
from db.schemas.mahasiswaSchema import MahasiswaSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseMappingMahasiswaSchema(BaseModel):
    id: Optional[int] = None
    perkuliahan_id: Optional[int] = None
    mahasiswa_id: Optional[int] = None

    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class MappingMahasiswaSchema(BaseMappingMahasiswaSchema):
    perkuliahan: Optional[PerkuliahanSchema] = None
    mahasiswa: Optional[MahasiswaSchema] = None

    class Config:
        orm_mode = True


class MappingMahasiswaCreateSchema(BaseMappingMahasiswaSchema):
    pass


class MappingMahasiswaUpdateSchema(BaseMappingMahasiswaSchema):
    id: int


class MappingMahasiswaDeleteSchema(BaseModel):
    id: int


class MappingMahasiswaResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[MappingMahasiswaSchema], MappingMahasiswaSchema] = None
    total: Optional[int] = None
