import re
import sys
import json
import indicoio
from textblob import TextBlob
import threading
import csv
import math
import time
import re
import multiprocessing as mp

indicoio.config.api_key = '88d678d74b87403ea387023ef27d70cb'

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
def start_join_all( processes_list, queues_list):
    """Starts and joins all the threads in the list."""
    for process in processes_list:
        process.start()
    for i in range(len(processes_list)):
        processes_list[i].join()


def clasificar(lista,linea,diccionario,inicio,fin):
    for elemento in range (inicio, fin):
        texto=linea[elemento]['texto']
        k=0
        for item in lista:

            i = 0
            text = TextBlob(texto)
            try:
                textAux = text.translate(from_lang='es', to='en')
            except Exception as e:
                pass
            textoFinal = ""
            j = 0
            for j in range(j, len(textAux.words)):
                textoFinal = textoFinal + " " + textAux.words[j]
            a = indicoio.sentiment(textoFinal)

            if item in preprocess(texto) and a < 5:
                i += 1

                if i == 1 and a < 0.5:
                    
                    diccionario['text']=textoFinal
                    diccionario['label']='pos'
                    outfile.write(json.dumps(diccionario))
                    outfile.write(",\n")
                    print(k)


                k += 1
        if k == 0 and a > 0.5:
            
            diccionario['text'] = textoFinal
            diccionario['label'] = 'pos'
            outfile.write(json.dumps(diccionario))
            outfile.write(",\n")
            k += 1
            print(k)
        elif k == 0 and a < 0.5:
            
            diccionario['text'] = textoFinal
            diccionario['label'] = 'neg'
            outfile.write(json.dumps(diccionario))
            outfile.write(",\n")
            k += 1
            print(k)


lista = ["@Lenin", "Mashi","#YoVotoNO","#7VecesNO","#PorLaPatriaDilesNO","#TodoNO","#TodoSi","#TodoSI",
         "#7VecesS","#7VecesSi","#VotaTodoS","#Votar"]


datos = 'consultaQuito.txt'
with open(datos) as file:
    linea = json.loads(file.read())


outfile= open ('hilosQuito.txt','w')
diccionario={}

outfile.write("[\n")
   

NUMBER_THREADS = mp.cpu_count()
    
queues = []
processes = []
i=0
for index in range(NUMBER_THREADS):
    processes.append(mp.Process(target=clasificar, args=(
    lista, linea,
    diccionario, i,i+187)))
    i=i+187

start_join_all( processes, queues)



outfile.write("]\n")