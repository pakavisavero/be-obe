from db.models import *
from db.database import Session
from db.schemas.roleMasterSchema import (
    RoleMasterCreateSchema,
    RoleMasterUpdateSchema,
)

from .utils import helper_static_filter
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Jakarta")


def helperRetrieveRole(db, data):
    for dt in data:
        permissions = db.query(RolePermission).filter_by(role_id=dt.id).all()
        setattr(dt, "permissions", permissions)


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def getAll(db: Session, token: str):
    data = db.query(RoleMaster).all()

    helperRetrieveRole(db, data)
    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(RoleMaster)

    data = base_query.all()
    total = base_query.count()

    helperRetrieveRole(db, data)
    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str):
    data, total = helper_static_filter(db, RoleMaster, filtered, offset)

    helperRetrieveRole(db, data)
    return {"data": data, "total": total}


def getByID(db: Session, id: int, token: str):
    data = db.query(RoleMaster).filter_by(id=id).first()

    helperRetrieveRole(db, [data])
    return data


def create(db: Session, username: str, data: RoleMasterCreateSchema):
    try:
        data.created_at = datetime.now()
        data.modified_at = datetime.now()
        data.created_by = username
        data.modified_by = username

        roleMaster = RoleMaster(**data.dict())
        db.add(roleMaster)
        db.commit()

        return roleMaster

    except Exception as e:
        print(e)
        return False


def update(db: Session, username: str, data: RoleMasterUpdateSchema):
    data["created_at"] = datetime.now()
    data["modified_at"] = datetime.now()
    data["created_by"] = username
    data["modified_by"] = username

    children = data["children"]
    help_remove_data(data)

    for child in children:
        filter = {
            'role_id': data['id'],
            'module_id': child['module_id']
        }

        exist = db.query(RolePermission).filter_by(**filter).first()
        if exist:
            db.query(RolePermission).filter_by(id=child['id']).\
                update({
                    'view': child['view'],
                    'add': child['add'],
                    'edit': child['edit'],
                    'printt': child['printt'],
                    'export': child['export'],
                })
                
            db.commit()
        else:
            rp = RolePermission(**data)
            db.add(rp)
            db.commit()

    return data


def delete(db: Session, id: int):
    return db.query(RoleMaster).filter_by(id=id).delete()


def help_remove_data(data):
    nameArray = [
        "permissions",
        "children",
    ]

    for a in nameArray:
        if a in data:
            del data[a]
