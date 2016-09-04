import urllib
import lxml.html
from lxml import html
from lxml.html import clean
import re
import operator

#Fernando Robles Munoz

#Diccionario de paginas visitadas
expandidos = {}

#Lista de paginas a visitar
siguientes = []

#Diccionario de palabras y sus idf
palabras = {}

#Cuenta de todas las palabras
global total
total=0

#Palabras a ignorar
irrelev = []
with open('irrelev.txt') as f:
    irrelev = f.read().splitlines()

#Maximo de paginas a visitar
global pagsMax
pagsMax = 270

#Numero de pagina actual
global count
count=0


class Documento:

    def __init__( self , url):
        #Obtener pagina
        self.pagina = html.fromstring(urllib.urlopen(url).read())

        #Corregir links
        self.pagina.make_links_absolute(base_url=url,resolve_base_href=True)

        #Obtener links y guardarlos en una lista
        self.links= []
        for link in self.pagina.xpath("//a"):
            test=link.get("href")
            if test!=None and test[0:4]=='http':
                self.links.append(link.get("href"))

        #Obtener texto limpio (sin html, javascript)
        cls = clean.Cleaner(links=False,page_structure=False)
        self.pagina = cls.clean_html(self.pagina)
        self.texto = lxml.html.tostring(self.pagina,encoding='utf-8',pretty_print=True, method='text').split()

        #Contar palabras
        global total
        self.palabras= {}
        self.tam=0
        for pala in self.texto:
            pala = re.sub(r'\W+', '', pala) #Elminar caracteres no alfanumericos
            pala=pala.lower()
            if not pala=='' and pala not in irrelev:
                if not self.palabras.has_key(pala):
                    self.palabras[pala]=1.0
                else:
                    self.palabras[pala]+=1.0
                self.tam+=1
                total+=1
                if not palabras.has_key(pala):
                    palabras[pala]=1.0
                else:
                    palabras[pala]+=1.0        


        #Relacion de cada palabra con el total para este documento
        for i in self.palabras:
            self.palabras[i]=self.palabras[i]/self.tam

        #Guardar
        global count
        f=open("crawl"+str(count),'w')
        count+=1
        print>>f,url
        for item in sorted(self.palabras.iteritems(),key=operator.itemgetter(1),reverse=True):
            print>>f, item
        f.close()
        

#Inicia documentos y maneja listas y variables sobre que visitar
def crawler(url):
    global pagsMax
    print "Entro a ",url
    print count
    pag= Documento(url)
    expandidos[url]=0
    #Se llena la lista de siguientes hasta que las paginas visitadas lleguen a 0
    for k in pag.links:
        if not expandidos.has_key(k):
            if pagsMax>0:
                siguientes.insert(0,k)
                pagsMax-=1




#Se visitan paginas hasta que vacie la lista de siguientes
crawler("http://bulbapedia.bulbagarden.net/wiki/Hoenn_Route_101")
while len(siguientes)>0:
    crawler(siguientes.pop())


#Relacion de cada palabra con el total para TODOS los documentos
for i in palabras:
    palabras[i]=palabras[i]/total



#Guardar
f=open("crawlTotal",'w')
print>>f,"Total"
for item in sorted(palabras.iteritems(),key=operator.itemgetter(1),reverse=True):
    print>>f, item
f.close() 


