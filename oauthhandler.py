import json
import traceback
import urllib.parse

import tornado.gen
import tornado.web

from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from spark import Spark
from settings import Settings

class OauthHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get_tokens(self, code):
        url = "https://api.ciscospark.com/v1/access_token"
        payload = "client_id={0}&".format(Settings.client_id)
        payload += "client_secret={0}&".format(Settings.client_secret)
        payload += "grant_type=authorization_code&"
        payload += "code={0}&".format(code)
        payload += "redirect_uri={0}".format(Settings.redirect_uri)
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
            }
        access_token = None
        refresh_token = None
        try:
            request = HTTPRequest(url, method="POST", headers=headers, body=payload)
            http_client = AsyncHTTPClient()
            response = yield http_client.fetch(request)
            resp = json.loads(response.body.decode("utf-8"))
            print("OauthHandler.get_tokens /access_token Response: {0}".format(resp))
            access_token = resp["access_token"]
            refresh_token = resp["refresh_token"]
        except Exception as e:
            print("OauthHandler.get_tokens Exception:{0}".format(e))
            traceback.print_exc()
        raise tornado.gen.Return([access_token, refresh_token])


    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = "Error"
        try:
            if self.get_argument("code", None):
                code = self.get_argument("code")
                access_token, refresh_token = yield self.get_tokens(code)
                person = yield Spark(access_token).get("https://webexapis.com/v1/people/me")
                print("OauthHandler.get person:{0}".format(person.body))
                person_id = person.body.get("id")
                self.application.settings['token_helper'].update_user(person_id, access_token, refresh_token)
                response = "Access Granted"
            else:
                redirect_uri = 'https://webexapis.com/v1/authorize?client_id={0}&response_type=code&redirect_uri={1}&scope={2}'
                redirect_uri = redirect_uri.format(Settings.client_id, urllib.parse.quote_plus(Settings.redirect_uri), Settings.scopes)
                print("OauthHandler.get redirect_uri:{0}".format(redirect_uri))
                self.redirect(redirect_uri)
                return
        except Exception as e:
            response = "{0}".format(e)
            print("OauthHandler.get Exception:{0}".format(e))
            traceback.print_exc()
        self.write(response)
