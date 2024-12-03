// Copyright (c) 2024, Soham Kulkarni and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Item", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Item", "onload", function(frm) {
    frm.set_query("default_warehouse", function() {
    console.log("Is this working")
    return {
    "filters": {
    "company": frm.doc.brand
    }
    };
    });
});

frappe.ui.form.on("Item",{
    same_as_default_warehouse(frm){
        if(frm.doc.same_as_default_warehouse){
            frm.set_value('opening_warehouse', frm.doc.default_warehouse)
        }
    }

})