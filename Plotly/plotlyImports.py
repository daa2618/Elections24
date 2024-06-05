#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

pio.templates["myWatermark"] = go.layout.Template(layout_annotations=[
    dict(name="watermark",
        text="Dev Anbarasu",
        #textangle=-30,
        opacity=0.1,
        font=dict(color="white", size=25),
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False)
])
pio.templates.default = "plotly_dark+myWatermark"



