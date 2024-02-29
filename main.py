import os
import json
import re
from itertools import repeat

# guardaremos un diccionario con el id de la nota como clave, y una lista de las notas a las que linkea como atributo.
resultado = {}

# adquirimos todas las notas en un diccionario id: [tipo, contenido json]
path = "path to json data"
todas = {}
for file in os.listdir(path):
    id = file[:-5]
    # cargamos cada json
    with open(path + "\\" + file, encoding="utf8") as f:
        nota = json.load(f)
    todas[id] = [nota["type_"], nota] # si aquí no salta error, todas las notas tienen campo type_

# ahoremos una lista de las notas para traducir sus id por sus posiciones
lista_notas = []

# buscamos los links en las notas de tipo 1, e ignoramos links a notas de otros tipos
path = "D:\\Coding\\PyCharm Workspace\\zettel_graph\\venv\\json"
for nota in todas.keys():
    tipo = todas[nota][0]
    contenido = todas[nota][1]
    # solo nos interesan notas de tipo 1
    if tipo != 1: # parece ser la diferencia entre notas normales y cuadernos, etc.
        continue
    lista_notas.append(nota)
    if "body" not in contenido:
        texto = ""
    else:
        texto = contenido["body"]
    links = []
    # extraemos links
    links = [texto[link.start() + 3:link.start() + 35] for link in re.finditer("\(:", texto)]
    if len(links) == 0:
        continue
    # comprobamos el tipo
    lista_links_correctos = []
    for link in links:
        if todas[link][0] != 1:
            continue
        lista_links_correctos.append(link)
    resultado[nota] = lista_links_correctos

# transformamos todo id en un número
def id_a_num(id, lista):
    # debemos comprobar si el id se encuentra en la lista, si eso ocurre
    return lista.index(id)
resultado = {id_a_num(key, lista_notas): list(map(id_a_num, value, repeat(lista_notas))) for (key, value) in resultado.items()}

# ahora vamos a crear la matriz de adyaciencia
matrix = [[] for nota in lista_notas]
for row in range(len(lista_notas)):
    # fila a fila
    if row not in resultado:
        # toda la línea es 0
        matrix[row].extend([0] * len(lista_notas))
        continue
    for col in range(len(lista_notas)):
        if col in resultado[row]:
            # este elemento es 1
            matrix[row].append(1)
        else:
            # este elemento es 0
            matrix[row].append(0)

# ahora, vamos a transformar la matriz de adyaciencia a formato de texto
def list_to_string(lista):
    s = ""
    for i in range(len(lista)):
        if i < len(lista) - 1:
            s += str(lista[i]) + ", "
        else:
            s += str(lista[i])
    return s

text = ""
for row in matrix:
    text += list_to_string(row)
    text += "\n"

# y lo escribimos
f = open("final.txt", "a")
f.write(text)
f.close()
