from Tkinter import BOTH, W, N, E, S, Canvas
from PIL import ImageTk, Image
from ttk import Frame, Button, Label, Style, Entry


class GUI(Frame):
    def __init__(self, parent, control):
        Frame.__init__(self, parent)
        self.mode = 0
        self.parent = parent
        self.addressViewer = None
        self.photoViewer = None
        self.control = control
        self.initUI()

    def quit(self):
        self.parent.destroy()

    def putPhotoOnCanvas(self, photo, mode):
        self.photoViewer.background = ImageTk.PhotoImage(photo)
        self.photoViewer.create_image(0,0,image=self.photoViewer.background,anchor='nw')
        self.mode = mode

    def resizeImage(self,photo):
        scale = 1
        while photo.size[0]/scale > 800 and photo.size[1]/scale>600:
            scale+=1
        photo = photo.resize((photo.size[0]/scale,photo.size[1]/scale), Image.ANTIALIAS)
        return photo

    def initUI(self):
        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, pad=7)

        buttonBrowse = Button(self, text="Browse", command= self.control.browseFile)
        buttonBrowse.grid(row=0, column=0, sticky=W+E, pady=4, padx=5)

        self.addressViewer = Entry(self)
        self.addressViewer.grid(row=0, column=1, sticky=W+E+N+S, pady=4, padx=5)

        self.photoViewer = Canvas(self,bd=0, highlightthickness=0, relief="raised")
        self.photoViewer.grid(row=1, column=0, columnspan=2, rowspan=7,
            padx=5, sticky=E+W+S+N)

        buttonGrayScale = Button(self, text="Original", command=self.control.showOriginal)
        buttonGrayScale.grid(row=1, column=3, pady= 4)

        buttonGrayScale = Button(self, text="Grayscale", command=self.control.turn2Grayscale)
        buttonGrayScale.grid(row=2, column=3, pady= 4)

        buttonInvers = Button(self, text="Invers", command=self.control.turn2Invers)
        buttonInvers.grid(row=3, column=3, pady=4)

        buttonSplit = Button(self, text="Split", command=self.control.splitImage)
        buttonSplit.grid(row=4, column=3, pady=4)

        buttonReLoad = Button(self, text="Re-Load", command=self.control.reload)
        buttonReLoad.grid(row=5, column=3, pady=4)

        buttonSolve = Button(self, text="Solve", command=self.control.solve)
        buttonSolve.grid(row=6, column=3, pady=4)

        # inputW = Entry(self, text = "300000")
        # inputW.grid(row=4, column=3, pady=4)

        buttonClose = Button(self, text="Close", command= self.quit)
        buttonClose.grid(row=7, column=3, pady=4)

        labelName = Label(self, text="Developer: Muh.Alif Akbar (1103132163)")
        labelName.grid(row=8,pady=5, padx=5)