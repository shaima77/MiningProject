import os

import numpy as np
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import customtkinter

from TrainTestGUI import TrainTestSC
from prepro import manngepre


def PreSC(mainGUIw):  # Responsible for the first system screen
    preproo = customtkinter.CTk()

    preproo.geometry("700x500")

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

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            preproo.destroy()
            mainGUIw.deiconify()

    preproo.protocol("WM_DELETE_WINDOW", on_closing)
    preproo.mainloop()
