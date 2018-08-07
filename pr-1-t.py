import time
import operator
import sys
import glob
import numpy

def heapify(arr, n, i):
    l = 2 * i + 1
    r = 2 * i + 2
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
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def bubble_sort(arr):
    l = len(arr)
    for i in range(0, 1):
        for j in range(0, l - i - 1):
            if arr[j][1] > arr[j + 1][1]:
                tempo = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = tempo
    return arr


def bubbleSort(arr):
    for i in range(len(arr) - 1, 0, -1):
        for k in range(i):
            if arr[k][1] > arr[k + 1][1]:
                aux = arr[k]
                arr[k] = arr[k + 1]
                arr[k + 1] = aux

class Row:
    def __init__(self,identifier,attrs):
        self.identifier=identifier
        self.attrs=attrs

    def get_ponderation(self,ponderator_vector):
        return numpy.dot(ponderator_vector,self.attrs)

class File:
    def __init__(self,file_name,rows_list):
        self.file_name=file_name
        self.rows_list=rows_list
        self.sorted_by_ponderator_vector={}

    def set_sorted_by_ponderator_vector(self,sorted_by_ponderator_vector):
        self.sorted_by_ponderator_vector=sorted_by_ponderator_vector
startTime = time.time()
CSV_DIRECTORY = "data/"
goals_hash = {}
ponderator_vectors=[]
for i in range(3**10):
    ponderator_vector=[int(pond) for pond in list("{0:b}".format(i).zfill(10))]
    ponderator_vectors.append(ponderator_vector)

total_time_seconds=10*60
allFiles = glob.glob("data/*.csv")
files_count=len(allFiles)
max_seconds_for_file=total_time_seconds/files_count
filesCases = {}
for file in allFiles:  # para cada archivo de data
    allCases = {}  # donde guardo los casos
    file_start_time=time.time()
    file_name=file.split("/")[-1]
    csv_file = open(file, 'r')
    first_line_len = len(csv_file.readline().strip().split(';')) - 1  # veo el largo de las columnas
    file_rows=[]
    all_csv_file = list(csv_file.readlines())  # guardo el archivo en una lista
    for csv_line in all_csv_file:
        attrs = csv_line.strip().split(';')
        identifier = attrs.pop(0)
        attrs=[float(attr) for attr in attrs]
        row=Row(identifier,attrs)
        file_rows.append(row)

    file_object=File(file_name,file_rows)
    sorted_by_ponderator={}
    for ponderator_vector in ponderator_vectors:
        sorted_rows=sorted(file_rows,key=lambda x:x.get_ponderation(ponderator_vector))
        sorted_by_ponderator[tuple(ponderator_vector)]=sorted_rows
        current_time=time.time()
        delta_seconds=int(current_time-file_start_time)
        if(delta_seconds>=max_seconds_for_file):
            file_object.set_sorted_by_ponderator_vector(sorted_by_ponderator)
            break
    filesCases[file.replace('data\\', '')] = allCases  # dejo como key el nombre del archivo
# print (filesCases[list(filesCases.keys())[-1]])

# PRE PROCESSING
# ASKING GOALS FILES
# SAVING IN GOALS HASH

# print goals_hash
resultFile = open("results1.txt", 'w')
for result in goals_hash.values():
    resultFile.write(result[0] + ": " + str(result[1]) + "\n")
resultFile.close()

print ('The script took {0} second !'.format(time.time() - startTime))
