# Copyright (c) 2024, Soham Kulkarni and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from pypika import functions as fn
from frappe import _

class StockEntry(Document):
	def validate(self):
		if self.entry_type == "Recieve":
			self.validate_recieve()
		if self.entry_type == "Consume":
			self.validate_consume()
		if self.entry_type == "Transfer":
			self.validate_transfer()
	
	def validate_recieve(self):
		for i in self.items:
			if not i.target_warehouse:
				frappe.throw("Src Warehouse not set")

	def validate_consume(self):
		for i in self.items:
			if not i.source_warehouse:
				frappe.throw("Target Warehouse not set")
			target_warehouse = i.source_warehouse
			self.check_quantity(entry_item = i, warehouse= target_warehouse)

	def validate_transfer(self):
		for i in self.items:
			if not i.source_warehouse:
				frappe.throw("Src Warehouse not set")
			if not i.target_warehouse:
				frappe.throw("Src Warehouse not set")
			warehouse = i.target_warehouse
			self.check_quantity(entry_item = i, warehouse= warehouse)

	def check_quantity(self, entry_item, warehouse):
		qty = frappe.db.get_values("Stock Ledger Entry", {
            "item": entry_item.item,
            "warehouse": warehouse
        }, ["qty_changed"])
		total_qty = sum([q[0] for q in qty])
		print("total", total_qty)
		if total_qty < entry_item.qty:
			frappe.throw(
					_(f"Quantity exceeds number of units available for {entry_item.item} in the inventory.")
			)

	def on_submit(self):
		print("Adding to ledger")
		if self.entry_type == "Transfer":
			for i  in self.items:
				self.make_transfer_entries(i)
		else:
			for i in self.items:
				if self.entry_type == "Consume":
					warehouse, entry_type, qty_changed = (i.source_warehouse, self.entry_type,-(i.qty))
				else:
					warehouse, entry_type, qty_changed = (i.target_warehouse, self.entry_type, i.qty)
				self.add_to_ledger(i,warehouse= warehouse,entry_type= entry_type ,qty_changed= qty_changed)

	def on_cancel(self):
		print("Cancelling the entry")
		if self.entry_type == "Transfer":
			for i in self.items:
				self.make_rev_transfer_entries(i)
		else:
			for i in self.items:
				if self.entry_type == "Consume":
					warehouse, entry_type, qty_changed = (i.source_warehouse, self.entry_type,i.qty)
				else:
					warehouse, entry_type, qty_changed = (i.target_warehouse, self.entry_type, -(i.qty))
				self.add_to_ledger(i,warehouse= warehouse,entry_type= entry_type ,qty_changed= qty_changed)


	def add_to_ledger(self,entry_item, warehouse ,entry_type, qty_changed):
			sle = frappe.new_doc("Stock Ledger Entry")
			sle.posting_date = self.entry_date,
			sle.posting_time = self.entry_time,
			sle.voucher = self
			sle.item = entry_item.item
			sle.warehouse =  warehouse
			sle.qty_changed = qty_changed
			sle.in_out_rate = entry_item.unit_cost
			if entry_type == "Receive":
				sle.quantity_in = entry_item.qty
				sle.valuation_rate = self.calculate_moving_average(entry_item= entry_item, warehouse= warehouse, type= entry_type)
			if entry_type == "Consume":
				sle.quantity_out = entry_item.qty
				sle.valuation_rate = self.calculate_moving_average(entry_item= entry_item, warehouse= warehouse, type= entry_type)
    

			sle.insert()
			return sle

	def make_transfer_entries(self,entry_item):
		entry_type ="Consume"
		warehouse = entry_item.source_warehouse
		qty_changed =  -(entry_item.qty)
		sle = self.add_to_ledger(entry_item,warehouse= warehouse,entry_type = entry_type,qty_changed= qty_changed)
		entry_item.unit_cost = sle.unit_cost
		entry_type = "Receive"
		warehouse = entry_item.target_warehouse
		qty_changed =  (entry_item.qty)
		self.add_to_ledger(entry_item,warehouse= warehouse,entry_type = entry_type,qty_changed= qty_changed)


	def make_rev_transfer_entries(self,entry_item):
		entry_type ="Consume"
		warehouse = entry_item.target_warehouse
		qty_changed =  -(entry_item.qty)
		sle = self.add_to_ledger(entry_item,warehouse= warehouse,entry_type = entry_type,qty_changed= qty_changed)
		entry_item.unit_cost = sle.unit_cost
		entry_type = "Receive"
		warehouse = entry_item.target_warehouse
		qty_changed =  (entry_item.qty)
		self.add_to_ledger(entry_item,warehouse= warehouse,entry_type = entry_type,qty_changed= qty_changed)

		
	def calculate_moving_average(self,entry_item,warehouse,type):
		sle =  frappe.qb.DocType("Stock Ledger Entry")
		query = (frappe.qb.from_(sle)
            .select(
                fn.Sum(sle.qty_changed * sle.in_out_rate).as_("sum of product of qty and cost"),
                fn.Sum(sle.qty_changed).as_("sum of qty")
            )
            .where(sle.item == entry_item.item)
            .where(sle.warehouse == warehouse)
		)
		results = query.run(as_dict=True)
		if results[0].get("sum of product of qty and cost"):
			numerator = results[0].get("sum of product of qty and cost") 
			denominator = results[0]["sum of qty"]
			if type != "Consume":
				numerator = numerator + (entry_item.unit_cost * entry_item.qty)
				denominator = denominator + entry_item.qty
		else:
			numerator = (entry_item.unit_cost * entry_item.qty)
			denominator =  entry_item.qty
		
		if numerator != None and denominator != None:
			try:
				moving_avg = numerator/denominator
				return moving_avg
			except:
				return 0

			

