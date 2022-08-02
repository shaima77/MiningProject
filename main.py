

import os

import numpy as np
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import customtkinter
import pathlib

from KNN import KNN
from Kmeans import Kmeans
from Modell import load, Display, DisplayKmeans
from id3tree import id3tree
from ourid3tree import ourid3tree
from naivebayes import NaiveBayes
from prepro import manngepre
import ourNB as nb


def preprocessingSC():  # Responsible for the first system screen
    preproo = customtkinter.CTk()
    windowWidth = 700
    windowHeight = 500
    screenHeight = preproo.winfo_screenheight()
    screenWidth = preproo.winfo_screenwidth()

    preproo.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, int(screenWidth / 2 - windowWidth / 2),
                                          int(screenHeight / 2 - windowHeight / 2)))
    preproo.title("Preprocessing")
    filename = 'temp'
    validator = 0

    def pre():
        if filename == 'temp' or filename == ' ':
            messagebox.showerror("input problem", "Fix your input, browse files again")
            return None
        if validator == 0:
            messagebox.showerror("input problem", "Fix your input: empty file. Browse files again")
            return None

        missingvaluesDic = {'classification': 0, 'all data': 1}
        intmissingvaluesDic = missingvaluesDic[missingvalues.get()]
        YesNoDic = {'Yes': 1, 'No': 0}
        intNormal = YesNoDic[normalizeORnot.get()]
        intdiscretization = YesNoDic[discretization.get()]
        discretizationTypeDic = {"Based equal-width": 1, "Based equal-frequency": 2, "Based entropy": 3}
        intdiscretizationType = discretizationTypeDic[discretizationType.get()]

        if intmissingvaluesDic == 0 or intmissingvaluesDic == 1:
            if intNormal == 0 or intNormal == 1:
                if intdiscretization == 0:
                    data = pd.read_csv(filename)
                    data.replace("?", np.nan, inplace=True)
                    manngepre(data, classificationcol.get(), intmissingvaluesDic, intNormal,
                              0, 0,
                              0,
                              int(w.get()) / 100)

                    # preproo.destroy()  # @@@
                    preproo.quit()
                    preproo.withdraw()
                    TrainTestSC(classificationcol.values, classificationcol.current_value,preproo)
                if intdiscretization == 1:
                    if intdiscretizationType == 1 or intdiscretizationType == 2 or intdiscretizationType == 3:
                        bins_num = 0
                        try:
                            bins_num = int(bins.get())
                        except:
                            pass
                        if bins_num >= 0:
                            data = pd.read_csv(filename)
                            data.replace("?", np.nan, inplace=True)
                            manngepre(data, classificationcol.get(), intmissingvaluesDic,
                                      intNormal,
                                      intdiscretization, intdiscretizationType,
                                      bins_num,
                                      int(w.get()) / 100)
                        # preproo.destroy()  # @@@
                        preproo.quit()
                        preproo.withdraw()
                        TrainTestSC(classificationcol.values, classificationcol.current_value,preproo)

    def browseFiles():
        nonlocal filename
        nonlocal validator
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("csv files",
                                                          "*.csv*"),
                                                         ("all files",
                                                          "*.*")))
        if filename != '':
            if os.stat(filename).st_size > 5:
                data = pd.read_csv(filename)
                nonlocal classificationcol
                vals = data.columns
                classificationcol.configure(values=vals)
                classificationcol.set(vals[0])
                validator = validator + 1

    customtkinter.CTkLabel(master=preproo, text="Browse CSV File:").pack()
    button_explore = customtkinter.CTkButton(master=preproo, text="Browse Files", command=browseFiles)
    button_explore.pack()
    customtkinter.CTkLabel(master=preproo, text="Classification column:").pack()
    classificationcol = customtkinter.CTkComboBox(master=preproo,
                                                  values=[""])
    classificationcol.pack()
    customtkinter.CTkLabel(master=preproo, text="Completion of missing values according to classification or "
                                                "all data:").pack()
    missingvalues = customtkinter.CTkComboBox(master=preproo,
                                              values=["classification", "all data"])
    missingvalues.pack()
    customtkinter.CTkLabel(master=preproo, text="normalize or not:").pack()
    normalizeORnot = customtkinter.CTkComboBox(master=preproo,
                                               values=["Yes", "No"])
    normalizeORnot.pack()
    customtkinter.CTkLabel(master=preproo, text="discretization:").pack()
    discretization = customtkinter.CTkComboBox(master=preproo,
                                               values=["Yes", "No"])

    discretization.pack()
    customtkinter.CTkLabel(master=preproo, text="discretization Type:").pack()

    discretizationType = customtkinter.CTkComboBox(master=preproo,
                                                   values=["Based equal-width", "Based equal-frequency",
                                                           "Based entropy"])
    discretizationType.pack()
    customtkinter.CTkLabel(master=preproo, text="bins:").pack()
    bins = customtkinter.CTkEntry(master=preproo,
                                  placeholder_text="0 or more")
    bins.pack()
    ratio = customtkinter.CTkLabel(master=preproo, text="Ratio for train / test:")
    ratio.pack()

    w = customtkinter.CTkSlider(master=preproo,
                                from_=50,
                                to=90,
                                number_of_steps=8
                                )
    w.pack()

    ratio.configure(text=str(
        "Ratio for train {}: / test: {}".format("%.2f" % (w.get() / 100), "%.2f" % (1 - float(w.get()) / 100))))
    ratio.pack()

    def updateValue(self):
        ratio.configure(text=str(
            "Ratio for train: {} / test: {}".format("%.2f" % (w.get() / 100), "%.2f" % (1 - float(w.get()) / 100))))
        ratio.pack()

    w.bind("<Leave>", updateValue)

    b = Button(preproo, text="ok", command=pre)
    b.pack()

    preproo.mainloop()


def TrainTestSC(classvalues, current,preproo):  # Responsible for the second screen in the system
    traintest = customtkinter.CTk()

    windowWidth = 700
    windowHeight = 500
    screenHeight = traintest.winfo_screenheight()
    screenWidth = traintest.winfo_screenwidth()

    traintest.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, int(screenWidth / 2 - windowWidth / 2),
                                            int(screenHeight / 2 - windowHeight / 2)))

    traintest.title("Train and Test")
    train = 'train_clean.csv'
    test = 'test_clean.csv'

    def trainfile():
        nonlocal train
        train = filedialog.askopenfilename(initialdir="/",
                                           title="Select a File",
                                           filetypes=(("csv files",
                                                       "*.csv*"),
                                                      ("all files",
                                                       "*.*")))

    def testfile():
        nonlocal test
        test = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("csv files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))

    def Testing():
        ModelTypee = {'NB sklearn': 1, 'KNN sklearn': 2, 'Kmeans sklearn': 3, 'tree sklearn': 4, 'ourNB': 5,
                      'ourTree': 6}
        intModelTypee = ModelTypee[ModelType.get()]
        TestorTrainn = {'Test': 1, 'Train': 2}
        intTestorTrainn = TestorTrainn[TestorTrain.get()]
        x = pd.read_csv(train)
        y = pd.read_csv(test)
        if (col.get() in x.columns) and (intTestorTrainn in [1, 2]):
            t = intModelTypee
            cur_k = 0  # default k
            try:
                cur_k = int(K.get())
            except:
                pass
            if ((t == 2 or t == 3) and cur_k > 0) or (t in [1, 4, 5, 6]):
                match t:
                    case 1:  # NB sklearn
                        train_na = NaiveBayes()
                        train_na.train(x, col.get())
                        if intTestorTrainn == 1:  # test
                            Performancest = train_na.test(y)
                            mostt = y[col.get()].value_counts().idxmax()
                            num = y[col.get()].value_counts()[mostt] / y.shape[0]
                            Display(Performancest, intTestorTrainn, num, "NB sklearn: Test")
                        if intTestorTrainn == 2:  # train
                            mostt = x[col.get()].value_counts().idxmax()
                            num = x[col.get()].value_counts()[mostt] / x.shape[0]
                            Performancest = train_na.test(x)
                            Display(Performancest, intTestorTrainn, num, "NB sklearn: Train")

                    case 2:  # KNN sklearn

                        train_na = KNN()
                        train_na.train(x, col.get(), cur_k)
                        if intTestorTrainn == 1:  # test
                            Performancest = train_na.test(y)
                            mostt = y[col.get()].value_counts().idxmax()
                            num = y[col.get()].value_counts()[mostt] / y.shape[0]
                            Display(Performancest, intTestorTrainn, num, "KNN sklearn: Test")
                        if intTestorTrainn == 2:  # train
                            mostt = x[col.get()].value_counts().idxmax()
                            num = x[col.get()].value_counts()[mostt] / x.shape[0]
                            Performancest = train_na.test(x)
                            Display(Performancest, intTestorTrainn, num, "KNN sklearn: Train")

                    case 3:  # Kmeans sklearn
                        x2 = x.drop(columns=col.get())
                        y2 = y.drop(columns=col.get())
                        train_na = Kmeans()
                        train_na.train(cur_k)
                        if intTestorTrainn == 1:  # test
                            train_na.test(y2, intTestorTrainn, "Kmeans sklearn: Test")
                        if intTestorTrainn == 2:  # train
                            train_na.test(x2, intTestorTrainn, "Kmeans sklearn: Train")
                    case 4:  # tree sklearn
                        train_na = id3tree()
                        train_na.train(x, col.get())
                        if intTestorTrainn == 1:  # test
                            Performancest = train_na.test(y)
                            mostt = y[col.get()].value_counts().idxmax()
                            num = y[col.get()].value_counts()[mostt] / y.shape[0]
                            Display(Performancest, intTestorTrainn, num, "Tree sklearn: Test")
                        if intTestorTrainn == 2:  # train
                            Performancest = train_na.test(x)
                            mostt = x[col.get()].value_counts().idxmax()
                            num = x[col.get()].value_counts()[mostt] / x.shape[0]
                            Display(Performancest, intTestorTrainn, num, "Tree sklearn: Train")

                    case 5:  # Our NB
                        debug = False  # change to False
                        train_na = nb.NB(x, y, col.get())
                        train_na.train()
                        if intTestorTrainn == 1:  # test
                            mostt = y[col.get()].value_counts().idxmax()
                            num = y[col.get()].value_counts()[mostt] / y.shape[0]
                            Performancest = train_na.test(y, col.get(), debug)
                            Display(Performancest, intTestorTrainn, num, "Our NB: Test")
                        if intTestorTrainn == 2:  # train
                            mostt = x[col.get()].value_counts().idxmax()
                            num = x[col.get()].value_counts()[mostt] / x.shape[0]
                            Performancest = train_na.train(debug)
                            Display(Performancest, intTestorTrainn, num, "Our NB: Train")

                    case 6:  # Our id3 tree
                        train_na = ourid3tree(x, col.get())
                        train_na.train()
                        if intTestorTrainn == 1:  # test
                            mostt = y[col.get()].value_counts().idxmax()
                            num = y[col.get()].value_counts()[mostt] / y.shape[0]
                            Performancest = train_na.test(y)
                            Display(Performancest, intTestorTrainn, num, "Our tree: Test")
                        if intTestorTrainn == 2:  # train
                            mostt = x[col.get()].value_counts().idxmax()
                            num = x[col.get()].value_counts()[mostt] / x.shape[0]
                            Performancest = train_na.test(x)
                            Display(Performancest, intTestorTrainn, num, "Our tree: Train")






            else:
                messagebox.showerror("input problem", "fix your input at ModelType or K")

        else:
            messagebox.showerror("input problem", "fix your input classification column or Test or Train")

    try:
        cur_path = pathlib.Path().resolve()
        train = str(cur_path) + "\\train_clean.csv"
        test = str(cur_path) + "\\test_clean.csv"
        pd.read_csv(train)
        print("Found default train file")
        pd.read_csv(test)
        print("Found default test file")
    except:
        pass

    customtkinter.CTkLabel(master=traintest, text="Browse train File:").pack()
    button_explore = customtkinter.CTkButton(master=traintest, text="Browse Files", command=trainfile)
    button_explore.pack()
    customtkinter.CTkLabel(master=traintest, text="Browse test File:").pack()
    button_explore2 = customtkinter.CTkButton(master=traintest, text="Browse Files", command=testfile)
    button_explore2.pack()
    customtkinter.CTkLabel(master=traintest, text="Model Type").pack()

    ModelType = customtkinter.CTkComboBox(master=traintest,
                                          values=["NB sklearn", "KNN sklearn", "Kmeans sklearn", "tree sklearn",
                                                  "ourNB", "ourTree"])

    ModelType.pack()
    customtkinter.CTkLabel(master=traintest, text="Classification column: ").pack()

    col = customtkinter.CTkEntry(master=traintest,
                                 placeholder_text="Classification column:")
    col = customtkinter.CTkComboBox(master=traintest,
                                    values=classvalues)
    col.set(current)
    col.pack()

    customtkinter.CTkLabel(master=traintest, text="K").pack()
    K = customtkinter.CTkEntry(master=traintest,
                               placeholder_text="1 or more")
    K.pack()
    customtkinter.CTkLabel(master=traintest, text="Test or Train").pack()

    TestorTrain = customtkinter.CTkComboBox(master=traintest,
                                            values=["Test", "Train"])
    TestorTrain.set("Train")
    TestorTrain.pack()

    customtkinter.CTkLabel(master=traintest, text="").pack()

    b = customtkinter.CTkButton(master=traintest, text="Create a model and test it", command=Testing)
    b.pack()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            traintest.destroy()
            preproo.deiconify()

    traintest.protocol("WM_DELETE_WINDOW", on_closing)
    traintest.mainloop()


preprocessingSC()
