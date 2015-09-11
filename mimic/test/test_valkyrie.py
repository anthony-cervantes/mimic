
from twisted.trial.unittest import SynchronousTestCase
from twisted.internet.task import Clock

from mimic.core import MimicCore
from mimic.resource import MimicRoot
from mimic.test.helpers import json_request


class ValkyrieAPITests(SynchronousTestCase):

    """
    Tests for the Valkyrie API
    """

    def setUp(self):
        """
        Initialize core and root
        """
        self.core = MimicCore(Clock(), [])
        self.root = MimicRoot(self.core).app.resource()
        self.url = "/valkyrie/v2"

    def test_post_auth_token_to_login_endpoint(self):
        """
        Obtain an auth token
        """
        data = {"something": "anything"}
        (response, content) = self.successResultOf(json_request(self, self.root,
                                                                "POST",
                                                                self.url + "/login", data))
        self.assertEqual(200, response.code)

    def test_post_auth_token_to_login_user_endpoint(self):
        """
        Obtain an auth token
        """
        data = {"something": "anything"}
        (response, content) = self.successResultOf(json_request(self, self.root,
                                                                "POST",
                                                                self.url + "/login_user", data))
        self.assertEqual(200, response.code)

    def test_get_devices_effective_permissions(self):
        """
        Obtain list of device permissions for contact 12 on account 1234
        """
        (response, content) = self.successResultOf(
            json_request(self, self.root, "GET",
                         self.url +
                         "/account/1234/permissions/contacts/devices/by_contact/12/effective"))
        self.assertEqual(200, response.code)
        self.assertTrue(content["contact_permissions"])
        self.assertEqual(len(content["contact_permissions"]), 3)

    def test_get_accounts_effective_permissions(self):
        """
        Obtain list of account permissions for contact 12 on account 1234
        """
        (response, content) = self.successResultOf(
            json_request(self, self.root, "GET",
                         self.url +
                         "/account/1234/permissions/contacts/accounts/by_contact/12/effective"))
        self.assertEqual(200, response.code)
        self.assertTrue(content["contact_permissions"])
        self.assertEqual(len(content["contact_permissions"]), 1)
        self.assertEqual(content["contact_permissions"][0]["permission_type"], 17)

    def test_effective_permissions(self):
        """
        Obtain list of device permissions for contact 78 on account 5678
        """
        (response, content) = self.successResultOf(
            json_request(self, self.root, "GET",
                         self.url +
                         "/account/5678/permissions/contacts/devices/by_contact/78/effective"))
        self.assertEqual(200, response.code)
        self.assertTrue(content["contact_permissions"])
        self.assertEqual(len(content["contact_permissions"]), 1)
        permission = content["contact_permissions"][0]
        self.assertEqual(permission["permission_type"], 11)
        self.assertEqual(permission["item_id"], 262144)
