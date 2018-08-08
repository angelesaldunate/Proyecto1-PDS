import time
import operator
import sys
import glob
import itertools
from numpy import *

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
        #print tuples

        if required_order == 'ASC':
            result = tuples[required_position-1]
        else:
            result = tuples[len(tuples) - required_position]

        goals_hash[goal_line] = result
    goals_file.close()
else:
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
                        numbers.append(float(attrs[i]))
                        ides_file.append(identifier)
                    allCases[i]=array(numbers) # guardo la lista generada con el key del binario
            # GUARDAR EN ALLCASES LAS COMBINACIONES
            size = len(allCases)
            a = list(allCases.keys())
            for i in range(2, size + 1):
                combs = list(itertools.combinations(a, i))
                for sub in combs:
                    vals = [allCases[x] for x in sub]
                    allCases[sub] = [sum(x) for x in zip(*vals)]
            #TODO: hacer las combinaciones y sumar
            filesCases[file.replace('data\\', '')] = allCases # dejo como key el nombre del archivo
            fileIdes[file.replace('data\\', '')] = ides_file
        print ('The pre procesin script took {0} second !'.format(time.time() - startTime))
        goals = input('Ingrese archivo: ')
        startTime = time.time()
        goals_file = open(goals,'r')
        for goal_line in goals_file:
            goal_no = goal_line
            goal_line = goal_line.strip().split()
            list_of_ones = [] # LISTAS DE APARICION DE UNOS
            contador = 0
            for k in goal_line[3:]: # CONTAR DONDE HAY UNOS
                if goal_line[3:][contador]=='1':
                    list_of_ones.append(contador)
                contador+=1
            required_file_name = goal_line.pop(0)
            required_position = int(goal_line.pop(0))
            required_order = goal_line.pop(0)
            final_array = zeros(len(fileIdes[required_file_name]))
            for number in list_of_ones:
                final_array+=filesCases[required_file_name][number]
            tuples = []
            for ide in range(len(fileIdes[required_file_name])):
                tuples.append((fileIdes[required_file_name][ide],final_array[ide]))
            result = ""
            tuples.sort(key=operator.itemgetter(1))
            # bubbleSort(tuples)
            # sorted(tuples, key=lambda x: x[1])
            # heap_sort(tuples)
            # print tuples

            if required_order == 'ASC':
                result = tuples[required_position - 1]
            else:
                result = tuples[len(tuples) - required_position]

            goals_hash[goal_no] = result



        #PRE PROCESSING
        #ASKING GOALS FILES
        #SAVING IN GOALS HASH
        print()
    else:
        print ("Error de comando")

#print goals_hash
resultFile = open("results1.txt", 'w')
for result in goals_hash.values():
    resultFile.write(result[0] +"\n")
resultFile.close()

print ('The script took {0} second !'.format(time.time() - startTime))
