import frappe
@frappe.whitelist()
def get_meta_from_doctype(doctype):
    meta = frappe.get_meta("Item")
    return meta.get_fieldnames_with_value()