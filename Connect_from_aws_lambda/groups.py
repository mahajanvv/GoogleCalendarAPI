# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import datetime
import time
import os
import dateutil.parser
import logging

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

SCOPES = ['https://www.googleapis.com/auth/admin.directory.resource.calendar',
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.group']


dic = {
    "refresh_token" : '<Refresh Token will come from Front-end/Lambda Event>',
    "id_token" : None,
    "token_uri" : 'https://oauth2.googleapis.com/token',
    "client_id" : '<client id from creds.json>',
    "client_secret" : '<client secret from creds.json>',
    "scopes" : ['https://www.googleapis.com/auth/admin.directory.resource.calendar',
                'https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/admin.directory.user',
                'https://www.googleapis.com/auth/admin.directory.group']
}

creds = Credentials.from_authorized_user_info(info = dic, scopes= SCOPES)
creds.refresh(Request())

def create_directory_service():
    creds.refresh(Request())
    return build('admin', 'directory_v1', credentials=creds)

def getGroupMailIds(name_of_group = None):
    service = create_directory_service()

    if name_of_group is not None:
        groups = service.groups().list(customer= 'my_customer', query="name="+ name_of_group +"*").execute()
    else:
        groups = service.groups().list(customer= 'my_customer').execute()    
    
    email_list = []

    if 'groups' in groups and len(groups['groups']) > 0:
        for group in groups['groups']:
            email_list.append(group['email'])

    return email_list
