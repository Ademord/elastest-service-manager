import unittest
from unittest.mock import patch
from unittest import skipIf

from adapters.storage_sql import ServiceInstanceSQL as ServiceInstance
from adapters.storage_sql import SampleServiceInstance
from adapters.storage_sql import MySQL_Driver

import os

@skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
class TestCaseServiceInstance(unittest.TestCase):
    def setUp(self):
        MySQL_Driver = MySQL_Driver()
        self.test_instance = SampleServiceInstance()
        self.test_instance.create_table()
        self.test_instance.setup()

    def tearDown(self):
        # schema.drop_if_exists('instances')
        del MySQL_Driver
        self.test_instance.delete_cascade()

    def test_get_instance_with_instance_id(self):
        instance = self.test_instance
        instance.save()
        result = MySQL_Driver.get_service_instance(instance_id=instance.id)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceInstance)

    @patch.object(ServiceInstance, 'find')
    def test_get_instance_with_instance_id_none_found(self, mock_find):
        instance = self.test_instance
        instance.save()
        mock_find.return_value = None
        result = MySQL_Driver.get_service_instance(instance_id=instance.id)
        self.assertEqual(len(result), 0)

    def test_get_instance_with_nothing(self):
        instance = self.test_instance
        instance.save()
        result = MySQL_Driver.get_service_instance(instance_id=None)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceInstance)

    def add_instance(self, instance):
        _, result = MySQL_Driver.add_service_instance(instance)
        self.assertEqual(result, 200, msg='Assert Service Instance Successful Add')
        instances = ServiceInstance.where('name', '=', '{}'.format(instance.name)).get().serialize()
        self.assertEqual(len(instances), 1, msg='Assert Service Instance exists.')

    def delete_instance(self, instance):
        _, result = MySQL_Driver.delete_service_instance(self.get_id_by_name(instance.name))
        self.assertEqual(result, 200, msg='Assert Service Deleted' + ' ' + _)
        instances = ServiceInstance.where('name', '=', '{}'.format(instance.name)).get().serialize()
        self.assertEqual(len(instances), 0, msg='Assert Service Instance does NOT Exist.')

    def get_id_by_name(self, name):
        service = ServiceInstance.where('name', '=', '{}'.format(name)).get().first()
        self.assertIsNotNone(service, msg='Assert get ID by Name')
        return service.id

    def test_add_delete_instance(self):
        instance = self.test_instance
        self.add_instance(instance)
        self.delete_instance(instance)

    @patch.object(ServiceInstance, 'get_id')
    def test_add_instance_unsucessful(self, mock_id):
        instance = self.test_instance
        mock_id.return_value = None
        _, result = MySQL_Driver.add_service_instance(instance)
        self.assertEqual(result, 500, msg='Assert Can NOT Add Service Instance')
        self.delete_instance(instance)

    def test_add_instance_existing(self):
        instance = self.test_instance
        self.add_instance(instance)
        _, result = MySQL_Driver.add_service_instance(instance)
        self.assertEqual(result, 201, msg='Assert Service Instance Already Exists')
        instances = ServiceInstance.where('name', '=', '{}'.format(instance.name)).get().serialize()
        self.assertEqual(len(instances), 1, msg='Assert Service Instance exists.')
        self.delete_instance(instance)

    def test_delete_instance_none(self):
        _, result = MySQL_Driver.delete_service_instance(None)
        self.assertEqual(result, 500, msg='Assert Delete Service ID None')

    def test_delete_instance_nonexistent(self):
        id = 126256598
        _, result = MySQL_Driver.delete_service_instance(id)
        self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')

# MANIFEST

    def setUp(self):
        ''' PREREQUISITES'''
        PlanAdapter.create_table()
        ServiceTypeAdapter.create_table()
        PlanServiceTypeAdapter.create_table()
        self.service = ServiceTypeAdapter.sample_model('manifest1')
        ServiceTypeAdapter.save(self.service)

        ManifestAdapter.create_table()
        self.test_model = ManifestAdapter.sample_model('manifest1')
        _, self.result = DriverSQL.add_manifest(self.test_model)

    def tearDown(self):
        DriverSQL.delete_manifest(self.test_model.id)
        ServiceTypeAdapter.delete(self.service.id)

    def test_manifest_create_table(self):
        self.assertTrue(ManifestSQL.table_exists())
        with self.assertRaises(orator.exceptions.query.QueryException):
            ManifestSQL.create_table()

    def test_sample_model_with_plans(self):
        self.assertIsInstance(self.test_model, Manifest)

        model_sql = ManifestAdapter.find_by_id_name(self.test_model.id)
        self.assertIsInstance(model_sql, ManifestSQL)

        ''' query associated service '''
        service = model_sql.service
        self.assertIsInstance(service, ServiceTypeSQL)

        ''' verify relations '''
        plans = service.plans
        plan = model_sql.plan
        self.assertTrue(plan in plans)

        ''' manifest also deleted '''
        PlanAdapter.delete(plan.id_name)
        self.assertFalse(ManifestAdapter.exists_in_db(model_sql.id_name))

        ''' service updated (has to be re-query-ed) '''
        ''' this is not correct! >> service = model_sql.service '''
        service = ServiceTypeAdapter.find_by_id_name(service.id_name)
        plans = service.plans
        ''' verify plans reduced '''
        self.assertEqual(len(plans), 1)
        ''' verify service has no manifest now '''
        self.assertTrue(service.manifests.is_empty())

    def test_adapter_delete(self):
        with self.assertRaises(Exception):
            ManifestAdapter.delete(id_name='')

    def test_adapter_save_to_update(self):
        self.test_model.name = 'new-name'
        model_sql = ManifestAdapter.save(self.test_model)
        exists = ManifestAdapter.exists_in_db(model_sql.id_name)
        self.assertTrue(exists)

    def test_get_manifest_with_id(self):
        manifests = DriverSQL.get_manifest(manifest_id=self.test_model.id)
        self.assertGreater(len(manifests), 0)
        self.assertIsInstance(manifests[0], Manifest)

    def test_get_manifest_with_manifest_id_and_plan_id(self):
        with self.assertRaises(Exception):
            DriverSQL.get_manifest(manifest_id=self.test_model.id, plan_id=self.test_model.plan_id)

    def test_get_manifest_with_manifest_id(self):
        result = DriverSQL.get_manifest(manifest_id=self.test_model.id, plan_id=None)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], Manifest)

    def test_get_manifest_with_plan_id(self):
        result = DriverSQL.get_manifest(manifest_id=None, plan_id=self.test_model.plan_id)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], Manifest)

    @patch.object(ManifestAdapter, 'exists_in_db')
    def test_get_manifest_with_id_and_not_found(self, mock_exists_in_db):
        mock_exists_in_db.return_value = False
        manifests = DriverSQL.get_manifest(self.test_model.id)
        self.assertEqual(manifests, [])

    def test_get_manifest_with_id_as_none(self):
        manifests = DriverSQL.get_manifest(manifest_id=None)
        self.assertNotEqual(manifests, [])

    def test_manifest_created(self):
        self.assertEqual(self.result, 200, msg='Assert Successful Add')
        exists = ManifestAdapter.exists_in_db(self.test_model.id)
        self.assertTrue(exists, msg='Assert manifest exists.')
        manifest_sql = ManifestAdapter.find_by_id_name(self.test_model.id)
        self.assertIsInstance(manifest_sql, ManifestSQL)

    def test_manifest_deletion(self):
        _, result = DriverSQL.delete_manifest(self.test_model.id)
        self.assertEqual(self.result, 200, msg='Assert Manifest Deleted')
        exists = ManifestAdapter.exists_in_db(self.test_model.id)
        self.assertFalse(exists, msg='Assert manifest does NOT Exist.')
        manifest_sql = ManifestAdapter.find_by_id_name(self.test_model.id)
        self.assertIsNone(manifest_sql)

    @patch.object(ManifestAdapter, 'exists_in_db')
    def test_add_manifest_existing(self, mock_exists):
        mock_exists.return_value = True
        _, result = DriverSQL.add_manifest(self.test_model)
        self.assertEqual(result, 409, msg='Assert Manifest Already Exists')

    def test_delete_manifest_nonexistent(self):
        _, result = DriverSQL.delete_manifest(self.test_model.id)
        _, result = DriverSQL.delete_manifest(self.test_model.id)
        self.assertEqual(result, 500, msg='Assert Delete Manifest Nonexistent')

    # TODO delete all implementation must be changed.
        # current: truncate/drop table
        # preferred: loop over entities and delete manually.

    # def test_delete_manifest_none(self):
    #     _, result = DriverSQL.delete_manifest(manifest_id=None)
    #     self.assertEqual(self.result, 200, msg='Assert Manifest Delete w/ \'None\'')
