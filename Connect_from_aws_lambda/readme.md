## Let's connect to Google Calendar using Lambda function

Here we will not fetch user credentials from cred.json or from token.pickle file, Considering will get the authorization token from front-end will embed this within our lambda_function and will create a credentials object. THis implementation helps to create REST APIs and Lambda Functions as well.

### Lambda Functions accepts zip file so we will create a zip file out of this folder and will upload, test


### (Installing all required libraries in this folder and use them) use Python 2.7 Runtime

```
pip install -t . --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```


### Here lambda_function.py file is our entry point from where will get inputs for Calendar API.




