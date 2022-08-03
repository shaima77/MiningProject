
import pickle
import tkinter

import numpy as np
from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, f1_score
from tkinter import *
import matplotlib.pyplot as plt



def save(model):  # save the model
    filename = 'model.sav'
    pickle.dump(model, open(filename, 'wb'))


def load():  # load the model
    loaded_model = pickle.load(open('model.sav', 'rb'))
    return loaded_model


def Performancest(z, y):  # Returns various metrics to the model
    return [
        accuracy_score(y, z),
        precision_score(y, z, average='macro'),
        recall_score(y, z, average='macro'),
        f1_score(y, z, average='macro'),
        confusion_matrix(y, z)
    ]


def Display(res, i, num, title):  # Shows results for the model
    results = Toplevel()
    results.title("Results")
    results.geometry("600x600")
    f = None
    Label(results, text=title, font='ariel 16 bold').pack()
    Label(results,
          text='Accuracy score: {0} \nPrecision score: {1} \nRecall score: {2} \nF1 score: {3} \nMajority rule: {4}'.format(
              res[0], res[1],
              res[2],
              res[3], num)).pack()
    display = metrics.ConfusionMatrixDisplay(confusion_matrix=res[4], display_labels=[False, True])
    display.plot()
    if i == 1:
        plt.savefig('test.png')
        img = tkinter.PhotoImage(file=r"test.png")
        w = tkinter.Label(results, image=img)
        w.pack()
    if i == 2:
        plt.savefig('train.png')
        img = tkinter.PhotoImage(file=r"train.png")
        w = tkinter.Label(results, image=img)
        w.pack()
    if i == 1:
        f = open('test.txt', 'w')
    if i == 2:
        f = open('train.txt', 'w')
    if f is not None:
        f.write("accuracy score: :" + str(res[0]) + '\n')
        f.write("precision score: :" + str(res[1]) + '\n')
        f.write("recall_score: :" + str(res[2]) + '\n')
        f.write("f1_score: :" + str(res[3]) + '\n')
        f.write("majority rule: :" + str(num) + '\n')
    plt.close('all')

    results.mainloop()


def DisplayKmeans(res, df, i, title):  # Shows results for the Kmeans model
    results = Toplevel()
    results.title("Results")
    results.geometry("600x600")
    Label(results, text=title, font='ariel 16 bold').pack()
    labels = np.unique(res)
    for x in labels:
        plt.scatter(df[res == x, 0], df[res == x, 1], label=x)
    if i == 1:
        plt.savefig('testKmeans.png')
        img = tkinter.PhotoImage(file=r"testKmeans.png")
        w = tkinter.Label(results, image=img)
        w.pack()
    if i == 2:
        plt.savefig('trainKmeans.png')
        img = tkinter.PhotoImage(file=r"trainKmeans.png")
        w = tkinter.Label(results, image=img)
        w.pack()
    plt.close('all')
    results.mainloop()
