import time
import operator
import sys
import glob
from numpy import *


def heapify(arr, n, i):
    l = 2*i + 1
    r = 2*i + 2
    largest = i
    if l < n and arr[i][1] < arr[l][1]:
        largest = l
    if r < n and arr[largest][1] < arr[r][1]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def bubble_sort(arr):
    l = len(arr)
    for i in range(0,1):
        for j in range (0, l-i-1):
            if arr[j][1] > arr[j+1][1]:
                tempo = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = tempo
    return arr

def bubbleSort(arr):
    for i in range(len(arr)-1,0,-1):
        for k in range(i):
            if arr[k][1]>arr[k+1][1]:
                aux = arr[k]
                arr[k] = arr[k+1]
                arr[k+1] = aux


startTime = time.time()
CSV_DIRECTORY = "data/"
goals_hash = {}
if len(sys.argv) >2:
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
        #bubbleSort(tuples)
        #sorted(tuples, key=lambda x: x[1])
        #heap_sort(tuples)
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
        for file in allFiles: # para cada archivo de data
            allCases = {} # donde guardo los casos
            csv_file = open(file,'r')
            first_line_len = len(csv_file.readline().strip().split(';'))-1 # veo el largo de las columnas
            get_bin = lambda x, n: format(x, 'b').zfill(n)#genera el binario como ponderador
            all_csv_file = list(csv_file.readlines())# guardo el archivo en una lista


            for i in range(first_line_len): # genero 2 elevado a las columnas
                    numbers =[]
                    ides = []
                    for csv_line in all_csv_file:
                        attrs = csv_line.strip().split(';')
                        identifier = attrs.pop(0)
                        numbers.append( float(attrs[i]))
                        ides.append(identifier)
                    allCases[i]=[identifier,array(numbers)] # guardo la lista generada con el key del binario

            filesCases[file.replace('data\\','')]=allCases # dejo como key el nombre del archivo

        goals = input('Ingrese archivo')
        goals_file = open(goals,'r')
        for goal_line in goals_file:
            goal_no = goal_line
            goal_line = goal_line.strip().split()
            list_of_ones = []
            contador = 0
            for k in goal_line[3:]:
                if goal_line[3:][contador]=='1':
                    list_of_ones.append(contador)
                contador+=1
            required_file_name = goal_line.pop(0)
            required_position = int(goal_line.pop(0))
            required_order = goal_line.pop(0)
            final_array = zeros(len(filesCases[required_file_name][0][1]))
            for number in list_of_ones:
                final_array+=filesCases[required_file_name][number][1]
            tuples = []
            for ide in range(len(filesCases[required_file_name][0][1])):
                tuples.append((filesCases[required_file_name][0][0],final_array[ide]))
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
    resultFile.write(result[0] + ": " + str(result[1]) + "\n")
resultFile.close()

print ('The script took {0} second !'.format(time.time() - startTime))
