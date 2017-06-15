# Copyright (C) 2017 Paoro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import flask.json as json

from apiai_webhook import APIAIWebhook


class APIAIWebhookTest(unittest.TestCase):
    def setUp(self):
        app = APIAIWebhook(__name__)
        app.testing = True
        app.debug = True
        self.test_client = app.test_client_apiai()

        @app.fulfillment("none")
        def my_fullfillment_none():
            return app.make_response_apiai(speech="Test with no parameter")

        @app.fulfillment("one")
        def my_fullfillment_one(one):
            return app.make_response_apiai(speech="Test with one parameter: %s" % one)

        @app.fulfillment("one-default")
        def my_fullfillment_one(one=None):
            return app.make_response_apiai(speech="Test with one parameter (default None): %s" % one)

        @app.fulfillment("multiple")
        def my_fullfillment_two(one, two):
            return app.make_response_apiai(speech="Test with multiple parameters: %s, %s" % (one, two))

    def test_none(self):
        r = self.test_client.webhook(result_action="none")
        assert r.status_code == 200
        assert "Test with no parameter" in r.data.decode("utf-8")

    def test_one(self):
        r = self.test_client.webhook(result_action="one",
                                     result_parameters={"one": "first parameter"})
        assert r.status_code == 200
        assert "Test with one parameter: first parameter" in r.data.decode("utf-8")

    def test_one_default_empty(self):
        r = self.test_client.webhook(result_action="one-default")
        assert r.status_code == 200
        assert "Test with one parameter (default None): None" in r.data.decode("utf-8")

    def test_multiple(self):
        r = self.test_client.webhook(result_action="multiple",
                                     result_parameters={
                                         "one": "first parameter",
                                         "two": "second parameter",
                                     })
        assert r.status_code == 200
        assert "Test with multiple parameters: first parameter, second parameter" in r.data.decode("utf-8")


class APIAIWebhookSecuredTest(unittest.TestCase):
    def setUp(self):
        app = APIAIWebhook(__name__, api_key_value="secret")
        app.testing = True
        app.debug = True
        self.app = app
        self.test_client = app.test_client()

        @app.fulfillment("none")
        def my_fullfillment_none():
            return app.make_response_apiai(speech="Test with no parameter")

    def test_invalid_api_key_header(self):
        r = self.test_client.post(
            self.app.webhook_url,
            data=json.dumps({}),
            content_type="application/json",
            headers={self.app.api_key_header[::-1]: self.app.api_key_value})
        assert r.status_code == 400

    def test_invalid_api_key_value(self):
        r = self.test_client.post(
            self.app.webhook_url,
            data=json.dumps({}),
            content_type="application/json",
            headers={self.app.api_key_header: self.app.api_key_value[::-1]})
        assert r.status_code == 401


if __name__ == '__main__':
    unittest.main(verbosity=2)
