import time
startTime = time.time()
goals = {}
openedFiles = {}
# abrir los goals y guardarlos usando el nombre de archivo como llave
goalsFiles=open("goals.txt")
for line in goalsFiles:
    positionNameFile = line.index(" ")# buscando el nombre del archivo que es hasta el primer espacio
    if line[0:positionNameFile] not in openedFiles:# si no se ha abierto el archivo
        goals[line[0:positionNameFile]] = [line[positionNameFile+1:-1]] #guardar todo el goal como string sin el salto de linea
        dataFile = open("data/"+line[0:positionNameFile])# abrir el archivo dentro de la carpeta data
        openedFiles[line[0:positionNameFile]] = []
        for lineData in dataFile: # guardar por linea el archivo sacandole el salto de linea
            openedFiles[line[0:positionNameFile]].append(lineData[:-1])# por eso no incluye el elemento -1
        dataFile.close()
    else:
        goals[line[0:positionNameFile]].append(line[positionNameFile + 1:]) # si ya se abrio solo agregar el goal y no volver a guardar el archivo
goalsFiles.close()

print(openedFiles["test1.csv"]) # asi quedaria guardado el archivo con data
print(goals) # asi quedaria guardado los goals

##Ahora hay que crear la lista segun los goals y los ponderadores para luego ordenarla



print ('The script took {0} second !'.format(time.time() - startTime))
