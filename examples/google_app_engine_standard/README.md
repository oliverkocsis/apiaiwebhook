# API.AI Webhook Example: Google App Engine Standard

This sample shows how to use API.AI Webhook with Google App Engine Standard.

The application is tested using `python 2.7`.

Before running or deploying this application, install the dependencies using
[pip](http://pip.readthedocs.io/en/stable/):

    pip install -r requirements.txt
    pip install -t lib -r requirements.txt
    
To run the application locally, just execute the python file:
    
    python hello_world.py
    
To test test the application locally, you can use either the in-built api.ai test client
    
    python hello_world_test.py
    
Or you can use curl
    
    curl -X POST -H "Content-Type: application/json" -H "api-key: secret" -d '{"result": {"action": "hello-world"}}' http://127.0.0.1:5000/webhook

To deploy your app to Google App Engine, run the following command from within the root directory of your application where the app.yaml file is located:

    gcloud app deploy --project <project-id>
    
Service name is included into the `app.yaml` file.
      
To view your application in the web browser run:
    
    gcloud app browse --project <project-id> --service <service-name>

For more information, see the [API.AI Webhook README](../../README.md)
