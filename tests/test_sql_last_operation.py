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
#         self.mysql_driver = MySQL_Driver()
#         self.test_operation = SampleServiceLastOperation()
#         self.test_operation.create_table()
#         self.test_operation.setup()
#
#     def tearDown(self):
#         # schema.drop_if_exists('operations')
#         del self.mysql_driver
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
#         result = self.mysql_driver.get_last_operation(instance_id=operation.instance_id)
#         self.assertGreater(len(result), 0)
#         self.assertIsInstance(result[0], ServiceLastOperation)
#
#     @patch.object(ServiceLastOperation, 'find')
#     def test_get_operation_with_operation_id_none_found(self, mock_find):
#         operation = self.test_operation
#         operation.save()
#         mock_find.return_value = None
#         result = self.mysql_driver.get_last_operation(instance_id=operation.instance_id)
#         self.assertEqual(len(result), 0)
#
#     def test_get_operation_with_nothing(self):
#         operation = self.test_operation
#         operation.save()
#         result = self.mysql_driver.get_last_operation(instance_id=None)
#         self.assertGreater(len(result), 0)
#         self.assertIsInstance(result[0], ServiceLastOperation)
#
#     def add_operation(self, operation):
#         _, result = self.mysql_driver.add_last_operation(operation.instance_id, operation)
#         self.assertEqual(result, 200, msg='Assert Service Instance Successful Add')
#         operations = ServiceLastOperation.where('name', '=', '{}'.format(operation.name)).get().serialize()
#         self.assertEqual(len(operations), 1, msg='Assert Service Instance exists.')
#
#     def delete_operation(self, operation):
#         _, result = self.mysql_driver.delete_last_operation(operation.instance_id)
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
#         _, result = self.mysql_driver.add_last_operation(operation.instance_id, operation)
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
#         _, result = self.mysql_driver.delete_last_operation(None)
#         self.assertEqual(result, 500, msg='Assert Delete Service ID None')
#
#     def test_delete_operation_nonexistent(self):
#         id = 126256598
#         _, result = self.mysql_driver.delete_last_operation(id)
#         self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')
