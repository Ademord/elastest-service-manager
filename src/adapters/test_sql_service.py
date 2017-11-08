import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock
from database_manager import schema
import pymysql
from storage_sql import Service
from storage_sql import MySQL_Driver
import orator


class TestService(Service):
    def __init__(self):
        super(TestService, self).__init__()
        self.id = 1
        self.name = 'service1'
        self.description = 'description1'
        self.bindable = False
        self.tags = 'description1'
        self.metadata = 'metadata1'
        self.requires = 'requirement1'
        self.dashboard_client = 'client1'

class MySQLDriver_ServiceType(unittest.TestCase):

    def create_table(self):
        with schema.create('service_types') as table:
            table.increments('id')
            table.string('name').unique()
            table.string('description').nullable()
            table.boolean('bindable').nullable()
            # TODO improve model for tags, metadata, requires
            table.string('tags').nullable()
            table.string('metadata').nullable()
            table.string('requires').nullable()
            # TODO relationship service_type*---*plan
            table.string('dashboard_client').nullable()

            table.datetime('created_at')
            table.datetime('updated_at')

    def setUp(self):
        try:
            self.create_table()
            print('Created Table Services')
        except:
            pass
            # print('Could not create the table Services')
        self.mysql_driver = MySQL_Driver()

    def tearDown(self):
        # schema.drop_if_exists('services')
        del self.mysql_driver

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
            print("I am unable to connect to the database")
        self.assertIsNotNone(connection)
        if connection:
            connection.close()

    def test_get_service_with_id(self):
        service = TestService()
        service.save()
        result = self.mysql_driver.get_service(service_id=service.id)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], Service)
        service.delete()

    @patch('storage_sql.Service.find')
    def test_get_service_with_id_and_not_found(self, mock_method):
        mock_method.return_value = []
        self.assertEqual(
            self.mysql_driver.get_service(service_id='1'), []
        )

    @patch('storage_sql.Service.all')
    def test_get_service_with_id_as_none(self, mock_method):
        mock_method.return_value = ['sevice1', 'service2']
        self.assertNotEqual(
            self.mysql_driver.get_service(service_id=None), []
        )

    def add_service(self, service):
        _, result = self.mysql_driver.add_service(service)
        self.assertEqual(result, 200, msg='Assert Successful Add')
        services = Service.where('name', '=', '{}'.format(service.name)).get().serialize()
        self.assertEqual(len(services), 1, msg='Assert service exists.')

    def delete_service(self, service):
        _, result = self.mysql_driver.delete_service(self.get_id_by_name(service.name))
        self.assertEqual(result, 200, msg='Assert Service Deleted')
        services = Service.where('name', '=', '{}'.format(service.name)).get().serialize()
        self.assertEqual(len(services), 0, msg='Assert service does NOT Exist.')

    def get_id_by_name(self, name):
        service = Service.where('name', '=', '{}'.format(name)).get().first()
        self.assertIsNotNone(service, msg='Assert get ID by Name')
        return service.id

    def test_add_delete_service(self):
        service = TestService()
        self.add_service(service)
        self.delete_service(service)

    @patch.object(Service, 'get_id')
    def test_add_service_unsucessful(self, mock_id):
        service = TestService()
        mock_id.return_value = None
        _, result = self.mysql_driver.add_service(service)
        self.assertEqual(result, 500, msg='Assert Can NOT Add')
        self.delete_service(service)

    @patch.object(Service, 'exists')
    def test_add_service_existing(self, mock_exists):
        service = TestService()
        mock_exists.return_value = True
        _, result = self.mysql_driver.add_service(service)
        self.assertEqual(result, 409, msg='Assert Service Already Exists')

    def test_delete_service_none(self):
        _, result = self.mysql_driver.delete_service(None)
        self.assertEqual(result, 500, msg='Assert Delete Service ID None')

    def test_delete_service_nonexistent(self):
        id = 126256598
        _, result = self.mysql_driver.delete_service(id)
        self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')

    # def test_storage_class(self):
    #     from storage import Storage
    #     storage = Storage()
    #     storage.add_service()
    #     self.assertRaises()