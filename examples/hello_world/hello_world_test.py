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
import hello_world

class HelloWorldTest(unittest.TestCase):
    def setUp(self):
        hello_world.app.testing = True
        self.test_client = hello_world.app.test_client_apiai()

    def test_hello_world_default(self):
        r = self.test_client.webhook(result_action="hello-world")
        assert r.status_code == 200
        assert "Hello World!" in r.data

    def test_hello_world_apiai(self):
        r = self.test_client.webhook(result_action="hello-world",
                                     result_parameters={"name": "api.ai webhook"})
        assert r.status_code == 200
        assert "Hello api.ai webhook!" in r.data


if __name__ == '__main__':
    unittest.main()
