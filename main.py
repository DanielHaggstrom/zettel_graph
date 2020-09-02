import os
import json
import re
from itertools import repeat

# guardaremos un diccionario con el id de la nota como clave, y una lista de las notas a las que linkea como atributo.
resultado = {}
# ahoremos una lista de las notas para traducir sus id por sus posiciones
lista_notas = []

# buscamos toda la información útil en la carpeta json
path = "D:\\Coding\\PyCharm Workspace\\zettel_graph\\venv\\json"
for file in os.listdir(path):
    id = file[:-5]
    lista_notas.append(id)
    # cargamos cada json
    with open(path + "\\" + file, encoding="utf8") as f:
        nota = json.load(f)
    # solo nos interesan notas con contenido
    if "body" not in nota.keys():
        continue
    texto = nota["body"]
    links = []
    # extraemos links
    links = [texto[link.start() + 3:link.start() + 35] for link in re.finditer("\(:", texto)]
    if len(links) == 0:
        continue
    # los añadimos al diccionario
    resultado[id] = links # las notas empiezan su numeración en 1, no 0

# transformamos todo id en un número
def id_a_num(id, lista):
    return lista.index(id)
resultado = {id_a_num(key, lista_notas): list(map(id_a_num, value, repeat(lista_notas))) for (key, value) in resultado.items()}

# ahora vamos a crear la matriz de adjaciencia
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

# ahora, vamos a transformar la matriz de adjaciencia a formato de texto
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