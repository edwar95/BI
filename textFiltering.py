'''
permite filtrar tweets solo referentes a la consulta
'''


import re
import couchdb
import sys
import urllib2
import json
import indicoio
from textblob import TextBlob
indicoio.config.api_key = '88d678d74b87403ea387023ef27d70cb'
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 


def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens



URL = 'localhost'
db_name = 'consulta_total'

'''========couchdb'=========='''
server = couchdb.Server('http://' + URL + ':5984/')  # ('http://245.106.43.184:5984/') poner la url de su base de datos
try:
    print db_name
    db = server[db_name]
    print 'success'

except:
    sys.stderr.write("Error: DB not found. Closing...\n")
    sys.exit()

url = 'http://127.0.0.1:5984/consulta_total/_design/vistas/_view/Quito'
req = urllib2.Request(url)
f = urllib2.urlopen(req)
d = json.loads(f.read())

lista1=["#Si7vecesSi","@MashiRafael","@Lenin","consulta","Mashi","#ConsultaMaosa","#YoVotoNO","#7VecesNO","#PorLaPatriaDilesNO",
        "#NoBotesTuVoto ","#YoVotNO","#ObvioQueS","#JuntosPorElS","#YoVotoNO","#EcuadorSaleAVotar","#VotaNulo","#ATuFuturoDileSi"
        ,"#votonacional","#votaconconciencia","#votaconresponsabilidad","#VotaS","#TodoNO","#TodoSi","#TodoSI","#Todono","#TodoS"
        ,"#ElPuebloContigoRafael","#7VecesS","#7VecesSi","#VotaTodoS","#Votar","#ReferendumConsultaPopular2018febrero04","#TerceraVaECUADOR ",
        "#Vota7vecesS.","#TerceraVa ","#TerceraVaECUADOR","#votaciones2018SI","#votaciones"]
      


outfile= open ('consultaQuitol.txt','w')
diccionario={}

outfile.write("[\n")
for x in d['rows']:

    b = x['value']
    texto = re.sub('http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', '', b)
    if texto != "":
        i = 0
        for item in lista1:
           
            if item in preprocess(texto):                
                if i==0:
                    diccionario['texto']=texto
                    outfile.write(json.dumps(diccionario))
                    outfile.write(",\n")

                    i += 1
                    print(i)
outfile.write("]\n")