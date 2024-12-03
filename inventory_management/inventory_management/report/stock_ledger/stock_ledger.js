// Copyright (c) 2024, Soham Kulkarni and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Ledger"] = {
	"filters": [
		{
			"fieldname": "item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "entry_date",
			"label": __("Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		}
	],
};
