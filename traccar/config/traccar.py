from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
         {
             "label": _("Traccar"),
             "items": [
                    {
                        "type":"doctype",
                        "name": "Billing Period",
                        "label": _("Billing Periods"),
                        "description": _("Billing Periods")
                    },
                    {
                        "type":"doctype",
                        "name": "Traccar Server",
                        "label": _("Traccar Servers"),
                        "description": _("Traccar Servers")
                    },
                 ]
        },
    ]