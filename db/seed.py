from database import Session
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder

# JSON_PATH = "db/fixtures"
# json_files = [
#     "vendor.json",
#     "failure_group.json",
#     "failure.json",
#     "region.json",
#     "client.json",
#     "product_model.json",
#     "product_type.json",
#     "item_location_type.json",
#     "warranty_type.json",
#     "acs_wh_type.json",
#     "impact.json",
#     "part_action.json",
#     "rqt_status.json",
#     "pickup_status.json",
#     "delivery_status.json",
#     "unit_status.json",

#     "contract_product_owner.json",
#     "contract_product_type.json",
# ]

JSON_PATH = "db/fixtures2"
json_files = [
    "opt.json"
]


def seed(session, entities):
    seeder = Seeder(session)
    seeder.seed(entities)
    session.commit()


for j in json_files:
    session = Session()
    entities = load_entities_from_json("{}/{}".format(JSON_PATH, j))

    seed(session, entities)
