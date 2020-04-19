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

def getRoomsMailIds(capacity = None):
    
    service = create_directory_service()

    query = None 

    if capacity is not None:
        query = 'capacity='+capacity

    rooms = []

    resources = service.resources().calendars().list(customer='my_customer', query=query).execute()

    rooms  = resources['items']

    if len(resources['items']) == 0:
        resources = service.resources().calendars().list(customer='my_customer').execute()
        capacity = int(capacity)
        for resource in  resources['items']:
            if resource['capacity']  >= capacity and resource['capacity'] - capacity <= 10 :
                rooms.append(resource)

    rooms_list = []
    for room in rooms:
        rooms_list.append(room['resourceEmail'])

    return rooms_list

def getAvailable_rooms_for_meeting(service, rooms_list, start_time, end_time):
    available_rooms = []
    items = [
        { "id" : room} for room in rooms_list
    ]

    body = {
        "timeMax" : end_time,
        "timeMin" : start_time,
        "items" : items
    }
    
    result = service.freebusy().query(body = body).execute()

    for room in rooms_list:
        if len(result['calendars'][room]['busy']) == 0:
            available_rooms.append(room)
    
    return available_rooms
