// Copyright (c) 2024, Soham Kulkarni and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Balance"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("As On Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label": __("As On Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		}
	]
};