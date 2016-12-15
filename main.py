#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json

import webapp2

import requests

from bs4 import BeautifulSoup


class MainHandler(webapp2.RequestHandler):
    def get(self):
        vpn = self.request.GET['vpn']
        lookUpMVRD(self, vpn)

    def post(self):
        vpn = self.request.get("vpn")
        lookUpMVRD(self, vpn)


def lookUpMVRD(self, vpn):
    try:
        response = requests.get("http://www.lsmvaapvs.org/search.php?vpn=" + str(vpn))
        text = removeNonAscii(response.text)
        soup = BeautifulSoup("<html><head></head><body>" + text + "</body></html>", "html.parser")
        trs = soup.find_all('tr')
        mvrd = {}
        if (len(trs) == 0):
            mvrd["status"] = "not available"
        else:
            mvrd["status"] = "success"
            for tr in trs:
                soup = BeautifulSoup("<html><head></head><body>" + str(tr) + "</body></html>", "html.parser")
                keyValue = soup.find_all("td")
                mvrd[keyValue[0].getText()] = keyValue[1].getText()
        self.response.write(json.dumps(mvrd))
    except:
        mvrd = {}
        mvrd["status"] = "failed. retry"
        self.response.write(json.dumps(mvrd))


def removeNonAscii(s):
    return "".join(filter(lambda x: ord(x) < 128, s))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
