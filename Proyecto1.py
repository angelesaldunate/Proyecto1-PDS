import time
import operator
import sys
import glob
from numpy import *
import itertools
import datetime


print (datetime.datetime.now().time())
startTime = time.time()
CSV_DIRECTORY = "data/"
goals_hash = {}
if len(sys.argv) <2:
    goals_file = open("goals.txt", "r")
    goal_line = goals_file.readline()
    while goal_line != "":
        splitted_line = goal_line.strip().split(' ')
        required_file_name = splitted_line.pop(0)
        required_position = int(splitted_line.pop(0))
        required_order = splitted_line.pop(0)
        ponderator_vector = [int(i) for i in splitted_line]
        tuples = []
        csv_file = open(CSV_DIRECTORY + required_file_name, 'r')
        first_line = csv_file.readline()
        for csv_line in csv_file:
            attrs = csv_line.strip().split(';')
            identifier = attrs.pop(0)
            ponderation = 0
            for (attr, ponderator) in zip(attrs, ponderator_vector):
                if ponderator == 1:
                    ponderation += float(attr)
            tuples.append((identifier, ponderation))
        csv_file.close()
        goal_line = goals_file.readline()
        # COMPUTE THE RESULT
        result = ""
        tuples.sort(key=operator.itemgetter(1))
        if required_order == 'ASC':
            result = tuples[required_position-1]
        else:
            result = tuples[len(tuples) - required_position]

        goals_hash[goal_line] = result
    goals_file.close()
else:
    # PRE PROCESSING
    # ASKING GOALS FILES
    # SAVING IN GOALS HASH
    if sys.argv[1] == "-p":
        allFiles = glob.glob("data\*.csv")
        filesCases = {}
        fileIdes = {}
        for file in allFiles: # para cada archivo de data
            allCases = {} # donde guardo los casos
            csv_file = open(file,'r')
            first_line_len = len(csv_file.readline().strip().split(';'))-1 # veo el largo de las columnas
            get_bin = lambda x, n: format(x, 'b').zfill(n)#genera el binario como ponderador
            all_csv_file = list(csv_file.readlines())# guardo el archivo en una lista
            for i in range(first_line_len):
                    ides_file = []
                    numbers =[]
                    for csv_line in all_csv_file:
                        attrs = csv_line.strip().split(';')
                        identifier = attrs.pop(0)
                        numbers.append( float(attrs[i]))
                        ides_file.append(identifier)
                    allCases[i]=array(numbers) # guardo la lista generada con el key el indice de la columna
            # GUARDAR EN ALLCASES LAS COMBINACIONES
            a = list(allCases.keys())
            for i in range(2, len(list(a)) + 1):
                lista = list(itertools.combinations(a, i))
                for k in lista:
                    if len(k) < 3:
                        suma = zeros(len(ides_file))
                        for j in k:
                            suma += allCases[j]
                        allCases[k] = suma
                    else:
                        allCases[k] = allCases[k[:len(k) - 1]] + allCases[k[-1]]

            filesCases[file.replace('data\\','')]=allCases # dejo como key el nombre del archivo
            fileIdes[file.replace('data\\', '')] = ides_file
        print ('The pre procesin script took {0} second !'.format(time.time() - startTime))
        print (datetime.datetime.now().time())
        goals = input('Ingrese archivo: ')
        print (datetime.datetime.now().time())
        startTime = time.time()
        goals_file = open(goals,'r')
        for goal_line in goals_file:
            goal_no = goal_line
            goal_line = goal_line.strip().split()
            list_of_ones = []
            contador = 0
            for k in goal_line[3:]: # CONTAR DONDE HAY UNOS
                if goal_line[3:][contador]=='1':
                    list_of_ones.append(contador)
                contador+=1
            required_file_name = goal_line.pop(0)
            required_position = int(goal_line.pop(0))
            required_order = goal_line.pop(0)
            if len(list_of_ones)>1:
                final_array = filesCases[required_file_name][tuple(list_of_ones)]
            elif len(list_of_ones)==1:
                final_array = filesCases[required_file_name][list_of_ones[0]]
            else:
                final_array = zeros(len(fileIdes[required_file_name]))

            tuples = []
            for ide in range(len(fileIdes[required_file_name])):
                tuples.append((fileIdes[required_file_name][ide],final_array[ide]))
            result = ""
            tuples.sort(key=operator.itemgetter(1))

            if required_order == 'ASC':
                result = tuples[required_position - 1]
            else:
                result = tuples[len(tuples) - required_position]

            goals_hash[goal_no] = result
    else:
        print ("Error de comando")

#print goals_has
resultFile = open("results1.txt", 'w')
for result in goals_hash.values():
    resultFile.write(result[0] +"\n")
resultFile.close()

print ('The script took {0} second !'.format(time.time() - startTime))
print (datetime.datetime.now().time())


