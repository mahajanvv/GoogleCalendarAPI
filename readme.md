# Exploring Google Calendar API to connect with Amazon Lex chatbot as well as with REST APIs


## Brief background about the problem statement

### Current Implementation

To book a meeting room in an organization we use calendar App given by Gsuite. We manually look for meeting rooms that are near to us and check the availablity of participants and meeting rooms then we book a room. It will take almost 2-3 mins sometimes more than that. Can we reduce it? Can we make it more interactive?

### Answers to above questions

#### Yes, We can reduce this time as well as we can make it more iteractive.

1) You can use Google Calendar APIs to book rooms or shared resources in your organization.
2) You can use Amazon Lex chat bot which will hit your REST API endpoints with the required information to book rooms/resources.


## This tutorial is involved in TWO Stages.

### Stage 1 (Making Google Calendar APIs Up and running):
* [Setup needs to be done on Google Calendar API Side](https://github.com/mahajanvv/GoogleCalendarAPI/blob/master/setup_required_on_google_calendar_side.md)
* [Connecting to Google Calendar from Lambda](https://github.com/mahajanvv/GoogleCalendarAPI/blob/master/Connect_from_aws_lambda) (AWS)
* [Connecting to Google Calendar from Local Machine](https://github.com/mahajanvv/GoogleCalendarAPI/blob/master/Connect_from_local_machine) (Optional)

### Stage 2 (Integrating Google Calendar APIs with Amazon Lex Chatbot)
* Creating a Chatbot which will take inputs from user and calls Google Calendar API using Lambda Function and books a room




