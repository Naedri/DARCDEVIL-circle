from tkinter import *
from Position import *
from Circle import *
from Solver import *
import fileinput
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename


class GUI(object):
    """description of class"""

    def __init__(self, master):
        # creation list for the read-in circles
        self.circles = []

        # the parent of this GUI = root
        self.master = master

        # bottom and top frames to improve the layout a bit
        self.top = Frame(master, bd=1, relief=SUNKEN, padx=1, pady=1)
        self.bottom = Frame(master, bd=1, relief=SUNKEN, padx=1, pady=1)
        self.top.pack(side=TOP, fill=BOTH, expand=True)
        self.bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

        # top in : divide even more frames left and right
        self.leftTOP = Frame(self.top, bd=1, relief=SUNKEN, padx=1, pady=1)
        self.rightTOP = Frame(self.top, bd=1, relief=SUNKEN, padx=1, pady=1)
        self.leftTOP.pack(side=LEFT, fill=BOTH, expand=True)
        self.rightTOP.pack(side=RIGHT, fill=BOTH, expand=True)

        # Label
        w = Label(self.rightTOP, text="Enter the path to to input file in the first field or use the browse input button"+"\n" +
                  "Enter the path to the output file in the second field or use the browse output button" + "\n" + "push the START button to start processing")
        w.pack()

        # buttons
        self.buttontext = StringVar()
        self.buttontext.set("START")
        self.startbutton = Button(
            master, textvariable=self.buttontext, command=self.clicked1, height=2)

        self.buttontext1 = StringVar()
        self.buttontext1.set("Browse input")
        self.browsebutton = Button(
            master, textvariable=self.buttontext1, command=self.clicked2, height=1)

        self.buttontext2 = StringVar()
        self.buttontext2.set("Browse output")
        self.browsebutton1 = Button(
            master, textvariable=self.buttontext2, command=self.clicked3, height=1)

        self.startbutton.pack(in_=self.rightTOP)
        self.browsebutton.pack(in_=self.leftTOP)
        self.browsebutton1.pack(in_=self.leftTOP)

        self.inputframe = Frame(
            master, width=500, height=500, bd=1, relief=SUNKEN, padx=1, pady=1, bg="blue")
        self.inputframe.pack(in_=self.bottom, side=LEFT)

        self.outputframe = Frame(
            master, width=500, height=500, bd=1, relief=SUNKEN, padx=1, pady=1, bg="blue")
        self.outputframe.pack(in_=self.bottom, side=LEFT)

        # entry fields
        self.entrytext = StringVar()
        self.inputEntry = Entry(
            master, textvariable=self.entrytext, width=50).pack(in_=self.leftTOP)

        self.entrytext1 = StringVar()
        self.outputEntry = Entry(
            master, textvariable=self.entrytext1, width=50).pack(in_=self.leftTOP)

    def output(self, path):
        if len(path) > 4:
            file = open(path, 'w')
            if (self.algo == 3):
                file.write("The "+"\i"+"th algorithm is not impemented")
                file.close()
            else:
                for inter in self.intersections[0]:
                    file.write(inter.to_string()+"\n")
                file.write("\n")
                file.write("Execution time in ms: " +
                           str(self.intersections[1]))
                file.close()

    def process(self, path):
        count = 0
        path = path.replace("\"", "")
        self.algo = 1
        for line in fileinput.input(files=(path)):
            if count == 0:
                self.algo = int(line[0])
            else:
                if " " in line:
                    cir = line.split(' ', 2)
                    pos = Position(float(cir[0]), float(cir[1]))
                    cir = Circle(pos, float(cir[2]))
                    self.circles.append(cir)
            count = count + 1
        self.solver = Solver(self.algo, self.circles)
        self.intersections = self.solver.find_intersect()
        self.intersections[1] = self.intersections[1]*1000

    def clicked1(self):
        self.process(self.entrytext.get())
        self.output(self.entrytext1.get())

        self.algoLabel = Label(
            self.master, text="The algorithm used is: " + str(self.algo))
        self.algoLabel.pack(in_=self.rightTOP)

        self.timeLabel = Label(self.master, text="Finding the intersections took: " +
                               str(self.intersections[1]) + " ms in beslag")
        self.timeLabel.pack(in_=self.rightTOP)

        cirkeltext = Text(self.inputframe)
        cirkeltext.insert(END, 'Your circles:')
        cirkeltext.pack()

        fig = plt.gcf()

        count = 1
        for circle in self.circles:
            cirkeltext.insert(END, "\n" + str(count) +
                              " => " + circle.to_string())
            fig.gca().add_artist(circle.getPlot())
            count += 1

        intertext = Text(self.outputframe)
        intertext.insert(END, 'The Intersection Points:')
        intertext.pack()

        count = 1
        for inter in self.intersections[0]:
            intertext.insert(END, "\n" + str(count)+" => " + inter.to_string())
            count += 1
        self.circles.clear()
        self.intersections.clear()
        plt.show()
        self.master.update_idletasks()

    def clicked2(self):
        self.entrytext.set(askopenfilename())

    def clicked3(self):
        self.entrytext1.set(askopenfilename())

    def button_click(self, e):
        pass
