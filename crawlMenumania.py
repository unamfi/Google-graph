import urllib
import lxml.html
import operator
import unicodedata
import random

#Fernando Robles Munoz



class Documento:

    def __init__( self , url):

        #Obtener pagina
        self.pagina = lxml.html.fromstring(urllib.urlopen(url).read())

        #Obtener algun dato
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

        identif=nombre+str(random.randint(1, 100000000))
        identif=identif.replace(' ','_')
        archivo=open("Restaurantes/"+identif+".txt",'w')
        print>>archivo, "'"+identif+"','nombre','"+nombre+"'"


        #Telefonos
        for nodo in self.pagina.xpath("//span[@class='tel']"):
            for k in nodo.text.split():
                print>>archivo, "'"+identif+"','telefono','"+k+"'"


	#Pagina web
        for nodo in self.pagina.xpath("//a[@title='web']"):
            print>>archivo, "'"+identif+"','web_page','"+nodo.get('href')+"'"
        
        
        #Estilos
        for nodo in self.pagina.xpath("//div[@class='estilos']/ul/li"):
            if(type(nodo.text) is type(u"nyan")):
                estilo=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            else:
                estilo=nodo.text
            print>>archivo, "'"+identif+"','estilo','"+estilo+"'"

        identifDir="DIR_"+nombre+str(random.randint(1, 1000))
        identifDir=identifDir.replace(' ','_')
        print>>archivo, "'"+identif+"','direccion','"+identifDir+"'"
        #Calle
        for nodo in self.pagina.xpath("//span[@class='street-address']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','calle','"+texto+"'"
        
        #Localidad
        for nodo in self.pagina.xpath("//span[@class='locality']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','colonia','"+texto+"'"

        #Region
        for nodo in self.pagina.xpath("//span[@class='region']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','region','"+texto+"'"

        #Cp
        for nodo in self.pagina.xpath("//span[@class='cp']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','c.p.','"+texto+"'"

        #Pais
        for nodo in self.pagina.xpath("//span[@class='country-name']"):
            texto=unicodedata.normalize('NFKD', nodo.text).encode('ascii','ignore')
            print>>archivo, "'"+identifDir+"','pais','"+texto+"'" 



        for h in lista:
            if(h[0]=='Precio' and len(h)>1):  #Precio
                print>>archivo, "'"+identif+"','precio_aprox','"+h[1]+"'"
            elif(h[0]=='Formas de Pago' and len(h)>1): #Formas de pago
                for m in h[1:]:
                    if(m is not None):
                        print>>archivo, "'"+identif+"','forma_pago','"+m+"'"
            elif(h[0]=='Horarios' and len(h)>1): #Horarios
                for m in h[1:]:
                    print>>archivo, "'"+identif+"','horario','"+m+"'"
            elif(h[0]=='Servicios Adicionales' and len(h)>1): #Servicios
                for m in h[1:]:
                    print>>archivo, "'"+identif+"','servicio','"+m+"'"

        archivo.close()




#Link de una lista cualquiera en menumania
url="http://menumania.seccionamarilla.com.mx/restaurantes/comida-japonesa/distrito-federal/1"

#Buscar toda la lista completa
pagina = lxml.html.fromstring(urllib.urlopen(url).read())
pagina.make_links_absolute(base_url=url,resolve_base_href=True) #Links absolutos
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


