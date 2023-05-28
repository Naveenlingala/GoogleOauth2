# Python on Replit

This is a template to get you started with Python on Replit. It's ready to go so you can just hit run and start coding!

## Running the repl

1. Setup a new secret environment variable (the lock icon) where the key is `SECRET_KEY` and the value is
   a randomly generated token of 32 bits of randomnese. To generate such a token type this into the shell and hit Enter:
```
python
import secrets
secrets.token_urlsafe(32)
```
2. Hit run!

## Google Cloud Setup

This guide will walk you through the setup process to enable Google Calendar API and obtain the necessary authorization credentials for integrating it with your Django REST API.

### Prerequisites
- Create a new project in the Google Cloud API and Services console.
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/20d1d93d-7397-4649-b341-b72e3feac59c)

### Step 1: Enable Google Calendar API
- In the Google Cloud API and Services console, navigate to your project and enable the Google Calendar API.
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/8bfd5962-77a5-49e6-9397-82dcb979854c)

### Step 2: Create Authorization Credentials
1. Go to the "Credentials" section in the Google Cloud API and Services console.
2. Click on "Create Credentials" and select "OAuth client ID".
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/fdfe8960-13a2-45cb-b086-10f952a7be65)
3. Choose "Web application" as the application type.
4. Set the authorized redirect URI to the URL of `rest/v1/calendar/redirect/`.
5. After saving the credentials, download the JSON file containing the client ID and client secret. Save this file as `credentials.json` in your project folder.


### Step 3: Set up OAuth Consent Screen
1. In the Google Cloud API and Services console, go to the "OAuth consent screen" section.
2. Configure the necessary details for the OAuth consent screen.
3. Add the scope `https://www.googleapis.com/auth/calendar.readonly` to the "Scopes" section.
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/2b83cd16-777b-4495-97bf-d27d12abef62)
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/366c8510-b304-40e0-b8fa-f88b55dbc66a)

**Note:** The scope `https://www.googleapis.com/auth/calendar.readonly` is considered a sensitive scope and may require verification or can be used while adding allowed users during testing mode.
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/1697e27f-e331-4f6a-a31d-7368b0a40874)

The obtained `credentials.json` file will be used in your Django REST API to authenticate and authorize access to the Google Calendar API.

## Working of Django REST API with Google Calendar Integration

This guide provides an overview of how the Django REST API integrates with Google Calendar to retrieve events from user calendars.

### Step 1: Authentication and Authorization
1. Users initiate the authentication process by accessing the `/rest/v1/calendar/init/` endpoint of the Django REST API.
2. The API returns an authorization URL generated using the Google Calendar API credentials.
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/f0bcabb9-bf5c-4a0a-87ba-5c938df721b9)
3. Users can got to the authorization URL, where they grant permission for the API to access their calendars.
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/c5d7321f-65ed-4e43-b1e9-158a34052a90)
4. Upon successful authorization, users are redirected to the `/rest/v1/calendar/redirect/` endpoint along with an authorization code and a state token would be saved in seesion for verification.

### Step 2: Accessing User Calendar Events
1. The `/rest/v1/calendar/redirect/` endpoint receives the authorization code.
2. The endpoint handles error secnarios such as permmsion denied by user and also checks for a matching state parameter to prevent CSRF attacks.
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/bb8cf41f-d52d-41cb-b1c0-9d4031c169db)
3. The endpoint verifies the code and if the verification is successful, the code is exchanged for an access token using the Google Calendar API credentials.
4. The access token is used to create the necessary credentials for accessing the Google Calendar API.
5. The API retrieves the list of user calendars using the `calendarList().list().execute()` method.
6. For each calendar, the API fetches the associated events using the `events().list(calendarId=cal_id, maxResults=10).execute()` method.
7. The events are stored in a list and returned as a response.
![image](https://github.com/Naveenlingala/GoogleOauth2/assets/60232407/0b710959-7edb-4c49-980a-03628a3f1e6c)

That's it! Users can now access their calendar events through the Django REST API, which securely integrates with the Google Calendar API using OAuth2 authentication and authorization.
