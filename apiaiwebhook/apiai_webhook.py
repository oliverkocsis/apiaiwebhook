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

import json
import flask


class APIAIWebhook(flask.Flask):
    def fulfillment(self, rule):
        def decorator(f):
            self.fulfillment_fucntions[rule] = f
            return f

        return decorator

    def webhook(self):
        api_key = flask.request.headers.get("api-key")
        if api_key is None:
            msg = "api-key http header is required"
            print(msg)
            flask.abort(400, msg)

        if api_key != self.api_key:
            msg = "api-key is invalid"
            print(msg)
            flask.abort(401, msg)

        req = flask.request.get_json(force=True)
        print("Request: " + json.dumps(req))

        result = req["result"]
        action = result.get("action", "")
        parameters = result.get("parameters", {})

        print ("%s: %s" % (action, parameters))

        res = self.fulfillment_fucntions[action](**parameters)

        res = json.dumps(res)
        print("Response: " + res)

        r = flask.make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

    def test_client_apiai(self):
        flask_test_client = super(APIAIWebhook, self).test_client()
        return APIAIWebhookTestClient(flask_test_client, self.api_key, self.webhook_url)

    def make_response_apiai(self,
                            speech=None,
                            displayText=None,
                            data=None,
                            contextOut=[],
                            followupEvent=None):
        return {
            "speech": speech,
            "displayText": displayText,
            "data": data,
            "contextOut": contextOut,
            "source": self.name,
            "followupEvent": followupEvent
        }

    def __init__(self,
                 import_name,
                 api_key,
                 webhook_url="/webhook",
                 static_path=None,
                 static_url_path=None,
                 static_folder='static',
                 template_folder='templates',
                 instance_path=None,
                 instance_relative_config=False,
                 root_path=None):
        super(APIAIWebhook, self).__init__(
            import_name,
            static_path,
            static_url_path,
            static_folder,
            template_folder,
            instance_path,
            instance_relative_config,
            root_path)

        self.api_key = api_key
        self.fulfillment_fucntions = {}
        self.webhook_url = webhook_url
        self.add_url_rule(webhook_url, "webhook", self.webhook, methods=['POST'])


class APIAIWebhookTestClient:
    def __init__(self, flask_test_client, api_key, webhook_url):
        self.flask_test_client = flask_test_client
        self.api_key = api_key
        self.webhook_url = webhook_url

    def webhook(self,
                result_action=None,
                result_parameters={}):
        req = {
            "result": {
                "action": result_action,
                "parameters": result_parameters
            }
        }
        return self.flask_test_client.post(
            self.webhook_url,
            data=json.dumps(req),
            content_type="application/json",
            headers={"api-key": self.api_key})
