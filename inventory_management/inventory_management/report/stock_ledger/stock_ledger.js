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
	formatter: function (value, row, column, data, default_warehose) {
		value = default_warehose(value, row, column, data)
		if (column.fieldname == "qty_changed" && data){
			if (data.qty_change < 0) {
				value = "<span style='color:red'>" + value + "</span>";
			}
			else {
				value = "<span style='color:green'>" + value + "</span>";
			}
		}
		return value
	},
};
