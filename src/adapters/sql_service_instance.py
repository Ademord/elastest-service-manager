from orator import Model

from esm.models.service_instance import ServiceInstance
from esm.models.service_type import ServiceType
from esm.models.last_operation import LastOperation
from adapters.sql_datasource import DashboardClientAdapter
from adapters.sql_datasource import ServiceMetadataAdapter
from adapters.sql_datasource import Helper

import json


class ServiceInstanceSQL(Model):
    __table__ = 'service_types'

    def __init__(self):
        super(ServiceInstanceSQL, self).__init__()
        Model.set_connection_resolver(Helper.db)

    @classmethod
    def delete_all(cls):
        Helper.db.table(cls.__table__).truncate()


''' 
    UPDATE WITH:
    self.swagger_types = {
            'service_type': ServiceType, (this is a service_id)
            'state': LastOperation, (this is a operation_id)
            'context': object (no idea what kind of object...)
        }

'''


class ServiceInstanceAdapter:
    @staticmethod
    def create_table():
        try:
            with Helper.schema.create('service_instance') as table:
                table.increments('id')
                ''' OBJECTS '''
                table.string('service_type')
                table.string('state')
                table.string('context').nullable()

        except:
            pass

    @staticmethod
    def sample_model() -> ServiceInstance:
        model = ServiceInstance()
        model.id = 1
        ''' OBJECTS '''
        model.service_type = ServiceType()
        model.state = LastOperation()
        model.context = object()
        return model

    @classmethod
    def sample_model_sql(cls) -> ServiceInstanceSQL:
        model = cls.sample_model()
        return cls.model_to_model_sql(model)

    @staticmethod
    def model_sql_to_model(model_sql: ServiceInstanceSQL) -> ServiceInstance:
        model = ServiceInstance()
        ''' OBJECTS '''
        model.service_type = ServiceMetadataAdapter.from_blob(model_sql.service_type)
        model.state = LastOperationAdapter.from_blob(model_sql.state)
        model.context = object()  # TODO no explict model for this, other than dict
        return model

    @staticmethod
    def model_to_model_sql(model: ServiceInstance):
        model_sql = ServiceInstanceSQL()
        ''' OBJECTS '''
        model_sql.service_type = ServiceMetadataAdapter.to_blob(model.service_type)
        model_sql.state = LastOperationAdapter.to_blob(model.state)
        model_sql.context = object()  # TODO no explict model for this, other than dict
        return model_sql

    @staticmethod
    def save(model: ServiceInstance) -> ServiceInstanceSQL:
        model_sql = ServiceInstanceAdapter.find_by_id_name(model.id) or None
        if model_sql:
            ''' OBJECTS '''
            model_sql.service_type = ServiceMetadataAdapter.to_blob(model.service_type)
            model_sql.state = LastOperationAdapter.to_blob(model.state)
            model_sql.context = object()  # TODO no explict model for this, other than dict
        else:
            model_sql = ServiceInstanceAdapter.model_to_model_sql(model)
            model_sql.save()
        return model_sql

    @staticmethod
    def delete_all() -> None:
        ServiceInstanceSQL.delete_all()

    @staticmethod
    def delete(id_name: str) -> None:
        model_sql = ServiceInstanceAdapter.find_by_id_name(id_name) or None
        if model_sql:
            model_sql.delete()
        else:
            raise Exception('model not found on DB to delete')

    @staticmethod
    def get_all() -> [ServiceInstance]:
        model = ServiceInstanceSQL()
        models = [] or model.all()  # .serialize()
        return [ServiceInstanceAdapter.model_sql_to_model(model) for model in models]

    @staticmethod
    def find_by_id_name(id_name: str) -> ServiceInstanceSQL or None:
        result = ServiceInstanceSQL.where('id_name', '=', '{}'.format(id_name)).get()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def exists_in_db(id_name: str) -> bool:
        result = ServiceInstanceAdapter.find_by_id_name(id_name)
        if result:
            return True
        else:
            return False
