import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock
from database_manager import schema
import pymysql
from storage_sql import ServiceManifest
from storage_sql import MySQL_Driver
import orator


class MySQLDriver_ServiceTest(unittest.TestCase):
    def create_service_manifest_table(self):
        with schema.create('service_manifests') as table:
            table.increments('id')
            table.foreign('service_id').references('id').on('service_types')
            table.foreign('plan_id').references('id').on('plans')
            table.string('name').unique()
            table.string('manifest_content')
            table.datetime('created_at')
            table.datetime('updated_at')
            # print('Created Table Services')

            # with schema.create('plans') as table:
            #     table.increments('id')
            #     table.string('name').unique()

    def setUp(self):
        try:
            self.create_service_manifest_table()
        except:
            pass
            # print('Could not create the table Services')
        self.mysql_driver = MySQL_Driver()
        self.test_manifest = ServiceManifest()
        self.test_manifest.id = 1
        self.test_manifest.name = 'service1-manifest'
        self.test_manifest.plan_id = 1
        self.test_manifest.manifest_content = 'hello'

    def tearDown(self):
        # schema.drop_if_exists('manifests')
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

    def test_get_manifest_with_manifest_id_and_plan_id(self):
        manifest = self.test_manifest
        with self.assertRaises(Exception):
            self.mysql_driver.get_manifest(manifest_id=manifest.id, plan_id=manifest.plan_id)

    def test_get_manifest_with_manifest_id(self):
        manifest = self.test_manifest
        manifest.save()
        result = self.mysql_driver.get_manifest(manifest_id=manifest.id, plan_id=None)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceManifest)
        manifest.delete()

    def test_get_manifest_with_plan_id(self):
        # TODO change service to this format, no mocks
        manifest = self.test_manifest
        manifest.save()
        result = self.mysql_driver.get_manifest(manifest_id=None, plan_id=manifest.plan_id)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceManifest)
        manifest.delete()

    @patch.object(ServiceManifest, 'find')
    def test_get_manifest_with_plan_id_none_found(self, mock_find):
        manifest = self.test_manifest
        manifest.save()
        mock_find.return_value = None
        result = self.mysql_driver.get_manifest(manifest_id=None, plan_id=manifest.plan_id)
        self.assertEqual(len(result), 0)
        manifest.delete()


    def test_get_manifest_with_nothing(self):
        manifest = self.test_manifest
        manifest.save()
        result = self.mysql_driver.get_manifest(manifest_id=None, plan_id=None)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], ServiceManifest)
        manifest.delete()

    def add_manifest(self, name):
        manifest = self.test_manifest
        _, result = self.mysql_driver.add_manifest(manifest)
        self.assertEqual(result, 200, msg='Assert Successful Add')
        manifests = ServiceManifest.where('name', 'like', '%{}%'.format(manifest.name)).get().serialize()
        self.assertEqual(len(manifests), 1, msg='Assert manifest exists.')

    def delete_manifest(self, name):
        id = self.get_id_by_name(name)
        self.assertIsNotNone(id)
        _, result = self.mysql_driver.delete_manifest(id)
        self.assertEqual(result, 200, msg='Assert Service Deleted' + ' ' + _)
        manifests = ServiceManifest.where('name', 'like', '%{}%'.format(name)).get().serialize()
        self.assertEqual(len(manifests), 0, msg='Assert manifest does NOT Exist.')

    def get_id_by_name(self, name):
        manifest = self.test_manifest
        manifests = ServiceManifest.where('name', 'like', '%{}%'.format(manifest.name)).get().serialize()
        if manifests: return manifests[0]['id']
        else: return None

    def test_add_delete_manifest(self):
        name = 'manifest1'
        self.add_manifest(name)
        self.delete_manifest(name)
    #
    @patch.object(ServiceManifest, 'get_id')
    def test_add_manifest_unsucessful(self, mock_id):
        manifest = self.test_manifest
        mock_id.return_value = None
        _, result = self.mysql_driver.add_manifest(manifest)
        self.assertEqual(result, 500, msg='Assert Can NOT Add')
        # it saves but the mock disrupts the call, so must delete
        self.delete_manifest(manifest.name)
    #
    @patch.object(ServiceManifest, 'exists')
    def test_add_manifest_existing(self, mock_exists):
        manifest = self.test_manifest
        mock_exists.return_value = True
        _, result = self.mysql_driver.add_manifest(manifest)
        self.assertEqual(result, 409, msg='Assert Service Already Exists')

    def test_delete_manifest_none(self):
        _, result = self.mysql_driver.delete_manifest(None)
        self.assertEqual(result, 500, msg='Assert Delete Service ID None')

    def test_delete_manifest_nonexistent(self):
        id = 126256598
        _, result = self.mysql_driver.delete_manifest(id)
        self.assertEqual(result, 500, msg='Assert Delete Service ID Nonexistent')
