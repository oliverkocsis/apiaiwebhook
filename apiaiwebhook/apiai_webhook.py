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

import flask
import flask.json as json


class APIAIWebhook(flask.Flask):
    def fulfillment(self, rule):
        def decorator(f):
            self.fulfillment_functions[rule] = f
            return f

        return decorator

    def webhook(self):
        if self.api_key_value is not None:
            api_key_value = flask.request.headers.get(self.api_key_header)
            if api_key_value is None:
                msg = "api-key http header is required"
                self.logger.error(msg)
                flask.abort(400, msg)

            if api_key_value != self.api_key_value:
                msg = "api-key is invalid"
                self.logger.error(msg)
                flask.abort(401, msg)

        req = flask.request.get_json(force=True)
        self.logger.debug("request: %s" % json.dumps(req))

        result = req["result"]
        action = result.get("action", "")
        parameters = result.get("parameters", {})

        self.logger.debug("%s: %s" % (action, parameters))

        res = self.fulfillment_functions[action](**parameters)

        res = json.dumps(res)
        self.logger.debug("response: %s" % res)

        r = flask.make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

    def test_client_apiai(self):
        flask_test_client = super(APIAIWebhook, self).test_client()
        return APIAIWebhookTestClient(flask_test_client, self)

    def make_response_apiai(self,
                            speech=None,
                            display_text=None,
                            data=None,
                            context_out=[],
                            followup_event=None):
        return {
            "speech": speech,
            "displayText": display_text,
            "data": data,
            "contextOut": context_out,
            "source": self.name,
            "followupEvent": followup_event
        }

    def __init__(self,
                 import_name,
                 api_key_header="api-key",
                 api_key_value=None,
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

        self.api_key_header = api_key_header
        self.api_key_value = api_key_value
        self.fulfillment_functions = {}
        self.webhook_url = webhook_url
        self.add_url_rule(webhook_url, "webhook", self.webhook, methods=['POST'])
        if self.api_key_value is None:
            self.logger.warning("api-key is empty! use 'api_key_value' parameter to define it.")


class APIAIWebhookTestClient:
    def __init__(self, flask_test_client, apiai_webhook):
        self.flask_test_client = flask_test_client
        self.apiai_webhook = apiai_webhook

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
            self.apiai_webhook.webhook_url,
            data=json.dumps(req),
            content_type="application/json",
            headers={self.apiai_webhook.api_key_header: self.apiai_webhook.api_key_value})
