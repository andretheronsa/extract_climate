from tkinter import Tk, Label, Button, filedialog, OptionMenu, StringVar, Entry, END
from pathlib import Path
from zipfile import ZipFile
from datetime import date, timedelta

'''
Program to extract the required climate variables from a specefic model
for a point and time period and save them in a two column output file withdate row and variable
Author: Andre Theron
Email: andretheronsa@gmail.com
'''

class GUI:
    def __init__(self, master):

        # Window title
        self.master = master

        # Input filepath to climate data zip file
        self.label = Label(master, text="Select zipped ARC format climate data file")
        self.label.pack()
        self.loadfile_button = Button(master, text="Browse", command=self.loadfile)
        self.loadfile_button.pack()

        # Input model type with drop down
        self.label = Label(master, text="Select climate model required")
        self.label.pack()
        self.model_variable = StringVar(master)
        self.model_variable.trace("w", self.model_changed)
        self.model_variable.set("csiro")
        self.model = OptionMenu(master, self.model_variable, "csiro", "gfdl20", "gfdl21", "miroc", "mpi", "ukmo")
        self.model.pack()

        # Input needed variable with drop down
        self.label = Label(master, text="Select variable of interest")
        self.label.pack()
        self.variable_variable = StringVar(master)
        self.variable_variable.trace("w", self.variable_changed)
        self.variable_variable.set("rain")
        self.variable = OptionMenu(master, self.variable_variable, "rain", "tn", "tx")
        self.variable.pack()

        # Input lat
        self.label = Label(master, text="Enter latitude (decimal degree)")
        self.label.pack()
        self.lat_variable = StringVar(master)
        self.lat_variable.trace("w", self.lat_changed)
        self.lat = Entry(master, textvariable = self.lat_variable)
        self.lat.pack()
        self.lat.insert(0, "-33")
        self.lat.focus_set()

        # Input lon
        self.label = Label(master, text="Enter longitude")
        self.label.pack()
        self.lon_variable = StringVar(master)
        self.lon_variable.trace("w", self.lon_changed)
        self.lon = Entry(master, textvariable = self.lon_variable)
        self.lon.pack()
        self.lon.insert(0, "20")
        self.lon.focus_set()

        # Input start
        self.label = Label(master, text="Enter start date (yyymmdd)")
        self.label.pack()
        self.start_variable = StringVar(master)
        self.start_variable.trace("w", self.start_changed)
        self.start = Entry(master, textvariable = self.start_variable)
        self.start.pack()
        self.start.insert(0, "19610101")
        self.start.focus_set()

        # Input end
        self.label = Label(master, text="Enter start date (yyymmdd format)")
        self.label.pack()
        self.end_variable = StringVar(master)
        self.end_variable.trace("w", self.end_changed)
        self.end = Entry(master, textvariable = self.end_variable)
        self.end.pack()
        self.end.insert(0, "21001231")
        self.end.focus_set()

        # Input outpt format with drop down
        self.label = Label(master, text="Select output file format")
        self.label.pack()
        self.format_variable = StringVar(master)
        self.format_variable.trace("w", self.format_changed)
        self.format_variable.set("csv")
        self.format = OptionMenu(master, self.format_variable, "vsc", "tab")
        self.format.pack()

        # Start processing
        self.label = Label(master, text="")
        self.label.pack()
        self.label = Label(master, text="Extract data:")
        self.label.pack()
        self.start_button = Button(master, text="Start", command=self.extract)
        self.start_button.pack()

        # Close the program
        self.label = Label(master, text="")
        self.label.pack()
        self.label = Label(master, text="Quit program")
        self.label.pack()
        self.close_button = Button(master, text="Exit", command=master.quit)
        self.close_button.pack()

    # Catch dropdown changes
    def variable_changed(self, *args):
        self.var_select = self.variable_variable.get()

    # Catch dropdown changes
    def format_changed(self, *args):
        self.form_select = self.format_variable.get()

    # Catch dropdown changes
    def model_changed(self, *args):
        self.model_select = self.model_variable.get()

    # Catch text changes
    def lat_changed(self, *args):
        self.lat_select = self.lat_variable.get()

    # Catch text changes
    def lon_changed(self, *args):
        self.lon_select = self.lon_variable.get()

    # Catch text changes
    def start_changed(self, *args):
        self.start_select = self.start_variable.get()

    # Catch text changes
    def end_changed(self, *args):
        self.end_select = self.end_variable.get()

    # File dialogue
    def loadfile(self):
        self.filepath = Path(filedialog.askopenfilename())

    # Main function
    def extract(self):
        # Load date time objects
        self.sdate = date(int(self.start_select[0:4]), int(self.start_select[4:6]), int(self.start_select[6:8]))
        self.edate = date(int(self.end_select[0:4]), int(self.end_select[4:6]), int(self.end_select[6:8]))
        self.delta = self.edate - self.sdate
        # Read archive file
        with ZipFile(self.filepath, 'r') as z:
            # loop over all time periods
            for i in range(self.delta.days + 1):
                # Build file path in archive to all expected date files per model/variables
                self.date = self.sdate + timedelta(days=i)
                self.path = "CC_asciigrids/"+self.model_select+"_"+self.var_select+"/"
                self.name = self.model_select+"."+str(self.date.strftime('%Y%m%d'))+"_"+self.var_select+".txt"
                self.file = self.path + self.name
                try:
                    with z.open(self.file) as o:
                        for line in o:
                            print(line)
                except KeyError as e:
                    print(e)

# Run main GUI program
def main():
    root = Tk()
    root.title("ARC climate model data extract tool")
    root.geometry("600x600+100+100")
    my_gui = GUI(root)
    root.mainloop()

# Run program if main
if __name__ == "__main__":
    main()
