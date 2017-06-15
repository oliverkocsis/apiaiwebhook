# API.AI Webhook

API.AI Webhook is a fulfillment microframework for [API.AI](https://api.ai/) based on [Flask](http://flask.pocoo.org/) for getting started quickly with API.AI [webhooks](https://docs.api.ai/docs/webhook). 

## Users' Guide 

### Quick Start
The application is tested using `python 2.7`.

Install the package with 
    
    pip install apiaiwebhook
    
A minimal api.ai Webhook application looks like this:
    
    from apiaiwebhook import APIAIWebhook
    app = APIAIWebhook(__name__)
    
    @app.fulfillment("hello-world")
    def hello_world():
        return "Hello, World!" 
    
    if __name__ == '__main__':
        app.run()
    
To run the application, just execute the python file:
    
    python hello_world.py
    
To test test the application, you can use either the in-built api.ai test client
    
    app.testing = True
    res = app.test_client_apiai().webhook(result_action="hello-world"})
    assert res.status_code == 200
    assert ""Hello, World!" in res.data
    
Or you can use curl
    
    curl -X POST -H "Content-Type: application/json" -d '{"result": {"action": "hello-world"}}' http://127.0.0.1:5000/webhook    

### Securing
The `APIAIWebhook` class defines the initialization parameters of `api_key_header` (default is `api-key`) and `api_key_value` (default is `None`) parameters. 

In order to secure your webhook, define a shared secret: 

    from apiaiwebhook import APIAIWebhook
    app = APIAIWebhook(__name__, api_key_value="secret") 

Then configure the authentication header in your API.AI agent. 
    
### Flask
The `APIAIWebhook` class is derived from `Flask`. Visit the official [website](http://flask.pocoo.org/) to extend the functionality of API.AI Webhook 

### Development

Before running or deploying this application, install the dependencies using
[pip](http://pip.readthedocs.io/en/stable/):

    pip install -r requirements.txt    
