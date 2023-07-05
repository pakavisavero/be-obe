from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


class BaseModuleGroupSchema(BaseModel):
    id: Optional[int] = None

    module_name: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class ModuleGroupSchema(BaseModuleGroupSchema):
    class Config:
        orm_mode = True


class ModuleGroupCreateSchema(BaseModuleGroupSchema):
    pass


class ModuleGroupUpdateSchema(BaseModuleGroupSchema):
    id: int


class ModuleGroupDeleteSchema(BaseModel):
    id: int


class ModuleGroupResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[ModuleGroupSchema], ModuleGroupSchema] = None
    total: Optional[int] = None
