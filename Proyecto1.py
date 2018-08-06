import time
import operator


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


startTime = time.time()
CSV_DIRECTORY = "data/"
goals_file = open("goals.txt", "r")
goal_line = goals_file.readline()
goals_hash = {}
while goal_line != "":
    splitted_line = goal_line.strip().split(' ')
    required_file_name = splitted_line.pop(0)
    required_position = int(splitted_line.pop(0))
    required_order = splitted_line.pop(0)
    ponderator_vector = [int(i) for i in splitted_line]
    tuples = []
    csv_file = open(CSV_DIRECTORY + required_file_name, 'r')
    for csv_line in csv_file:
        attrs = csv_line.strip().split(';')
        identifier = attrs.pop(0)
        ponderation = 0
        for (attr, ponderator) in zip(attrs, ponderator_vector):
            if ponderator == 1:
                ponderation += float(attr)
        tuples.append((identifier, ponderation))
    goal_line = goals_file.readline()
    # COMPUTE THE RESULT
    result = ""
    # tuples.sort(key=operator.itemgetter(1))
    bubble_sort(tuples)
    # sorted(tuples, key=lambda x: x[1])
    # heap_sort(tuples)
    if required_order == 'ASC':
        result = tuples[required_position]
    else:
        result = tuples[len(tuples) - required_position]

    goals_hash[goal_line] = result
print goals_hash
resultFile = open("results1.txt", 'w')
for result in goals_hash.values():
    resultFile.write(result[0] + ": " + str(result[1]) + "\n")
resultFile.close()

print ('The script took {0} second !'.format(time.time() - startTime))
