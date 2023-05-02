import pandas as pd
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import datetime

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

        """ This convert the dates in a Timestamp object"""

        df = self.df
        df[self.dN] = pd.to_datetime(df[self.dN]) 
        #this should be improved to standardize even when they are already Timestamp.. 
    
    def curveNormalization(self, columnName, outputName):

        """This normalize (i.e., dividing by tha maximum value) a list"""

        df = self.df
        df[outputName] = df[columnName]/df[columnName].abs().max()
        #print(df)

    def curveSmoothing(self,columnToSmooth,outputName):

        """this method made a Gaussian filter of any column in the dataframe"""
        
        df = self.df
        df[outputName] = gaussian_filter(df[columnToSmooth], self.kernel)
        
    
    def discreteDerivative(self,columnToDerivate,outputName):
        
        """this method made a discrete derivate of any column in the dataframe"""
        
        df = self.df
        df[outputName] = df[columnToDerivate].rolling(2).agg(lambda x : x.iloc[1]-x.iloc[0])
        #print(df)
        #if we can do this exactly as in mathematica delete NaN, suba los valores desde la 
        # posicion 2 a la 1  and put it in the last position
    
    def plottingTheCurveNormalized(self):

        df = self.df

        plt.figure(figsize=(12,12))
        
        plt.plot(df[self.dN],df["NormalizedCases"], color = "gray")
        plt.plot(df[self.dN],df["SmoothedNCases"], color="red")
        plt.ylabel("cases")
        plt.xlabel("time")
        plt.show()

    def plottingTheCurveNoNormalized(self):

        df = self.df

        plt.figure(figsize=(12,12))
        
        plt.plot(df[self.dN],df[self.cN], color = "gray")
        plt.plot(df[self.dN],df["SmoothedCases"], color="red")
        plt.ylabel("cases")
        plt.xlabel("time")
        plt.show()



class detectingWaves(curves):

    #def __init__(self):
    #super(???)



    def idenNegatPositCuts(self,outputName,columnToFindCuts):

        """This identifies the positions with a Positive value"""

        df = self.df

        df[outputName]= (df[columnToFindCuts].rolling(2).agg(lambda x : True if x.iloc[0]<0 and x.iloc[1]>0 else False)).fillna(False)

    
    def idenPreviousDates(self,rollingCoName, columnToFindCuts):#column name from where the rolling comes from

        #idenPreviousDates
        df = self.df
        positions1 = df[df[rollingCoName]==True][[self.dN,columnToFindCuts]].reset_index(drop=True)
        print(positions1[self.dN])
        print(type(positions1[self.dN][0]))
        positions2 = df[df[self.dN].isin(list(positions1[self.dN] - datetime.timedelta(days=1)))][[self.dN,columnToFindCuts]].reset_index(drop=True)
        positions2.rename(columns={self.dN:self.dN+"1",columnToFindCuts:columnToFindCuts+"1"},inplace=True)
        positions = pd.concat([positions1, positions2], axis=1)
        #print(positions)

        #gettingCutDates
        self.cutDays=list(positions.agg(lambda x : x[self.dN] if abs(x[columnToFindCuts])<abs(x[columnToFindCuts+"1"])  else x[self.dN+"1"], axis=1))
        #print(a1)

    def thresholdPos(self):

        thresholdP = 0

        self.cutDays = df[df[self.dN].isin(self.cutDays)].reset_index(drop = True)
        self.cutDays = self.cutDays.agg(lambda x : x[self.dN] if  x["SecondDerivate"] > thresholdP else [],axis=1)
        self.cutDays = pd.to_datetime(self.cutDays.explode())
        self.cutDays = self.cutDays[~np.isnat(self.cutDays)]



    def plottingTheCurveNormalized(self):

        super().plottingTheCurveNormalized()
        for date in self.cutDays:
            plt.axvline(x=date, color='black', ymax= max(cases), linestyle='--', linewidth=.91)

        


    def plottingTheCurveNoNormalized(self):

        super().plottingTheCurveNoNormalized()
        for date in self.cutDays:
            plt.axvline(x=date, color='black', ymax= max(cases), linestyle='--', linewidth=.91)    



class detectingPeaksValleys(curve,detectingWaves):

    def idenCutPoints(self,outputName,columnToFindCuts): 

        """This identifies the positions of the Negative values in the consecutive pair Negative/Positive 
        and Positive values in the consecutive pair Positive/Negative
        """

        df = self.df

        df[outputName]= (df[columnToFindCuts].rolling(2).agg(lambda x : True if (x.iloc[0]<0 and x.iloc[1]>0) or (x.iloc[0]>0 and x.iloc[1]<0) else False)).fillna(False)

    

















