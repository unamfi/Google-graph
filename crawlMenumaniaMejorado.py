import urllib
import lxml.html
import operator
import unicodedata
import random
import os
import urllib2
from lxml import html
from lxml.html import clean
import re
import time
from bs4 import BeautifulSoup

#Fernando Robles Munoz

#Link de una lista cualquiera en menumania
url_inicial="http://menumania.seccionamarilla.com.mx/restaurantes/comida-japonesa/distrito-federal/1"

#Nombre de la carpeta de salida
carpeta="Restaurantes/"
try:
    os.makedirs(carpeta)
except(Exception):
    pass

#Clase que guarda los resultados de la primera pagina de google de una query
class Googlear:

    #Constructor:
    #Recibe query y nombreIdentificacion del restaurante
    #No regresa nada pero guarda los resultados de la query en la carpeta del restaurante
    def __init__( self , query,nameID):
        time.sleep(3)
        s = google(query,True)
        soup = BeautifulSoup(s)
        i=0
        #Limpiar y obtener cada liga de busqueda
        for c in soup.select("h3.r a[href]"):
            try:
                url = c.get("href").replace("/url?q=","")
                if(re.match('http.*',url)):
                    new=re.sub('&sa=U.*$', '', url)
                    i+=1
                    #Url obtenida, a guardar
                    self.guardar(new,nameID,i)
            except(urllib2.HTTPError) as e:
                continue #Descartar si hay errores

    def guardar(self, url,nameID,i):
        #Obtener pagina
        try:
            pagina = html.fromstring(google(url,False).read())
        except(urllib2.HTTPError,urllib2.URLError,lxml.etree.XMLSyntaxError,Exception) as e:
            return -1 #Descartar si hay errores

        try:
            #Obtener texto limpio (sin html, javascript)
            cls = clean.Cleaner(links=False,page_structure=False)
            pagina = cls.clean_html(pagina)
            texto = lxml.html.tostring(pagina,encoding='utf-8',pretty_print=True, method='text')
        except(urllib2.HTTPError,urllib2.URLError,lxml.etree.XMLSyntaxError,Exception) as e:
            return -1 #Descartar si hay errores

        #guardar en archivo
        archivo=open("Restaurantes/"+nameID+"/"+"result_"+str(i)+".txt",'w')
        print>>archivo,texto.lower()
        archivo.close()


#Abrir google como firefox, recibe una query y un booleano op
#Si op = True, la query se abre con google
#Si op = False, la query se trata como una url
def google(query,op):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/19.0')]
    if(op):
        return opener.open('http://www.google.com.mx/search?q=' + query)
    else:
        return opener.open(query)


#Clase que encuentra todos los datos en menumania de un restaurante dado por una url
class Documento:

    def __init__( self , url):

        #Obtener pagina
        self.pagina = lxml.html.fromstring(urllib.urlopen(url).read())

        #Obtener datos dentro de la clase=servicios_adicionales
        lista=[]
        cuenta=0
        tmp=[]
        for nodo in self.pagina.xpath("//div[@class='servicios_adicionales']"):
            for i in nodo:
                cuenta=cuenta+1
                if (cuenta==1):
                    tmp.append(i.text)
                else:
                    for y in i.getchildren():
                        if(i.get('class')=='tarjetas'):
                            tmp.append(y[0].get('title'))
                        else:
                            if(type(y.text) is type(u"nyan")):
                                texto=unicodedata.normalize('NFKD', y.text).encode('ascii','ignore')
                            else:
                                texto=y.text
                            tmp.append(texto)
                    lista.append(tmp)
                    tmp=[]
                    cuenta=0

                

	#Nombre
        nombre='error'
        for nodo in self.pagina.xpath("//h1[@class='informacion_nombre_sam fn org organization-name']"):
            if(type(nodo.text) is type(u"nyan")):
                nombre=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            else:
                nombre=nodo.text

        #identificador aleatorio para el restaurante
        identif=nombre+str(random.randint(1, 100000000))
        identif=identif.replace(' ','_')
        os.makedirs(carpeta+identif)
        #Abrir archivo nombreRestaurante(num aleatorio).txt
        archivo=open(carpeta+identif+"/"+identif+".txt",'w')
        print>>archivo, "'"+identif+"','nombre','"+nombre.lower()+"'"


        #Telefonos
        for nodo in self.pagina.xpath("//span[@class='tel']"):
            for k in nodo.text.split():
                print>>archivo, "'"+identif+"','telefono','"+re.sub("\(.+\)","",k.lower())+"'"


	    #Pagina web
        for nodo in self.pagina.xpath("//a[@title='web']"):
            print>>archivo, "'"+identif+"','web_page','"+nodo.get('href')+"'"
        
        
        #Estilos
        for nodo in self.pagina.xpath("//div[@class='estilos']/ul/li"):
            if(type(nodo.text) is type(u"nyan")):
                estilo=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            else:
                estilo=nodo.text
            print>>archivo, "'"+identif+"','estilo','"+estilo.lower()+"'"

        identifDir="DIR_"+nombre+str(random.randint(1, 1000))
        identifDir=identifDir.replace(' ','_')
        print>>archivo, "'"+identif+"','direccion','"+identifDir+"'"
        #Calle
        for nodo in self.pagina.xpath("//span[@class='street-address']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','calle','"+texto.lower()+"'"
        
        #Localidad
        for nodo in self.pagina.xpath("//span[@class='locality']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','colonia','"+texto.lower()+"'"

        #Region
        for nodo in self.pagina.xpath("//span[@class='region']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','region','"+texto.lower()+"'"

        #Cp
        for nodo in self.pagina.xpath("//span[@class='cp']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','c.p.','"+texto.lower().strip("c.p ,")+"'"

        #Pais
        for nodo in self.pagina.xpath("//span[@class='country-name']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','pais','"+texto.lower()+"'" 



        #Forma de pago
        for h in lista:
            if(h[0]=='Precio' and len(h)>1):  #Precio
                print>>archivo, "'"+identif+"','precio_aprox','"+h[1].lower()+"'"
            elif(h[0]=='Formas de Pago' and len(h)>1): #Formas de pago
                for m in h[1:]:
                    if(m is not None):
                        print>>archivo, "'"+identif+"','forma_pago','"+m.lower()+"'"
            elif(h[0]=='Horarios' and len(h)>1): #Horarios
                for m in h[1:]:
                    print>>archivo, "'"+identif+"','horario','"+m.lower()+"'"
            elif(h[0]=='Servicios Adicionales' and len(h)>1): #Servicios
                for m in h[1:]:
                    print>>archivo, "'"+identif+"','servicio','"+m.lower()+"'"

        archivo.close()

        #Googlear el restaurante
        newName=nombre.replace(' ','+')
        newName=newName.lower()
        Googlear("restaurante+"+newName+"+distrito+federal",identif)






#Buscar toda la lista completa
pagina = lxml.html.fromstring(urllib.urlopen(url_inicial).read())
pagina.make_links_absolute(base_url=url_inicial,resolve_base_href=True) #Links absolutos
busquedas=[]
for busqueda in pagina.xpath("//div[@class='paginacion']/ul/li[@class='pageNumber']/a"): #Sacar todas las ligas a paginas de la lista
    busquedas.append(busqueda.get('href'))

#Correr el programa para cada restaurante en la lista
for PPP in busquedas:
    tempP = lxml.html.fromstring(urllib.urlopen(PPP ).read())             
    links=[]
    for nodo in tempP.xpath("//ul[@class='listado']/li//div[@class='mas_info_listado']/a"): #Para cada liga obtener cada restaurante
        links.append(nodo.get('href'))

    for y in links:
        Documento(y)  #Llamar el programa para cada restaurante


