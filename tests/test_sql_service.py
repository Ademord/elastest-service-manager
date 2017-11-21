# import unittest
# from unittest.mock import patch
# from unittest import skipIf
#
# import os
#
# from adapters.storage_sql import ServiceSQL as Service
# from adapters.storage_sql import SampleService
# from adapters.storage_sql import MySQL_Driver
#
#
# @skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
# class TestCaseServiceType(unittest.TestCase):
#     def setUp(self):
#         self.mysql_driver = MySQL_Driver()
#         self.test_service = SampleService()
#         self.test_service.create_table()
#
#     def tearDown(self):
#         # schema.drop_if_exists('services')
#         del self.mysql_driver
#
#     def test_get_service_with_id(self):
#         service = self.test_service
#         service.save()
#         result = self.mysql_driver.get_service(service_id=service.id)
#         self.assertGreater(len(result), 0)
#         self.assertIsInstance(result[0], Service)
#         service.delete()
#
#     @patch('adapters.storage_sql.ServiceSQL.find')
#     def test_get_service_with_id_and_not_found(self, mock_method):
#         mock_method.return_value = []
#         self.assertEqual(
#             self.mysql_driver.get_service(service_id='1'), []
#         )
#
#     @patch('adapters.storage_sql.ServiceSQL.all')
#     def test_get_service_with_id_as_none(self, mock_method):
#         mock_method.return_value = ['sevice1', 'service2']
#         self.assertNotEqual(
#             self.mysql_driver.get_service(service_id=None), []
#         )
#
#     def add_service(self, service):
#         _, result = self.mysql_driver.add_service(service)
#         self.assertEqual(result, 200, msg='Assert Successful Add')
#         services = Service.where('name', '=', '{}'.format(service.name)).get().serialize()
#         self.assertEqual(len(services), 1, msg='Assert service exists.')
#
#     def delete_service(self, service):
#         _, result = self.mysql_driver.delete_service(self.get_id_by_name(service.name))
#         self.assertEqual(result, 200, msg='Assert Service Deleted')
#         services = Service.where('name', '=', '{}'.format(service.name)).get().serialize()
#         self.assertEqual(len(services), 0, msg='Assert service does NOT Exist.')
#
#     def get_id_by_name(self, name):
#         service = Service.where('name', '=', '{}'.format(name)).get().first()
#         self.assertIsNotNone(service, msg='Assert get ID by Name')
#         return service.id
#
#     def test_add_delete_service(self):
#         service = self.test_service
#         self.add_service(service)
#         self.delete_service(service)
#
#     @patch.object(Service, 'get_id')
#     def test_add_service_unsucessful(self, mock_id):
#         service = self.test_service
#         mock_id.return_value = None
#         _, result = self.mysql_driver.add_service(service)
#         self.assertEqual(result, 500, msg='Assert Can NOT Add')
#         self.delete_service(service)
#
#     @patch.object(Service, 'exists')
#     def test_add_service_existing(self, mock_exists):
#         service = self.test_service
#         mock_exists.return_value = True
#         _, result = self.mysql_driver.add_service(service)
#         self.assertEqual(result, 409, msg='Assert Service Already Exists')
#
#     def test_delete_service_none(self):
#         _, result = self.mysql_driver.delete_service(None)
#         self.assertEqual(result, 500, msg='Assert Delete Service ID None')
#
#     def test_delete_service_nonexistent(self):
#         id = 126256598
#         _, result = self.mysql_driver.delete_service(id)
#         self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')
#
#     # def test_storage_class(self):
#     #     from storage import Storage
#     #     storage = Storage()
#     #     storage.add_service()
#     #     self.assertRaises()