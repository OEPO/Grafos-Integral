import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from scipy.spatial import distance
import pandas as pd
import numpy as np
import math

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


def validar_entrega(puntosVenta, cantidades) :

    listaPtos = []

    listaCantidades = []

    puntosVenta.replace(" ","")
    cantidades.replace(" ","")

    listaPtos = puntosVenta.split(",")
    listaCantidades =  cantidades.split(",")

    if len(listaPtos) == len(listaCantidades) :
        
        for i in listaPtos : 

            if i.isdigit() == False :

                return False
    
        for j in listaCantidades :

            if j.isdigit() == False :

                return False
    
            else : 

                if int(j) > 1000 : 

                    return False
    
    else : 
        
        return False

    return True


    ############

def ruta_camion(centro,puntos,productos):
    productos = productos.split(",")
    # print(productos)
    puntos = puntos.split(",")
    puntos_aux = puntos.copy()

    cantidad_camiones = 0
    for i in productos:
        cantidad_camiones += int(i)
    cantidad_camiones = math.ceil(cantidad_camiones/1000)

    camiones = {}

    #camiones coor + producto
    for x in range(cantidad_camiones):
        a = {x:{"coord":centro,
        "producto":1000,
        "ruta":[]}}
        camiones.update(a)


    while len(puntos_aux) !=0:
        for a in camiones: #{0: {'coord': '66', 'producto': 1000, 'ruta': []}
            # print(puntos_aux)
            p = short(camiones[a]["coord"],puntos_aux)
            if p == "":
                break
            else:
                # print(puntos.index(p),p)
                if camiones[a]["producto"] >= int(productos[puntos.index(p)]):
                    # print(camiones[a]["producto"],int(productos[puntos.index(p)]))
                    camiones[a]["producto"] = camiones[a]["producto"] - int(productos[puntos.index(p)])
                    puntos_aux.remove(p)
                    camiones[a]["coord"] = p
                    camiones[a]["ruta"].append(p)
                # print("----")

        return camiones
        


def short(punto_uno,puntos): #"ID",Lista de puntos
    short = 1000000000000000
    punto = ""
    for p in puntos:
        #print(p,distancia(punto_uno,p))
        if distancia(punto_uno,p) < short:
            short = distancia(punto_uno,p)
            punto = p
    return punto



def coor(id):
    f = open("static/data/file.txt","r")
    for x in f:
        x = x.split(";")
        if id == x[1]:
            A = x[2].replace("\n","").split(",")
            for i in range(0, len(A)):
                A[i] = int(A[i])
            return A
    f.close()


def distancia(punto_uno,punto_dos):
    A = coor(punto_uno)
    B = coor(punto_dos)
    return round(distance.euclidean(A,B),5)


