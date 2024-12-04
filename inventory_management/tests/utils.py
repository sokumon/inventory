import frappe
def create_item():
        if not frappe.db.exists("Item", "TEST-001"):
            test_item = frappe.get_doc({
                "doctype": "Item",
                "item_name": "Item 1",
                "item_code": "TEST-001",
                "opening_stock_quantity": 10,
                "opening_stock_unit_cost": 10,
                "opening_warehouse":"WH-0001",
                "default_warehouse":"WH-0001"
            })
            test_item.insert()

def create_stock_entry():
        create_item()
        item = frappe.get_doc("Item", "TEST-001")
        if not frappe.db.exists("Stock Entry", "SE-1111"):
            test_stock_entry = frappe.get_doc({
                "doctype": "Stock Entry",
                "entry_type": "Consume",
                "entry_date": frappe.utils.today(),
                "entry_time": frappe.utils.now(),
                "items": [{
                    "item": item,
                    "source_warehouse": item.default_warehouse,
                    "qty": 1,
                    "unit_cost": 1
                }]
            })
            test_stock_entry.insert()
            test_stock_entry.submit()