from orator import Model

from esm.models.service_type import ServiceInstance
from esm.models.dashboard_client import DashboardClient
from esm.models.service_metadata import ServiceMetadata
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
            with Helper.schema.create('service_types') as table:
                table.increments('id')
                ''' STRINGS '''
                table.string('id_name').unique()
                table.string('name').unique()
                table.string('short_name')
                table.string('description').nullable()
                ''' BOOLEANS '''
                table.boolean('bindable').nullable()
                table.boolean('plan_updateable').nullable()
                ''' LISTS '''
                table.string('tags').nullable()
                table.string('requires').nullable()
                ''' OBJECTS '''
                table.string('metadata').nullable()
                table.string('dashboard_client').nullable()
                ''' DATES '''
                table.datetime('created_at')
                table.datetime('updated_at')
        except:
            pass

    @staticmethod
    def sample_model() -> ServiceInstance:
        model = ServiceInstance()
        model.id = 1
        ''' STRINGS '''
        model.name = 'service1'
        model.id_name = 'service1'
        model.short_name = 'service1'
        model.description = 'description1'
        ''' BOOLEANS '''
        model.bindable = False
        model.plan_updateable = False
        ''' LISTS '''
        model.tags = ['description1']
        model.requires = ['requirement1']
        ''' OBJECTS '''
        model.metadata = ServiceMetadata(display_name='metadata1')
        model.dashboard_client = DashboardClient(id='client1')
        return model

    @classmethod
    def sample_model_sql(cls) -> ServiceInstanceSQL:
        model = cls.sample_model()
        return cls.model_to_model_sql(model)

    @staticmethod
    def model_sql_to_model(model_sql: ServiceInstanceSQL) -> ServiceInstance:
        model = ServiceInstance()
        ''' STRINGS '''
        model.name = model_sql.name
        model.id_name = model_sql.id
        model.short_name = model_sql.short_name
        model.description = model_sql.description
        ''' BOOLEANS '''
        model.bindable = model_sql.bindable
        model.plan_updateable = model_sql.plan_updateable
        ''' LISTS '''
        model.tags = json.loads(model_sql.tags)
        model.requires = json.loads(model_sql.requires)
        ''' OBJECTS '''
        model.metadata = ServiceMetadataAdapter.from_blob(model_sql.metadata)
        model.dashboard_client = DashboardClientAdapter.from_blob(model_sql.dashboard_client)
        return model

    @staticmethod
    def model_to_model_sql(model: ServiceInstance):
        model_sql = ServiceInstanceSQL()
        ''' STRINGS '''
        model_sql.name = model.name
        model_sql.id_name = model.id
        model_sql.short_name = model.short_name
        model_sql.description = model.description
        ''' BOOLEANS '''
        model_sql.bindable = model.bindable
        model_sql.plan_updateable = model.plan_updateable
        ''' LISTS '''
        model_sql.tags = json.dumps(model.tags)
        model_sql.requires = json.dumps(model.requires)
        ''' OBJECTS '''
        model_sql.metadata = ServiceMetadataAdapter.to_blob(model.metadata)
        model_sql.dashboard_client = DashboardClientAdapter.to_blob(model.dashboard_client)
        return model_sql

    @staticmethod
    def save(model: ServiceInstance) -> ServiceInstanceSQL:
        model_sql = ServiceInstanceAdapter.find_by_id_name(model.id) or None
        if model_sql:
            ''' STRINGS '''
            model_sql.name = model.name
            model_sql.id_name = model.id
            model_sql.short_name = model.short_name
            model_sql.description = model.description
            ''' BOOLEANS '''
            model_sql.bindable = model.bindable
            model_sql.plan_updateable = model.plan_updateable
            ''' LISTS '''
            model_sql.tags = json.dumps(model.tags)
            model_sql.requires = json.dumps(model.requires)
            ''' OBJECTS '''
            model_sql.metadata = ServiceMetadataAdapter.to_blob(model.metadata)
            model_sql.dashboard_client = DashboardClientAdapter.to_blob(model.dashboard_client)
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
