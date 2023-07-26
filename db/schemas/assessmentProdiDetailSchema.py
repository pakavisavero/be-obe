from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
from db.schemas.siklusProdiSchema import SiklusProdiSchema

import pytz

tz = pytz.timezone("Asia/Jakarta")


class BaseAssessmentProdiDetailSchema(BaseModel):
    id: Optional[int] = None
    parent_id: Optional[str] = None
    siklus_id: Optional[str] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class AssessmentProdiDetailSchema(BaseAssessmentProdiDetailSchema):
    siklus: Optional[SiklusProdiSchema] = None

    class Config:
        orm_mode = True


class AssessmentProdiDetailCreateSchema(BaseAssessmentProdiDetailSchema):
    pass


class AssessmentProdiDetailUpdateSchema(BaseAssessmentProdiDetailSchema):
    id: int


class AssessmentProdiDetailDeleteSchema(BaseModel):
    id: int


class AssessmentProdiDetailResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[AssessmentProdiDetailSchema],
                AssessmentProdiDetailSchema] = None
    total: Optional[int] = None
