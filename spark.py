"""
Copyright 2016 Cisco Systems Inc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import json
import os
import tornado.gen

from tornado.httpclient import AsyncHTTPClient, HTTPRequest

class Result(object):
    def __init__(self, result):
        self.headers = result.headers
        self.errors = None
        self.code = result.code
        try:
            print("Result - Code:{0}, TrackingId:{1}".format(result.code, result.headers.get("Trackingid")))
        except Exception as ex:
            print("Result Exception - Code:{0}, No TrackingId.".format(result.code))
            print(result.headers)
        try:
            self.body = json.loads(result.body.decode("utf-8"))
        except ValueError as e:
            self.errors = e

class Spark(object):
    def __init__(self, token):
        self.token = token

    @tornado.gen.coroutine
    def get(self, url):
        headers={"Accept" : "application/json",
                "Content-Type":"application/json",
                "Authorization": "Bearer " + self.token}
        if os.environ.get('MY_USER_AGENT'):
            headers.update({"User-Agent":os.environ.get('MY_USER_AGENT')})
        print("Spark.simple_request User-Agent:{0}- GET {1}".format(headers.get('User-Agent'), url))
        request = HTTPRequest(url, method="GET", headers=headers, request_timeout=40)
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(request)
        raise tornado.gen.Return(Result(response))
