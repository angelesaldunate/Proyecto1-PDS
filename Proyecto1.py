import time
import operator

startTime = time.time()
CSV_DIRECTORY = "data/"
goals_file = open("goals.txt", "r")
goal_line = goals_file.readline()
goals_hash = {}
while (goal_line != ""):
    splitted_line = goal_line.strip().split(' ')
    required_file_name = splitted_line.pop(0)
    required_position = int(splitted_line.pop(0))
    required_order = splitted_line.pop(0)
    ponderator_vector = [int(i) for i in splitted_line]
    touples = []
    csv_file = open(CSV_DIRECTORY + required_file_name, 'r')
    for csv_line in csv_file:
        attrs = csv_line.strip().split(';')
        identifier = attrs.pop(0)
        ponderation = 0
        for (attr, ponderator) in zip(attrs, ponderator_vector):
            if (ponderator == 1):
                ponderation += float(attr)
        touples.append((identifier, ponderation))
    goal_line = goals_file.readline()
    # COMPUTE THE RESULT
    result = ""
    touples.sort(key=operator.itemgetter(1))
    if required_order == 'ASC':
        result = touples[required_position]
    else:
        result = touples[len(touples)-required_position]

    goals_hash[goal_line] = result
resultFile = open("resultsX.txt",'w' )
for result in goals_hash.values():
    resultFile.write(result[0]+"\n")
resultFile.close()
print ('The script took {0} second !'.format(time.time() - startTime))
