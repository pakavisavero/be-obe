from database import Session
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder

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
    "child_module.json",
    "role_master.json",
    "user.json",
    "user_role.json",
    "role_permission.json",
    "status_mahasiswa.json",
]


def seed(session, entities):
    seeder = Seeder(session)
    seeder.seed(entities)
    session.commit()


for j in json_files:
    session = Session()
    entities = load_entities_from_json("{}/{}".format(JSON_PATH, j))

    seed(session, entities)
