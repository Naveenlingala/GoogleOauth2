from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.response import Response
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import os

# Authorise HTTP servers
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
REDIRECT_URL = "https://googleoauth2--naveenlingala.repl.co/rest/v1/calendar/redirect/"

class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = Flow.from_client_secrets_file('./credentials.json', SCOPES)
        flow.redirect_uri = REDIRECT_URL

        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')

        # Save state in session for identification
        request.session['state'] = state

        return Response({'authorization_url': authorization_url})


class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        # Handle if permissions not granted
        error = request.GET.get('error')
        if error:
            return Response({'error': error }, status=403)

        # Handle CSRF attack by checking if redirect is from an authorized website
        state = request.session.get('state')
        if 'state' not in request.GET or request.GET['state'] != state:
            # Handle the case where the state parameter does not match the session or is invalid
            return Response({'error': "error_message"}, status=400)

        flow = Flow.from_client_secrets_file('./credentials.json', scopes=None, state=state)
        flow.redirect_uri = REDIRECT_URL

        # Extract code from request to generate access token
        code = request.GET.get('code')
        flow.fetch_token(code=code)

        credentials = flow.credentials
        credentials = self.credentials_to_dict(credentials)  # Can save them to request.session

        # Load credentials
        credentials = Credentials(**credentials)
        service = build('calendar', 'v3', credentials=credentials, static_discovery=False)

        # List all calendars
        calendar_list = service.calendarList().list().execute()

        # Getting 10 events associated with each calendar
        events_list = []
        for calendar in calendar_list['items']:
            cal_id = calendar['id']
            events = service.events().list(calendarId=cal_id, maxResults=10).execute()
            events_list.append({cal_id: events})

        if len(events_list) == 0:
            return Response({'Message': "No Calendar Found"}, status=200)

        return Response(events_list)

    def credentials_to_dict(self, credentials):
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
