# Webhook Dispatcher for api.ai 

### About
api.ai Webhook is a python package for getting started quickly with api.ai [webhooks](https://docs.api.ai/docs/webhook). 

### Quick Start
Download and install `python 2.7`.

Install the package with 
    
    pip install apiaiwebhook
    
A minimal api.ai Webhook application looks like this:

    from apiaiwebhook import APIAIWebhook
    app = APIAIWebhook(__name__, "secret")
    
    @app.fulfillment("hello-world")
    def hello_world():
        return "Hello, World!" 
    
    if __name__ == '__main__':
        app.run()
 
To run the application, just execute the python file

    python hello_world.py

To test test the application, you can use the in-built api.ai test client

    app.testing = True
    res = app.test_client_apiai().webhook(result_action="hello-world"})
    assert res.status_code == 200
    assert ""Hello, World!" in res.data

Or you can use curl

    curl -X POST -H "Content-Type: application/json" -H "api-key: secret" -d '{"result": {"action": "hello-world"}}' http://127.0.0.1:5000/webhook    
    
### Development

Before running or deploying this application, install the dependencies using
[pip](http://pip.readthedocs.io/en/stable/):

    pip install -r requirements.txt    
