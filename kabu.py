import pandas as pd
from scipy.ndimage.filters import gaussian_filter

class curves:

    def __init__(self,databasePath,datesName,casesName,kernel,thresholdW,thresholdPV):
        
        #database
        self.df = pd.read_csv(databasePath)
        # in this frst version the database is a DataFrame with 2 columns 
        # But it could be for more columns or curves.
        # the dates could be strings or datetimes

        #column names
        self.dN = datesName
        self.cN = casesName
        
        #parameters
        self.kernel = kernel/2 # is the same kernel for both smoothing
        self.thresholdW = thresholdW
        self.thresholdPV = thresholdPV


    def stansardizingDates(self):
        df[self.dN] = pd.to_datetime(df[self.dN]) 
        #this should be improved to standardize even when they are already Timestamp.. 
    
    def curveNormalization(self):
        df = self.df
        df["NormalizedCases"] = df[self.cN]/df[self.cN].abs().max()
        #print(df)

    def curveSmoothing(self):
        df["SmoothedCases"] = gaussian_filter(df[self.cN], self.kernel)
    
    #def discreteDerivative(self):

    def plottingCurves(self):

        plt.figure(figsize=(12,12))
        plt.plot(df[self.dN],df["NormalizedCases"])
        plt.plot(df[self.dN],df["SmoothedCases"])
        plt.ylabel("cases")
        plt.xlabel("time")



