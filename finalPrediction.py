from textblob.classifiers import NaiveBayesClassifier
import json

def entrenarClasificador(train):
    with open(train, 'r')as fp:
        cl = NaiveBayesClassifier(fp, format="json")
        return cl
def testearClasificador(test, clasificador):
    with open(test,'r')as test:
	    print(clasificador.accuracy(test,format="json"))
def predecir(datos,cl):
    with open(datos) as file:
        linea = json.loads(file.read())

    pos=0
    neg=0
    for element in linea:
        a=cl.classify(element['text'])
        if a=='pos':
            pos+=1
        elif a=="neg":
            neg+=1

    b=pos+neg
    si=pos/float(b)
    no=neg/float(b)

    return(si,no)

if __name__ == "__main__":
    cuenca=entrenarClasificador("trainCuenca.json")
    testearClasificador("testCuenca.json",cuenca)
    resultadosCuenca=predecir("predictCuenca.json",cuenca)
    print("Cuenca",resultadosCuenca)
    

    guayaquil=entrenarClasificador("trainGuayaquil.json")
    testearClasificador("testGuayaquil.json",guayaquil)
    resultadosGuayaquil=predecir("predicGuayaquil.json",guayaquil)
    print("Guayaquil",resultadosGuayaquil)

    quito=entrenarClasificador("trainQuito.json")
    testearClasificador("testQuito.json",quito)
    resultadosQuito=predecir("predictQuito.json",quito)
    print("Quito",resultadosQuito)

