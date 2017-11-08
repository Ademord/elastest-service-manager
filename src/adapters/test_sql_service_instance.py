import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock
from database_manager import schema
import pymysql
from storage_sql import ServiceInstance
from storage_sql import MySQL_Driver
import orator


class MySQLDriver_ServiceTest(unittest.TestCase):
    def create_service_instance_table(self):
        with schema.create('service_instances') as table:
            table.increments('id')
            table.integer('plan_id').unique()
            # table.integer('user_id').unsigned()
            # .references('id').on('plans')
            table.string('instance_content')
            table.string('name').unique()
            table.datetime('created_at')
            table.datetime('updated_at')
            # print('Created Table Services')

            # with schema.create('plans') as table:
            #     table.increments('id')
            #     table.string('name').unique()

    def setUp(self):
        try:
            self.create_service_instance_table()
        except:
            pass
            # print('Could not create the table Services')
        self.mysql_driver = MySQL_Driver()
        self.test_instance = ServiceInstance()
        self.test_instance.id = 1
        self.test_instance.name = 'service1-instance'
        self.test_instance.plan_id = 1
        self.test_instance.instance_content = 'hello'

    def tearDown(self):
        # schema.drop_if_exists('instances')
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

    def test_get_instance_with_instance_id(self):
        instance = self.test_instance
        instance.save()
        result = self.mysql_driver.get_service_instance(instance_id=instance.id)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceInstance)
        instance.delete()

    @patch.object(ServiceInstance, 'find')
    def test_get_instance_with_instance_id_none_found(self, mock_find):
        instance = self.test_instance
        instance.save()
        mock_find.return_value = None
        result = self.mysql_driver.get_service_instance(instance_id=instance.id)
        self.assertEqual(len(result), 0)
        instance.delete()

    def test_get_instance_with_nothing(self):
        instance = self.test_instance
        instance.save()
        result = self.mysql_driver.get_service_instance(instance_id=None)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceInstance)
        instance.delete()

    def add_instance(self, name):
        instance = self.test_instance
        _, result = self.mysql_driver.add_service_instance(instance)
        self.assertEqual(result, 200, msg='Assert Service Instance Successful Add')
        instances = ServiceInstance.where('name', 'like', '%{}%'.format(instance.name)).get().serialize()
        self.assertEqual(len(instances), 1, msg='Assert Service Instance exists.')

    def delete_instance(self, name):
        id = self.get_id_by_name(name)
        self.assertIsNotNone(id)
        _, result = self.mysql_driver.delete_service_instance(id)
        self.assertEqual(result, 200, msg='Assert Service Instance Deleted' + ' ' + _)
        instances = ServiceInstance.where('name', 'like', '%{}%'.format(name)).get().serialize()
        self.assertEqual(len(instances), 0, msg='Assert Service Instance does NOT Exist.')

    def get_id_by_name(self, name):
        instance = self.test_instance
        instances = ServiceInstance.where('name', 'like', '%{}%'.format(instance.name)).get().serialize()
        if instances: return instances[0]['id']
        else: return None

    def test_add_delete_instance(self):
        name = 'instance1'
        self.add_instance(name)
        self.delete_instance(name)

    @patch.object(ServiceInstance, 'get_id')
    def test_add_instance_unsucessful(self, mock_id):
        instance = self.test_instance
        mock_id.return_value = None
        _, result = self.mysql_driver.add_service_instance(instance)
        self.assertEqual(result, 500, msg='Assert Can NOT Add Service Instance')
        # it saves but the mock disrupts the call, so must delete
        self.delete_instance(instance.name)

    def test_add_instance_existing(self):
        instance = self.test_instance
        self.add_instance(instance.name)
        instance.name = instance.name + 'v2'
        _, result = self.mysql_driver.add_service_instance(instance)
        self.assertEqual(result, 201, msg='Assert Service Already Exists')
        instances = ServiceInstance.where('name', 'like', '%{}%'.format(instance.name)).get().serialize()
        self.assertEqual(len(instances), 1, msg='Assert Service Instance exists.')

        self.delete_instance(instance.name)


    def test_delete_instance_none(self):
        _, result = self.mysql_driver.delete_service_instance(None)
        self.assertEqual(result, 500, msg='Assert Delete Service ID None')

    def test_delete_instance_nonexistent(self):
        id = 126256598
        _, result = self.mysql_driver.delete_service_instance(id)
        self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')
