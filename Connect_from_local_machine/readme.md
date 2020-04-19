### Let's invoke GoogleCalendarAPI from local machine and fetch umcoming 10 events for a particular User

### Prerequisites:
* Python 2.6 or greater( Preferred 2.7)
* The pip package management tool
* A Google account with Google Calendar enabled

### Install the Google Client Library
Run the following command to install the library using pip:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Let's write code to fetch upcoming 10 events for logged in user
[Code is here](https://github.com/mahajanvv/GoogleCalendarAPI/blob/master/Connect_from_local_machine/fetch_upcoming_ten_events.py)

### Let's run this file on local machine 
Run using the following command:
```
python fetch_upcoming_ten_events.py
```


* The code will attempt to open a new window or tab in your default browser. If this fails copy the URL from the console and manually open it in your browser.

* If you are not already logged into your Google account, you will be prompted to log in. If you are logged into multiple Google accounts, you will be asked to select one account to use for the authorization.

* Click the Accept button.

The code will proceed automatically, and you may close the window/tab.
