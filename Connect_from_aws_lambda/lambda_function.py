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

def CreateUserService():
    creds.refresh(Request())
    return build('calendar', 'v3', credentials=creds)

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


def getattendeesArray(Resources_list = None, Organisers_list = None, Attendees_list = None):
    ls = []
    if Resources_list is not None:
        for resource in Resources_list:
            dic = {}
            dic["responseStatus"] = "accepted"
            dic["resource"] = True
            dic["email"] = resource
            ls.append(dic)
    if Organisers_list is not None:
        for organiser in Organisers_list:
            dic = {}
            dic["responseStatus"] = "needsAction"
            dic["email"] = organiser
            dic["organizer"] = True
            ls.append(dic)
    if Attendees_list is not None:
        for attendee in Attendees_list:
            dic = {}
            dic["responseStatus"] = "needsAction"
            dic["email"] = attendee
            ls.append(dic)
    return ls

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


def get_end_time(start_time, duration):
    hours, mins = map(int, duration.split(':'))
    return start_time + datetime.timedelta(hours= hours, minutes= mins)


def getAttendees_list(attendeeEmail = None):
    attendee_list = []
    if attendeeEmail is not None:
        ls = list(attendeeEmail.split(','))
        for mail in ls:
            if mail.endswith('@calbooker.in'):
                attendee_list.append(mail)
            else:
                group_mail_ids = getGroupMailIds(mail)
                attendee_list.extend(group_mail_ids)

    return attendee_list


def createNewEvent(intent_request = None, meeting_duration = None, meeting_date = None, meeting_time = None, organiser = None, capacity = None, attendeeEmail = None):

    rooms_list = getRoomsMailIds(capacity= capacity)

    service = CreateUserService()

    year, month, day = map(int, meeting_date.split('-'))

    hour, minute = map(int, meeting_time.split(':'))

    # start_time = datetime.datetime(year, month, day, hour, minute, 0).isoformat()+'+05:30'
    # end_time = datetime.datetime(year, month, day, hour+1, minute,0).isoformat()+'+05:30'
    start_time = datetime.datetime(year, month, day, hour, minute, 0)
    end_time = get_end_time(start_time, meeting_duration)

    # Converting datetime to Indian Time Strings
    start_time  = start_time.isoformat()+'+05:30'
    end_time = end_time.isoformat()+'+05:30'
    

    available_rooms = getAvailable_rooms_for_meeting(service, rooms_list, start_time, end_time)

    if len(available_rooms) == 0:
        return elicit_slot( intent_name =  intent_request['currentIntent']['name'],
                             slots = intent_request['currentIntent']['slots'], slot_to_elicit = 'time', message = 'No rooms available for the requested time, kindly choose some other time')
    

    attendees_list = getAttendees_list(attendeeEmail)

    if len(attendees_list) == 0:
        return elicit_slot( intent_name =  intent_request['currentIntent']['name'],
                             slots = intent_request['currentIntent']['slots'], slot_to_elicit = 'attendeeEmail', message = 'Please provide valid email addresses of attendees')
        # return {
        #     "dialogAction": {
        #         "type": "Close",
        #         "fulfillmentState": "Failed",
        #         "message": {
        #             "contentType": "PlainText",
        #             "content": ""
        #         }
        #     }
        # }
    
    resource_list = [available_rooms[0]]
    organiser_list = [organiser]
    # attendees_list = [attendeeEmail]

    # print(resource_list, organiser_list, attendees_list)

    # print(getattendeesArray(resource_list, organiser_list, attendees_list))

    body = {
        "organizer": {
            "self": False, 
            "email": organiser_list[0]
        },
        "summary": "Meeting Room Is Booked", # Title of the event.
        "attendees": getattendeesArray(resource_list, organiser_list, attendees_list),
        "start": { 
            "dateTime": start_time
        },
        "description": "What to do next 15 Days we discuss", # Description of the event. Optional.
        "reminders": { 
            "overrides": [
                {
                    "minutes": 30, 
                    "method": "email", 
                },
                {
                    "minutes": 15, 
                    "method": "sms", 
                },
                {
                    "minutes": 10, 
                    "method": "popup", 
                },
                {
                    "minutes": 5, 
                    "method": "popup", 
                }
            ],
            "useDefault": False
        },
        "end": {
            "dateTime": end_time
        }
    }

    response = service.events().insert(calendarId = 'primary', body = body, sendUpdates= 'all').execute()

    if 'status' in response:
        return close(fulfillment_state = "Fulfilled", message = "Your booking is "+response['status'])
        # return {
        #     "dialogAction": {
        #         "type": "Close",
        #         "fulfillmentState": "Fulfilled",
        #         "message": {
        #             "contentType": "PlainText",
        #             "content": "Your booking is "+response['status']
        #         }
        #     }
        # }
    else:
        return close(fulfillment_state = "Failed", message = "Your booking is Failed")
        # return {
        #     "dialogAction": {
        #         "type": "Close",
        #         "fulfillmentState": "Failed",
        #         "message": {
        #             "contentType": "PlainText",
        #             "content": "Your booking is Failed"
        #         }
        #     }
        # }


def elicit_slot(intent_name, slots, slot_to_elicit, message):
    return {
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message' : {
                'contentType': "PlainText",
                'content' : message
            }
        }
    }

def close(fulfillment_state, message):
    response = {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {
                "contentType": "PlainText",
                "content": message
            }
        }
    }

    return response

# --- Helper Functions ---


def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None



def book_room(intent_request):
    meeting_duration = try_ex(lambda: intent_request['currentIntent']['slots']['duration'])
    meeting_date = try_ex(lambda: intent_request['currentIntent']['slots']['date'])
    meeting_time = try_ex(lambda: intent_request['currentIntent']['slots']['time'])
    organiser = try_ex(lambda: intent_request['currentIntent']['slots']['organizer'])
    capacity =  try_ex(lambda: intent_request['currentIntent']['slots']['people'])
    attendeeEmail = try_ex(lambda: intent_request['currentIntent']['slots']['attendeeEmail'])

    # print(meeting_date, meeting_duration, meeting_time, organiser, capacity, attendeeEmail)

    response = createNewEvent(intent_request, meeting_duration, meeting_date, meeting_time, organiser, capacity, attendeeEmail)

    return response






# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    # logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'BookRoom':
        return book_room(intent_request)
    

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'Asia/Calcutta'
    time.tzset()
    # logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
