#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, os, json
from urllib.parse import urlsplit, urlunsplit


# In[9]:


class Response:
    def __init__(self, url, **kwargs):
        self.url = url
        self.headers = kwargs.get("headers")
        self.cookies = kwargs.get("cookies")
        self.params = kwargs.get("params")

    def assertResponse(self):
        response = requests.get(url=self.url,
                               params=self.params,
                               headers=self.headers,
                               cookies=self.cookies)
        assert response.status_code == 200, response.raise_for_status()
        return response

    def getJsonFromResponse(self):
        responseDict = json.loads(self.assertResponse().content)
        return responseDict

    def getBaseUrl(self):
        split = urlsplit(self.url)
        return "://".join([split.scheme, split.netloc])


# In[ ]:




