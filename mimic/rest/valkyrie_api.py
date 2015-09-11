# -*- test-case-name: mimic.test.test_valkyrie -*-
"""
API Mock for Valkyrie.
"""

from mimic.rest.mimicapp import MimicApp


class ValkyrieApi(object):
    """
    Rest endpoints for the Valkyrie API.
    """

    app = MimicApp()

    def __init__(self, core):
        """
        :param MimicCore core: The core to which the Valkyrie Api will be
        communicating.
        """
        self.core = core

    @app.route('/login', methods=['POST'])
    def login(self, request):
        """
        Responds with response code 200 and returns an auth token
        """
        return self.core.valkyrie_store.create_token(request)

    @app.route('/login_user', methods=['POST'])
    def login_user(self, request):
        """
        Responds with response code 200 and returns an auth token
        """
        return self.core.valkyrie_store.create_token(request)

    @app.route('/account/<int:account_number>/permissions/contacts/accounts/by_contact/<int:contact_id>/effective',
               methods=['GET'])
    def effective_accounts_permissions(self, request, account_number, contact_id):
        """
        Responds with response code 200 and returns a list of permissions
        for the given account and contact
        """
        return self.core.valkyrie_store.get_accounts_permissions(request,
                                                                 account_number, contact_id)

    @app.route('/account/<int:account_number>/permissions/contacts/devices/by_contact/<int:contact_id>/effective',
               methods=['GET'])
    def effective_devices_permissions(self, request, account_number, contact_id):
        """
        Responds with response code 200 and returns a list of permissions
        for the given account and contact
        """
        return self.core.valkyrie_store.get_devices_permissions(request,
                                                                account_number, contact_id)
