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
url = 'https://www.hackthissite.org/missions/prog/1/'
dico_nom_fichier = 'wordlist.txt'

# chargement dico
dico_fichier = open(dico_nom_fichier, 'r')
dico = dico_fichier.readlines()
for i, mot in enumerate(dico):
    dico[i] = mot.strip(' \t\n\r')
    print(dico[i])

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
regex = " (\w{5,8}) \n"
motsOrdonnes = []
motsDesordonnes = []
for match in re.finditer(regex, texte):
    motsDesordonnes.append(match.group(1))

# à ce stade, on a les mots désordonnés et le dico

# pour chaque mot, on regarde pour chaque mot du dico ça correspond
for motDesordonne in motsDesordonnes:
    for m in dico:
        if len(m) != len(motDesordonne):
            continue
        mot_ok = True
        for lettre in motDesordonne:
            if motDesordonne.count(lettre) != m.count(lettre):
                mot_ok = False
                break;
        if mot_ok:
            motsOrdonnes.append(m)
            break

# on concatène tout et on envoie :)
solution = ','.join(motsOrdonnes)
data = urllib.urlencode({'solution':solution})
html = opener.open(url, data).read().decode("utf-8")
print(html)

# html devrait contenir 'Good Job, PSEUDO, You have successfully completed this mission'
print('FIN')
