from orator import DatabaseManager, Schema
from esm.models.service_type import ServiceType
from esm.models.dashboard_client import DashboardClient
from esm.models.service_metadata import ServiceMetadata
from adapters.sql_service_type import ServiceTypeAdapter

from typing import List
import pymysql
import json
import time
import os


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


class DashboardClientAdapter(DashboardClient):
    @classmethod
    def to_blob(cls, model: DashboardClient) -> dict:
        my_dict = {}
        my_dict['id'] = model._id
        my_dict['secret'] = model._secret
        my_dict['redirect_uri'] = model._redirect_uri
        return json.dumps(my_dict)

    @classmethod
    def from_blob(cls, blob) -> DashboardClient:
        return cls.from_dict(dict(json.loads(blob)))


class MetadataAdapter(ServiceMetadata):
    @classmethod
    def to_blob(cls, model: ServiceMetadata) -> dict:
        my_dict = {}
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
