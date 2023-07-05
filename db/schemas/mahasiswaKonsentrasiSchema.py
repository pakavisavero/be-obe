from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.mahasiswaSchema import MahasiswaSchema
from db.schemas.konsentrasiSchema import KonsentrasiSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseMahasiswaKonsentrasiSchema(BaseModel):
    id: Optional[int] = None
    mahasiswa_id: Optional[int] = None
    konsentrasi_id: Optional[int] = None

    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class MahasiswaKonsentrasiSchema(BaseMahasiswaKonsentrasiSchema):
    mahasiswa: Optional[MahasiswaSchema] = None
    konsentrasi: Optional[KonsentrasiSchema] = None

    class Config:
        orm_mode = True


class MahasiswaKonsentrasiCreateSchema(BaseMahasiswaKonsentrasiSchema):
    pass


class MahasiswaKonsentrasiUpdateSchema(BaseMahasiswaKonsentrasiSchema):
    id: int


class MahasiswaKonsentrasiDeleteSchema(BaseModel):
    id: int


class MahasiswaKonsentrasiResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[MahasiswaKonsentrasiSchema], MahasiswaKonsentrasiSchema] = None
    total: Optional[int] = None
