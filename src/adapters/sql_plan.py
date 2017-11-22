from orator import Model
from orator.orm import has_many

from esm.models.service_type import Plan
from esm.models.manifest import Manifest

from esm.models.service_metadata import ServiceMetadata
from adapters.sql_datasource import Helper
from adapters.sql_service_type import MetadataAdapter
import json


class PlanSQL(Model):
    __table__ = 'plans'

    def __init__(self):
        super(PlanSQL, self).__init__()
        Model.set_connection_resolver(Helper.db)

    @classmethod
    def delete_all(cls):
        Helper.db.table(cls.__table__).truncate()


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
        model.bindable = False
        model.bindable = False
        model.tags = ['description1']
        model.requires = ['requirement1']
        ''' OBJECTS '''
        model.metadata = ServiceMetadata(display_name='metadata1')
        return model

    @classmethod
    def sample_model_sql(cls) -> PlanSQL:
        model = cls.sample_model()
        return cls.model_to_model_sql(model)

    @staticmethod
    def model_sql_to_model(model_sql: PlanSQL) -> Plan:
        model = Plan()
        model.name = model_sql.name
        model.id_name = model_sql.id
        model.short_name = model_sql.short_name
        model.description = model_sql.description
        model.bindable = model_sql.bindble
        ''' LISTS '''
        model.tags = json.loads(model_sql.tags)
        model.requires = json.loads(model_sql.requires)
        ''' OBJECTS '''
        model.metadata = MetadataAdapter.from_blob(model_sql.metadata)
        return model

    @staticmethod
    def model_to_model_sql(model: Plan):
        model_sql = PlanSQL()
        model_sql.name = model.name
        model_sql.id_name = model.id
        model_sql.short_name = model.short_name
        model_sql.description = model.description
        model_sql.bindable = model.bindable
        ''' LISTS '''
        model_sql.tags = json.dumps(model.tags)
        model_sql.requires = json.dumps(model.requires)
        ''' OBJECTS '''
        model_sql.metadata = MetadataAdapter.to_blob(model.metadata)
        return model_sql

    @staticmethod
    def save(model: Plan) -> PlanSQL:
        model_sql = PlanAdapter.find_by_id_name(model.id) or None
        if model_sql:
            model_sql.name = model.name
            model_sql.id_name = model.id
            model_sql.short_name = model.short_name
            model_sql.description = model.description
            model_sql.bindable = model.bindable
            ''' LISTS '''
            model_sql.tags = json.dumps(model.tags)
            model_sql.requires = json.dumps(model.requires)
            ''' OBJECTS '''
            model_sql.metadata = MetadataAdapter.to_blob(model.metadata)
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