import Tkinter
from PIL import Image, ImageTk
import ttk
import tkFont
import sys

sys.dont_write_bytecode = True

# class to provide e.g. custom theme
class gui(object):
    
    # initialise class
    def __init__(self):
        super(gui,self).__init__()
        # default values
        self.root                      = []
        self.mainframe                 = []
        self.toolbar                   = []
        self.notebook                  = []
        self.subframeF                 = []
        self.subframeS                 = []
        self.subframeI                 = []
        self.subframeV                 = []
        self.loadIcon                  = []
        self.useLoadIcon               = []
        self.loadBtn                   = []
        self.refreshConfigIcon         = []
        self.useRefreshConfigIcon      = []
        self.refreshConfigBtn          = []
        self.quitIcon                  = []
        self.useQuitIcon               = []
        self.folderIcon                = []
        self.useFolderIcon             = []
        self.quitBtn                   = []
        self.popup                     = []
        self.width                     = 200
        self.height                    = 100
        self.gridx                     = 20
        self.gridy                     = 25
        self.nx                        = 3
        self.ny                        = 3
        self.pad                       = str(self.gridx) \
                                         + " " + str(self.gridy) \
                                         + " " + str(self.nx) \
                                         + " " + str(self.ny)
        self.hexx                      = '#000000'
        self.linuxMintHEX              = '#505050'
        self.linuxMintHEX_brighter     = '#575757'
        self.linuxMintHEX_evenBrighter = '#5e5e5e'
        self.linuxMintHEX_brightest    = '#6c6c6c'
        self.linuxMintHEX_folder       = '#7da446'
        self.sliderHEX                 = '#334353'
        self.styleGUI                  = []
        self.sans9                     = []
        self.componentFrameF           = []
        self.componentFrameS           = []
        self.entryMinF                 = []
        self.entryMaxF                 = []
        self.entryMinS                 = []
        self.entryMaxS                 = []
        self.nodeFrameS                = []
    
    # resize handler
    def resize(self, event):
        self.width  = event.width
        self.height = event.height
    
    # configure root window
    def configureRoot(self):
        self.root.title("FSIViewer")
        self.root.attributes('-zoomed', True)
        self.root.bind("<Configure>", self.resize)
        self.root.configure(bg=self.linuxMintHEX)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.width  = self.root.winfo_width()
        self.height = self.root.winfo_height()
    
    # container for vtk viewport etc.
    def configureMainframe(self):
        self.mainframe.grid(column=0, row=0, \
                          rowspan=self.gridy-1, columnspan=self.gridx-1, \
                          sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
        self.mainframe.columnconfigure(0, weight=0)
        self.mainframe.columnconfigure(1, weight=0)
        for i in xrange(2, self.gridx):
            self.mainframe.columnconfigure(i, weight=1)
        for i in xrange(0, self.gridy-3):
            self.mainframe.rowconfigure(i, weight=1)
    
    # toolbar to create a visualization and quit application
    def configureToolbar(self, installDir):
        self.toolbar.grid(row=0, column=0, \
                          columnspan=2, \
                          sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
        self.loadIcon             = Image.open(installDir + "icons/add.png")
        self.useLoadIcon          = ImageTk.PhotoImage(self.loadIcon)
        self.refreshConfigIcon    = Image.open(installDir \
                                               + "icons/book_next.png")
        self.useRefreshConfigIcon = ImageTk.PhotoImage(self.refreshConfigIcon)
        self.quitIcon             = Image.open(installDir + "icons/cross.png")
        self.useQuitIcon          = ImageTk.PhotoImage(self.quitIcon)
        self.folderIcon           = Image.open(installDir + "icons/folder.png")
        self.useFolderIcon        = ImageTk.PhotoImage(self.folderIcon)
    
    # notebook to customize fluid, solid, interface visualization and viewer
    def configureNotebook(self):
        self.notebook.grid(column=0, row=1, rowspan=self.gridy-2, columnspan=2, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
        self.notebook.columnconfigure(0, weight=0)
        self.notebook.rowconfigure(0, weight=0)
        self.notebook.enable_traversal()
    
    # custom theme (Linux Mint 16 - like)
    def configureGUI(self):
        self.styleGUI = ttk.Style()
        self.sans9 = tkFont.Font(family='Sans', size=9, weight='normal')
        self.styleGUI.configure('My.TLabel', background=self.linuxMintHEX, \
            foreground="white", font=self.sans9)
        self.styleGUI.map('My.TLabel', \
            foreground=[('disabled', 'grey'), ('pressed', 'white'), \
            ('active', 'white')],
            background=[('disabled', 'linuxMintHEX'), ('pressed', 'focus', \
            self.linuxMintHEX), ('active', self.linuxMintHEX)], \
            highlightcolor=[('focus', 'green'), ('!focus', 'red')], \
            # relief={flat, groove, raised, ridge, solid, sunken}
            relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        self.styleGUI.configure('My.TButton', \
            background=self.linuxMintHEX_brighter, foreground="white", \
            font=self.sans9, highlightthickness='20')
        self.styleGUI.map('My.TButton', \
            foreground=[('disabled', 'white'), ('pressed', 'white'), \
            ('active', 'white')], \
            background=[('disabled', 'grey'), ('pressed', 'focus', \
            self.linuxMintHEX_brightest), \
            ('active', self.linuxMintHEX_evenBrighter)], \
            highlightcolor=[('focus', 'green'), ('!focus', 'red')], \
            # relief={flat, groove, raised, ridge, solid, sunken}
            relief=[('pressed', 'flat'), ('!pressed', 'raised')])
        self.styleGUI.configure('My.TRadiobutton', \
            background=self.linuxMintHEX, foreground="white", font=self.sans9, \
            highlightthickness='20')
        self.styleGUI.map('My.TRadiobutton', \
            foreground=[('disabled', 'white'), ('pressed', 'white'), \
            ('active', 'white')], background=[('disabled', 'grey'), \
            ('pressed', 'focus', self.linuxMintHEX_brightest), \
            ('active', self.linuxMintHEX_evenBrighter)], \
            highlightcolor=[('focus', 'green'), ('!focus', 'red')], \
            # relief={flat, groove, raised, ridge, solid, sunken}
            relief=[('pressed', 'flat'), ('!pressed', 'raised')])
        self.styleGUI.configure('My.TCheckbutton', \
            background=self.linuxMintHEX, foreground="white", font=self.sans9, \
            highlightthickness='20')
        self.styleGUI.map('My.TCheckbutton', \
            foreground=[('disabled', 'white'), ('pressed', 'white'), \
            ('active', 'white')], \
            background=[('disabled', 'grey'), \
            ('pressed', 'focus', self.linuxMintHEX_brightest), \
            ('active', self.linuxMintHEX_evenBrighter)], \
            highlightcolor=[('focus', 'green'), ('!focus', 'red')], \
            # relief={flat, groove, raised, ridge, solid, sunken}
            relief=[('pressed', 'flat'), ('!pressed', 'raised')])
        self.styleGUI.configure('My.TFrame', background=self.linuxMintHEX)
        self.styleGUI.configure('My.TSlider', background=self.linuxMintHEX)
        self.styleGUI.map('My.TSlider', \
            foreground=[('disabled', 'grey'), ('pressed', 'white'), \
            ('active', 'white')], \
            background=[('disabled', 'linuxMintHEX'), \
            ('pressed', 'focus', self.linuxMintHEX), \
            ('active', self.linuxMintHEX)], \
            highlightcolor=[('focus', 'green'), ('!focus', 'red')], \
            # relief={flat, groove, raised, ridge, solid, sunken}
            relief=[('pressed', 'sunken'), ('!pressed', 'sunken')])
        self.styleGUI.configure("My.TNotebook", background=self.linuxMintHEX, \
            foreground='white', borderwidth=0)
        self.styleGUI.configure("My.TNotebook.Tab", \
            background=self.linuxMintHEX, foreground='white', \
            expand=self.linuxMintHEX, borderwidth=0)
        self.styleGUI.map("My.TNotebook.Tab", \
            background=[("selected", self.linuxMintHEX_brightest), \
            ('active', self.linuxMintHEX_evenBrighter)], \
            foreground=[("selected", 'yellow'), ('active', 'yellow')], \
            expand=[('selected', self.linuxMintHEX)])
    
