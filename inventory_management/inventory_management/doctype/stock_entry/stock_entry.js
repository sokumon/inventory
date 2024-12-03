// Copyright (c) 2024, Soham Kulkarni and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Stock Entry", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Stock Entry Item",{
    item(frm,cdt,cdn){
        let row = frappe.get_doc(cdt, cdn)
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                'doctype': 'Item',
                'filters': { 'name': row.item },
                'fieldname': [
                    'default_warehouse',
                ]
            },
            callback: function(r){
                if(!r.exc){
                    if (frm.doc.entry_type == 'Receive'){
                        frappe.model.set_value(cdt, cdn, "target_warehouse", (r.message.default_warehouse));
                    }
                    else {
                        frappe.model.set_value(cdt, cdn, "source_warehouse", (r.message.default_warehouse));
                    }
                }
            }
    
        
        })
    }
})