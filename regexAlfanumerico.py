__author__ = 'elikary'

'''


 QUITO
==============
'''
import couchdb
import sys
import urllib2
import json
import re


from textblob import TextBlob




URL = 'localhost'
db_name = 'dbnewyork'


'''========couchdb'=========='''
server = couchdb.Server('http://'+URL+':5984/')  #('http://245.106.43.184:5984/') poner la url de su base de datos
try:
    print db_name
    db = server[db_name]
    print 'success'

except:
    sys.stderr.write("Error: DB not found. Closing...\n")
    sys.exit()



url = 'http://127.0.0.1:5984/dbnewyork/_design/view/_view/tweets'
req = urllib2.Request(url)
f = urllib2.urlopen(req)
d = json.loads(f.read())





f = open('datos.json','w')
f.write('[\n')



for x in d['rows']:
    a = x['value']['text']

    texto = re.sub('[^A-Za-z\s]+','', a)
    final = TextBlob(texto)
    print(final)

    
    polaridad = final.sentiment.polarity

    
    datos = {'texto' : texto,'label'   : ''}

    if polaridad == 0:
        datos['label']= 'neu'
    elif polaridad < 0:
        datos['label'] = 'neg'
    else:
        datos['label'] = 'pos'

    f.write("{texto :"+ datos[texto]+ "label :"+datos[label]+"} ,")

f.write(']')
   



