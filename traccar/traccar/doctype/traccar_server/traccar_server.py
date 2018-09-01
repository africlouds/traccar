# -*- coding: utf-8 -*-
# Copyright (c) 2018, Africlouds Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests

class TraccarServer(Document):
    def sync(self):
        self.sync_customers()
        self.sync_devices()

    def sync_customers(self):
        groups = requests.get("%s/api/groups" % self.url, auth=(self.username, self.password)).json()
        self.customers = len(groups)
        counter = 0
        if groups:
            for group in groups:
                check = frappe.get_all("Customer", filters={"traccar_id": group['id']})
                if not check:
                    customer = frappe.new_doc("Customer")
                    customer.customer_name = group['name']
                    customer.customer_type = "Company"
                    customer.territory = "Rwanda"
                    customer.customer_group = "Commercial"
                    customer.traccar_id = group["id"]
                    customer.insert()
                    counter += 1
        frappe.publish_realtime("msgprint", "Finished syncing %d customers" % counter)
        self.save()

    def sync_devices(self):
        devices = requests.get("%s/api/devices" % self.url, auth=(self.username, self.password)).json()
        self.devices = len(devices)
        counter = 0
        if devices:
            for device in devices:
                check = frappe.get_all("Vehicle", filters={"license_plate": device['name']})
                if not check:
                    customer = frappe.get_all("Customer", filters={"traccar_id": device["groupId"]}, fields=["customer_name"])
                    if customer:
                        vehicle  = frappe.new_doc("Vehicle")
                        vehicle.customer = customer[0]["customer_name"]
                        vehicle.license_plate = device['name']
                        vehicle.make = "NaN"
                        vehicle.model = "NaN"
                        vehicle.last_odometer = "NaN"
                        vehicle.fuel_type = "Diesel"
                        vehicle.uom = "Kilogram/Litre"
                        vehicle.traccar_id = device["id"]
                        vehicle.group_id = device["groupId"]
                        vehicle.serial_number = device["uniqueId"]
                        vehicle.status = device["status"]
                        vehicle.last_update = device["lastUpdate"]
                        vehicle.position_id = device["positionId"]
                        vehicle.phone = device["phone"]
                        vehicle.insert()
                        counter += 1

        frappe.publish_realtime("msgprint", "Finished syncing %d devices" % counter)
        self.save()
