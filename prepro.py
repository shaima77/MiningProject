

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


# Performs pre-processing
def pre(data, target, targetORoverall, normalizeORnot, discretization, discretizationType, binss):
    data.dropna(subset=[target], inplace=True)
    num = data.select_dtypes(include=np.number).columns
    category = data.select_dtypes(include=object).columns

    # target=1 or overall=0
    if targetORoverall == 0:
        data[num] = data[num].fillna(data.mean(numeric_only=True))
        data[category] = data[category].fillna(data.mode().iloc[0])
    if targetORoverall == 1:
        data[num] = data[num].fillna(data.groupby(target)[num].transform("mean"))
        groups = data.groupby(target)
        mode_by_group = groups[category].transform(lambda x: x.mode()[0])
        data[category] = data[category].fillna(mode_by_group)
    # normalizeORnot=1 do:
    if normalizeORnot == 1:
        num = data.select_dtypes(include=np.number).columns
        for x in num:
            data[x] = MinMaxScaler().fit_transform(np.array(data[x]).reshape(-1, 1))

    if discretization == 1:
        columns = data.select_dtypes(include=np.number).columns
        match discretizationType:
            case 1:
                for x in columns:
                    data[x] = pd.cut(x=data[x], bins=binss)
            case 2:
                for x in columns:
                    data[x] = pd.qcut(x=data[x], q=binss)
            case 3:
                pass

    return data


def manngepre(data, target, targetORoverall, normalizeORnot, discretization, discretizationType, binss,
              ratioTestTrain):  # Divides the files and activates preprocessing
    train, test = train_test_split(data, train_size=ratioTestTrain)

    train = pre(train, target, targetORoverall, normalizeORnot, discretization, discretizationType, binss)
    test = pre(test, target, targetORoverall, normalizeORnot, discretization, discretizationType, binss)
    f = open('preprocessing.txt', 'w')
    train.to_csv("train_clean.csv", index=False)
    test.to_csv("test_clean.csv", index=False)

    if targetORoverall == 1:
        f.write("targetORoverall :" + "target" + '\n')
    else:
        f.write("targetORoverall :" + "all data" + '\n')
    if normalizeORnot == 1:
        f.write("normalizeORnot :" + "Yes" + '\n')
    else:
        f.write("normalizeORnot :" + "No" + '\n')
    if discretization == 1:
        f.write("discretization :" + 'Yes' + '\n')
    else:
        f.write("discretization :" + 'No' + '\n')
    if discretizationType == 1:
        f.write("discretizationType :" + "Based equal-width" + '\n')
    elif discretizationType == 2:
        f.write("discretizationType :" + "Based equal-frequency" + '\n')
    elif discretizationType == 2:
        f.write("discretizationType :" + "Based entropy" + '\n')
    f.write("binss :" + str(binss) + '\n')

    f.write("ratioTestTrain :" + str(ratioTestTrain) + '\n')
