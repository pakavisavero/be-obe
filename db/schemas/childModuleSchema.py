from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.moduleSchema import ModuleSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseChildModuleSchema(BaseModel):
    id: Optional[int] = None
    module_id: Optional[int] = None

    module_name: Optional[str] = None
    route: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class ChildModuleSchema(BaseChildModuleSchema):
    module: Optional[ModuleSchema] = None

    class Config:
        orm_mode = True


class ChildModuleCreateSchema(BaseChildModuleSchema):
    pass


class ChildModuleUpdateSchema(BaseChildModuleSchema):
    id: int


class ChildModuleDeleteSchema(BaseModel):
    id: int


class ChildModuleResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[ChildModuleSchema], ChildModuleSchema] = None
    total: Optional[int] = None
