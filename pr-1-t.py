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
    def get_identifier(self):
        return self.identifier

class File:
    def __init__(self,file_name,rows_list):
        self.file_name=file_name
        self.rows_list=rows_list
        self.sorted_by_ponderator_vector={}


    def set_sorted_by_ponderator_vector(self,sorted_by_ponderator_vector):
        self.sorted_by_ponderator_vector=sorted_by_ponderator_vector

    def get_sorted_by_ponderator_vector(self):
        return self.sorted_by_ponderator_vector

    def set_key_in_sorted_by_ponderator_vector(self,key,value):
        self.sorted_by_ponderator_vector[key]=value
    def get_rows(self):
        return self.rows_list


def get_rows_from_csv(csv_file_name):
    csv_file = open(CSV_DIRECTORY+"/"+csv_file_name, 'r')
    attrs_count = len(csv_file.readline().strip().split(';')) - 1  # veo el largo de las columnas
    file_rows = []
    csv_file.readline() #remove first line
    all_csv_file = list(csv_file.readlines())  # guardo el archivo en una lista
    line_count=1
    for csv_line in all_csv_file:
        attrs = csv_line.strip().split(';')
        identifier = attrs.pop(0)
        attrs = [float(attr) for attr in attrs]
        base_ponderator = "0" * attrs_count

        row_ponderations={base_ponderator:0}
        for i in range(0,attrs_count-1):
            row_pond_extension={}
            for ponderator in row_ponderations:
                new_ponderator_vector=list(ponderator)
                new_ponderator_vector[i]='1'
                new_ponderator=''.join(new_ponderator_vector)
                new_ponderation=attrs[i]+row_ponderations[ponderator]
                row_pond_extension[new_ponderator]=new_ponderation

            row_ponderations.update(row_pond_extension)
        row = Row(identifier, attrs)
        file_rows.append(row)
        line_count+=1
        print line_count
    csv_file.close()
    return attrs_count,file_rows

startTime = time.time()

preprocess_mode=True
CSV_DIRECTORY = "data/"
goals_hash = {}

total_time_seconds=3*60
allFiles = glob.glob("data\*.csv")
files_count=len(allFiles)

file_objects_by_file_name={}
goals_path="goals.txt"
if preprocess_mode:
    max_seconds_for_file=total_time_seconds/files_count
    for file in allFiles:  # para cada archivo de data
        allCases = {}  # donde guardo los casos
        file_start_time=time.time()
        file_name=file.split("\\")[-1]
        csv_file = open(file, 'r')
        attrs_count,file_rows=get_rows_from_csv(file_name)
        file_object=File(file_name,file_rows)

        ponderator_vectors = []
        for i in range(0,2**(attrs_count)):
            ponderator_vector = [int(pond) for pond in list("{0:b}".format(i).zfill(10))]
            ponderator_vectors.append(ponderator_vector)

        sorted_by_ponderator={}
        for ponderator_vector in ponderator_vectors:
            sorted_rows=sorted(file_rows,key=lambda x:x.get_ponderation(ponderator_vector))
            sorted_by_ponderator[tuple(ponderator_vector)]=sorted_rows
            current_time=time.time()
            delta_seconds=int(current_time-file_start_time)
            if(delta_seconds>=max_seconds_for_file):
                file_object.set_sorted_by_ponderator_vector(sorted_by_ponderator)
                break
        file_objects_by_file_name[file_name]=file_object
    goals_path=raw_input("ingrese nombre del archivo goals")

goals_file=open(goals_path,'r')
goal_line = goals_file.readline()
while goal_line != "":
    splitted_line = goal_line.strip().split(' ')
    required_file_name = splitted_line.pop(0)
    required_position = int(splitted_line.pop(0))
    required_order = splitted_line.pop(0)
    ponderator_vector = [int(i) for i in splitted_line]
    tuples = []
    if (required_file_name not in file_objects_by_file_name):
        attrs_count,rows=get_rows_from_csv(required_file_name)
        file_objects_by_file_name[required_file_name]=File(required_file_name,rows)
    file_object=file_objects_by_file_name[required_file_name]


    if tuple(ponderator_vector) not in file_object.get_sorted_by_ponderator_vector():
        sorted_rows=sorted(file_object.get_rows(),key=lambda x:x.get_ponderation(ponderator_vector))
        file_object.set_key_in_sorted_by_ponderator_vector(tuple(ponderator_vector),sorted_rows)

    # COMPUTE THE RESULT
    # bubbleSort(tuples)
    # sorted(tuples, key=lambda x: x[1])
    # heap_sort(tuples)
    # print tuples
    if(required_order=='DESC'):
        required_position = len(file_object.get_sorted_by_ponderator_vector()[tuple(ponderator_vector)]) - required_position

    result = file_object.get_sorted_by_ponderator_vector()[tuple(ponderator_vector)][required_position].get_identifier()


    goal_line = goals_file.readline()

goals_file.close()

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
