// Copyright (c) 2018, Africlouds Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Traccar Server', {
	refresh: function(frm) {
		frm.add_custom_button(__("Sync with Traccar Server"), function () {
			frappe.call({
				method: "traccar.api.sync",
				args:{
					server: "Tracking Paymatic"
				},
				callback: function(r) {
				}
			})
		})
	}
});
