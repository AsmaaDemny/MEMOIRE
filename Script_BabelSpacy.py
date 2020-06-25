
# coding: utf-8

# ### import spacy
# import requests 
# import it_core_news_sm
# from bs4 import BeautifulSoup as bs
# import json
# 
# def ecrire_json(chemin , contenu):
#     w = open(chemin , "w", encoding="utf-8")
#     w.write(json.dumps(contenu , indent=2, ensure_ascii=False))
#     w.close()

# In[42]:

import os 

repertoire_json_resultatSpacy = "resultatSpacy"
if not os.path.exists(repertoire_json_resultatSpacy):
    os.makedirs(repertoire_json_resultatSpacy)
    
repertoire_json_resultatBabelfy = "resultatBabelfy"
if not os.path.exists(repertoire_json_resultatBabelfy):
    os.makedirs(repertoire_json_resultatBabelfy)
    
repertoire_json_resultatSpacy = "resultatSpacy"
if not os.path.exists(repertoire_json_resultatSpacy):
    os.makedirs(repertoire_json_resultatSpacy)


# In[43]:

URL ="https://babelfy.io/v1/disambiguate?"    #babelfly

lang = 'IT'

key  = ""

if not key:
    raise ValueError("No Babelfy key provided, please modify source code")



# In[48]:

import ast,re # module pour détecter le format de liste dans un string

with open("wikiItalien.xml", "r", encoding="utf-8") as file:
    content=file.read()
    textes= []
    for texte in re.finditer('<text .*>((\n|.|\t)*?)</text>', content):
        contenu=texte.group(1)
        match=re.search("==", contenu)
        if match!=None:
            contenu = texte.group(1)[0:match.start()]
        textes.append(contenu)
    par = {
    "text" : "",
    "lang" : "IT",
    "key" : key
}
    print(textes[6])# à enlever 
    nlp = it_core_news_sm.load()
    for cpt, i in enumerate(textes):
        dico={}
        dicBabel={}
        if len(i) < 6000:  # vérifier que le fichier n'est pas trop grand (valeur maximale à vérifier)
            par['text']= i
            r = requests.get(url = URL, params = par) 
            dicBabel = json.dumps(r.json())
            dicBabel = ast.literal_eval(dicBabel) # transformation de string en liste
            doc=nlp(i)
            nom = "DOC_%s" % (cpt+1)
            for ent in doc.ents:
                resultatSpacy=ent.start_char,ent.end_char,ent.label_
                entite=list(resultatSpacy)
                dico[ent.text] = entite
            ecrire_json("resultatSpacy/Spacy_%s.json" % nom,dico)
            ecrire_json("resultatBabelfy/Babel_%s.json" % nom,dicBabel)


# In[ ]:



