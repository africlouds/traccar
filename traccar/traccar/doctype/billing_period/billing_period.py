# -*- coding: utf-8 -*-
# Copyright (c) 2018, Africlouds Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BillingPeriod(Document):
    def generate_invoices(self):
        customers = frappe.get_all("Customer", fields=["name"])
        frappe.publish_realtime('msgprint', 'Starting invoice generation...')
        counter = 0
        for customer in customers:
            vehicles = frappe.get_all("Vehicle", filters={"customer": customer["name"]}, fields=["license_plate", "phone", "serial_number"])
            if vehicles:
                check_invoices = frappe.get_list("Sales Invoice", filters={"billing_period": self.name, "customer": customer["name"]})
                if not check_invoices:
                    vehicle_details = ""
                    for veh in vehicles:
                        vehicle_details += " " + veh['license_plate']
                    invoice = frappe.new_doc("Sales Invoice")
                    invoice.customer = customer["name"]
                    invoice.billing_period = self.name
                    invoice.taxes_and_charges = "Rwanda Tax - PL"
                    invoice.append("items", {
                        "item_code": "Online Service",
                        "qty":len(vehicles),
                        "rate": 3000,
                        "description": vehicle_details
                    })
                    invoice = invoice.insert()
                    frappe.db.commit()
                    counter += 1
        frappe.publish_realtime("msgprint", "Generated %d invoices" % counter)
    def validate(self):
        invoices = frappe.get_list("Sales Invoice", filters={"billing_period": self.name}, fields=["total"])
        if invoices:
            self.invoices = len(invoices)
            amount = 0
            for invoice in invoices:
                amount += invoice['total']
            self.amount = amount
            self.paid = 0
            self.outstanding = amount
        
