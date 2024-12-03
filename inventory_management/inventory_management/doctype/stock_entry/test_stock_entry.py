# Copyright (c) 2024, Soham Kulkarni and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase
import frappe

# On IntegrationTestCase, the doctype test records and all
# link-field test record depdendencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class TestStockEntry(UnitTestCase):
	"""
	Unit tests for StockEntry.
	Use this class for testing individual functions and methods.
	"""
	def setUp(self):
		create_stock_entry()
		self.assertTrue(frappe.db.exists("Stock Entry", "SE-1111"))

def create_item():
	if not frappe.db.exists("Item", "TEST-001"):
		test_item = frappe.get_doc("Item",{
				"item_name":"Item 1",
				"item_code":"TEST-001",
				"opening_quantity":10,
				"opening_unit_cost":10
		})
		test_item.insert()

def create_stock_entry():
	create_item()
	item = frappe.get_doc("Item", "TEST-001")
	if not frappe.db.exists("Stock Entry", "SE-1111"):
		test_stock_entry = frappe.get_doc("Stock Entry",{
				"name":"Stock Entry",
				"entry_type": "Consume",
				"entry_date": frappe.utils.today(),
				"entry_time": frappe.utils.now(),
				"items":{
					"item": item,
					"source_warehouse": item.default_warehouse,
					"qty":10,
					"unit_cost":1
				}
		})
		test_stock_entry.insert()
		test_stock_entry.submit()


class TestStockEntry(IntegrationTestCase):
	"""
	Integration tests for StockEntry.
	Use this class for testing interactions between multiple components.
	"""

	pass
