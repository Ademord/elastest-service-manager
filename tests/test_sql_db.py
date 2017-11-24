# GENERICS
from adapters.sql_datasource import DriverSQL
from unittest.mock import patch
import orator
# TESTS
from unittest import skipIf
import unittest
import os


DriverSQL.set_up()


# @skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
class TestCaseManifestManifest(unittest.TestCase):

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