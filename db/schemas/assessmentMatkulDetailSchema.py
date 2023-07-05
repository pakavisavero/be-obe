from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.siklusProdiDetailSchema import SiklusProdiDetailSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseAssessmentMatkulDetailSchema(BaseModel):
    id: Optional[int] = None

    name: Optional[str] = None
    description: Optional[str] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class AssessmentMatkulSchema(BaseAssessmentMatkulDetailSchema):
    children: List[SiklusProdiDetailSchema] = None

    class Config:
        orm_mode = True


class AssessmentMatkulCreateSchema(BaseAssessmentMatkulDetailSchema):
    pass


class AssessmentMatkulUpdateSchema(BaseAssessmentMatkulDetailSchema):
    id: int


class AssessmentMatkulDeleteSchema(BaseModel):
    id: int


class AssessmentMatkulResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[AssessmentMatkulSchema], AssessmentMatkulSchema] = None
    total: Optional[int] = None
