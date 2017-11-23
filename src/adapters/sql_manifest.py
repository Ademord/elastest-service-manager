from orator import Model

from esm.models.manifest import Manifest
from adapters.sql_datasource import Helper

import json


class ManifestSQL(Model):
    __table__ = 'service_manifests'

    def __init__(self):
        super(ManifestSQL, self).__init__()
        Model.set_connection_resolver(Helper.db)

    @classmethod
    def delete_all(cls):
        Helper.db.table(cls.__table__).truncate()


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
        try:
            with Helper.schema.create('service_manifest') as table:
                table.increments('id')
                ''' STRINGS '''
                # TODO note that the field is to be rendered as id to be compliant with OSBA
                table.string('id_name').unique()
                table.string('plan_id')
                table.string('service_id')
                table.string('manifest_type')
                table.string('manifest_content')
                ''' OBJECTS '''
                table.string('endpoints').nullable()
        except:
            pass

    @staticmethod
    def sample_model() -> Manifest:
        model = Manifest()
        model.id = 1
        ''' STRINGS '''
        model.id_name = 'id_name'
        model.plan_id = 'plan_id'
        model.service_id = 'service_id'
        model.manifest_type = 'manifest_type'
        model.manifest_content = 'manifest_content'
        ''' OBJECTS '''
        model.endpoints = object()  # TODO no explict model for this, dict is narrower
        return model

    @classmethod
    def sample_model_sql(cls) -> ManifestSQL:
        model = cls.sample_model()
        return cls.model_to_model_sql(model)

    @staticmethod
    def model_sql_to_model(model_sql: ManifestSQL) -> Manifest:
        model = Manifest()
        ''' STRINGS '''
        model.id_name = model_sql.id_name
        model.plan_id = model_sql.plan_id
        model.service_id = model_sql.service_id
        model.manifest_type = model_sql.manifest_type
        model.manifest_content = model_sql.manifest_content
        ''' OBJECTS '''
        model.endpoints = model_sql.endpoints  # TODO no explict model for this the adapter???
        # model.dashboard_client = DashboardClientAdapter.from_blob(model_sql.dashboard_client)
        return model

    @staticmethod
    def model_to_model_sql(model: Manifest):
        model_sql = ManifestSQL()
        ''' STRINGS '''
        model_sql.id_name = model.id
        model_sql.plan_id = model.plan_id
        model_sql.service_id = model.service_id
        model_sql.manifest_type = model.manifest_type
        model_sql.manifest_content = model.manifest_content
        ''' OBJECTS '''
        model_sql.endpoints = model.endpoints  # TODO no explict model for this the adapter???
        # model_sql.metadata = ServiceMetadataAdapter.to_blob(model.metadata)
        return model_sql

    @staticmethod
    def save(model: Manifest) -> ManifestSQL:
        model_sql = ManifestAdapter.find_by_id_name(model.id) or None
        if model_sql:
            ''' STRINGS '''
            model_sql.id_name = model.id
            model_sql.plan_id = model.plan_id
            model_sql.service_id = model.service_id
            model_sql.manifest_type = model.manifest_type
            model_sql.manifest_content = model.manifest_content
            ''' OBJECTS '''
            model_sql.endpoints = model.endpoints  # TODO no explict model for this the adapter???
            # model_sql.metadata = ServiceMetadataAdapter.to_blob(model.metadata)
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
