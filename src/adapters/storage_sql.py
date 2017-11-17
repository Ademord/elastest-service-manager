import os
from typing import List
# import adapters.log
# from esm.models.last_operation import LastOperation
# from esm.models.manifest import Manifest
# from esm.models.service_instance import ServiceInstance
# from esm.models.service_type import ServiceType
# LOG = adapters.log.get_logger(name=__name__)

from orator import Model
from orator.orm import belongs_to
from orator.orm import has_many
import pymysql

from orator import DatabaseManager, Schema
import os
config = {
    'mysql': {
        'driver': 'mysql',
        'host': os.environ.get('DATABASE_HOST', 'localhost'),
        'database': os.environ.get('DATABASE_NAME', 'elastest'),
        'user': os.environ.get('DATABASE_USER', 'root'),
        'password': os.environ.get('DATABASE_PASSWORD', ''),
        'prefix': '',
        'port': os.environ.get('DATABASE_PORT', 3306)
    }
}
db = DatabaseManager(config)
schema = Schema(db)

class Service(Model):
    __table__ = 'service_types'

    def __init__(self):
        super(Service, self).__init__()
        Model.set_connection_resolver(db)
        id = None
        name = None
        description = None
        bindable = False
        tags= None
        metadata = None
        requires = None
        dashboard_client = None

        # def test_DB_service_model_consistent(self):
        #     pass
        #

    def exists(self):
        # TODO must search based on unique keys that wont crash when updated

        return len(Service.where('name', '=', '{}'.format(self.name)).get().serialize()) > 0

    def get_id(self):
        return self.id

class Plan(Model):
    __table__ = 'plans'

    @has_many('service_id')  # foreign key
    def manifests(self):
        return ServiceManifest

    def __init__(self):
        super(Plan, self).__init__()
        Model.set_connection_resolver(db)
        id = None
        name = None
        description = None
        bindable = False
        free = True
        metadata = None

        # def test_DB_service_model_consistent(self):
        #     pass
        #

class ServiceManifest(Model):
    __table__ = 'service_manifests'

    @belongs_to('plan_id')  # local key
    def plan(self):
        return Plan

    @belongs_to('service_id')  # local key
    def service(self):
        return Service

    @has_many('manifest_id')  # foreign key
    def instances(self):
        return ServiceInstance

    def __init__(self):
        super(ServiceManifest, self).__init__()
        Model.set_connection_resolver(db)
        name = None
        content = None
        type = None

    def exists(self):
        # TODO must search based on unique keys that wont crash when updated
        return len(ServiceManifest.where('name', 'like', '%{}%'.format(self.name)).get().serialize()) > 0

    def get_id(self):
        return self.id

class ServiceInstance(Model):
    __table__ = 'service_instances'

    @belongs_to('manifest_id')  # local key
    def manifest(self):
        return ServiceManifest

    @has_many('instance_id')  # foreign key
    def operations(self):
        return ServiceLastOperation

    def __init__(self):
        super(ServiceInstance, self).__init__()
        Model.set_connection_resolver(db)
        id = None
        name = None
        context = None

    def exists(self):
        # TODO must search based on unique keys that wont crash when updated
        return len(ServiceInstance.where('name', '=', '{}'.format(self.name)).get().serialize()) > 0

    def get_id(self):
        return self.id

class ServiceLastOperation(Model):
    __table__ = 'last_operations'

    @belongs_to('instance_id')  # local key
    def instance(self):
        return ServiceInstance

    def __init__(self):
        super(ServiceLastOperation, self).__init__()
        Model.set_connection_resolver(db)
        id = None
        name = None
        instance_id =  None

    def exists(self):
        # TODO must search based on unique keys that wont crash when updated
        results = ServiceLastOperation.where('name', '=', '{}'.format(self.name)).get().serialize()
        return len(results) > 0

    def get_id(self):
        return self.id

class MySQL_Driver():

    def __init__(self) -> None:
        # start connection
        name = 'MySQLStorage'
        # LOG.info('Using the {storage_client}.'.format(storage_client=self.name))
        # LOG.info('{storage_client} is persistent.'.format(storage_client=self.name))
        self.test_DB_connect_exception()

    def test_DB_connect_exception(self):
        connection = None
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='',
                                         db='elastest',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
        except:
            raise Exception('DB is unreachable')
        if connection:
            connection.close()

    def get_service(self, service_id: str=None): # -> List[ServiceType]
        if service_id:
            model = Service()
            service = model.find(service_id) # .serialize()
            if service:
                return [service]
                # TODO adapt to data type
                # return [ServiceType.from_dict(service)]
            else:
                # LOG.warn('Requested service type not found: {id}'.format(id=service_id))
                return []
        else:
            model = Service()
            services = [] or model.all() # .serialize()
            return services
            # TODO adapt to data type
            # for service in Service.all().serialize():
            #     services.append(ServiceType.from_dict(service))
            # return services

    def add_service(self, _service) -> tuple:
         # TODO since when does an 'add' arrive with a service.id?
        # _service = service.to_dict()
        service = Service()
        service.name = _service.name
        service.description = _service.description
        service.bindable = _service.bindable
        service.tags = _service.tags
        service.metadata = _service.metadata
        service.requires = _service.requires
        service.dashboard_client = _service.dashboard_client

        if service.exists():
            return 'The service already exists in the catalog.', 409
        else:
            service.save()
            if service.get_id() is None:

                return 'Could not save the Service in the DB', 500
            else:
                # TODO compare if '200' is accepted
                return 'Service added succesfully', 200

    def delete_service(self, service_id: str=None): # -> None
        if service_id:
            service = Service.find(service_id)
            if service:
                service.delete()
                return 'Service Deleted', 200
            else:
                return 'Service ID not found', 500
                # self.ESM_DB.services.delete_one({'id': service_id})
        else:
            return 'Service id not found', 500
            # TODO what's this?
            # self.ESM_DB.services.delete_many({})

    def get_manifest(self, manifest_id: str=None, plan_id: str=None): #  -> List[Manifest]
        if manifest_id and plan_id:
            raise Exception('Query manifests only by manifest_id OR plan_id')
        if plan_id:
            manifests = ServiceManifest.where('plan_id', 'like', '%{}%'.format(plan_id)).get().serialize()
            if manifests:
                manifest_id = manifests[0]['id']
        if manifest_id:
            model = ServiceManifest()
            model = model.find(manifest_id)  # .serialize()\
            if model:
                # LOG.debug("replacing <br/> with newlines")
                model.content = model.content.replace('</br>', '\n')
                return [model] # TODO adapt to [Manifest.from_dict(m)]
            else:
                # LOG.warn('Requested manifest not found: {id}'.format(id=manifest_id))
                return []
        else:
            manifests = [] or ServiceManifest.all()
            for manifest in manifests:
                # LOG.debug("replacing <br/> with newlines")
                manifest.content = manifest.content.replace('</br>', '\n')
            return manifests

    def add_manifest(self, manifest) -> tuple:
        manifestSQL = ServiceManifest()
        manifestSQL.plan_id = manifest.plan_id
        manifestSQL.service_id = manifest.service_id
        manifestSQL.name = manifest.name  # TODO must change
        manifestSQL.type = manifest.type
        manifestSQL.content = manifest.content
        manifestSQL.content = manifest.content.replace('\n', '</br>')

        # TODO this function must be updated to correctly search through the manifests
        if manifestSQL.exists():
            return 'The Service Manifest already exists in the catalog.', 409
        else:
            manifestSQL.save()
            if manifestSQL.get_id() is None:
                return 'Could not save the Service Manifest in the DB', 500
            else:
                # TODO compare if '200' is accepted
                return 'Service Manifest added succesfully', 200

    def delete_manifest(self, manifest_id: str=None): #-> None:
        if manifest_id:
            service = ServiceManifest.find(manifest_id)
            if service:
                service.delete()
                return 'Service Manifest Deleted', 200
            else:
                return 'Service Manifest ID not found', 500
                # self.ESM_DB.services.delete_one({'id': service_id})
        else:
            return 'Service Manifest ID not found', 500
            # TODO what's this?
            # self.ESM_DB.services.delete_many({})

    def get_service_instance(self, instance_id: str=None): # -> List[ServiceInstance]:
        if instance_id:
            model = ServiceInstance()
            instance = model.find(instance_id) # .serialize()
            if instance:
                return [instance]
                # TODO adapt to data type
                # return [ServiceType.from_dict(service)]
            else:
                # LOG.warn('Requested service type not found: {id}'.format(id=service_id))
                return []
        else:
            model = ServiceInstance()
            instances = [] or model.all() # .serialize()
            return instances
            # TODO adapt to data type
            # for service in Service.all().serialize():
            #     services.append(ServiceType.from_dict(service))
            # return services

    def add_service_instance(self, instance) -> tuple:
        instanceSQL = ServiceInstance()
        instanceSQL.name = instance.name
        instanceSQL.manifest_id = instance.manifest_id
        instanceSQL.context = instance.context
        instanceSQL.state = instance.state
        instanceSQL.context = instance.context.replace('\n', '</br>')
        if instanceSQL.exists():
            # LOG.info('A duplicate service instance was attempted to be stored. '
            #          'Updating the existing service instance {id}.'
            #          'Content supplied:\n{content}'.format(id=service_instance.context['id'],
            #                                                content=service_instance.to_str()))
            # TODO keep consistency here
            instances = ServiceInstance.where('name', '=', '{}'.format(instanceSQL.name)).get()
            instanceSQL = instances.get(0)
            instanceSQL.name = instance.name
            instanceSQL.context = instance.context
            instanceSQL.context = instance.context.replace('\n', '</br>')
            instanceSQL.update()
            return 'The Service Instance already exists in the catalog. Updating the registry.', 201
        else:
            instanceSQL.save()
            if instanceSQL.get_id() is None:
                return 'Could not save the Service Instance in the DB', 500
            else:
                # TODO compare if '200' is accepted
                return 'Service Instance added succesfully', 200

    def delete_service_instance(self, instance_id: str = None):  # -> None:
        if instance_id:
            instance = ServiceInstance.find(instance_id)
            if instance:
                instance.delete()
                return 'Service Instance Deleted', 200
            else:
                return 'Service Instance ID not found', 500
                # self.ESM_DB.services.delete_one({'id': service_id})
        else:
            return 'Service Instance ID not found', 500
            # TODO what's this?
            # self.ESM_DB.services.delete_many({})

    def get_last_operation(self, instance_id: str=None): # -> List[LastOperation]:
        if instance_id:
            model = ServiceLastOperation()
            results = ServiceLastOperation.where('instance_id', 'like',
                                                 '%{}%'.format(instance_id)).get().serialize()
            operation = model.find(results[0]['id']) # .serialize()
            if operation:
                return [operation]
                # TODO adapt to data type
                # return [LastOperation.from_dict(last_operations.find_one(id)]
            else:
                # LOG.warn('Requested last operation type not found: {id}'.format(id=instance_id))
                return []
        else:
            model = ServiceLastOperation()
            operation = [] or model.all() # .serialize()
            return operation
            # TODO adapt to data type
            # for service in Service.all().serialize():
            #     services.append(ServiceType.from_dict(service))
            # return services

    def add_last_operation(self, instance_id, last_operation) -> tuple:
        if instance_id:
            last_operationSQL = ServiceLastOperation()
            last_operationSQL.name = last_operation.name
            last_operationSQL.state = last_operation.state
            last_operationSQL.description = last_operation.description
            last_operationSQL.instance_id = instance_id
            last_operationSQL.save()
            if last_operationSQL.get_id() is None:
                return 'Could not save the Service Instance Last Operation in the DB', 500
            else:
                # TODO compare if '200' is accepted
                return 'Service Instance Last Operation added succesfully', 200

    def delete_last_operation(self, instance_id: str=None) -> tuple: # -> None:
        if instance_id:
            operations = ServiceLastOperation.where('instance_id', 'like', '%{}%'.format(instance_id)).order_by('created_at', 'desc').get()
            if operations:
                operation = operations.first()
                operation.delete()
                return 'Service Instance Last Operation Deleted', 200
            else:
                return 'Operation not found for this Service Instance ID', 500
                # self.ESM_DB.services.delete_one({'id': service_id})
        else:
            return 'Service Instance ID not found', 500
            # TODO what's this?
            # self.ESM_DB.services.delete_many({})
