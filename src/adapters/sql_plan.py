from orator import Model
from orator.orm import has_many

from esm.models.plan import Plan
from esm.models.plan_metadata import PlanMetadata
from esm.models.manifest import Manifest

from esm.models.service_metadata import ServiceMetadata
from adapters.sql_datasource import Helper
from adapters.sql_service_type import ServiceMetadataAdapter
import json


class PlanSQL(Model):
    __table__ = 'plans'

    def __init__(self):
        super(PlanSQL, self).__init__()
        Model.set_connection_resolver(Helper.db)

    @classmethod
    def delete_all(cls):
        Helper.db.table(cls.__table__).truncate()


'''
    self.swagger_types = {
        'id': str,
        'name': str,
        'description': str,

        'free': bool,
        'bindable': bool

        'metadata': PlanMetadata,
    }
'''


class PlanAdapter:
    @staticmethod
    def create_table():
        try:
            with Helper.schema.create('service_types') as table:
                table.increments('id')
                ''' STRINGS '''
                table.string('id_name').unique()
                table.string('name').unique()
                table.string('description').nullable()
                ''' BOOLEANS '''
                table.boolean('free').nullable()
                table.boolean('bindable').nullable()
                ''' OBJECTS '''
                table.string('metadata').nullable()
                ''' DATES '''
                table.datetime('created_at')
                table.datetime('updated_at')
        except:
            pass

    @staticmethod
    def sample_model() -> Plan:
        model = Plan()
        model.id = 1
        ''' STRINGS '''
        model.name = 'service1'
        model.id_name = 'service1'
        model.description = 'description1'
        ''' BOOLEANS '''
        model.free = True
        model.bindable = False
        ''' OBJECTS '''
        model.metadata = PlanMetadata(display_name='metadata1')
        return model

    @classmethod
    def sample_model_sql(cls) -> PlanSQL:
        model = cls.sample_model()
        return cls.model_to_model_sql(model)

    @staticmethod
    def model_sql_to_model(model_sql: PlanSQL) -> Plan:
        model = Plan()
        ''' STRINGS '''
        model.name = model_sql.name
        model.id_name = model_sql.id
        model.short_name = model_sql.short_name
        model.description = model_sql.description
        ''' BOOLEANS '''
        model.bindable = model_sql.bindable
        model.free = model_sql.free
        ''' OBJECTS '''
        model.metadata = ServiceMetadataAdapter.from_blob(model_sql.metadata)
        return model

    @staticmethod
    def model_to_model_sql(model: Plan):
        model_sql = PlanSQL()
        ''' STRINGS '''
        model_sql.name = model.name
        model_sql.id_name = model.id
        model_sql.short_name = model.short_name
        model_sql.description = model.description
        ''' BOOLEANS '''
        model_sql.bindable = model.bindable
        model_sql.free = model.free
        ''' OBJECTS '''
        model_sql.metadata = ServiceMetadataAdapter.to_blob(model.metadata)
        return model_sql

    @staticmethod
    def save(model: Plan) -> PlanSQL:
        model_sql = PlanAdapter.find_by_id_name(model.id) or None
        if model_sql:
            ''' STRINGS '''
            model_sql.name = model.name
            model_sql.id_name = model.id
            model_sql.short_name = model.short_name
            model_sql.description = model.description
            model_sql.bindable = model.bindable
            ''' LISTS '''
            model_sql.tags = json.dumps(model.tags)
            model_sql.requires = json.dumps(model.requires)
            ''' OBJECTS '''
            model_sql.metadata = ServiceMetadataAdapter.to_blob(model.metadata)
        else:
            model_sql = PlanAdapter.model_to_model_sql(model)
            model_sql.save()
        return model_sql

    @staticmethod
    def delete_all() -> None:
        PlanSQL.delete_all()

    @staticmethod
    def delete(id_name: str) -> None:
        model_sql = PlanAdapter.find_by_id_name(id_name) or None
        if model_sql:
            model_sql.delete()
        else:
            raise Exception('model not found on DB to delete')

    @staticmethod
    def get_all() -> [Plan]:
        model = PlanSQL()
        models = [] or model.all()  # .serialize()
        return [PlanAdapter.model_sql_to_model(model) for model in models]

    @staticmethod
    def find_by_id_name(id_name: str) -> PlanSQL or None:
        result = PlanSQL.where('id_name', '=', '{}'.format(id_name)).get()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def exists_in_db(id_name: str) -> bool:
        result = PlanAdapter.find_by_id_name(id_name)
        if result:
            return True
        else:
            return False