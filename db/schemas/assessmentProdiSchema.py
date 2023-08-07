from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
from db.schemas.assessmentProdiDetailSchema import AssessmentProdiDetailSchema
import pytz

tz = pytz.timezone("Asia/Jakarta")


class BaseAssessmentProdiSchema(BaseModel):
    id: Optional[int] = None

    name: Optional[str] = None
    description: Optional[str] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class AssessmentProdiSchema(BaseAssessmentProdiSchema):
    children: List[AssessmentProdiDetailSchema] = None
    listSiklus = []
    graph = []

    class Config:
        orm_mode = True


class AssessmentProdiCreateSchema(BaseAssessmentProdiSchema):
    pass


class AssessmentProdiUpdateSchema(BaseAssessmentProdiSchema):
    id: int


class AssessmentProdiDeleteSchema(BaseModel):
    id: int


class AssessmentProdiResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[AssessmentProdiSchema], AssessmentProdiSchema] = None
    total: Optional[int] = None
