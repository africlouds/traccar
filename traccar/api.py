import frappe
import requests
from frappe.utils.background_jobs import enqueue


@frappe.whitelist()
def sync(server):
    #1: get groups from traccar
    #2: for each group, check if a correspong customer exists
    #3: if customer doesnt exists create customers
    enqueue("traccar.api.sync_bg", server=server)

def sync_bg(server):
    #1: get groups from traccar
    #2: for each group, check if a correspong customer exists
    #3: if customer doesnt exists create customers
    server = frappe.get_doc("Traccar Server", server)
    server.sync()

@frappe.whitelist()
def generate_invoices(period):
    enqueue("traccar.api.generate_invoices_bg", period=period)


def generate_invoices_bg(period):
    period = frappe.get_doc("Billing Period", period)
    period.generate_invoices()

