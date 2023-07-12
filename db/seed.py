from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder

from database import Session
import bcrypt

JSON_PATH = "db/fixtures"

json_files = [
    "kurikulum.json",
    "fakultas.json",
    "prodi.json",
    "konsentrasi.json",
    "mata_kuliah.json",
    "matkul_konsentrasi.json",
    "module_group.json",
    "module.json",
    "role_master.json",
    "user.json",
    "user_role.json",
    "role_permission.json",
    "status_mahasiswa.json",
    "tahun_ajaran.json",
    "docstatus.json",
    "prodi_stuktural.json",
    "fakultas_stuktural.json",
]


def seed(session, entities):
    seeder = Seeder(session)
    seeder.seed(entities)
    session.commit()


for j in json_files:
    try:
        session = Session()
        entities = load_entities_from_json("{}/{}".format(JSON_PATH, j))

        if j == "user.json":
            for i, j in enumerate(entities["data"]):
                salt = bcrypt.gensalt()
                pwd = entities["data"][i]["password"]
                bytes = pwd.encode("utf-8")

                entities["data"][i]["password"] = bcrypt.hashpw(bytes, salt)

            seed(session, entities)
        else:
            seed(session, entities)

    except Exception as e:
        print(e)
