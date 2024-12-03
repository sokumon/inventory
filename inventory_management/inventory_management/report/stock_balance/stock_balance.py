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
			"label": _("Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 150
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
		},
		{
            "label": _("Balance Qty"),
            "fieldname": "balance_qty",
			"fieldtype": "Float",
        },{
            "label": _("Valuation Rate"),
            "fieldname": "valuation_rate",
            "fieldtype": "Currency",
            "width": 200,
        },{
			"label": _("Balance Value"),
			"fieldname":"balance_value",
            "fieldtype": "Currency",
            "width": 100,
		}

	]


def get_data(filters=None) -> list[list]:
    ledgers = get_ledger_entries(filters=filters)

    for entry_item in ledgers:
        sle = frappe.qb.DocType("Stock Ledger Entry")
        balance_qty_query = f"""
		SELECT 
			SUM(`qty_changed`) AS 'balance_qty',
			`valuation_rate` 
		FROM 
			`tabStock Ledger Entry` 
		WHERE 
			`item` = '{entry_item["item"]}' 
			AND `posting_date` = '{entry_item["posting_date"]}' 
			AND `warehouse` = '{entry_item["warehouse"]}';
		"""

        print(balance_qty_query)
        # ORDER BY `valuation_rate` DESC LIMIT 1
        valudation_rate_query = f"SELECT `valuation_rate` FROM `tabStock Ledger Entry` WHERE `item` = '{entry_item["item"]}' AND `posting_date` = '{entry_item["posting_date"]}' AND `warehouse` = '{entry_item["warehouse"]}' ORDER BY `valuation_rate` DESC LIMIT 1;"

        balance_result = frappe.db.sql(balance_qty_query, as_dict=1)
        valuation_rate_result = frappe.db.sql(valudation_rate_query, as_dict=1)
        
        entry_item["balance_qty"] = balance_result[0]["balance_qty"]
        entry_item["valuation_rate"] = valuation_rate_result[0]["valuation_rate"]
        entry_item["balance_value"] = entry_item["balance_qty"] * entry_item["valuation_rate"]

    return ledgers






def get_ledger_entries(filters):
	sle = frappe.qb.DocType("Stock Ledger Entry")
	
	query = (
		frappe.qb.from_(sle)
		.select(
			sle.warehouse,
			sle.item,
			sle.posting_date,

		)
		.groupby(sle.item,sle.warehouse,sle.posting_date)
		.orderby(sle.posting_date)
	)
	print(query.get_sql())
	query = apply_filters(filters, sle , query)

	results = query.run(as_dict=True)
	return results

# Query

		  
def apply_filters(filters, sle, query):
	if "from_date" in filters:
		query = query.where(sle.posting_date == filters["posting_date"])
	if "warehouse" in filters:
		query = query.where(sle.warehouse == filters["warehouse"])
	if "item" in filters:
		query = query.where(sle.item == filters["item"])
	return query
		
