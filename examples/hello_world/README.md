# API.AI Webhook Example: Hello World

The application is tested using `python 2.7`.

Install the package with 
    
    pip install apiaiwebhook
    
To run the application, just execute the python file:
    
    python hello_world.py
    
To test test the application, you can use either the in-built api.ai test client
    
    python hello_world_test.py
    
Or you can use curl
    
    curl -X POST -H "Content-Type: application/json" -H "api-key: secret" -d '{"result": {"action": "hello-world"}}' http://127.0.0.1:5000/webhook
