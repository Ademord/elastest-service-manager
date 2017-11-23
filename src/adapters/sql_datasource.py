from esm.models.service_type import ServiceType
from esm.models.dashboard_client import DashboardClient
from esm.models.service_metadata import ServiceMetadata
from esm.models.last_operation import LastOperation

from esm.models.plan import Plan
from esm.models.plan_metadata import PlanMetadata

from orator import DatabaseManager, Schema
from orator import Model
from typing import List
import pymysql
import json
import time
import os



'''
    ********************
    ********************
    **** TESTED CODE ***
    ********************
    ****** PLAN ********
    ********************
    ******** ♥ *********
    ********************
'''


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
            with Helper.schema.create('plans') as table:
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
        model.id = model_sql.id_name
        model.description = model_sql.description
        ''' BOOLEANS '''
        model.bindable = model_sql.bindable
        model.free = model_sql.free
        ''' OBJECTS '''
        model.metadata = PlanMetadataAdapter.from_blob(model_sql.metadata)
        return model

    @staticmethod
    def model_to_model_sql(model: Plan):
        model_sql = PlanSQL()
        ''' STRINGS '''
        model_sql.name = model.name
        model_sql.id_name = model.id
        model_sql.description = model.description
        ''' BOOLEANS '''
        model_sql.bindable = model.bindable
        model_sql.free = model.free
        ''' OBJECTS '''
        model_sql.metadata = PlanMetadataAdapter.to_blob(model.metadata)
        return model_sql

    @staticmethod
    def save(model: Plan) -> PlanSQL:
        model_sql = PlanAdapter.find_by_id_name(model.id) or None
        if model_sql:
            ''' STRINGS '''
            model_sql.name = model.name
            model_sql.id_name = model.id
            model_sql.description = model.description
            ''' BOOLEANS '''
            model_sql.bindable = model.bindable
            model_sql.free = model.free
            ''' OBJECTS '''
            model_sql.metadata = PlanMetadataAdapter.to_blob(model.metadata)
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
        models = [] or model.all()
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

'''
       self.swagger_types = {
            'bullets': str,
            'display_name': str,
            'costs': object,
            'extras': object

'''


class PlanMetadataAdapter(PlanMetadata):
    @classmethod
    def to_blob(cls, model: PlanMetadata) -> dict:
        my_dict = {}
        ''' STRINGS '''
        my_dict['bullets'] = model._bullets
        my_dict['display_name'] = model._display_name
        # TODO ambiguity | content will be lost | treated as None/List
        ''' OBJECTS '''
        my_dict['costs'] = model._costs
        my_dict['extras'] = model._extras
        return json.dumps(my_dict)

    @classmethod
    def from_blob(cls, blob) -> PlanMetadata:
        return cls.from_dict(dict(json.loads(blob)))


class DriverSQL:
    @staticmethod
    def get_connection():
        try:
            connection = pymysql.connect(
                host=Helper.host,
                port=Helper.port,
                user=Helper.user,
                password=Helper.password,
                db=Helper.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except:
            # Time required to setup the database
            return None

    @staticmethod
    def set_up(wait_time=10):
        connection = DriverSQL.get_connection()
        count = 3
        while not connection and count:
            # print('Retrying to connect to Database \'{}\'...'.format(Helper.database))
            count = count - 1
            time.sleep(wait_time)
            connection = DriverSQL.get_connection()

        if connection:
            # print('Successfully connected to Database \'{}\'...'.format(Helper.database))
            connection.close()
        else:
            raise Exception('Could not connect to the DB')

    @staticmethod
    def get_service(service_id: str=None) -> List[ServiceType]:
        if service_id:
            if ServiceTypeAdapter.exists_in_db(service_id):
                model_sql = ServiceTypeAdapter.find_by_id_name(service_id)
                model = ServiceTypeAdapter.model_sql_to_model(model_sql)
                return [model]
            else:
                # LOG.warn('Requested service type not found: {id}'.format(id=service_id))
                return []
        else:
            return ServiceTypeAdapter.get_all()

    @staticmethod
    def add_service(service: ServiceType) -> tuple:
        # TODO get plan and save it
        if ServiceTypeAdapter.exists_in_db(service.id):
            return 'The service already exists in the catalog.', 409

        ServiceTypeAdapter.save(service)
        # PlansAdapter.add_from_service(service) # ADDS ASSOCIATED PLANS TO THIS SERVICE
        if ServiceTypeAdapter.exists_in_db(service.id):
            return 'Service added successfully', 200
        else:
            return 'Could not save the Service in the DB', 500

    @staticmethod
    def delete_service(service_id: str = None) -> tuple:
        if service_id:
            if ServiceTypeAdapter.exists_in_db(service_id):
                ServiceTypeAdapter.delete(service_id)
                # PlansAdapter.delete_from_service(service) # DELETES ASSOCIATED PLANS TO THIS SERVICE
                return 'Service Deleted', 200
            else:
                return 'Service ID not found', 500
        else:
            ServiceTypeAdapter.delete_all()
            return 'Deleted all Services', 200


'''
    ********************
    ********************
    **** TESTED CODE ***
    ********************
    ***** SERVICE ******
    ********************
    ******** ♥ *********
    ********************
'''


class ServiceTypeSQL(Model):
    __table__ = 'service_types'

    def __init__(self):
        super(ServiceTypeSQL, self).__init__()
        Model.set_connection_resolver(Helper.db)

    @classmethod
    def delete_all(cls):
        Helper.db.table(cls.__table__).truncate()


class ServiceTypeAdapter:
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
    def sample_model() -> ServiceType:
        model = ServiceType()
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
    def sample_model_sql(cls) -> ServiceTypeSQL:
        model = cls.sample_model()
        return cls.model_to_model_sql(model)

    @staticmethod
    def model_sql_to_model(model_sql: ServiceTypeSQL) -> ServiceType:
        model = ServiceType()
        ''' STRINGS '''
        model.name = model_sql.name
        model.id = model_sql.id_name
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
    def model_to_model_sql(model: ServiceType):
        model_sql = ServiceTypeSQL()
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
    def save(model: ServiceType) -> ServiceTypeSQL:
        model_sql = ServiceTypeAdapter.find_by_id_name(model.id) or None
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
            model_sql = ServiceTypeAdapter.model_to_model_sql(model)
            model_sql.save()
        return model_sql

    @staticmethod
    def delete_all() -> None:
        ServiceTypeSQL.delete_all()

    @staticmethod
    def delete(id_name: str) -> None:
        model_sql = ServiceTypeAdapter.find_by_id_name(id_name) or None
        if model_sql:
            model_sql.delete()
        else:
            raise Exception('model not found on DB to delete')

    @staticmethod
    def get_all() -> [ServiceType]:
        model = ServiceTypeSQL()
        models = [] or model.all()
        return [ServiceTypeAdapter.model_sql_to_model(model) for model in models]

    @staticmethod
    def find_by_id_name(id_name: str) -> ServiceTypeSQL or None:
        result = ServiceTypeSQL.where('id_name', '=', '{}'.format(id_name)).get()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def exists_in_db(id_name: str) -> bool:
        result = ServiceTypeAdapter.find_by_id_name(id_name)
        if result:
            return True
        else:
            return False


class DashboardClientAdapter(DashboardClient):
    @classmethod
    def to_blob(cls, model: DashboardClient) -> dict:
        my_dict = {}
        ''' STRINGS '''
        my_dict['id'] = model._id
        my_dict['secret'] = model._secret
        my_dict['redirect_uri'] = model._redirect_uri
        return json.dumps(my_dict)

    @classmethod
    def from_blob(cls, blob) -> DashboardClient:
        return cls.from_dict(dict(json.loads(blob)))


class ServiceMetadataAdapter(ServiceMetadata):
    @classmethod
    def to_blob(cls, model: ServiceMetadata) -> dict:
        my_dict = {}
        ''' STRINGS '''
        my_dict['display_name'] = model._display_name
        my_dict['image_url'] = model._image_url
        my_dict['long_description'] = model._long_description
        my_dict['provider_display_name'] = model._provider_display_name
        my_dict['documentation_url'] = model._documentation_url
        my_dict['support_url'] = model._support_url
        my_dict['extras'] = model._extras
        return json.dumps(my_dict)

    @classmethod
    def from_blob(cls, blob) -> ServiceMetadata:
        return cls.from_dict(dict(json.loads(blob)))


class LastOperationAdapter(LastOperation):
    @classmethod
    def to_blob(cls, model: LastOperation) -> dict:
        my_dict = {}
        ''' STRINGS '''
        my_dict['state'] = model.state
        my_dict['description'] = model.description

        return json.dumps(my_dict)

    @classmethod
    def from_blob(cls, blob) -> LastOperation:
        return cls.from_dict(dict(json.loads(blob)))


'''
    ********************
    ********************
    **** TESTED CODE ***
    ********************
    ***** EXTRAS *******
    ********************
    ******** ♥ *********
    ********************
'''


class Helper:
    host = os.environ.get('DATABASE_HOST', '0.0.0.0')
    user = os.environ.get('DATABASE_USER', 'root')
    password = os.environ.get('DATABASE_PASSWORD', '')
    database = os.environ.get('DATABASE_NAME', 'mysql')
    port = int(os.environ.get('MYSQL_3306_TCP', 3306))
    config = {
        'mysql': {
            'driver': 'mysql',
            'prefix': '',
            'host': host,
            'database': database,
            'user': user,
            'password': password,
            'port': port
        }
    }
    db = DatabaseManager(config)
    schema = Schema(db)

