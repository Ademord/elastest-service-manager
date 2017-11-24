from esm.models.service_type import Plan
from adapters.sql_datasource import PlanSQL
from adapters.sql_datasource import PlanAdapter
from adapters.sql_datasource import DriverSQL
from adapters.sql_datasource import ServiceTypeAdapter
from adapters.sql_datasource import PlanServiceTypeAdapter
from adapters.sql_datasource import ManifestAdapter

from unittest.mock import patch
from unittest import skipIf
import unittest
import os
import orator


@skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
class TestCasePlan(unittest.TestCase):

    def setUp(self):
        self.test_model = PlanAdapter.sample_model()
        PlanAdapter.create_table()
        PlanAdapter.save(self.test_model)

    def tearDown(self):
        if PlanAdapter.exists_in_db(self.test_model.id):
            PlanAdapter.delete(self.test_model.id)

    def test_plan_create_table(self):
        self.assertTrue(PlanSQL.table_exists())
        with self.assertRaises(orator.exceptions.query.QueryException):
            PlanSQL.create_table()

    def test_sample_model(self):
        self.assertIsInstance(self.test_model, Plan)
        model_sql = PlanAdapter.sample_model_sql()
        self.assertIsInstance(model_sql, PlanSQL)
        model = PlanAdapter.model_sql_to_model(model_sql)
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

    # def test_adapter_delete_all(self):
    #     PlanServiceTypeAdapter.delete_all()
    #     ManifestAdapter.delete_all()
    #     PlanAdapter.delete_all()
    #     results = PlanAdapter.get_all()
    #     self.assertEqual(len(results), 0)

    def test_adapter_create_from_service(self):
        service = ServiceTypeAdapter.sample_model()
        plans_sql = PlanAdapter.plans_sql_from_service(service)
        self.assertGreater(len(plans_sql), 0)
        self.assertIsInstance(plans_sql[0], PlanSQL)

