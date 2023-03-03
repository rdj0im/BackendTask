# Google Calendar Integration (Django REST API, OAuth2)

This Django App fetches the events from the user's Google Calendar. It uses OAuth2 for authentication, after which, the google calendar API is used to read the events and display it in the json format.

## Google API Setup
Go to the [Google Cloud Console](https://console.cloud.google.com/) and sign in with your Google account. Use this [Python Quickstart](https://developers.google.com/calendar/api/quickstart/python) as a refernce and enable the Calendar API and get the credentials to be used in place of credentials.json.

While generating credentials:
1. Select "Web application" as the application type, and enter a name for your application.
2. In the "Authorized JavaScript Origins" and "Authorized Redirect URIs" fields, enter the URLs of your application that will be handling the OAuth flow.
In this project, "http://localhost:8000" is set as the "Authorized JavaScript Origins" and "http://localhost:8000/rest/v1/calendar/redirect" is set as the "Authorized Redirect URIs" field for local testing.
3. You can now use the generated client ID and client secret to authenticate with the Google Calendar API in your application.

## Endpoints
There are two Endpoints setup:
1. `/rest/v1/calendar/init/` -> `GoogleCalendarInitView()` - This view starts step 1 of the OAuth. Which will prompt user for his/her credentials.
2. `/rest/v1/calendar/redirect/` -> `GoogleCalendarRedirectView()`
This view will do two things:
    1. Handles redirect request sent by google with code for token.
    2. On recieving the access_token, gets list of events in users calendar.

## Development Setup

1. Install Python and Django on your machine
2. Clone or download the project from the repository
3. Navigate to the project directory in the command line
4. Run the command `pip install -r requirements.txt` to install the project dependencies
5. Run the command `python manage.py makemigrations` to create the database tables
6. Run the command `python manage.py migrate` to apply the migrations to the database
7. Run the command `python manage.py runserver` to start the development server
8. Visit "[http://localhost:8000/rest/v1/calendar/init](http://localhost:8000/rest/v1/calendar/init)" in your web browser to start the OAuth process.
9. This initiates the OAuth flow and takes you to a google authorization page where you either login or choose an account and grant the calendar permission.
10. Once permission is granted, the site will redirect you to the  redirect_uri specified (which is http://localhost:8000/rest/v1/calendar/redirect in this setup).
11. This view retrieves the events using the Calendar API.

## Resources

| Name | Sources |
| ------ | ------ |
| Google Identity: Using OAuth 2.0 for Web Server Applications | [/identity/protocols/oauth2/web-server][PlDb] |
| Google Calendar API | [/calendar/api/v3/referenc][PlGh] |
| Google Account Credentials| [/identity/protocols/oauth2/web-server#exchange-authorization-code][PlIa] |
| Calendar API Python Quickstart | [https://developers.google.com/calendar/api/quickstart/python][PlGp]|


[PlDb]: <https://developers.google.com/identity/protocols/oauth2/web-server>
[PlGh]: <https://developers.google.com/calendar/api/v3/reference>
[PlIa]: <https://developers.google.com/identity/protocols/oauth2/web-server#exchange-authorization-codee>
[PlGp]: <https://developers.google.com/calendar/api/quickstart/python>