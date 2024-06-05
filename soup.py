#!/usr/bin/env python
# coding: utf-8

# In[32]:


from response import Response
from bs4 import BeautifulSoup as bs
import re, json, os


# In[35]:


class Soup(Response):
    def makeSoup(self):
        soup = bs(self.assertResponse().content, "html.parser")
        return soup

    def getDocumentUrls(self):
        urls = self.makeSoup().find_all("a", href=True)
        urls = [{
            "title" : re.sub("\s*", "", x.text.title()),
            "url" : x.attrs.get("href")
        }for x in urls]
        return urls

    def getAllExtensions(self):
        extensions = [os.path.splitext(x.get("url"))[1] for x in self.getDocumentUrls()]
        extensions = list(set(extensions))
        return extensions
    
    


# In[ ]:




