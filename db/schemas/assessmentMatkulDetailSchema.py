from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.tahunAjaranSchema import TahunAjaranSchema
from db.schemas.perkuliahanSchema import PerkuliahanSchema
from db.schemas.cplSchema import CPLSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseAssessmentMatkulDetailSchema(BaseModel):
    id: Optional[int] = None
    perkuliahan_id: int

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class AssessmentMatkulDetailSchema(BaseAssessmentMatkulDetailSchema):
    perkuliahan: Optional[PerkuliahanSchema] = None

    class Config:
        orm_mode = True


class AssessmentMatkulDetailCreateSchema(BaseAssessmentMatkulDetailSchema):
    pass


class AssessmentMatkulDetailUpdateSchema(BaseAssessmentMatkulDetailSchema):
    id: int


class AssessmentMatkulDetailDeleteSchema(BaseModel):
    id: int


class AssessmentMatkulDetailResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[AssessmentMatkulDetailSchema], AssessmentMatkulDetailSchema] = None
    total: Optional[int] = None
