#!/usr/bin/env python
# coding: utf-8

# In[470]:


from soup import Soup
import sys, os, git, io, re, datetime, pytz, json
sys.path.append(os.path.join(git.Repo(".", search_parent_directories=True).working_tree_dir, "plotly"))
from plotlyImports import *
from dataset import WriteFile
import pandas as pd

class LiveResults:
    def __init__(self, url):
        self.url = url
        
    def getResults(self):
        return Soup(self.url).getJsonFromResponse()
    
    def getPlotData(self):
        soup=Soup(self.url).makeSoup()

        plotDat=soup.find_all(name="script", attrs={"type":"text/javascript"})[-1]

        plotDat=plotDat.text

        plotDat=re.sub("\s*", "", plotDat)
        return plotDat 
    
    def getSpan(self):
        span={
            "doughnut" : re.search("DoughnutCharts", self.getPlotData()).span(),
            "pie" : re.search("PiCharts", self.getPlotData()).span()
        }
        return span

        
        
    
    def getPlotValues(self, dat):
    

        dat=re.sub(";?var", "", dat)

        xValues=re.search("xValues=", dat).span()
        yValues=re.search("yValues=", dat).span()
        barColors=re.search("barColors=", dat).span()


        values = {
            "x" : re.findall(r"[A-Za-z\(?)?]+", dat[xValues[1]:yValues[0]]),
            "y" : re.findall("\w+", dat[yValues[1]:barColors[0]]),
            "colors" : re.findall("\#\w+", dat[barColors[1]:].split(";")[0])
        }

        return values
    
    
    
    def piePlot(self, valuesDict):
    
        
        fig = go.Figure()
        fig.add_trace(go.Pie(values=valuesDict.get("y"),
                            labels=valuesDict.get("x"),
                            hole=0.3,
                            #rotation=90,
                        #direction="clockwise"
                            ))
        fig.update_traces(hoverinfo='label+percent', 
                          textinfo='value', 
                          #textfont_size=20,
                          marker=dict(colors=valuesDict.get("colors"), line=dict(color='#000000', width=2)))
        return fig
    
    def plotValues(self):
        span = self.getSpan()
        plotDat = self.getPlotData()
        donutValues = self.getPlotValues(plotDat[span['doughnut'][1]:span['pie'][0]])
        pieValues = self.getPlotValues(plotDat[span['pie'][1]:])
    
        fig = make_subplots(rows=1, cols=2, specs = [[{"type" : "domain"}, {"type" : "domain"}]],
                           subplot_titles=("Number of Seats", "Percentage Share of Polled Votes"),
                           vertical_spacing=0,
                           )
        fig.add_trace(go.Pie(self.piePlot(donutValues).data[0]),
                     row=1, col=1)
        fig.add_trace(go.Pie(self.piePlot(pieValues).data[0]),
                     row=1, col=2)
        fig.update_traces(textinfo="percent", row=1, col=2)
        fig.update_layout(title=f"<b>Results</b><br><sup>As at: {datetime.datetime.strftime(datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')), '%B %d %H:%M:%S')}</sup>",
                          legend={
            "orientation" : "h",
            #"yanchor" : "bottom",
            "x" : 0.095
        })
        fig.add_annotation( 
                   text=f"""<a href="{self.url}" target="_blank">Source: Election Commission of India</a>""",
                   showarrow=False,
                   xref="paper", yref="paper",
                   x=0.95,
                   y=-0.05
                  )
        return fig
    
    def getPCWiseResults(self):
        soup=Soup(self.url).makeSoup()

        dat=[x for x in soup.find_all("div", {"class" : "card-header"}) if "Constituency Wise Results" in x.text][0]

        pcValues=[{"pc" : x.text,
         "value" : x.attrs.get("value")} for x in dat.find_all("option") if not x.attrs.get("value") == ""]


        for pc in pcValues:
            label = pc.get('pc').lower().replace(' ', '')
            print("="*127)
            print("Parliamentary Constituency: ", label)
            url = f'{Soup(self.url).getBaseUrl()}/PcResultGenJune2024/Constituencywise{pc.get("value")}.htm'
            df=pd.read_html(url)[0]

            df.columns=[x.replace(" ", "_").lower() for x in df.columns]

            result=json.loads(df.iloc[:,1:].to_json(orient="records"))
            WriteFile(basePath="data", dataToWrite=result, fileName=f"tnPE24_{label}", extension="json").writeFileToDisk()
            print("="*127)
        
        return None
        

