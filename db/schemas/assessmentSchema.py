from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.assessmentDetailSchema import AssessmentDetailSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseAssessmentSchema(BaseModel):
    id: Optional[int] = None

    name: Optional[str] = None
    description: Optional[str] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class AssessmentSchema(BaseAssessmentSchema):
    children: List[AssessmentDetailSchema] = None

    class Config:
        orm_mode = True


class AssessmentCreateSchema(BaseAssessmentSchema):
    pass


class AssessmentUpdateSchema(BaseAssessmentSchema):
    id: int


class AssessmentDeleteSchema(BaseModel):
    id: int


class AssessmentResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[AssessmentSchema], AssessmentSchema] = None
    total: Optional[int] = None
