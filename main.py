"""Main window."""
import tkinter as tk
from threading import Thread
testdir = os.path.dirname(__file__)
srcdir = '../Games'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from labirint import start_labirint
from tetris import main_menu
import tic
import snake
import platform_and_ball
import meteor
import gettext
sys.path.remove(os.path.abspath(os.path.join(testdir, srcdir)))

gettext.install("messages", ".", names=("ngettext",))


class Application(tk.Frame):
    """Application class."""

    def __init__(self, master=None):
        """Init class."""
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        """Create buttons."""
        self.SnakeButton = tk.Button(self, text=_('Snake'),
                                     command=self.snakebut)
        self.PlatformButton = tk.Button(self, text=_('Platform and ball'),
                                        command=self.platformbut)
        self.MeteorButton = tk.Button(self, text=_('Meteor'),
                                      command=self.meteorbut)
        self.TicButton = tk.Button(self, text=_('Tic'), command=self.ticbut)
        self.TetrisButton = tk.Button(self, text=_('Tetris'),
                                      command=self.tetrisbut)
        self.LabirintButton = tk.Button(self, text=_("Bug's Labirint"),
                                        command=self.labirintbut)
        self.quitButton = tk.Button(self, text=_('Quit'), command=self.quit)

        self.SnakeButton.grid(row=0, column=0, sticky='NEWS')
        self.PlatformButton.grid(row=0, column=1, sticky='NEWS')
        self.TicButton.grid(row=1, column=0, sticky='NEWS')
        self.TetrisButton.grid(row=1, column=1, sticky='NEWS')
        self.MeteorButton.grid(row=2, column=0, sticky='NEWS')
        self.LabirintButton.grid(row=2, column=1, sticky='NEWS')
        self.quitButton.grid(row=3, column=0, columnspan=2, sticky='NEWS')

    def snakebut(self):
        """Snake button."""
        thread1 = Thread(target=snake.main)
        thread1.start()
        thread1.join()

    def platformbut(self):
        """Platform and ball button."""
        thread2 = Thread(target=platform_and_ball.main)
        thread2.start()
        thread2.join()

    def meteorbut(self):
        """Meteor button."""
        thread2 = Thread(target=meteor.main)
        thread2.start()
        thread2.join()

    def ticbut(self):
        """Tic button."""
        thread2 = Thread(target=tic.Game().start)
        thread2.start()
        thread2.join()

    def tetrisbut(self):
        """Tetris button."""
        thread2 = Thread(target=main_menu)
        thread2.start()
        thread2.join()

    def labirintbut(self):
        """Labirint button."""
        thread2 = Thread(target=start_labirint)
        thread2.start()
        thread2.join()


app = Application()
app.master.title(_('Game application'))
app.mainloop()
