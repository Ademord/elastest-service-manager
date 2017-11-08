import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock
from database_manager import schema
import pymysql
from storage_sql import ServiceTypePlans
from storage_sql import MySQL_Driver
import orator


class TestServiceTypePlans(ServiceTypePlans):
    def __init__(self):
        super(TestServiceTypePlans, self).__init__()
        self.id = 1
        self.service_type_id = 1
        self.plan_id = 1
        self.plan_updateable = False

class MySQLDriver_ServiceTypePlansType(unittest.TestCase):
    def create_table(self):
        with schema.create('plan_service_types') as table:
            table.increments('id')
            table.integer('service_type_id')
            table.integer('plan_id')
            table.boolean('plan_updateable').nullable()
            table.datetime('created_at')
            table.datetime('updated_at')

    def setUp(self):
        try:
            self.create_table()
            print('Created Table ServiceTypePlans')
        except:
            pass
            # print('Could not create the table ServiceTypePlanss')
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

    def add_model(self, model):
        model.save()
        self.assert_existence(model, 1, 'Assert model exists.')

    def delete_model(self, model):
        model.delete()
        self.assert_existence(model, 0, 'Assert model does NOT Exist.')

    def assert_existence(self, model, quantity, message=None):

        service_type_models = ServiceTypePlans.where(
            'plan_id', '=', '{}'.format(model.plan_id),
            'and',
            'service_type_id', '=', '{}'.format(model.service_type_id),
        ).get().serialize()
        self.assertEqual(len(service_type_models), 0, msg=message)

    def test_add_delete_model(self):
        model = TestServiceTypePlans()
        self.add_model(model)
        self.delete_model(model)
