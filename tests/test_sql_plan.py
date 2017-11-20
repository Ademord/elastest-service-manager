import unittest
from unittest import skipIf

from adapters.storage_sql import PlanSQL as Plan
from adapters.storage_sql import SamplePlan
from adapters.storage_sql import MySQL_Driver

import os


@skipIf(os.getenv('MYSQL_TESTS', 'NO') != 'YES', "MYSQL_TESTS_TESTS not set in environment variables")
class TestCasePlan(unittest.TestCase):

    def setUp(self):
        self.mysql_driver = MySQL_Driver()
        self.test_plan = SamplePlan()
        self.test_plan.create_table()

    def tearDown(self):
        # schema.drop_if_exists('services')
        del self.mysql_driver

    def add_plan(self, plan):
        plan.save()
        plans = Plan.where('name', '=', '{}'.format(plan.name)).get().serialize()
        self.assertEqual(len(plans), 1, msg='Assert plan exists.')

    def delete_plan(self, plan):
        plan.delete()
        plans = Plan.where('name', '=', '{}'.format(plan.name)).get().serialize()
        self.assertEqual(len(plans), 0, msg='Assert plan does NOT Exist.')

    def test_add_delete_plan(self):
        plan = SamplePlan()
        self.add_plan(plan)
        self.delete_plan(plan)
