from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.konsentrasiSchema import KonsentrasiSchema
from db.schemas.prodiSchema import ProdiSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseKonsentrasiProdiSchema(BaseModel):
    id: Optional[int] = None
    konsentrasi_id: Optional[int] = None
    prodi_id: Optional[int] = None

    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class KonsentrasiProdiSchema(BaseKonsentrasiProdiSchema):
    konsentrasi: Optional[KonsentrasiSchema] = None
    prodi: Optional[ProdiSchema] = None

    class Config:
        orm_mode = True


class KonsentrasiProdiCreateSchema(BaseKonsentrasiProdiSchema):
    pass


class KonsentrasiProdiUpdateSchema(BaseKonsentrasiProdiSchema):
    id: int


class KonsentrasiProdiDeleteSchema(BaseModel):
    id: int


class KonsentrasiProdiResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[KonsentrasiProdiSchema], KonsentrasiProdiSchema] = None
    total: Optional[int] = None
