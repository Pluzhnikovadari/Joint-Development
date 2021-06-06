import tkinter as tk
import pygame
import time
import random
from threading import Thread
import os
from labirint import start_labirint
from tetris import main_menu
import tic

def Snake():
    import snake

def Plat():
    import platform_and_ball

def Meteor():
    import meteor



class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.SnakeButton = tk.Button(self, text='Snake', command=self.snakebut)
        self.PlatformButton = tk.Button(self, text='Platform and ball', command=self.platformbut)
        self.MeteorButton = tk.Button(self, text='Meteor', command=self.meteorbut)
        self.TicButton = tk.Button(self, text='Tic', command=self.ticbut)
        self.TetrisButton = tk.Button(self, text='Tetris', command=self.tetrisbut)
        self.LabirintButton = tk.Button(self, text="Bug's Labirint", command=self.labirintbut)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)

        self.SnakeButton.grid(row=0, column=0, sticky='NEWS')
        self.PlatformButton.grid(row=0, column=1, sticky='NEWS')
        self.TicButton.grid(row=1, column=0, sticky='NEWS')
        self.TetrisButton.grid(row=1, column=1, sticky='NEWS')
        self.MeteorButton.grid(row=2, column=0, sticky='NEWS')
        self.LabirintButton.grid(row=2, column=1, sticky='NEWS')
        self.quitButton.grid(row=3, column=0, columnspan=2, sticky='NEWS')


    def snakebut(self):
        thread1 = Thread(target=Snake)
        thread1.start()
        thread1.join()


    def platformbut(self):
        thread2 = Thread(target=Plat)
        thread2.start()
        thread2.join()



    def meteorbut(self):
        thread2 = Thread(target=Meteor)
        thread2.start()
        thread2.join()



    def ticbut(self):
        thread2 = Thread(target=tic.Game().start())
        thread2.start()
        thread2.join()



    def tetrisbut(self):
        thread2 = Thread(target=main_menu())
        thread2.start()
        thread2.join()



    def labirintbut(self):
        thread2 = Thread(target=start_labirint)
        thread2.start()
        thread2.join()




app = Application()
app.master.title('Game application')
app.mainloop()
