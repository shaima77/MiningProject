import tkinter
import webbrowser
from tkinter import *
import tkinter
import tkinter.messagebox
from PIL import Image
from PIL import ImageTk

import customtkinter

from TrainTestGUI import TrainTestSC
from preprocessingGUI import PreSC


def mainGUI():
    def PreGUI():
        mainGUI.withdraw()
        PreSC(mainGUI)

    def ModelGUI():
        mainGUI.withdraw()
        TrainTestSC(mainGUI)

    def About():
        def callback(url):
            webbrowser.open_new_tab(url)

        about = Toplevel()
        about.title("About")
        about.geometry("1800x1250")

        bg = PhotoImage(file=r"aboutpic.png")

        # Show image using label
        label1 = Label(about, image=bg)
        label1.pack()

        label4 = Label(master=about, text=""
                                          ""
                                          " ")
        label4.pack()

        label3 = Label(master=about, text="This project was created with the aim of allowing many\n "
                                          "people who want to test different models as well as \n"
                                          "processing information in different ways, intended for\n "
                                          "beginners in the field of data science and even for\n "
                                          "advanced in the field\n"
                                          "The project was written by : Shai Mastitz\n"
                                          "Linkedin page:"
                       )
        label3.pack()
        link = Label(about, text="Linkedin link", font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e:
        callback("www.linkedin.com/in/shai-mastitz"))

        about.mainloop()

    mainGUI = customtkinter.CTk()
    mainGUI.geometry(f"{700}x{500}")
    mainGUI.title("main GUI")
    width = 1800
    height = 700
    img = Image.open("data-mining.png")
    img = img.resize((width, height))
    photoImg = ImageTk.PhotoImage(img)
    w = tkinter.Label(image=photoImg)
    w.pack()
    mainGUI.configure(bg='black')

    labe2l = customtkinter.CTkLabel(master=mainGUI, text=""
                                                         ""
                                                         "")

    labe2l.pack()
    buttonpreGUI = customtkinter.CTkButton(master=mainGUI, text="Preprocessing", command=PreGUI)
    buttonpreGUI.pack()
    label = customtkinter.CTkLabel(master=mainGUI, text=""
                                                        ""
                                                        ""
                                                        ""
                                                        "")

    label.pack()
    buttonpreGUI2 = customtkinter.CTkButton(master=mainGUI, text="TrainTest", command=ModelGUI)
    buttonpreGUI2.pack()
    label = customtkinter.CTkLabel(master=mainGUI, text=""
                                                        ""
                                                        ""
                                                        ""
                                                        "")

    label.pack()
    About = customtkinter.CTkButton(master=mainGUI, text="About", command=About)
    About.pack()

    mainGUI.mainloop()
