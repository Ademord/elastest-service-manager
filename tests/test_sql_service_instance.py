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
        self.mysql_driver = MySQL_Driver()
        self.test_instance = SampleServiceInstance()
        self.test_instance.create_table()
        self.test_instance.setup()

    def tearDown(self):
        # schema.drop_if_exists('instances')
        del self.mysql_driver
        self.test_instance.delete_cascade()

    def test_get_instance_with_instance_id(self):
        instance = self.test_instance
        instance.save()
        result = self.mysql_driver.get_service_instance(instance_id=instance.id)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceInstance)

    @patch.object(ServiceInstance, 'find')
    def test_get_instance_with_instance_id_none_found(self, mock_find):
        instance = self.test_instance
        instance.save()
        mock_find.return_value = None
        result = self.mysql_driver.get_service_instance(instance_id=instance.id)
        self.assertEqual(len(result), 0)

    def test_get_instance_with_nothing(self):
        instance = self.test_instance
        instance.save()
        result = self.mysql_driver.get_service_instance(instance_id=None)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceInstance)

    def add_instance(self, instance):
        _, result = self.mysql_driver.add_service_instance(instance)
        self.assertEqual(result, 200, msg='Assert Service Instance Successful Add')
        instances = ServiceInstance.where('name', '=', '{}'.format(instance.name)).get().serialize()
        self.assertEqual(len(instances), 1, msg='Assert Service Instance exists.')

    def delete_instance(self, instance):
        _, result = self.mysql_driver.delete_service_instance(self.get_id_by_name(instance.name))
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
        _, result = self.mysql_driver.add_service_instance(instance)
        self.assertEqual(result, 500, msg='Assert Can NOT Add Service Instance')
        self.delete_instance(instance)

    def test_add_instance_existing(self):
        instance = self.test_instance
        self.add_instance(instance)
        _, result = self.mysql_driver.add_service_instance(instance)
        self.assertEqual(result, 201, msg='Assert Service Instance Already Exists')
        instances = ServiceInstance.where('name', '=', '{}'.format(instance.name)).get().serialize()
        self.assertEqual(len(instances), 1, msg='Assert Service Instance exists.')
        self.delete_instance(instance)

    def test_delete_instance_none(self):
        _, result = self.mysql_driver.delete_service_instance(None)
        self.assertEqual(result, 500, msg='Assert Delete Service ID None')

    def test_delete_instance_nonexistent(self):
        id = 126256598
        _, result = self.mysql_driver.delete_service_instance(id)
        self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')
