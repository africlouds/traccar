// Copyright (c) 2018, Africlouds Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Billing Period', {
	refresh: function(frm) {
			frm.add_custom_button(__("Generate Invoices"), function () {
				frappe.call({
						method: "traccar.api.generate_invoices",
						args:{
							period: frm.doc.name
						},	
						callback: function(r) {
						}
				})
			});
			frm.add_custom_button(__("View Invoices"), function () {
				frappe.set_route("List", "Sales Invoice",{"billing_period": frm.doc.name});	
			});
		}
});
