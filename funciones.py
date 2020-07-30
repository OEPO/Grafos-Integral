import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from scipy.spatial import distance
import pandas as pd
import numpy as np

import os

from flask import request

def distancias():
    distancias = {}
    #crea dict tipo {Centro:{}}
    centros = open("static/data/centros.txt","r")
    for linea_centro in centros:
        linea_centro = linea_centro.replace(";",",").replace("\n","").split(",")
        nodo = linea_centro[1]
        distancias[nodo] = {}
    centros.close()
    #crea dict tipo {Centro:{PtoVenta:Distancia}}
    centros = open("static/data/centros.txt","r")
    for linea_centro in centros:
        linea_centro = linea_centro.replace(";",",").replace("\n","").split(",")
        nodo = linea_centro[1]
        axis = ( int(linea_centro[2]), int(linea_centro[3]) )
        #print(linea_centro)
        venta = open("static/data/ventas.txt","r")
        for linea_venta in venta:
            linea_venta = linea_venta.replace(";",",").replace("\n","").split(",")
            #print(linea_venta)
            v = linea_venta[1]
            axis_2 = ( int(linea_venta[2]), int(linea_venta[3]) )
            distancias[nodo][v] = round(distance.euclidean(axis,axis_2),5)
        venta.close()
    centros.close()
    return distancias


def centros_ventas():
    #centros.txt y ventas.txt para centros de distribucion y puntos de ventas.
    documento = open("static/data/file.txt","r")
    centros = open("static/data/centros.txt","w")
    ventas = open("static/data/ventas.txt","w")
    for linea in documento:
        if linea[0]== 'P':
                ventas.write(linea)
        if linea[0] == 'C':
                centros.write(linea)
    documento.close()
    centros.close()
    ventas.close()

def guardar():
    #Guarda el archivo principal.
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(APP_ROOT, "static/data")
    #print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        #print(file)
        filename = "file.txt"
        destination = "/".join([target,filename])
        #print(destination)
        file.save(destination)

def aux_graficar():
    plt.clf()
    plt.style.use('seaborn')
    #Procesamiento
    X = []
    Y = []
    documento = open("static/data/centros.txt","r")
    for linea in documento:
        linea = linea.replace(";",",").replace("\n","").split(",") #lista ["T","N","X","Y"]
        #print(linea)
        X.append(int(linea[2]))
        Y.append(int(linea[3]))
    documento.close()
    plt.scatter(X,Y,marker='o')

    X = []
    Y = []
    documento = open("static/data/ventas.txt","r")
    for linea in documento:
        linea = linea.replace(";",",").replace("\n","").split(",") #lista ["T","N","X","Y"]
        #print(linea)
        X.append(int(linea[2]))
        Y.append(int(linea[3]))
    documento.close()
    plt.scatter(X,Y,marker='x')

    #Grafica y guarda
    
    plt.title("Centros de Distribucion vs Puntos de Venta")
    plt.xlabel("Distancia X en Km")
    plt.ylabel("Distancia Y en Km")
    plt.tight_layout()
    plt.savefig("static/img/graph")










    

