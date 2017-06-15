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

from apiai_webhook import APIAIWebhook
import unittest


class APIAIWebhookTest(unittest.TestCase):
    def setUp(self):
        app = APIAIWebhook(__name__, "secret")
        app.testing = True
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
        assert "Test with no parameter" in r.data

    def test_one(self):
        r = self.test_client.webhook(result_action="one",
                                     result_parameters={"one": "first parameter"})
        assert r.status_code == 200
        assert "Test with one parameter: first parameter" in r.data

    def test_one_default_empty(self):
        r = self.test_client.webhook(result_action="one-default")
        assert r.status_code == 200
        assert "Test with one parameter (default None): None" in r.data

    def test_multiple(self):
        r = self.test_client.webhook(result_action="multiple",
                                     result_parameters={
                                         "one": "first parameter",
                                         "two": "second parameter",
                                     })
        assert r.status_code == 200
        assert "Test with multiple parameters: first parameter, second parameter" in r.data


if __name__ == '__main__':
    unittest.main(verbosity=2)
