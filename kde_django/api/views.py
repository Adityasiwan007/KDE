from django.shortcuts import render
from django.conf import settings
import json
import requests
import urllib
import os


query_questions = {
    "1": "Peak number of covid cases in reference to number of attractions.",
    "2": "​Peak number of covid cases in reference to number of accomodations.",
    "3": "Date of crossing first 100 cases in reference to number of attractions.",
    "4": "​Date of crossing first 100 cases in reference to number of accomodations.",
    "5": "The number of attractions in reference to the number of accomodations.",
    "6": "​County with largest number of attraction per capita.",
    "7": "County with largest number of accomodations per capita.",
    "8": "Impact on GDP due to COVID as compared to highest GDP quarter. ",
    "9": "Difference in number of Covid cases between county with most accommodations to county with least accommodations.",
    "10": "Difference in number of Covid cases between county with most attractions to county with least attractions."
    }

query_headers = {
    "1": [ "County", "Peak Number of Covid Cases", "Number of Attractions"],
    "2": [ "County", "Peak Number of Covid Cases", "Number of Accomodations" ],
    "3": [ "County", "Date of Crossing 100 Cases", "Number of Attractions" ],
    "4": [ "County", "Date of Crossing 100 Cases", "Number of Accomodations" ],
    "5": [ "County", "Number of Attractions", "Number of Accomodations" ],
    "6": [ "County", "Number of Covid Cases", "Number of Attractions", "Attractions per 10,000 people"],
    "7": [ "County", "Number of Covid Cases", "Number of Accomodations", "Accomodations per 10,000 people"],
    "8": [ "Date", "GDP", "Number of Covid Cases" ],
    "9": [ "Number of Covid Cases in County with Most Attractions ", "Number of Covid Cases in County with Fewest Attractions", "Difference"  ],
    "10": [ "Number of Covid Cases in County with Most Accomodations", "Number of Covid Cases in County with Fewest Attractions", "Difference"  ],
    }

BASE_URL = 'http://69c899f17515.ngrok.io//repositories/COVID_AFFECTS_KDE_PROJECT_V3?query='

def index(request, query_id=None):
    html_template = 'home.html'
    context = {}
    
    query_id = request.GET.get("query_id", None)
    results = []
    print("Query id: ", query_id)
    question = ""
    if(query_id!=None):
        question, query_string = getQuery(query_id)
    #query_string = 'select%20*%20where%20%7B%20%20%09%3Fs%20%3Fp%20%3Fo%20.%20%7D%20limit%20100%20'
    
    
        url = BASE_URL + query_string
        headers = {'Accept': 'application/sparql-results+json'}
        r = requests.get(url, headers=headers)
        content = r.content.decode("utf8")
        #print("Content: ", content)
        js = json.loads(content)
        results = js["results"]['bindings']
        
        results = ProcessResults(results, query_id)
        context["current_question"] = question
    
    context["headers"] = query_headers.get(query_id, ["Col1", "Col2", "Col3"])
    context["questions"] = list(query_questions.values())
    context["query_id"] = query_id
    context["results"] = results
    #pprint(js)
    response = render(request, template_name = html_template, context=context)
    
    return response


def ProcessResults(results, query_id):
    
    processed = [] 
    for result in results:
        processed.append([x["value"].split("/")[-1] for x in result.values() ])
     
    
    for r in processed:
        if(query_id in ["1", "3"]):
            r[0], r[1] = r[1], r[0] 
            r[0], r[2] = r[2], r[0] 
            
        if(query_id == "5"):
            #r[1], r[2] = r[2], r[1] 
            #r.pop(-1)
            pass
        
        if(query_id in ["6"]):
            r[0], r[3] = r[3], r[0] 
            r[1], r[2] = r[2], r[1] 
            r[1], r[3] = r[3], r[1] 
            #r[0], r[2] = r[2], r[0] 
        
        if(query_id in ["7"]):
            r[1], r[2] = r[2], r[1] 
            
    return processed
    
    
    
def getQuery(query_id):
    query_id = str(query_id)
    question = query_questions.get(str(query_id), None)
    query_string = ""
    if(question!=None):
    
        query_path = os.path.join(settings.QUERY_FOLDER, query_id+".txt")
        query_string = " ".join(open(query_path, "r").readlines())
    
        query_string = urllib.parse.quote(query_string)

#    print("Question: ", question)
#    print("Query String: ", query_string)
#    print()
    
    return question, query_string

    
    