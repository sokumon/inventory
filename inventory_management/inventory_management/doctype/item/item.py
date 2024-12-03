# Copyright (c) 2024, Soham Kulkarni and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe import _
import frappe
class Item(Document):
	def validate(self):
		if self.opening_stock_quantity:
			self.validate_cost()
			self.validate_warehouse()
	
	def validate_cost(self):
		if self.opening_stock_unit_cost is None:
			frappe.throw(_("Unit Cost is not set"))

	def validate_warehouse(self):
		if self.opening_warehouse is None:
			frappe.throw(_("Opening Warehouse is not set "))

	def before_save(self):
		print("Adding a item")
		self.opening_stock_balance = self.opening_stock_quantity * self.opening_stock_unit_cost
	
	def after_insert(self):
		self.create_stock_entry()
	
	def create_stock_entry(self):
		print('Adding to stock entry')
		se = frappe.new_doc("Stock Entry")
		se = frappe.get_doc({
			"doctype": "Stock Entry",
			"entry_type": "Receive",
			"entry_date": frappe.utils.today(),
			"entry_time": frappe.utils.now(),
			"valuation_method": "Moving Average",
			"items":[		frappe._dict(
					item = self.item_code,
					qty =  self.opening_stock_quantity,
					unit_cost=  self.opening_stock_unit_cost,
					target_warehouse = self.opening_warehouse,
		)] }
		)
		se.insert()
		se.submit()
		
