from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.tahunAjaranSchema import TahunAjaranSchema
from db.schemas.perkuliahanSchema import PerkuliahanSchema
from db.schemas.cplSchema import CPLSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseAssessmentDetailSchema(BaseModel):
    id: Optional[int] = None
    parent_id: int
    tahun_ajaran_id: int
    perkuliahan_id: int
    cpl_id: int

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class AssessmentDetailSchema(BaseAssessmentDetailSchema):
    tahunAjaran: Optional[TahunAjaranSchema] = None
    perkuliahan: Optional[PerkuliahanSchema] = None
    cpl: Optional[CPLSchema] = None

    class Config:
        orm_mode = True


class AssessmentDetailCreateSchema(BaseAssessmentDetailSchema):
    pass


class AssessmentDetailUpdateSchema(BaseAssessmentDetailSchema):
    id: int


class AssessmentDetailDeleteSchema(BaseModel):
    id: int


class AssessmentDetailResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[AssessmentDetailSchema], AssessmentDetailSchema] = None
    total: Optional[int] = None
