import tkinter as tk
import pygame
import time
import random
from threading import Thread
import os

def Snake():
	import snake

def Plat():
	import platform_and_ball


class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		self.SnakeButton = tk.Button(self, text='Snake', command=self.snakebut)
		self.PlatformButton = tk.Button(self, text='Platform and ball', command=self.platformbut)
		self.quitButton = tk.Button(self, text='Quit', command=self.quit)
		self.SnakeButton.grid(row = 0, column = 0)
		self.PlatformButton.grid(row=0, column=1)
		self.quitButton.grid(columnspan=2)


	def snakebut(self):
		thread1 = Thread(target=Snake, daemon=True)
		thread1.start()


	def platformbut(self):
		thread2 = Thread(target=Plat, daemon=True)
		thread2.start()





app = Application()
app.master.title('Game application')
app.mainloop()