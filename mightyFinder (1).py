#!/usr/bin/env python3

import urllib.request, urllib.response,urllib.error
import re
from bs4 import BeautifulSoup

def google(query):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/19.0')]
    return opener.open('http://www.google.com/search?q=' + query)

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


s = google("python+stackoverflow+BeautifulSoup")


soup = BeautifulSoup(s)
links = []
texts  =[]
for c in soup.select("h3.r a[href]"):
    try:
        url = c.get("href").replace("/url?q=","")
        print(url)
        pag = urllib.request.urlopen(url)
        sopa = BeautifulSoup(pag)
        text = soup.findAll(text=True)
        visible_texts = [x for x in filter(visible,text)]
        texts.append(" ".join(visible_texts))
    except(urllib.error.HTTPError) as e:
        print("error")

for t in texts:
    print(t)
    print("")
