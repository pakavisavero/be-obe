from db.models import *
from db.database import Session
from db.schemas.userSchema import (
    UserCreateSchema,
    UserUpdateSchema,
)

from .utils import helper_static_filter, error_handling
from datetime import datetime
from sqlalchemy import or_

import pytz
import bcrypt

tz = pytz.timezone("Asia/Jakarta")


def helperRetrieveDosen(db, data):
    perkuliahan = (
        db.query(Perkuliahan)
        .filter(
            or_(
                Perkuliahan.dosen_id == data.id,
                Perkuliahan.dosen2_id == data.id,
                Perkuliahan.dosen3_id == data.id,
            )
        )
        .all()
    )

    doswal = db.query(MahasiswaDoswal).filter_by(dosen_id=data.id).all()
    mahasiswa = []
    for mhs in doswal:
        mahasiswa.append(
            {
                "nim": mhs.mahasiswa.nim,
                "full_name": mhs.mahasiswa.full_name,
                "status": mhs.mahasiswa.status.status,
                "angkatan": mhs.angkatan,
            }
        )

    roles = []
    ur = db.query(UserRole).filter_by(user_id=data.id).all()
    for u in ur:
        roles.append(u.roleMaster)

    setattr(data, "perkuliahan", perkuliahan)
    setattr(data, "mahasiswa", mahasiswa)
    setattr(data, "roles", roles)


def errArray(idx):
    if idx < 2:
        return 0
    else:
        return 1


def getAll(db: Session, token: str):
    data = db.query(User).all()

    return data


def getAllPaging(db: Session, offset: int, token: str):
    base_query = db.query(User)

    data = base_query.all()
    total = base_query.count()

    return {"data": data, "total": total}


def getAllPagingFiltered(db: Session, offset: int, filtered: dict, token: str, xtra={}):
    data, total = helper_static_filter(db, User, filtered, offset, xtra)

    return {"data": data, "total": total}


def getAllPagingFilteredSpecialDosen(
    db: Session, offset: int, filtered: dict, token: str, xtra={}
):
    data, total = helper_static_filter(db, User, filtered, offset, xtra)

    return {"data": data, "total": total}


def getByID(db: Session, id: int):
    data = db.query(User).filter_by(id=id).first()

    helperRetrieveDosen(db, data)
    return data


def getOnlyDosen(db: Session, data: list, filtered_data: dict):
    outputData = []
    for dt in data:
        dosen = db.query(User).filter_by(id=dt.user_id).first()
        outputData.append(dosen)

    return outputData


def checkUserFilter(db, args={}):
    return db.query(User).filter_by(**args).first()


def create(db: Session, username: str, data: dict):
    try:
        roles = None
        password = None

        if 'password' in data:
            password = data['password']

        if 'roles' in data:
            roles = data['roles']

        existNIP = checkUserFilter(db, {'nip': data['nip']})
        if existNIP:
            raise Exception({'message': 'nip is already taken!'})

        existUsername = checkUserFilter(
            db, {'username': data['username']})
        if existUsername:
            raise Exception({'message': 'username is already taken!'})

        existEmail = checkUserFilter(
            db, {'email': data['email']})
        if existEmail:
            raise Exception({'message': 'email is already taken!'})

        salt = bcrypt.gensalt()
        bytes = password.encode("utf-8")
        password = bcrypt.hashpw(bytes, salt)

        data['password'] = password
        data['created_at'] = datetime.now()
        data['modified_at'] = datetime.now()
        data['created_by'] = username
        data['modified_by'] = username

        help_remove_data(data)

        user = User(**data.dict())
        db.add(user)
        db.commit()

        if roles:
            for role in roles:
                r = UserRole(**{
                    'user_id': user.id,
                    'role_id': role['id'],
                })
                db.add(r)
                db.commit()

        return {
            'status': True,
            'data': user
        }

    except Exception as e:
        return error_handling(e)


def update(db: Session, username: str, data: dict):
    try:
        id = data['id']
        roles = None
        password = None
        new_password = None

        if 'old_password' in data:
            password = data['old_password']

        if 'new_password' in data:
            new_password = data['new_password']

        if 'roles' in data:
            roles = data['roles']

        result = None
        existUser = checkUserFilter(db, {'id': id})

        if password and existUser:
            userBytes = password.encode('utf-8')
            result = bcrypt.checkpw(userBytes, existUser.password)
            if existUser.nip != data['nip']:
                existNIP = checkUserFilter(db, {'nip': data['nip']})
                if existNIP:
                    raise Exception({'message': 'nip is already taken!'})

            if existUser.username != data['username']:
                existUsername = checkUserFilter(
                    db, {'username': data['username']})
                if existUsername:
                    raise Exception({'message': 'username is already taken!'})

            if existUser.email != data['email']:
                existEmail = checkUserFilter(
                    db, {'email': data['email']})
                if existEmail:
                    raise Exception({'message': 'email is already taken!'})

        if result or not password:
            if password:
                salt = bcrypt.gensalt()
                bytes = new_password.encode("utf-8")
                password = bcrypt.hashpw(bytes, salt)
                data['password'] = password

            data['modified_at'] = datetime.now()
            data['modified_by'] = username

            help_remove_data(data)

            user = db.query(User).filter(User.id == id).update(dict(data))
            db.commit()

            if roles:
                db.query(UserRole).filter_by(user_id=id).delete()
                for role in roles:
                    r = UserRole(**{
                        'user_id': id,
                        'role_id': role['id'],
                    })
                    db.add(r)
                    db.commit()

            return {
                'status': True,
                'data': user
            }
        else:
            raise Exception({'message': 'password is not valid!'})

    except Exception as e:
        return error_handling(e)


def updatePassword(db: Session, username: str, data: dict):
    try:
        id = data['id']
        data['modified_at'] = datetime.now()
        data['modified_by'] = username

        del data['id']
        user = db.query(User).filter(User.id == id).first()

        userBytes = data['old_password'].encode('utf-8')
        result = bcrypt.checkpw(userBytes, user.password)

        if result:
            salt = bcrypt.gensalt()
            bytes = data['new_password'].encode("utf-8")
            password = bcrypt.hashpw(bytes, salt)

            user = db.query(User).filter(User.id == id).update(
                {'password': password})
            db.commit()

            return user

        raise Exception("Wrong password!")

    except Exception as e:
        return False


def delete(db: Session, id: int):
    return db.query(User).filter_by(id=id).delete()


def help_remove_data(data):
    nameArray = [
        "id",
        "email_verified_at",
        "last_login",
        "is_dosen",
        "prodi",
        "perkuliahan",
        "mahasiswa",
        "roles",
        "prodi_id_name",
        "old_password",
        "new_password",
        "confirm_new_password",
        "confirm_password"
    ]

    for a in nameArray:
        if a in data:
            del data[a]
