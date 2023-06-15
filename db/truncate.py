from database import Session, engine
from sqlalchemy.orm import sessionmaker
import models

list_of_models = [
    models.Failure,
    models.ItemAction,
    models.ItemLocation,
    models.ItemLocationType,
    models.ItemStatus,
    models.LokasiRaks,
    models.MappingAsoAcsHub,
    models.PartAction,
    models.Priority,
    models.Problem,
    models.WarrantyItemSerial,
    models.WarrantyItem,
    models.WarrantyType,
    models.AttachmentContract,
    models.ContractPMPeriod,
    models.ContractPMPlan,
    models.ContractUnit,
    models.Contract,
    models.Product,
    models.ProductModel,
    models.ProductType,
    models.ServiceCategory,
    models.ServiceCoverage,
    models.SlaDetail,
    models.Sla,
    models.Impact,
    models.Solution,
    models.StockStatus,
    models.StoreType,
    models.Store,
    models.UserSales,
    models.Vendor,
    models.WorkOrderAction,
    models.StoreType,
    models.Store,
    models.Client,
    models.Address,
    models.Customer,
    models.CustomerCategory,
    models.CustomerRelation,
    models.Person,
    models.Region,
    models.Salesman,
    models.Return,
    models.StoreCustomerRelations,
]


def delete_all_tables(engine):
    for model in list_of_models:
        Session = sessionmaker(bind=engine)
        session = Session()

        f = session.query(model).delete()
        session.commit()


delete_all_tables(engine)
