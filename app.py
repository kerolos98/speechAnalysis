
from itertools import count
from flask import Flask ,render_template,request,redirect
import speech_recognition as sr
import re
from collections import Counter
import json
import plotly
import plotly.express as px
import pandas as pd
app=Flask(__name__,static_url_path='/static')
@app.route("/", methods=["GET","POST"])
def index():
    transcript=""
    graphSON=""
    if request.method=="POST":
        print("FORM DATA RECEIVE")
        if "file" not in request.files:
            return redirect(request.url)
        file=request.files["file"]
        if file.filename=="":
            return redirect(request.url)
        if file:
    
            recognizer=sr.Recognizer()
            audio=sr.AudioFile(file)
            with audio as source:
                data =recognizer.record(source)
            text=recognizer.recognize_google(data ,key=None)
            transcript=text
            list_text=text.split(' ')
            nonPunct = re.compile('.*[A-Za-z0-9].*')  
            filtered = [w for w in list_text if nonPunct.match(w)]
            counts = Counter(filtered)
            topcounts=topwords(counts)
            words_pd=pd.DataFrame()
            words_pd["words"]=topcounts.keys()
            words_pd["counts"]=topcounts.values()
            fig = px.bar(words_pd, x='words', y='counts', barmode='group')
            graphSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
           


    return render_template("index.html",transcript=transcript,graphJSON=graphSON)
def topwords(counts):
    topcount=dict()
    for k,v in counts.items():
        if v  >> 1:
            if len(k)>=3:
               topcount[k]=v 
            
    return topcount        
if __name__=="__main__" :
    app.run(debug=True,threaded=True)  
