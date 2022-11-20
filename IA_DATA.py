# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pandas as pd
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import os



es = Elasticsearch("http://localhost:9200")

pd.set_option('display.max_columns', None)
def init():

#dans un premier temps, il faut récupérer les données d'élastic.
    result = es.search(index='firewall', query={"match_all":{}}, size=1000)
   
    #Ici on crée les datasets
    data = result["hits"]["hits"]
    stored = []
    for i in data:
        donnee = i["_source"]
        stored.append(donnee)
       
    df = pd.DataFrame(stored)
   
    # #La c'est la version final
    dataclear = df[["timestamp",
                    "event",
                    "src_ip",
                    "dest_ip",
                    "length",
                    "tos",
                    "prec",
                    "ttl",
                    "id",
                    "proto",
                    "src_port",
                    "dst_port",
                    'icmp_type']]
   


    dataclear.to_csv('/home/elastic/file.csv')
    return dataclear
   
def oneHotKey(dataclear):
    i = 0
#     # On définit les tableau one hot
    tabOneHot = pd.DataFrame(columns=['src_ip_reseau', 'src_ip_externe',
                                      'dest_ip_reseau', 'dest_ip_externe',
                                      'src_port_22', 'src_port_80', 'src_port_inconnu',
                                      'dest_port_22', 'dest_port_80', 'dest_port_inconnu',
                                      'icmp_type',
                                      'proto_TCP', 'proto_ICMP'])
   
    tabNormal = pd.DataFrame(columns=['src_ip_reseau', 'src_ip_externe',
                                      'dest_ip_reseau', 'dest_ip_externe',
                                      'src_port_22', 'src_port_80', 'src_port_inconnu',
                                      'dest_port_22', 'dest_port_80', 'dest_port_inconnu',
                                      'icmp_type',
                                      'proto_TCP', 'proto_ICMP'])
   
   
    for index, row in dataclear.iterrows():
#         # On regarde pour chaque ligne
        rowToDict = row.to_dict()
       
        for key, value in rowToDict.items():
#         # On créer toutes les règles et c'est la que ça a de la valeur    
            if key == "src_ip":
                a = str(value)
                if "10.0.3." in a:
                    tabOneHot.loc[i, 'src_ip_reseau'] = 1
                    tabNormal.loc[i, 'src_ip_reseau'] = 1
       
                else:
                    tabOneHot.loc[i, 'src_ip_externe'] = 1
                    tabNormal.loc[i, 'src_ip_externe'] = 1
            if key =="dest_ip":
                a = str(value)
                if "10.0.3." in a:
                    tabOneHot.loc[i, "dest_ip_reseau"] = 1
                    tabNormal.loc[i, "dest_ip_reseau"] = 1
                else:
                    tabOneHot.loc[i, "dest_ip_externe"] = 1
                    tabNormal.loc[i, "dest_ip_externe"] = 1
            if key == "proto":
                a = str(value)
                if "TCP" in a:
                    tabOneHot.loc[i, "proto_TCP"] = 1
                    tabNormal.loc[i, "proto_TCP"] = 1
                if "ICMP" in a:
                    tabOneHot.loc[i, "proto_ICMP"] = 1
                    tabNormal.loc[i, "proto_ICMP"] = 1
            if key == "icmp_type":
                a = str(value)
                if a == "8":
                    tabNormal.loc[i, 'icmp_type'] = 1
                    tabOneHot.loc[i, 'icmp_type'] = 1
                else:
                    tabNormal.loc[i, 'icmp_type'] = 0
                    tabOneHot.loc[i, 'icmp_type'] = 0
                   
            if key == "dst_port":
                if pd.isna(value) == False:
                    valeur = int(value)
                    if valeur == 22:
                        tabOneHot.loc[i, "dest_port_22"] = 0
                        tabNormal.loc[i, "dest_port_22"] = 1
                    if valeur == 80:
                        tabOneHot.loc[i, "dest_port_80"] = 1
                        tabNormal.loc[i, "dest_port_80"] = 0
            else:
                pass
               
        i = i+1
       
        dfAnormal = tabOneHot.fillna(0)
        dfNormal = tabNormal.fillna(0)
    return dfAnormal, dfNormal
       

def train(x, y):
    mlp = MLPClassifier(random_state=1, max_iter=500).fit(x, y)
    return mlp

def travail(x_test, y_test, mlp):
    resultat = mlp.predict(x_test)
    score = mlp.score(x_test, y_test)
    return resultat, score
   

       
if __name__=='__main__':
    es = Elasticsearch("http://localhost:9200")
   
    dataclear = init()
    oneHotKey(dataclear)
    temp = [[1, 0], [0, 1]]
    y = []
    x_anormal = oneHotKey(dataclear)[0]
    x_normal = oneHotKey(dataclear)[1]
   
    print(x_normal)
   
    for i in range(len(x_anormal)):
        y.append([1, 0])
       
    for i in range(len(x_normal)):
        y.append([0, 1])
       
    y = pd.DataFrame(y)
    x = pd.concat([x_anormal, x_normal])
   
    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, random_state=1)
   
    mlp = train(x_train, y_train)
   
    score = travail(x_test, y_test, mlp)
   
    print(score[1])
