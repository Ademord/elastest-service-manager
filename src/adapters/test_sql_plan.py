import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock
from database_manager import schema
import pymysql
from storage_sql import Plan
from storage_sql import MySQL_Driver
import orator


class TestPlan(Plan):
    def __init__(self):
        super(TestPlan, self).__init__()
        self.id = 1
        self.name = 'service1'
        self.description = 'description1'
        self.bindable = False
        self.free = True
        self.metadata = 'metadata1'

class MySQLDriver_PlanType(unittest.TestCase):

    def create_table(self):
        with schema.create('plans') as table:
            table.increments('id')
            table.string('name').unique()
            table.string('description').nullable()
            table.boolean('bindable').nullable()
            table.boolean('free').nullable()
            # TODO improve model for tags, metadata, requires
            table.string('metadata').nullable()

            table.datetime('created_at')
            table.datetime('updated_at')

    def setUp(self):
        try:
            self.create_table()
            print('Created Table Plans')
        except:
            pass
            # print('Could not create the table Plans')
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

    def add_plan(self, plan):
        plan.save()
        plans = Plan.where('name', '=', '{}'.format(plan.name)).get().serialize()
        self.assertEqual(len(plans), 1, msg='Assert plan exists.')

    def delete_plan(self, plan):
        plan.delete()
        plans = Plan.where('name', '=', '{}'.format(plan.name)).get().serialize()
        self.assertEqual(len(plans), 0, msg='Assert plan does NOT Exist.')

    def test_add_delete_plan(self):
        plan = TestPlan()
        self.add_plan(plan)
        self.delete_plan(plan)
