from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.moduleGroupSchema import ModuleGroupSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseModuleSchema(BaseModel):
    id: Optional[int] = None

    module_group_id: Optional[int] = None
    module_name: Optional[str] = None
    route: Optional[str] = None
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class ModuleSchema(BaseModuleSchema):
    moduleGroup: Optional[ModuleGroupSchema] = None

    class Config:
        orm_mode = True


class ModuleCreateSchema(BaseModuleSchema):
    pass


class ModuleUpdateSchema(BaseModuleSchema):
    id: int


class ModuleDeleteSchema(BaseModel):
    id: int


class ModuleResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[ModuleSchema], ModuleSchema] = None
    total: Optional[int] = None
