# INSTANCE
from adapters.sql_datasource import PlanAdapter, ServiceTypeAdapter, PlanServiceTypeAdapter, \
    ServiceInstanceAdapter as Adapter, DriverSQL, ServiceInstanceSQL, ServiceTypeSQL, LastOperationAdapter
from esm.models.service_instance import ServiceInstance
# GENERAL
import unittest
from unittest.mock import patch
from unittest import skipIf
import orator
import os



# @skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
class TestCaseServiceInstance(unittest.TestCase):
    def setUp(self):
        ''' PREREQUISITES'''
        PlanAdapter.create_table()
        ServiceTypeAdapter.create_table()
        PlanServiceTypeAdapter.create_table()
        # ManifestAdapter.create_table()
        self.service = ServiceTypeAdapter.sample_model('instance1')
        ServiceTypeAdapter.save(self.service)

        Adapter.create_table()
        self.test_model = Adapter.sample_model('instance1')
        self.id_name = Adapter.get_id(self.test_model)
        _, self.result = DriverSQL.add_service_instance(self.test_model)

    def tearDown(self):
        DriverSQL.delete_service_instance(Adapter.get_id(self.test_model))
        ServiceTypeAdapter.delete(self.service.id)

    def test_instance_create_table(self):
        self.assertTrue(ServiceInstanceSQL.table_exists())
        with self.assertRaises(orator.exceptions.query.QueryException):
            ServiceInstanceSQL.create_table()

    def test_sample_model(self):
        self.assertIsInstance(self.test_model, ServiceInstance)

        model_sql = Adapter.find_by_id_name(self.id_name)
        self.assertIsInstance(model_sql, ServiceInstanceSQL)

        ''' query associated service '''
        service = model_sql.service
        self.assertIsInstance(service, ServiceTypeSQL)

        ''' verify relations '''
        instances = service.instances
        # print(instances)
        # print(instances.all())
        # print(model_sql)
        # print(instances.is_empty())
        self.assertGreater(len(instances), 0)

    def test_get_instance_with_instance_id(self):
        result = DriverSQL.get_service_instance(instance_id=self.id_name)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceInstance)

    # @patch.object(ServiceInstance, 'find')
    # def test_get_instance_with_instance_id_none_found(self, mock_find):
    #     mock_find.return_value = None
    #     result = DriverSQL.get_service_instance(instance_id=self.id_name)
    #     self.assertEqual(len(result), 0)

    # def test_get_instance_with_nothing(self):
    #     instance = self.test_instance
    #     instance.save()
    #     result = MySQL_Driver.get_service_instance(instance_id=None)
    #     self.assertGreater(len(result), 0)
    #     self.assertIsInstance(result[0], ServiceInstance)
    #
    # def add_instance(self, instance):
    #     _, result = MySQL_Driver.add_service_instance(instance)
    #     self.assertEqual(result, 200, msg='Assert Service Instance Successful Add')
    #     instances = ServiceInstance.where('name', '=', '{}'.format(instance.name)).get().serialize()
    #     self.assertEqual(len(instances), 1, msg='Assert Service Instance exists.')
    #
    # def delete_instance(self, instance):
    #     _, result = MySQL_Driver.delete_service_instance(self.get_id_by_name(instance.name))
    #     self.assertEqual(result, 200, msg='Assert Service Deleted' + ' ' + _)
    #     instances = ServiceInstance.where('name', '=', '{}'.format(instance.name)).get().serialize()
    #     self.assertEqual(len(instances), 0, msg='Assert Service Instance does NOT Exist.')
    #
    # def get_id_by_name(self, name):
    #     service = ServiceInstance.where('name', '=', '{}'.format(name)).get().first()
    #     self.assertIsNotNone(service, msg='Assert get ID by Name')
    #     return service.id
    #
    # def test_add_delete_instance(self):
    #     instance = self.test_instance
    #     self.add_instance(instance)
    #     self.delete_instance(instance)
    #
    # @patch.object(ServiceInstance, 'get_id')
    # def test_add_instance_unsucessful(self, mock_id):
    #     instance = self.test_instance
    #     mock_id.return_value = None
    #     _, result = MySQL_Driver.add_service_instance(instance)
    #     self.assertEqual(result, 500, msg='Assert Can NOT Add Service Instance')
    #     self.delete_instance(instance)
    #
    # def test_add_instance_existing(self):
    #     instance = self.test_instance
    #     self.add_instance(instance)
    #     _, result = MySQL_Driver.add_service_instance(instance)
    #     self.assertEqual(result, 201, msg='Assert Service Instance Already Exists')
    #     instances = ServiceInstance.where('name', '=', '{}'.format(instance.name)).get().serialize()
    #     self.assertEqual(len(instances), 1, msg='Assert Service Instance exists.')
    #     self.delete_instance(instance)
    #
    # def test_delete_instance_none(self):
    #     _, result = MySQL_Driver.delete_service_instance(None)
    #     self.assertEqual(result, 500, msg='Assert Delete Service ID None')
    #
    # def test_delete_instance_nonexistent(self):
    #     id = 126256598
    #     _, result = MySQL_Driver.delete_service_instance(id)
    #     self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')

# MANIFEST

    def test_adapter_delete(self):
        with self.assertRaises(Exception):
            Adapter.delete(id_name='')

    def test_adapter_save_to_update(self):
        self.test_model.state = LastOperationAdapter.sample_model('instance-updated!')
        model_sql = Adapter.save(self.test_model)
        exists = Adapter.exists_in_db(model_sql.id_name)
        self.assertTrue(exists)

    def test_get_instance_with_id(self):
        models = DriverSQL.get_service_instance(instance_id=self.id_name)
        self.assertGreater(len(models), 0)
        self.assertIsInstance(models[0], ServiceInstance)

    @patch.object(Adapter, 'exists_in_db')
    def test_get_instance_with_id_and_not_found(self, mock_exists_in_db):
        mock_exists_in_db.return_value = False
        models = DriverSQL.get_service_instance(self.id_name)
        self.assertEqual(models, [])

    def test_get_instance_with_id_as_none(self):
        models = DriverSQL.get_service_instance(instance_id=None)
        self.assertNotEqual(models, [])

    def test_instance_created(self):
        self.assertEqual(self.result, 200, msg='Assert Successful Add')
        exists = Adapter.exists_in_db(self.id_name)
        self.assertTrue(exists, msg='Assert Instance exists.')
        model_sql = Adapter.find_by_id_name(self.id_name)
        self.assertIsInstance(model_sql, ServiceInstanceSQL)

    def test_instance_deletion(self):
        _, result = DriverSQL.delete_service_instance(self.id_name)
        self.assertEqual(self.result, 200, msg='Assert Instance Deleted')
        exists = Adapter.exists_in_db(self.id_name)
        self.assertFalse(exists, msg='Assert Instance does NOT Exist.')
        model_sql = Adapter.find_by_id_name(self.id_name)
        self.assertIsNone(model_sql)

    @patch.object(Adapter, 'exists_in_db')
    def test_add_instance_existing(self, mock_exists):
        mock_exists.return_value = True
        _, result = DriverSQL.add_service_instance(self.test_model)
        self.assertEqual(result, 409, msg='Assert Instance Already Exists')

    def test_delete_instance_nonexistent(self):
        _, result = DriverSQL.delete_service_instance(self.id_name)
        _, result = DriverSQL.delete_service_instance(self.id_name)
        self.assertEqual(result, 500, msg='Assert Delete Instance Nonexistent')

