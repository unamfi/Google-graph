import os
import re
from os import listdir
from  nltk.classify import NaiveBayesClassifier
import collections


#Fernando Robles Munoz

#Instrucciones:
#Correr primero crawlMenumaniaMejorado.py (si se desea, puede cambiar la variable url_inicial 
#                                           al inicio del archivo y reemplazar con una busqueda de menumania)
#No se mostrara resultado en pantalla, pero generara archivos y carpetas dentro de la carpeta restaurantes
#Al finalizar, correr etiqueta.py
#Genera una salida en pantalla y archivos con los nombres de las etiquetas clasificadas

#Carpeta de restaurantes
raiz="Restaurantes/"


#Limpia cosas en el texto que los cleaners no (css mal hecho, tablas raras, etc)
def limpia(linea):
	limpio=[]

	if re.search("#.+{.+}",linea) is not None: #quita ccs mal hecho
		pass
	elif re.search("\.\.\.\.+ [0-9]{4}-[0-9]{4}",linea) is not None: #separa tablas por telefono
		matchs=re.split("([0-9]{4}-[0-9]{4})",linea.lower())
		for i in range(0,len(matchs)/2):
			limpio.append(matchs[i*2]+matchs[i*2+1])
	else:
		limpio.append(linea.lower())

	return limpio



restaurantes = [ f for f in listdir(raiz) ]  #Buscar todas las carpetas



lista=[]
limite=int(len(restaurantes)*9/10)  #90% para entrenar


for nodo in restaurantes[:limite]:
	relaciones=[]

	#abrir el archivo de datos del restaurante y obtener datos 2 y 3 de las triplas
	with open(raiz+nodo+"/"+nodo+".txt",'r') as archivo:
		for line in archivo:
			tmp=line.replace("'","").split(',') #Separar y quitar comillas
			if(tmp[1]=='telefono'):
				tmp[2]=re.sub("\(.+\)","",tmp[2].lower())
			relaciones.append([tmp[1],tmp[2]])

	textos=[ f for f in listdir(raiz+nodo) ] #Obtener archivos dentro de carpeta
	for texto in textos:
		if(texto != nodo+".txt"): #Abrir solo si es diferente al de los datos (abierto justo arriba)
			with open(raiz+nodo+"/"+texto,'r') as archivo:
				for line in archivo:
					for linea in limpia(line): #Limpiar linea
						for r in relaciones: 
							if r[1] in linea:  #Para cada linea limpia buscar relaciones
								lista.append(({'text':linea},r[0]))  #etiquetar

							
clasy= NaiveBayesClassifier.train(lista)  #entrenar

#Diccionario para seultados
result={}
for label in clasy.labels():
        result[label]=[]


#Recorrer archivos para prueba
for nodo in restaurantes[limite:]:
        textos=[ f for f in listdir(raiz+nodo) ]
        for texto in textos:
                if(texto != nodo+".txt"):
                        with open(raiz+nodo+"/"+texto,'r') as archivo:
                                for line in archivo:
                                	for linea in limpia(line):
                                		#Para cada linea limpia, clasificar y meter a resultados
	                            		clasif=clasy.classify({'text':linea})
	                            		result[clasif].append(linea)



#Etiquetas encontradas por el clasificador
print clasy.labels()


#Cuantos resultados encontrados por etiqueta
for e in result.keys():
        print e+":"+str(len(result[e]))

#Se crean archivos para resultados de cada etiqueta
for e in result.keys():
	archivo=open(e+".txt",'w')
	for linea in result[e]:
		print>>archivo,linea
		print>>archivo,"@\n@\n"
	archivo.close()
