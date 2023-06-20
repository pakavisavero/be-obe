from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
import pytz

from db.schemas.prodiSchema import ProdiSchema

tz = pytz.timezone("Asia/Jakarta")


class BaseRolePermissionSchema(BaseModel):
    id: Optional[int] = None
    role_id: Optional[int] = None
    module_id: Optional[int] = None

    view: Optional[bool] = False
    add: Optional[bool] = False
    edit: Optional[bool] = False
    printt: Optional[bool] = False
    export: Optional[bool] = False
    is_active: Optional[bool] = None

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


class RolePermissionSchema(BaseRolePermissionSchema):
    prodi: Optional[ProdiSchema] = None

    class Config:
        orm_mode = True


class RolePermissionCreateSchema(BaseRolePermissionSchema):
    pass


class RolePermissionUpdateSchema(BaseRolePermissionSchema):
    id: int


class RolePermissionDeleteSchema(BaseModel):
    id: int


class RolePermissionResponseSchema(BaseModel):
    code: int
    message: str
    data: Union[List[RolePermissionSchema], RolePermissionSchema] = None
    total: Optional[int] = None
