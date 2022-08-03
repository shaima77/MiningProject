import pandas as pd
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
import ourNB as nb


def TrainTestSC(mainGUI):  # Responsible for the second screen in the system
    traintest = customtkinter.CTk()

    traintest.geometry("700x500")
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
    x = pd.read_csv(train)

    col = customtkinter.CTkComboBox(master=traintest,
                                    values=x.columns)
    col.set(x.columns)
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
            mainGUI.deiconify()

    traintest.protocol("WM_DELETE_WINDOW", on_closing)
    traintest.mainloop()
