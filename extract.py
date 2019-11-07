from tkinter import Tk, Label, Button, filedialog, OptionMenu, StringVar, Entry, END, Radiobutton, IntVar
from pathlib import Path
from zipfile import ZipFile
from datetime import date, timedelta
import pandas as pd
import os

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
        self.label = Label(master, text="Select zipped ARC format climate data file").pack()
        self.loadfile_button = Button(master, text="Browse", command=self.loadfile).pack()

        # Input model type with drop down
        self.label = Label(master, text="Select climate model required").pack()
        self.model_variable = StringVar(master)
        self.model_variable.trace("w", self.model_changed)
        self.model_variable.set("csiro")
        self.model = OptionMenu(master, self.model_variable, "csiro", "gfdl20", "gfdl21", "miroc", "mpi", "ukmo").pack()

        # Input needed variable with drop down
        self.label = Label(master, text="Select variable of interest").pack()
        self.variable_variable = StringVar(master)
        self.variable_variable.trace("w", self.variable_changed)
        self.variable_variable.set("rain")
        self.variable = OptionMenu(master, self.variable_variable, "rain", "tn", "tx").pack()

        # Input lat
        self.label = Label(master, text="Enter latitude (decimal degree)").pack()
        self.lat_variable = StringVar(master)
        self.lat_variable.trace("w", self.lat_changed)
        self.lat = Entry(master, textvariable = self.lat_variable)
        self.lat.insert(0, "-24")
        self.lat.focus_set()
        self.lat.pack()

        # Input lon
        self.label = Label(master, text="Enter longitude (decimal degree)").pack()
        self.lon_variable = StringVar(master)
        self.lon_variable.trace("w", self.lon_changed)
        self.lon = Entry(master, textvariable = self.lon_variable)
        self.lon.insert(0, "20")
        self.lon.pack()

        # Input start
        self.label = Label(master, text="Enter start date (yyymmdd)").pack()
        self.start_variable = StringVar(master)
        self.start_variable.trace("w", self.start_changed)
        self.start = Entry(master, textvariable = self.start_variable)
        self.start.insert(0, "19610101")
        self.start.pack()

        # Input end
        self.label = Label(master, text="Enter start date (yyymmdd)").pack()
        self.end_variable = StringVar(master)
        self.end_variable.trace("w", self.end_changed)
        self.end = Entry(master, textvariable = self.end_variable)
        self.end.insert(0, "21001231")
        self.end.pack()

        # Input na data value
        self.label = Label(master, text="Enter required no data value").pack()
        self.na_variable = StringVar(master)
        self.na_variable.trace("w", self.na_changed)
        self.na = Entry(master, textvariable = self.na_variable)
        self.na.insert(0, -9999)
        self.na.pack()

        # Input outpt format with drop down
        self.label = Label(master, text="Select output file format")
        self.label.pack()
        self.format_variable = StringVar(master)
        self.format_variable.trace("w", self.format_changed)
        self.format_variable.set("csv")
        self.format = OptionMenu(master, self.format_variable, "csv", "tab").pack()

        # Input whether file header is needed
        self.header_variable = IntVar(master)
        self.header = Radiobutton(master, text="Header in output", variable=self.header_variable, value=1).pack()
        self.header = Radiobutton(master, text="No Header in output", variable=self.header_variable, value=0).pack()

        # Start processing
        self.label = Label(master, text="Extract data:").pack()
        self.start_button = Button(master, text="Start", command=self.extract).pack()

        # Close the program
        self.label = Label(master, text="Quit program").pack()
        self.close_button = Button(master, text="Exit", command=master.quit).pack()

    # Catch dropdown changes
    def variable_changed(self, *args):
        self.var_select = self.variable_variable.get()
        
    # Catch dropdown changes
    def na_changed(self, *args):
        self.na_select = self.na_variable.get()

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
            series = {}
            for i in range(self.delta.days + 1):
                # Build file path in archive to all expected date files per model/variables
                self.date_obj = self.sdate + timedelta(days=i)
                self.date = str(self.date_obj.strftime('%Y%m%d'))
                self.path = "CC_asciigrids/"+self.model_select+"_"+self.var_select+"/"
                self.name = self.model_select+"."+self.date+"_"+self.var_select+".txt"
                self.file = self.path + self.name
                try:
                    with z.open(self.file) as o:
                        data = []
                        for l in o:
                            line = l.decode('utf8').strip().split()
                            # Read metadata ont op of file
                            if len(line) == 2:
                                if "ncols" in line:
                                    ncols = float(line[1])
                                elif "nrows" in line:
                                    nrows = float(line[1])
                                elif "xllcorner" in line:
                                    xllcorner = float(line[1])
                                elif "yllcorner" in line:
                                    yllcorner = float(line[1])
                                elif "cellsize" in line:
                                    cellsize = float(line[1])
                                elif "NODATA_value" in line:
                                    NODATA_value = float(line[1])
                            # Read file itself
                            elif len(line) > 2:
                                data.append(line)
                        # Create pandas dataframe
                        lons = [xllcorner + (count * cellsize) for count in range(int(ncols))]
                        lats = [yllcorner + (count * cellsize) for count in range(int(nrows))]
                        lats.reverse()
                        df = pd.DataFrame(data, index = lats, columns = lons)
                        series[self.date] = df
                except KeyError as e:
                    series[self.date] = False
            # Create output file
            # Load required field seperator
            if self.form_select == "csv":
                self.seperator = ","
                self.extension = ".csv"
            elif self.form_select == "tab":
                self.seperator = "\t"
                self.extension = ".txt"
            self.out = self.filepath.parent / ("_".join([str(self.model_select), str(self.var_select), str(self.start_select), str(self.end_select), str(self.lat_select), str(self.lon_select)]) + self.extension)
            # Iterate over entire series dictionary - and extract date value pairs
            self.lat_round = round(float(self.lat_select) * 2.0 ) / 2.0
            self.lon_round = round(float(self.lon_select) * 2.0 ) / 2.0
            #  Write output file - after deleting files if found
            try:
                os.remove(self.out)
            except OSError:
                pass
            with open(self.out, "a+") as outfile:
                # Add header if needed
                if self.header_variable.get() == 1:
                    outfile.write(self.seperator.join(["date", str(self.var_select)]) + "\n")
                # Write to file if data was found for date - otherwise write no data
                count = 0
                for key, val in series.items():
                    if count == 0:
                        if not isinstance(val, bool):
                            outfile.write(self.seperator.join([key, str(val.loc[self.lat_round][self.lon_round])]))
                        else:
                            outfile.write(self.seperator.join([key, self.na_select]))
                    else: 
                        if not isinstance(val, bool):
                            outfile.write("\n" + self.seperator.join([key, str(val.loc[self.lat_round][self.lon_round])]))
                        else:
                            outfile.write("\n" + self.seperator.join([key, self.na_select]))
                    count =+ 1

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
