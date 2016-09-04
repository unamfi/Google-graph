import urllib2
import urllib
import lxml.html
from lxml import html
from lxml.html import clean
import re
import unicodedata
import time
from bs4 import BeautifulSoup

class Googlear:

    def __init__( self , query,nameID):
        os.makedirs("Restaurantes/"+nameID)
        s = google(query,True)
        soup = BeautifulSoup(s)
        i=0
        for c in soup.select("h3.r a[href]"):
            try:
                url = c.get("href").replace("/url?q=","")
                if(re.match('http.*',url)):
                    new=re.sub('&sa=U.*$', '', url)
                    i+=1
                    self.guardar(new,nameID,i)
            except(urllib2.HTTPError) as e:
                continue

    def guardar(self, url,nameID,i):
        #Obtener pagina
        pagina = html.fromstring(google(url,False).read())

        #Obtener texto limpio (sin html, javascript)
        cls = clean.Cleaner(links=False,page_structure=False)
        pagina = cls.clean_html(pagina)
        texto = lxml.html.tostring(pagina,encoding='utf-8',pretty_print=True, method='text')

        #guardar
        archivo=open("Restaurantes/"+nameID+"_result_"+i+".txt",'w')
        print>>archivo,texto
        archivo.close()


def google(query,op):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/19.0')]
    if(op):
        return opener.open('http://www.google.com/search?q=' + query)
    else:
        return opener.open(query)

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', unicodedata.normalize('NFKD', element).encode('ascii','ignore')):
        return False
    return True





