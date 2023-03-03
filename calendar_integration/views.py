from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os


# Set to True to enable OAuthlib's HTTPs verification when running locally.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CLIENT_SECRETS_FILE= 'credentials.json'

class GoogleCalendarInitView(View):
    """
        /rest/v1/calendar/init/ -> GoogleCalendarInitView()
        This view starts step 1 of the OAuth. Which will prompt user for
        his/her credentials
    """

    def get(self, request, *args, **kwargs):


        
        # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES, redirect_uri='http://localhost:8000/rest/v1/calendar/redirect') 
        #redirect_uri should be the same one configured in the API Console

        authorization_url, state = flow.authorization_url(
            # access the user's data when the user is not online(actively using app)
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true',
        )

        # Store the state so the callback can verify the auth server response.
        request.session['state'] = state

        # Redirect the user to the authorization URL.
        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    """
    /rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()
    This view will do two things
    1. Handle redirect request sent by google with code for token.
    """

    def get(self, request, *args, **kwargs):
        # Retrieve the state from the session
        state = request.session.pop('state', None)
        # Create a flow instance to get the tokens 
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES,state=state,redirect_uri='http://localhost:8000/rest/v1/calendar/redirect')
        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        # Store the credentials
        credentials = flow.credentials

        """
        2. Once got the access_token get list of events in users calendar.
        """

        # Create a Google Calendar API client
        service = build('calendar', 'v3', credentials=credentials)

        # Call the Calendar API
        events_result = service.events().list(calendarId='primary',
                                                maxResults=100).execute()
        events = events_result.get('items', [])
        # Return retrieved events 
        return JsonResponse({'status': 'success',
                                'message': 'Events have been fetched.',
                                'data': events
                                })
