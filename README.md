# Getting Started
First, you will need to create an app (create an integration) here:
https://developer.webex.com/my-apps

1. For most of the fields, like name, icon and description enter any values.

   a. For Redirect URI(s), enter: https://localhost:8000/oauth
      (or the url where you intend to deploy this code.  The app expects the url to end in ``/oauth``)

   b. For scopes, select only ``spark:all``
      (or the scopes you intend to use for your integration)
      If you do not select ``spark:all``, ``spark:people_read`` is required for this demo.

   c. Scroll to the bottom and click Add Integration.

# Running the Code
Requirements:
1. python 3.7.4 or higher
2. pip install tornado==4.5.2

Environment Variables:
Please review the ``sample_environ_vars.sh`` file and edit the values to include the integration client_id and secret from the getting started step.  If you used a different redirect_uri or scopes from the Getting Started step, then you'll need to edit those values here as well, or set them as environment variables via your preferred method.  For example, you can run the following in a unix terminal to set the environment variables in that local terminal window:
 ``>>>username$ source sample_environ_vars.sh``
 
Running the App from the terminal:
``>>>username$ python app.py --debug``


# About the App
Once the app is running...
1. Navigate to https://localhost:8000/oauth in your browser.
2. Sign into your integration.
   a. You will be redirected back to your local app server.
3. Wait.  Your app will check for old tokens every ``EVENT_LOOP_SLEEP_SECONDS`` (default 3600 seconds, or 1 hour).
   a. If the user's token is older than ``EVENT_LOOP_DAYS`` (default 1 day), app will attempt to refresh it.
   b. You can increase the frequency for testing purposes, but please note:
      Tokens refreshed more than once every 24 hours will often leave the values, including the expire time, unchanged.
      This essentially means that a token can only be truly refreshed at most once daily.
