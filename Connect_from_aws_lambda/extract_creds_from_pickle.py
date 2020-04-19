import json
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

with open('../client_cred/token.pickle', 'rb') as token:
    creds = pickle.load(token)
    creds.refresh(Request())
# print(json.dumps(creds.__dict__, indent=2, sort_keys= True))
print(creds.token, "token")
print(creds.refresh_token, "refresh_token")
print(creds.id_token, "id_token")
print(creds.token_uri, "token_uri")
print(creds.client_id, "client_id")
print(creds.client_secret, "client_secret")
print(creds.scopes, "scopes")




print(creds.expired, "expired")
print(creds.valid, "valid")

dic = {
    "refresh_token" : creds.refresh_token,
    "id_token" : creds.id_token,
    "token_uri" : creds.token_uri,
    "client_id" : creds.client_id,
    "client_secret" : creds.client_secret,
    "scopes" : creds.scopes
}

creds = Credentials.from_authorized_user_info(info = dic, scopes= ['https://www.googleapis.com/auth/admin.directory.resource.calendar',
                                                                    'https://www.googleapis.com/auth/calendar',
                                                                    'https://www.googleapis.com/auth/admin.directory.user',
                                                                    'https://www.googleapis.com/auth/admin.directory.group'])
creds.refresh(Request())


print(creds.token, "token")
print(creds.refresh_token, "refresh_token")
print(creds.id_token, "id_token")
print(creds.token_uri, "token_uri")
print(creds.client_id, "client_id")
print(creds.client_secret, "client_secret")
print(creds.scopes, "scopes")




print(creds.expired, "expired")
print(creds.valid, "valid")
