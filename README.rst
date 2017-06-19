# API.AI Webhook ![Travis CI build status image for master branch](https://travis-ci.org/paoro-solutions/apiaiwebhook.svg?branch=master)

API.AI Webhook is a fulfillment microframework for [API.AI](https://api.ai/) based on [Flask](http://flask.pocoo.org/) for getting started quickly with API.AI [webhooks](https://docs.api.ai/docs/webhook). 

## Users' Guide 

### Quick Start

Install the package with 
    
    pip install apiaiwebhook
    
A minimal api.ai Webhook application looks like this:
    
    from apiaiwebhook import APIAIWebhook
    app = APIAIWebhook(__name__)
    
    @app.fulfillment("hello-world")
    def hello_world():
        return app.make_response_apiai(speech="Hello World!")

    if __name__ == '__main__':
        app.run()

To run the application, just execute the python file:

    python hello_world.py

To test the application, you can use either the in-built api.ai test client

    app.testing = True
    res = app.test_client_apiai().webhook(action="hello-world"})
    assert res.status_code == 200
    assert ""Hello, World!" in res.data

Or you can use curl

    curl -X POST -H "Content-Type: application/json" -d '{"result": {"action": "hello-world"}}' http://127.0.0.1:5000/webhook

### Parameters

The parameters are extracted from `results/parameters`.
This dictionary is passed to the fulfillment function via  `**` operator (unpacked):

    {
        "results": {
            "action": "hello-world",
            "parameters": {
                "parameter": "example value"
                }
        }
    }

The fulfillment function declaration should look like this:

    @app.fulfillment("hello-world")
    def hello_world(parameter = None, **kwargs):
        return app.make_response_apiai(speech="Hello, %s!" % parameter)

The default value is required when the parameter can be empty.
Kwargs is useful when additional parameters are expected in the future.

### Response
The webhook dispatcher responses:

* HTTP 400 when `api_key_value` is defined but it the authentication header is not provided.
* HTTP 401 when `api_key_value` is defined but it is invalid.
* HTTP 404 when fulfillment function is not defined for the provided action.

Otherwise it returns a valid application/json content-type HTTP response.
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

### Securing
The `APIAIWebhook` class defines the initialization parameters of `api_key_header` (default is `api-key`) and `api_key_value` (default is `None`) parameters.

In order to secure your webhook, define a shared secret:

    from apiaiwebhook import APIAIWebhook
    app = APIAIWebhook(__name__, api_key_value="secret")

Then configure the authentication header in your API.AI agent.

### Testing

The API.AI Webhook Client extends the Flask Client in order to post valid webhook messages.

    app.testing = True
    app.debug = True
    r = app.test_client_apiai().webhook(action="hello-world",
                                        parameters={"param": "value"})

### Flask
The `APIAIWebhook` class is derived from `Flask`. Visit the official [website](http://flask.pocoo.org/) to extend the functionality of API.AI Webhook 

## Development

Before running or deploying this application, install the framework using
[pip](http://pip.readthedocs.io/en/stable/):

    pip install -e .
    
To test the framework, execute the unit tests via:

    python unit_tests.py
