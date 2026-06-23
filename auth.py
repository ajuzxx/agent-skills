import os
from google_auth_oauthlib.flow import Flow

def login():
    """Starts the Google OAuth2 flow by generating the authorization URL."""
    client_secrets_path = os.environ.get('GOOGLE_CLIENT_SECRETS_PATH', 'client_secret.json')
    
    flow = Flow.from_client_secrets_file(
        client_secrets_path,
        scopes=[
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid'
        ],
        redirect_uri='http://localhost:8080/callback'
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    return authorization_url, state

