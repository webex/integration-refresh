import os

class Settings(object):
	port = int(os.environ.get("MY_APP_PORT"))
	client_id = os.environ.get("MY_APP_CLIENT_ID")
	client_secret = os.environ.get("MY_APP_SECRET_ID")
	redirect_uri = os.environ.get("MY_APP_REDIRECT_URI")
	scopes = os.environ.get("MY_APP_SCOPES")
	loop_interval_sleep_seconds = int(os.environ.get("EVENT_LOOP_SLEEP_SECONDS"))
	max_token_age_days = int(os.environ.get("EVENT_LOOP_DAYS"))
