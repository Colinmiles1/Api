import tweepy
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Your Twitter API credentials
API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
CALLBACK_URI = 'http://localhost:8000/callback'

# Handle OAuth Callback
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = "Authentication successful! You can close this window."
        self.wfile.write(bytes(message, "utf8"))

        query = self.path.split('?')[-1]
        oauth_verifier = dict(q.split('=') for q in query.split('&')).get('oauth_verifier')
        if oauth_verifier:
            global oauth_verifier_token
            oauth_verifier_token = oauth_verifier

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET, CALLBACK_URI)
try:
    redirect_url = auth.get_authorization_url()
    webbrowser.open(redirect_url)

    # Start a simple server to handle the callback
    server = HTTPServer(('localhost', 8000), RequestHandler)
    server.handle_request()

    # Fetch the access token
    auth.get_access_token(oauth_verifier_token)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Verify authentication
    api.verify_credentials()
    print("Authentication OK")

    # Now you can interact with the Twitter API
    search_words = "#example"
    date_since = "2023-01-01"

    tweets = tweepy.Cursor(api.search_tweets,
                           q=search_words,
                           lang="en",
                           since=date_since).items(100)

    for tweet in tweets:
        print(f"Username: {tweet.user.screen_name}")
        print(f"Tweet: {tweet.text}")
        print(f"Created at: {tweet.created_at}")
        print('-' * 40)

except tweepy.TweepError as e:
    print(f"Error! Failed to get request token: {e}")
