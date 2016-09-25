#! /usr/bin/python
# coding: utf-8

"""
Florian Courgey
"""

# imports
import urllib, urllib2
from bs4 import BeautifulSoup
import re

# imports perso
import config

# constantes
url = 'https://www.hackthissite.org/missions/prog/11/index.php'

# chargement url
opener = urllib2.build_opener()
opener.addheaders.append(('Referer', url))
opener.addheaders.append(('Cookie', config.COOKIE))
print('Chargement de '+url)
html = opener.open(url).read().decode("utf-8")
print('html chargé')
soup = BeautifulSoup(html, 'html.parser')
texte = soup.get_text()
texte = texte.replace(u'\xa0', u' ')
# recherche nombres
texteNombres = re.search('Generated String: (.+)Shift', texte).group(1)
regex = "(\d{2,3})[$&\(\)\-\\\/#+*_%\"\.,:']"
nombres = []
for match in re.finditer(regex, texteNombres):
    n = int(match.group(1))
    if n>0:
        nombres.append(n)
# recherche shift
matchObj = re.search('Shift: (-?\d+)', texte)
shift = int(matchObj.group(1))

lettres = []
for n in nombres:
    lettre = str(unichr(n-shift))
    lettres.append(lettre)
    print(str(n)+" : "+lettre)

# on concatène tout et on envoie :)
solution = ''.join(lettres)
print("solution : "+solution)
data = urllib.urlencode({'solution':solution})
html = opener.open(url, data).read().decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')
texte = soup.get_text()
print(texte)

# html devrait contenir 'Good Job, PSEUDO, You have successfully completed this mission'
print('FIN')
