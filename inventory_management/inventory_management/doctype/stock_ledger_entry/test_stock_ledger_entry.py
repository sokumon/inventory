# Copyright (c) 2024, Soham Kulkarni and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase
from inventory_management.tests.utils import create_item, create_stock_entry
import frappe
# On IntegrationTestCase, the doctype test records and all
# link-field test record depdendencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class TestStockLedgerEntry(UnitTestCase):
	"""
	Unit tests for StockLedgerEntry.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestStockLedgerEntry(IntegrationTestCase):
	"""
	Integration tests for StockLedgerEntry.
	Use this class for testing interactions between multiple components.
	"""
	def setUp(self):
		create_stock_entry()

	def test_check_stock_ledger(self):
		result = frappe.db.sql("SELECT `name` FROM `tabStock Ledger Entry` where `item` = 'TEST-001';", as_dict = 1)
		result_num = len(result)
		self.assertEqual(result_num,2)
