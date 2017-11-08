import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock
from database_manager import schema
import pymysql
from storage_sql import ServiceLastOperation
from storage_sql import MySQL_Driver
import orator


class MySQLDriver_ServiceTest(unittest.TestCase):
    def create_last_operation_table(self):
        with schema.create('last_operations') as table:
            table.increments('id')
            table.integer('instance_id')
            table.string('name').unique()
            table.datetime('created_at')
            table.datetime('updated_at')

    def setUp(self):
        try:
            self.create_last_operation_table()
        except:
            pass
            # print('Could not create the table Services')
        self.mysql_driver = MySQL_Driver()
        self.test_operation = ServiceLastOperation()
        self.test_operation.name = 'service1-operation'
        self.test_operation.instance_id = 1

    def tearDown(self):
        # schema.drop_if_exists('operations')
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

    def test_get_operation_with_operation_id(self):
        operation = self.test_operation
        operation.save()
        result = self.mysql_driver.get_last_operation(instance_id=operation.instance_id)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceLastOperation)
        operation.delete()

    @patch.object(ServiceLastOperation, 'find')
    def test_get_operation_with_operation_id_none_found(self, mock_find):
        operation = self.test_operation
        operation.save()
        mock_find.return_value = None
        result = self.mysql_driver.get_last_operation(instance_id=operation.instance_id)
        self.assertEqual(len(result), 0)
        operation.delete()

    def test_get_operation_with_nothing(self):
        operation = self.test_operation
        operation.save()
        result = self.mysql_driver.get_last_operation(instance_id=None)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceLastOperation)
        operation.delete()

    def add_operation(self, operation):
        _, result = self.mysql_driver.add_last_operation(operation.instance_id, operation)
        self.assertEqual(result, 200, msg='Assert Service Instance Successful Add')
        operations = ServiceLastOperation.where('name', 'like', '%{}%'.format(operation.name)).get().serialize()
        self.assertEqual(len(operations), 1, msg='Assert Service Instance exists.')


    def delete_operation(self, operation):
        _, result = self.mysql_driver.delete_last_operation(operation.instance_id)
        self.assertEqual(result, 200, msg='Assert Service Instance Deleted' + ' ' + _)
        operation_result = operation.find(self.get_id_by_name(operation.name))
        self.assertIsNone(operation_result, msg='Assert Service Instance does NOT Exist.')

    def get_id_by_name(self, name):
        operation = self.test_operation
        operations = ServiceLastOperation.where('name', '=', '{}'.format(operation.name)).get().serialize()
        if operations: return operations[0]['id']
        else: return None

    def test_add_delete_operation(self):
        operation = self.test_operation
        self.add_operation(operation)
        self.delete_operation(operation)

    @patch.object(ServiceLastOperation, 'get_id')
    def test_add_operation_unsucessful(self, mock_id):
        operation = self.test_operation
        mock_id.return_value = None
        _, result = self.mysql_driver.add_last_operation(operation.instance_id, operation)
        self.assertEqual(result, 500, msg='Assert Can NOT Add Service Instance')
        # it saves but the mock disrupts the call, so must delete
        self.delete_operation(operation)

    def test_add_two_operation(self):
        import copy
        operation = copy.deepcopy(self.test_operation)
        operation2 = copy.deepcopy(self.test_operation)
        operation2.name = operation2.name + 'v2'
        self.add_operation(operation)
        self.add_operation(operation2)
        self.delete_operation(operation)
        self.delete_operation(operation2)

    def test_delete_operation_none(self):
        _, result = self.mysql_driver.delete_last_operation(None)
        self.assertEqual(result, 500, msg='Assert Delete Service ID None')

    def test_delete_operation_nonexistent(self):
        id = 126256598
        _, result = self.mysql_driver.delete_last_operation(id)
        self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')
