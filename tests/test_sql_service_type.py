from esm.models.service_type import ServiceType

from adapters.sql_datasource import ServiceTypeSQL
from adapters.sql_datasource import PlanServiceTypeSQL
from adapters.sql_datasource import ServiceTypeAdapter
from adapters.sql_datasource import PlanServiceTypeAdapter
from adapters.sql_datasource import PlanAdapter
from adapters.sql_datasource import DriverSQL

from unittest.mock import patch
from unittest import skipIf
import unittest
import os
import orator

# @skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
class TestCaseServiceType(unittest.TestCase):
    def setUp(self):
        self.test_model = ServiceTypeAdapter.sample_model('service1')
        ServiceTypeAdapter.create_table()
        PlanAdapter.create_table()
        PlanServiceTypeAdapter.create_table()
        _, self.result = DriverSQL.add_service(self.test_model)

    def tearDown(self):
        DriverSQL.delete_service(self.test_model.id)

    def test_plan_service_type_create_table(self):
        self.assertTrue(PlanServiceTypeSQL.table_exists())
        with self.assertRaises(orator.exceptions.query.QueryException):
            PlanServiceTypeSQL.create_table()

    def test_service_type_create_table(self):
        self.assertTrue(ServiceTypeSQL.table_exists())
        with self.assertRaises(orator.exceptions.query.QueryException):
            ServiceTypeSQL.create_table()

    def test_sample_model_with_plans(self):
        self.assertIsInstance(self.test_model, ServiceType)

        model_sql = ServiceTypeAdapter.find_by_id_name(self.test_model.id)
        self.assertIsInstance(model_sql, ServiceTypeSQL)
        self.assertFalse(model_sql.plans.is_empty())

        plans = PlanAdapter.plans_from_service_sql(model_sql)
        self.assertGreater(len(plans), 1)

        model = ServiceTypeAdapter.model_sql_to_model(model_sql)
        self.assertGreater(len(model.plans), 1)

    def test_adapter_delete(self):
        with self.assertRaises(Exception):
            ServiceTypeAdapter.delete(id_name='')

    def test_adapter_save_to_update(self):
        self.test_model.name = 'new-name'
        model_sql = ServiceTypeAdapter.save(self.test_model)
        exists = ServiceTypeAdapter.exists_in_db(model_sql.id_name)
        self.assertTrue(exists)

    def test_get_service_with_id(self):
        services = DriverSQL.get_service(service_id=self.test_model.id)
        self.assertGreater(len(services), 0)
        self.assertIsInstance(services[0], ServiceType)

    @patch.object(ServiceTypeAdapter, 'exists_in_db')
    def test_get_service_with_id_and_not_found(self, mock_exists_in_db):
        mock_exists_in_db.return_value = False
        services = DriverSQL.get_service(self.test_model.id)
        self.assertEqual(services, [])

    def test_get_service_with_id_as_none(self):
        services = DriverSQL.get_service(service_id=None)
        self.assertNotEqual(services, [])

    def test_service_created(self):
        self.assertEqual(self.result, 200, msg='Assert Successful Add')
        exists = ServiceTypeAdapter.exists_in_db(self.test_model.id)
        self.assertTrue(exists, msg='Assert service service exists.')
        service_sql = ServiceTypeAdapter.find_by_id_name(self.test_model.id)
        self.assertIsInstance(service_sql, ServiceTypeSQL)

    def test_service_deletion(self):
        _, result = DriverSQL.delete_service(self.test_model.id)
        self.assertEqual(self.result, 200, msg='Assert Service Deleted')
        exists = ServiceTypeAdapter.exists_in_db(self.test_model.id)
        self.assertFalse(exists, msg='Assert service does NOT Exist.')
        service_sql = ServiceTypeAdapter.find_by_id_name(self.test_model.id)
        self.assertIsNone(service_sql)

    @patch.object(ServiceTypeAdapter, 'exists_in_db')
    def test_add_service_existing(self, mock_exists):
        mock_exists.return_value = True
        _, result = DriverSQL.add_service(self.test_model)
        self.assertEqual(result, 409, msg='Assert Service Already Exists')

    def test_delete_service_nonexistent(self):
        _, result = DriverSQL.delete_service(self.test_model.id)
        _, result = DriverSQL.delete_service(self.test_model.id)
        self.assertEqual(result, 500, msg='Assert Delete Service Nonexistent')

    def test_delete_all(self):
        _, result = DriverSQL.delete_service(service_id=None)
        self.assertEqual(self.result, 200, msg='Assert Service Delete w/ \'None\'')


# import unittest
# from unittest.mock import patch
# from unittest import skipIf
#
# from adapters.storage_sql import ServiceLastOperationSQL as ServiceLastOperation
# from adapters.storage_sql import SampleServiceLastOperation
# from adapters.storage_sql import MySQL_Driver
#
# import os
#
# # TODO implement exception in every part of the tree when deleting something nested
# # (deleting a plan when there is an instance running)
# # TODO update delete_instance method based off plan_id... * multiple *
# @skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
# class TestCaseLastOperation(unittest.TestCase):
#     def setUp(self):
#         MySQL_Driver = MySQL_Driver()
#         self.test_operation = SampleServiceLastOperation()
#         self.test_operation.create_table()
#         self.test_operation.setup()
#
#     def tearDown(self):
#         # schema.drop_if_exists('operations')
#         del MySQL_Driver
#         self.test_operation.delete_cascade()
#
#     def test_consistent_creation(self):
#         # operation parent instance
#         print('\t', '********************************************************************')
#         print('\t', 'Saving operation...', self.test_operation.id)
#         self.test_operation.save()
#         print()
#         print('\t', '********************************************************************')
#         print('\t', 'Last Operation: Parent Instance')
#         instance = self.test_operation.instance
#         print('\t', '\t', instance)
#         print('\t', '\t', instance.id, ': ', instance.name)
#
#         # instance > operations
#         print('\t', '********************************************************************')
#         print('\t', 'Instance: Existing Operations')
#         # TODO fix this
#         operations = instance.operations
#         print('\t', '\t', operations)
#         print('\t', '\t', operations.is_empty(), ': ', operations.all())
#
#         # instance parent manifest
#         print('\t', '********************************************************************')
#         print('\t', 'Instance: Parent Manifest')
#         manifest = instance.manifest
#         print('\t', '\t', manifest)
#         print('\t', '\t', manifest.id, ': ', manifest.name)
#
#         # manifest > instances
#         print('\t', '********************************************************************')
#         print('\t', 'Manifest: Existing Instances')
#         instances = manifest.instances
#         print('\t', '\t', instances)
#         print('\t', '\t', instances.is_empty(), ': ', instances.all())
#
#         # manifest parent plan | INVERSE UNSUPPORTED
#         print('\t', '********************************************************************')
#         print('\t', 'Manifest: Parent Plan')
#         plan = manifest.plan
#         print('\t', '\t', plan)
#         print('\t', '\t', plan.id, ': ', plan.name)
#
#         # manifest parent service | INVERSE UNSUPPORTED
#         print('\t', '********************************************************************')
#         print('\t', 'Manifest: Parent Service')
#         service = manifest.service
#         print('\t', '\t', service)
#         print('\t', '\t', service.id, ': ', service.name)
#
#         # plan > manifests
#         print('\t', '********************************************************************')
#         print('\t', 'Plan: Existing Manifests')
#         manifests = plan.manifests
#         print('\t', '\t', manifests)
#         print('\t', '\t', manifests.is_empty(), ': ', manifests.all())
#
#         print('\t', '********************************************************************')
#         print()
#         # TODO test each model with classic object received
#
#
#     def test_get_operation_with_operation_id(self):
#         operation = self.test_operation
#         operation.save()
#         result = MySQL_Driver.get_last_operation(instance_id=operation.instance_id)
#         self.assertGreater(len(result), 0)
#         self.assertIsInstance(result[0], ServiceLastOperation)
#
#     @patch.object(ServiceLastOperation, 'find')
#     def test_get_operation_with_operation_id_none_found(self, mock_find):
#         operation = self.test_operation
#         operation.save()
#         mock_find.return_value = None
#         result = MySQL_Driver.get_last_operation(instance_id=operation.instance_id)
#         self.assertEqual(len(result), 0)
#
#     def test_get_operation_with_nothing(self):
#         operation = self.test_operation
#         operation.save()
#         result = MySQL_Driver.get_last_operation(instance_id=None)
#         self.assertGreater(len(result), 0)
#         self.assertIsInstance(result[0], ServiceLastOperation)
#
#     def add_operation(self, operation):
#         _, result = MySQL_Driver.add_last_operation(operation.instance_id, operation)
#         self.assertEqual(result, 200, msg='Assert Service Instance Successful Add')
#         operations = ServiceLastOperation.where('name', '=', '{}'.format(operation.name)).get().serialize()
#         self.assertEqual(len(operations), 1, msg='Assert Service Instance exists.')
#
#     def delete_operation(self, operation):
#         _, result = MySQL_Driver.delete_last_operation(operation.instance_id)
#         self.assertEqual(result, 200, msg='Assert Service Instance Deleted' + ' ' + _)
#         operation_result = operation.find(self.get_id_by_name(operation.name))
#         self.assertIsNone(operation_result, msg='Assert Service Instance does NOT Exist.')
#
#     def get_id_by_name(self, name):
#         operations = ServiceLastOperation.where('name', '=', '{}'.format(name)).get().serialize()
#         if operations: return operations[0]['id']
#         else: return None
#
#     def test_add_delete_operation(self):
#         operation = self.test_operation
#         self.add_operation(operation)
#         self.delete_operation(operation)
#
#     @patch.object(ServiceLastOperation, 'get_id')
#     def test_add_operation_unsucessful(self, mock_id):
#         operation = self.test_operation
#         mock_id.return_value = None
#         _, result = MySQL_Driver.add_last_operation(operation.instance_id, operation)
#         self.assertEqual(result, 500, msg='Assert Can NOT Add Service Instance')
#         # it saves but the mock disrupts the call, so must delete
#         self.delete_operation(operation)
#
#     def test_add_two_operation(self):
#         import copy
#         operation = copy.deepcopy(self.test_operation)
#         operation2 = copy.deepcopy(self.test_operation)
#         operation2.name = operation2.name + 'v2'
#         self.add_operation(operation)
#         self.add_operation(operation2)
#         self.delete_operation(operation)
#         self.delete_operation(operation2)
#
#     def test_delete_operation_none(self):
#         _, result = MySQL_Driver.delete_last_operation(None)
#         self.assertEqual(result, 500, msg='Assert Delete Service ID None')
#
#     def test_delete_operation_nonexistent(self):
#         id = 126256598
#         _, result = MySQL_Driver.delete_last_operation(id)
#         self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')
