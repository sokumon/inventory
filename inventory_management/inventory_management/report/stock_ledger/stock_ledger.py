# Copyright (c) 2024, Soham Kulkarni and contributors
# For license information, please see license.txt

# import frappe
from frappe import _
import frappe
from pypika import functions as fn

def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Voucher"),
			"fieldname": "voucher",
			"fieldtype": "Link",
			"options": "Stock Entry",
			"width": 100
		},
		{
			"label": _("Date"),
			"fieldname": "posting_date",
			"fieldtype": "date",
			"width": 200
		},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options":"Warehouse",
			"width": 100
		},
		{
			"label": _("Item"),
			"fieldname": "item",
			"fieldtype": "link",
			"options":"Item",
			"width": 100
		},{
			"label": _("Qty Changed"),
            "fieldname": "qty_changed",
            "fieldtype": "Float",
            "width": 100,
		},
		{
            "label": _("Rate"),
            "fieldname": "in_out_rate",
            "fieldtype": "Currency",
            "width": 200,
        },
        {
            "label": _("Valuation Rate"),
            "fieldname": "valuation_rate",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": _("Value Change"),
            "fieldtype": "Float",
            "fieldname":"value",
            "width": 150,
        },
        # {
        #     "label": _("Available Qty"),
        #     "fieldtype": "Int",
        #     "fieldname":"available_qty",
        #     "width": 150,
        # }
	]




def get_data(filters=None) -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	ledger_entries = get_ledger_entries(filters)
	for entry in ledger_entries:
			sle = frappe.qb.DocType("Stock Ledger Entry")
			query =  (
				frappe.qb.from_(sle)
          		.select(
                	fn.Sum(sle.qty_changed).as_("available_qty"),
                	fn.Sum(sle.qty_changed * sle.in_out_rate).as_("total_incoming_value"),
					sle.quantity_in
            	)
            	.where(sle.item == entry["item"])
				.where(sle.warehouse == entry["warehouse"])
			)
			results = query.run(as_dict=True)
			print(results)
			entry["available_qty"] = results[0]["available_qty"]
			# entry["value"] = results[0]["quantity_in"] * sle.quantity_in
			# entry["valuation_rate"] = results[0]["total_value"]/entry["available_qty"]
	return ledger_entries


def get_ledger_entries(filters):
	sle = frappe.qb.DocType("Stock Ledger Entry")
	query =  (frappe.qb.from_(sle)).select(
			sle.voucher,
			sle.posting_date,
			sle.warehouse,
			sle.item,
			(sle.qty_changed * sle.in_out_rate).as_("value"),
			sle.in_out_rate,
			sle.valuation_rate,
			sle.qty_changed,
	).orderby(sle.posting_date)
    
	query = apply_filters(filters= filters ,sle = sle, query= query)
	results = query.run(as_dict=True)
	print(results)
	return results

def apply_filters(filters, sle, query):
    
    if "voucher" in filters and filters["voucher"]:
        query = query.where(sle.voucher_name == filters["voucher"])
    if "item" in filters and filters["item"]:
        query = query.where(sle.item == filters["item"])
    if "posting_date" in filters and filters["entry_date"]:
        query = query.where(sle.entry_date == filters["entry_date"])
    if "warehouse" in filters and filters["warehouse"]:
        query = query.where(sle.warehouse == filters["warehouse"])
    return query