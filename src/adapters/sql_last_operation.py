from orator import Model

from esm.models.last_operation import LastOperation
from adapters.sql_datasource import Helper

import json


class LastOperationSQL(Model):
    __table__ = 'last_operations'
    
    def __init__(self):
        super(LastOperationSQL, self).__init__()
        Model.set_connection_resolver(Helper.db)

    @classmethod
    def delete_all(cls):
        Helper.db.table(cls.__table__).truncate()


''' 
    UPDATE WITH:
       self.swagger_types = {
            'state': str,
            'description': str
        }
    
'''


class LastOperationAdapter:
    @staticmethod
    def create_table():
        try:
            with Helper.schema.create('service_types') as table:
                table.increments('id')
                ''' STRINGS '''
                table.string('state')
                table.string('description').nullable()
        except:
            pass

    @staticmethod
    def sample_model() -> LastOperation:
        model = LastOperation()
        model.id = 1
        ''' STRINGS '''
        model.state = 'state'
        model.description = 'description'
        return model

    @classmethod
    def sample_model_sql(cls) -> LastOperationSQL:
        model = cls.sample_model()
        return cls.model_to_model_sql(model)

    @staticmethod
    def model_sql_to_model(model_sql: LastOperationSQL) -> LastOperation:
        model = LastOperation()
        ''' STRINGS '''
        model.state = model_sql.state
        model.description = model_sql.description
        return model

    @staticmethod
    def model_to_model_sql(model: LastOperation):
        model_sql = LastOperationSQL()
        ''' STRINGS '''
        model_sql.state = model.state
        model_sql.description = model.description
        return model_sql

    @staticmethod
    def save(model: LastOperation) -> LastOperationSQL:
        model_sql = LastOperationAdapter.find_by_id_name(model.id) or None
        if model_sql:
            ''' STRINGS '''
            model_sql.state = model.state
            model_sql.description = model.description
        else:
            model_sql = LastOperationAdapter.model_to_model_sql(model)
            model_sql.save()
        return model_sql

    @staticmethod
    def delete_all() -> None:
        LastOperationSQL.delete_all()

    @staticmethod
    def delete(id_name: str) -> None:
        model_sql = LastOperationAdapter.find_by_id_name(id_name) or None
        if model_sql:
            model_sql.delete()
        else:
            raise Exception('model not found on DB to delete')

    @staticmethod
    def get_all() -> [LastOperation]:
        model = LastOperationSQL()
        models = [] or model.all()  # .serialize()
        return [LastOperationAdapter.model_sql_to_model(model) for model in models]

    @staticmethod
    def find_by_id_name(id_name: str) -> LastOperationSQL or None:
        result = LastOperationSQL.where('id_name', '=', '{}'.format(id_name)).get()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def exists_in_db(id_name: str) -> bool:
        result = LastOperationAdapter.find_by_id_name(id_name)
        if result:
            return True
        else:
            return False
