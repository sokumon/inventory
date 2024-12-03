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


class TestItem(UnitTestCase):
	"""
	Unit tests for Item.
	Use this class for testing individual functions and methods.
	"""
	def setUp(self):
		create_item()
		self.assertTrue(frappe.db.exists("Item", "ITEM-001"))

def create_item():
	if not frappe.db.exists("Item", "ITEM-001"):
		test_item = frappe.get_doc("Item",{
				"item_name":"Item 1",
				"item_code":"TEST-001",
				"opening_quantity":10,
				"opening_unit_cost":10
		})
		test_item.insert()

class TestItem(IntegrationTestCase):
	"""
	Integration tests for Item.
	Use this class for testing interactions between multiple components.
	"""
	def setUp(self):
		create_items()
		self.assertTrue(frappe.db.exists("Stock Entry", {"entry_type": "Receive", "items":[{"item": "TEST-001"}]}))
	
