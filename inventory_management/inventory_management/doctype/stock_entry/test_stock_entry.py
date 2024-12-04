# Copyright (c) 2024, Soham Kulkarni and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase
import frappe
from inventory_management.tests.utils import create_item,create_stock_entry

# On IntegrationTestCase, the doctype test records and all
# link-field test record depdendencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestStockEntry(UnitTestCase):
    """
    Unit tests for StockEntry.
    Use this class for testing individual functions and methods.
    """
    def test_hello(self):
        print("Hello")




class TestStockEntry(IntegrationTestCase):
    """
    Integration tests for StockEntry.
    Use this class for testing interactions between multiple components.
    """
    def setUp(self):
        create_stock_entry()

 

    def test_check_item(self):
        create_item()
        self.assertTrue(frappe.db.exists("ITEM", "TEST-001"))

    def test_check_stock_entry(self):
        result = frappe.db.sql("SELECT `parent` FROM `tabStock Entry Item` where item = 'TEST-001';", as_dict = 1)
        self.assertTrue(frappe.db.exists("Stock Entry",result[0]['parent']))


