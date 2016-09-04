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

class Googlear:

    def __init__( self , query,nameID):
        time.sleep(3)
        s = google(query,True)
        soup = BeautifulSoup(s)
        i=0
        for c in soup.select("h3.r a[href]"):
            try:
                url = c.get("href").replace("/url?q=","")
                if(re.match('http.*',url)):
                    new=re.sub('&sa=U.*$', '', url)
                    i+=1
                    #hacer algo un la url
            except(urllib2.HTTPError) as e:
                continue

def google(query,op):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/19.0')]
    if(op):
        return opener.open('http://www.google.com.mx/search?q=' + query)
    else:
        return opener.open(query)

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', unicodedata.normalize('NFKD', element).encode('ascii','ignore')):
        return False
    return True




