from esm.models.service_type import Plan
from adapters.sql_datasource import PlanSQL
from adapters.sql_datasource import PlanAdapter
from adapters.sql_datasource import DriverSQL

from unittest.mock import patch
from unittest import skipIf
import unittest
import os


# @skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
class TestCasePlan(unittest.TestCase):

    def setUp(self):
        self.test_model = PlanAdapter.sample_model()
        PlanAdapter.create_table()
        PlanAdapter.save(self.test_model)

    def tearDown(self):
        if PlanAdapter.exists_in_db(self.test_model.id):
            PlanAdapter.delete(self.test_model.id)

    def test_db_connect_successful(self):
        connection = DriverSQL.get_connection()
        self.assertIsNotNone(connection)
        connection.close()
        wait_time = 0
        DriverSQL.set_up(wait_time)

    @patch.object(DriverSQL, 'get_connection')
    def test_db_connect_not_successful(self, mock_connection):
        wait_time = 0
        mock_connection.return_value = None
        with self.assertRaises(Exception):
            DriverSQL.set_up(wait_time)

    def test_sample_model(self):
        self.assertIsInstance(self.test_model, Plan)
        model_sql = PlanAdapter.sample_model_sql()
        self.assertIsInstance(model_sql, PlanSQL)
        model = PlanAdapter.model_sql_to_model(model_sql)
        print('woo')
        self.assertIsInstance(model, Plan)

    def test_adapter_delete(self):
        with self.assertRaises(Exception):
            PlanAdapter.delete(id_name='')

    def test_adapter_save_to_update(self):
        self.test_model.name = 'new-name'
        model_sql = PlanAdapter.save(self.test_model)
        exists = PlanAdapter.exists_in_db(model_sql.id_name)
        self.assertTrue(exists)

    def test_adapter_get_all(self):
        results = PlanAdapter.get_all()
        self.assertGreater(len(results), 0)

    def test_adapter_delete_all(self):
        PlanAdapter.delete_all()
        results = PlanAdapter.get_all()
        self.assertEqual(len(results), 0)

