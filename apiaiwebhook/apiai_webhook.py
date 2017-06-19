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
import flask.testing


class APIAIWebhook(flask.Flask):
    """
    The API.AI webhook object extends the Flask WSGI application and acts as the central
    object. Once it is created it will act as a central registry for
    the fulfillment functions.

    Usually you create a :class:`APIAIWebhook` instance in your main module or
    in the :file:`__init__.py` file of your package like this::

        from apiaiwebhook import APIAIWebhook
        app = APIAIWebhook(__name__)

    :param import_name:     the name of the application package

    :param api_key_header:  HTTP authentication header name for the shared secret is shared by API.AI.
                            Defaults to 'api-key'.

    :param api_key_value:   HTTP authentication header name for the shared secret is shared by API.AI.
                            When None is provided the HTTP authentication header is not validated.
                            Defaults to None.
    :param webhook_url:     URL rule for the webhook dispatcher. Defaults to '/webhook/'.

    For more information, see the specification of Flask object.

    """

    def fulfillment(self, rule):
        """
        A decorator that is used to register a fulfillment function for a
        given action. usage::

            @app.fulfillment("hello-world")
            def hello_world():
                return "Hello, World!"

        :param rule The 'action' as string.
                    The action is extracted from::
                        {
                            "results": {
                                "action": <HERE>,
                                "parameters": {
                                    "parameter": <EXAMPLE>
                                    }
                            }
                        }
        """

        def decorator(f):
            self.fulfillment_functions[rule] = f
            return f

        return decorator

    def webhook(self):
        """
        Webhook dispatcher. It extracts the action and the parameters from the HTTP REST request,
        then calls the fulfillment function with the extracted parameters.

        The action and parameters are extracted from:

            {
                "results": {
                    "action": "hello-world",
                    "parameters": {
                        "parameter": "example value"
                        }
                }
            }

        The function declaration should look like this:

            @app.fulfillment("hello-world")
            def hello_world(parameter = None, **kwargs):
                return app.make_response_apiai(speech="Hello, %s!" % parameter)

        The default value is required when the parameter can be empty.
        Kwargs is useful when additional parameters are expected in the future.

        :return:
            * HTTP 400 when `api_key_value` is defined but it the authentication header is not provided.
            * HTTP 401 when `api_key_value` is defined but it is invalid.
            * HTTP 404 when fulfillment function is not defined for the provided action.
            * Otherwise it returns a valid application/json content-type HTTP response.

            The response can be create using the helper function of `make_response_apiai()`

            Example:

                    @app.fulfillment("hello-world")
                    def my_fulfillment_none():
                        return app.make_response_apiai(speech="Hello, World!"
                                                       display_text="Hello, World! I am please to meet you!")

            The response will be like:

                    {
                        "speech": "Hello, World!",
                        "displayText": "Hello, World! I am please to meet you!",
                        "data": None,
                        "contextOut": [],
                        "source": <name of Flask application>,
                        "followupEvent": None
                    }
        """
        if self.api_key_value is not None:
            api_key_value = flask.request.headers.get(self.api_key_header)
            if api_key_value is None:
                msg = "api-key http header is required"
                self.logger.error(msg)
                flask.abort(400, msg)
                return

            if api_key_value != self.api_key_value:
                msg = "api-key is invalid"
                self.logger.error(msg)
                flask.abort(401, msg)
                return

        req = flask.request.get_json(force=True)
        self.logger.debug("request: %s" % json.dumps(req))

        result = req["result"]
        action = result.get("action", "")
        parameters = result.get("parameters", {})

        self.logger.debug("%s: %s" % (action, parameters))

        if action in self.fulfillment_functions:
            res = self.fulfillment_functions[action](**parameters)
        else:
            msg = "fulfillment is not implemented: %s" % action
            self.logger.error(msg)
            flask.abort(404, msg)
            return

        res = json.dumps(res)
        self.logger.debug("response: %s" % res)

        r = flask.make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

    def test_client_apiai(self):
        """
        Creates a test client for this application. For example::

            app.testing = True
            client = app.test_client_apiai()

        :return: A APIAIWebhookTestClient class
        """
        flask_test_client = super(APIAIWebhook, self).test_client()
        flask_test_client.__class__ = APIAIWebhookClient
        flask_test_client.apiai_webhook = self
        return flask_test_client

    def make_response_apiai(self,
                            speech=None,
                            display_text=None,
                            data=None,
                            context_out=[],
                            followup_event=None):
        """
        Convert the return value from a fulfillment function to the expected response.

        :param speech: String. Response to the request.
        :param display_text: String. Response to the request.
        :param data: Object. Additional data required for performing the action on the client side.
        The data is sent to the client in the original form and is not processed by API.AI.
        :param context_out: Array of context objects. Such contexts are activated after intent completion.
        Example: "contextOut": [{"name":"weather", "lifespan":2, "parameters":{"city":"Rome"}}]
        :param followup_event: Object. Event name and optional parameters sent from the web service to API.AI.
        Example: {"followupEvent":{"name":"<event_name>","data":{"<parameter_name>":"<parameter_value>"}}}
        :return: dictionary which can be converted to a JSON object by the webhook dispatcher.
        """
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
                 webhook_url="/webhook/",
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


class APIAIWebhookClient(flask.testing.FlaskClient):
    """
    The API.AI Webhook Client extends the Flask Client in order to post valid webhook messages.

        app.testing = True
        app.debug = True
        r = app.test_client_apiai().webhook(action="hello-world",
                                            parameters={"param": "value"})
    """

    def __init__(self, *args, **kwargs):
        super(APIAIWebhookClient, self).__init__(*args, **kwargs)
        self.apiai_webhook = None

    def webhook(self,
                action=None,
                parameters={}):
        """
        Uses a regular Flask test client in order to post valid webhook messages.

        :param action: action to tested
        :param parameters: parameters of the action as dictionary
        :return: returns a response object as a regular Flask test client
        """
        req = {
            "result": {
                "action": action,
                "parameters": parameters
            }
        }

        return self.post(
            self.apiai_webhook.webhook_url,
            data=json.dumps(req),
            content_type="application/json",
            headers={self.apiai_webhook.api_key_header: self.apiai_webhook.api_key_value})
