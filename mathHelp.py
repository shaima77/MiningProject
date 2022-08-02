


import math


def entropy_data_all(data, target):  # Calculation of entropy in relation to all information
    sum_entropy = 0
    size = len(data.index)
    listTargetVal = data[target].unique()

    for x in listTargetVal:
        newdataset = data[data[target] == x]
        tempsize = len(newdataset) / size
        sum_entropy = sum_entropy + (tempsize * math.log(tempsize, 2))
    sum_entropy = sum_entropy * -1
    return sum_entropy


def calc_entropy(col, target, targetunique):  # Calculation of entropy in relation to the column
    sumentropy = 0

    for x in targetunique:
        newdataset = len(col[col[target] == x])
        if newdataset != 0:
            probability = newdataset / len(col)
            sumentropy = sumentropy + (probability * math.log(probability, 2))

    sumentropy = sumentropy * -1

    return sumentropy


def calc_info_gain(col, data, target, targetunique):  # Calculates the information gain
    colVal = data[col].unique()
    size = len(data)
    sumCol = 0

    for x in colVal:
        entropyVal = calc_entropy(data[data[col] == x], target, targetunique)
        sumCol += (len(data[data[col] == x]) / size) * entropyVal

    return entropy_data_all(data, target) - sumCol


def find_most_informative_feature(data, target, targetunique):  # Finds the column with the best information gain
    newdata = data.drop(columns=[target])

    tempmax = 0
    maxx = None

    for x in newdata:
        current = calc_info_gain(x, data, target, targetunique)
        if tempmax < current:
            tempmax = current
            maxx = x

    return maxx
