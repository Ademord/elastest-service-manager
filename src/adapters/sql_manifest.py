from orator import Model

from esm.models.manifest import Manifest
from adapters.sql_datasource import Helper
from adapters.sql_datasource import ServiceTypeSQL
from adapters.sql_datasource import ServiceTypeAdapter
from adapters.sql_datasource import PlanAdapter
from orator.orm import belongs_to
import json


class ManifestSQL(Model):
    __table__ = 'service_manifests'

    @belongs_to
    def service(self):
        return ServiceTypeSQL

    def __init__(self):
        super(ManifestSQL, self).__init__()
        Model.set_connection_resolver(Helper.db)

    @classmethod
    def delete_all(cls):
        if Helper.schema.has_table(cls.__table__):
            Helper.db.table(cls.__table__).truncate()

    @classmethod
    def create_table(cls):
        with Helper.schema.create(cls.__table__) as table:
            with Helper.schema.create('service_manifest') as table:
                table.increments('id')
                ''' STRINGS '''
                table.string('id_name').unique()
                table.string('manifest_type')
                table.string('manifest_content')
                ''' FOREIGN KEY '''
                table.string('service_id_name')
                table.integer('service_id').unsigned()
                table.foreign('service_id').references('id').on('service_types')
                ''' FOREIGN KEY '''
                table.string('plan_id_name')
                table.integer('plan_id').unsigned()
                table.foreign('plan_id').references('id').on('plans')
                ''' OBJECTS '''
                table.string('endpoints').nullable()

    @classmethod
    def table_exists(cls):
        return Helper.schema.has_table(cls.__table__)

''' 
    UPDATE WITH:
         self.swagger_types = {
            'id_name': str,
            'plan_id': str,
            'service_id': str,
            'manifest_type': str,
            'manifest_content': str,
            'endpoints': object
        }

'''


class ManifestAdapter:
    @staticmethod
    def create_table():
        if not ManifestSQL.table_exists():
            ManifestSQL.create_table()

    @staticmethod
    def sample_model() -> Manifest:
        model = Manifest()
        ''' STRINGS '''
        model.id = 'id_name'
        model.plan_id = 'plan_id'
        model.service_id = 'service_id'
        model.manifest_type = 'manifest_type'
        model.manifest_content = 'manifest_content'
        ''' OBJECTS '''
        model.endpoints = {'endpoint': 'endpoint'}  # using dict
        return model

    @staticmethod
    def model_to_model_sql(model: Manifest):
        model_sql = ManifestSQL()
        ''' STRINGS '''
        model_sql.id_name = model.id
        model_sql.manifest_type = model.manifest_type
        model_sql.manifest_content = model.manifest_content
        ''' FOREIGN KEY '''
        model_sql.service_id_name = model.service_id
        service = ServiceTypeAdapter.find_by_id_name(model.service_id)
        if not service:
            raise Exception('Bad Service ID provided')
        model_sql.service_id =  service.id
        ''' FOREIGN KEY '''
        model_sql.plan_id_name = model.plan_id
        plan = PlanAdapter.find_by_id_name(model.plan_id)
        if not plan:
            raise Exception('Bad Plan ID provided')
        model_sql.plan_id = PlanAdapter.find_by_id_name(model.plan_id)
        ''' OBJECTS '''
        model_sql.endpoints = Helper.to_blob(model.endpoints)
        return model_sql

    @classmethod
    def sample_model_sql(cls) -> ManifestSQL:
        model = cls.sample_model()
        return cls.model_to_model_sql(model)

    @staticmethod
    def model_sql_to_model(model_sql: ManifestSQL) -> Manifest:
        model = Manifest()
        ''' STRINGS '''
        model.id_name = model_sql.id_name
        model.manifest_type = model_sql.manifest_type
        model.manifest_content = model_sql.manifest_content
        ''' FOREIGN KEY '''
        model.service_id = model_sql.service_id_name
        ''' FOREIGN KEY '''
        model.plan_id = model_sql.plan_id_name
        ''' OBJECTS '''
        model.endpoints = model_sql.endpoints
        return model

    @staticmethod
    def save(model: Manifest) -> ManifestSQL:
        model_sql = ManifestAdapter.find_by_id_name(model.id) or None
        if model_sql:
            ''' STRINGS '''
            model_sql.id_name = model.id
            model_sql.manifest_type = model.manifest_type
            model_sql.manifest_content = model.manifest_content
            ''' FOREIGN KEY '''
            model_sql.service_id_name = model.service_id
            service = ServiceTypeAdapter.find_by_id_name(model.service_id)
            if not service:
                raise Exception('Bad Service ID provided')
            model_sql.service_id =  service.id
            ''' FOREIGN KEY '''
            model_sql.plan_id_name = model.plan_id
            plan = PlanAdapter.find_by_id_name(model.plan_id)
            if not plan:
                raise Exception('Bad Plan ID provided')
            model_sql.plan_id = PlanAdapter.find_by_id_name(model.plan_id)
            ''' OBJECTS '''
            model_sql.endpoints = Helper.to_blob(model.endpoints)
        else:
            model_sql = ManifestAdapter.model_to_model_sql(model)
            model_sql.save()
        return model_sql

    @staticmethod
    def delete_all() -> None:
        ManifestSQL.delete_all()

    @staticmethod
    def delete(id_name: str) -> None:
        model_sql = ManifestAdapter.find_by_id_name(id_name) or None
        if model_sql:
            model_sql.delete()
        else:
            raise Exception('model not found on DB to delete')

    @staticmethod
    def get_all() -> [Manifest]:
        model = ManifestSQL()
        models = [] or model.all()  # .serialize()
        return [ManifestAdapter.model_sql_to_model(model) for model in models]

    @staticmethod
    def find_by_id_name(id_name: str) -> ManifestSQL or None:
        result = ManifestSQL.where('id_name', '=', '{}'.format(id_name)).get()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def exists_in_db(id_name: str) -> bool:
        result = ManifestAdapter.find_by_id_name(id_name)
        if result:
            return True
        else:
            return False
