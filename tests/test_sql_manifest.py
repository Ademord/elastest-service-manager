# import unittest
# from unittest.mock import patch
# from unittest import skipIf
#
# from adapters.storage_sql import ServiceManifestSQL as ServiceManifest
# from adapters.storage_sql import SampleServiceManifest
# from adapters.storage_sql import MySQL_Driver
#
# import os
#
#
# @skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
# class TestCaseServiceManifest(unittest.TestCase):
#
#     def setUp(self):
#         self.mysql_driver = MySQL_Driver()
#         self.test_manifest = SampleServiceManifest()
#         self.test_manifest.create_table()
#         self.test_manifest.setup()
#
#     def tearDown(self):
#         # schema.drop_if_exists('manifests')
#         del self.mysql_driver
#         self.test_manifest.delete_cascade()
#
#     def test_get_manifest_with_manifest_id_and_plan_id(self):
#         manifest = self.test_manifest
#         with self.assertRaises(Exception):
#             self.mysql_driver.get_manifest(manifest_id=manifest.id, plan_id=manifest.plan_id)
#
#     def test_get_manifest_with_manifest_id(self):
#         manifest = self.test_manifest
#         manifest.save()
#         result = self.mysql_driver.get_manifest(manifest_id=manifest.id, plan_id=None)
#         self.assertGreater(len(result), 0)
#         self.assertIsInstance(result[0], ServiceManifest)
#
#     def test_get_manifest_with_plan_id(self):
#         manifest = self.test_manifest
#         manifest.save()
#         result = self.mysql_driver.get_manifest(manifest_id=None, plan_id=manifest.plan_id)
#         self.assertGreater(len(result), 0)
#         self.assertIsInstance(result[0], ServiceManifest)
#
#     @patch.object(ServiceManifest, 'find')
#     def test_get_manifest_with_plan_id_none_found(self, mock_find):
#         manifest = self.test_manifest
#         manifest.save()
#         mock_find.return_value = None
#         result = self.mysql_driver.get_manifest(manifest_id=None, plan_id=manifest.plan_id)
#         self.assertEqual(len(result), 0)
#
#     def test_get_manifest_with_nothing(self):
#         manifest = self.test_manifest
#         manifest.save()
#         result = self.mysql_driver.get_manifest(manifest_id=None, plan_id=None)
#         self.assertGreater(len(result), 0)
#         self.assertIsInstance(result[0], ServiceManifest)
#
#     def add_manifest(self, manifest):
#         _, result = self.mysql_driver.add_manifest(manifest)
#         self.assertEqual(result, 200, msg='Assert Successful Add')
#         manifests = ServiceManifest.where('name', '=', '{}'.format(manifest.name)).get().serialize()
#         self.assertEqual(len(manifests), 1, msg='Assert manifest exists.')
#
#     def delete_manifest(self, manifest):
#         _, result = self.mysql_driver.delete_manifest(self.get_id_by_name(manifest.name))
#         self.assertEqual(result, 200, msg='Assert Service Deleted' + ' ' + _)
#         manifests = ServiceManifest.where('name', '=', '{}'.format(manifest.name)).get().serialize()
#         self.assertEqual(len(manifests), 0, msg='Assert manifest does NOT Exist.')
#
#     def get_id_by_name(self, name):
#         service = ServiceManifest.where('name', '=', '{}'.format(name)).get().first()
#         self.assertIsNotNone(service, msg='Assert get ID by Name')
#         return service.id
#
#     def test_add_delete_manifest(self):
#         manifest = self.test_manifest
#         self.add_manifest(manifest)
#         self.delete_manifest(manifest)
#
#     @patch.object(ServiceManifest, 'get_id')
#     def test_add_manifest_unsucessful(self, mock_id):
#         manifest = self.test_manifest
#         mock_id.return_value = None
#         _, result = self.mysql_driver.add_manifest(manifest)
#         self.assertEqual(result, 500, msg='Assert Can NOT Add')
#         self.delete_manifest(manifest)
#
#     @patch.object(ServiceManifest, 'exists')
#     def test_add_manifest_existing(self, mock_exists):
#         manifest = self.test_manifest
#         mock_exists.return_value = True
#         _, result = self.mysql_driver.add_manifest(manifest)
#         self.assertEqual(result, 409, msg='Assert Service Already Exists')
#
#     def test_delete_manifest_none(self):
#         _, result = self.mysql_driver.delete_manifest(None)
#         self.assertEqual(result, 500, msg='Assert Delete Service ID None')
#
#     def test_delete_manifest_nonexistent(self):
#         id = 126256598
#         _, result = self.mysql_driver.delete_manifest(id)
#         self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')
