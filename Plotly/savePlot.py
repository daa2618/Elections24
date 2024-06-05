#!/usr/bin/env python
# coding: utf-8

# In[9]:


import os
import datetime
import plotly.express as px
import kaleido


# In[11]:

class SavePlot:
    def __init__(self, fig, fileName, imageType, recurring=False, scale=6, width=600, height=540):
        self.fig = fig
        self.fileName = fileName
        self.imageType = imageType
        self.recurring = recurring
        self.scale = scale
        self.width = width
        self.height = height
        
    
    def save(self):
        if not isinstance(self.scale, int) or not isinstance(self.width, int) or not isinstance(self.height, int):
            raise TypeError("All of scale, width, and height should be integers")

        basePath = "images"
        
        if not "." in self.imageType:
            imageType = f".{self.imageType}"
        if not os.path.exists(basePath):
            os.mkdir(basePath)
        if not self.recurring:
            checkFile = [x for x in os.listdir(basePath) if self.fileName in x]
            if checkFile:
                fn = checkFile[0]
                os.remove(os.path.join(basePath, fn))
            fileName = self.fileName + imageType
        else:
            fileName = self.fileName + datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M") + imageType
        filePath = os.path.join(basePath, fileName)

        self.fig.write_image(filePath, scale=self.scale, width=self.width, height=self.height, engine="kaleido")
        imageFilePath = os.path.abspath(filePath)
        print(f"The image was written at {os.path.normpath(f'{imageFilePath}{os.sep}{os.pardir}')}")
        return None

