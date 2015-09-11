"""
Model objects for the Valkyrie mimic.
"""
from characteristic import attributes, Attribute
from uuid import uuid4
from json import loads, dumps

from mimic.util.helper import random_hex_generator

class AccountContactPermission(object):
    """
    An intersection object representing a certain contact's permissions on a certain account's items
    """

    permission_type_map = {
        6: "view_domain",
        4: "view_billing",
        14: "admin_product",
        10: "manage_users",
        8: "manage_certificates",
        19: "edit_firewall_config",
        2: "edit_ticket",
        18: "view_firewall_config",
        15: "account_admin",
        7: "edit_domain",
        13: "edit_product",
        3: "view_community",
        17: "view_reports",
        16: "move_manager",
        12: "view_product",
        11: "manage_contact",
        9: "upgrade_account",
        5: "edit_billing",
        1: "view_ticket"}

    item_type_map = {
        1: "accounts",
        2: "devices"}

    def __init__ (self, account_number, contact_id, permission_type, item_id, item_type_id):
        self.account_number = account_number
        self.contact_id = contact_id
        self.permission_type = permission_type
        self.permission_name = self.permission_type_map.get(self.permission_type, "unknown")
        self.item_id = item_id
        self.item_type_id = item_type_id
        self.item_type_name = self.item_type_map.get(self.item_type_id, "unknown")

    def json(self):
        return {
            "account_number": self.account_number,
            "contact_id": self.contact_id,
            "permission_type": self.permission_type,
            "permission_name": self.permission_name,
            "item_id": self.item_id,
            "item_type_id": self.item_type_id,
            "item_type_name": self.item_type_name
        }

@attributes([Attribute("valkyrie_store", default_factory=list)])
class ValkyrieStore(object):
    """

    Extremely barebones Valkyrie backing store with some direct, static permissions.

    No create or delete permissions endpoints are implemented.
    No logic for determining effective permissions from indirect permissions is present.

    A GET on the following URI, for example, should always return three effective permissions:

        http://localhost:8900/valkyrie/v2/account/1234/permissions/contacts/devices/by_contact/12/effective

    ...while a GET on this URI should return one:

        http://localhost:8900/valkyrie/v2/account/1234/permissions/contacts/accounts/by_contact/12/effective

    TODO: some things are only guessed at, since the published Valkyrie docs don't include response code or negative response information
    TODO: obvious next step would be to implement endpoint /account/{account_number}/permissions/contacts/{accounts,devices}/by_contact/{contact_id}
    in order to allow dynamic loading of this mock backing store.

    """

    permissions = []
    # Arguments are: account, contact, (direct) permission, item, item_type (account or device)
    permissions.append(AccountContactPermission(1234, 12, 1, 256, 2))
    permissions.append(AccountContactPermission(1234, 12, 17, 1234, 1))
    permissions.append(AccountContactPermission(1234, 12, 2, 4096, 2))
    permissions.append(AccountContactPermission(1234, 12, 3, 16384, 2))
    permissions.append(AccountContactPermission(1234, 34, 1, 16384, 2))
    permissions.append(AccountContactPermission(5678, 12, 1, 65536, 2))
    permissions.append(AccountContactPermission(5678, 56, 1, 65536, 2))
    permissions.append(AccountContactPermission(5678, 56, 1, 262144, 2))
    permissions.append(AccountContactPermission(5678, 78, 11, 262144, 2))

    def create_token(self, request):
        """
        Create an auth token without even interrogating the POSTed credential data
        """
        request.setResponseCode(200)
        token = {"X-Auth-Token": str(random_hex_generator(16))}
        return dumps(token)

    def get_accounts_permissions(self, request, account_number, contact_id):
        """
        Find and format the set of permissions held on account items by the given contact for the given account.
        """
        pm = []
        for p in self.permissions:
            if p.account_number == account_number and p.contact_id == contact_id and p.item_type_id == 1:
                pm.append(p)

        if len(pm) == 0:
            request.setResponseCode(404)
            return b''

        response_message = { "contact_permissions": [] }
        for p in pm:
            response_message['contact_permissions'].append(p.json( ))

        return dumps(response_message)

    def get_devices_permissions(self, request, account_number, contact_id):
        """
        Find and format the set of permissions held on device items by the given contact for the given account.
        """
        pm = []
        for p in self.permissions:
            if p.account_number == account_number and p.contact_id == contact_id and p.item_type_id == 2:
                pm.append(p)

        if len(pm) == 0:
            request.setResponseCode(404)
            return b''

        response_message = { "contact_permissions": [] }
        for p in pm:
            response_message['contact_permissions'].append(p.json( ))

        return dumps(response_message)

