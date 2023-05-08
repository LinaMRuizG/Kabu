import pandas as pd
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import datetime
import numpy as np

class curves:

    def __init__(self,databasePath,datesName,casesName,kernel,plotName):
        
        #database
        self.df = pd.read_csv(databasePath)
        # in this frst version the database is a DataFrame with 2 columns 
        # But it could be for more columns or curves.
        # the dates could be strings or datetimes

        #column names variable
        self.dN = datesName
        self.cN = casesName
        
        #parameters
        self.kernel = kernel/2 # is the same kernel for both smoothing

        #to fit
        self.plotName = plotName


    def stansardizingDates(self):

        """It converts the dates in a Timestamp object"""

        df = self.df
        df[self.dN] = pd.to_datetime(df[self.dN]) 
        #this should be improved to standardize even when they are already Timestamp.. 

    
    def curveNormalization(self, inputNormalization, outputNormalization):

        """It normalizes (i.e., dividing by tha maximum value) a list"""

        df = self.df
        df[outputNormalization] = df[inputNormalization]/df[inputNormalization].abs().max()
        #print(df)


    def curveSmoothing(self,inputToSmooth,outputSmoothed):

        """It makes a Gaussian filter of any column in the dataframe"""
        
        df = self.df
        df[outputSmoothed] = gaussian_filter(df[inputToSmooth], self.kernel)

    
    def curveSmoothing2(self,inputToSmooth,outputSmoothed):
        
        """It makes a Gaussian filter of any column in the dataframe"""

        smoothed_cases = []
        df = self.df
        
        for date in sorted(df[self.dN]):
            df['gaussian'] = np.exp( - (((df[self.dN] - date).apply(lambda x: x.days)) ** 2) / (2 * (self.kernel ** 2)))
            
            df['gaussian'] /= df['gaussian'].sum()
            
            smoothed_cases.append((df[inputToSmooth] * df['gaussian']).sum())
            
        
        df[outputSmoothed] = smoothed_cases
      
    
    def discreteDerivative(self,inputToDerivate,outputDerivate):
        
        """It makes a discrete derivate of any column in the dataframe"""
        
        df = self.df
        df[outputDerivate] = df[inputToDerivate].rolling(2).agg(lambda x : x.iloc[1]-x.iloc[0])
        #print(df)
        #if we can do this exactly as in mathematica delete NaN, suba los valores desde la 
        # posicion 2 a la 1  and put it in the last position

    
    def plottingTheCurveNormalized(self):

        """It makes a plot of the Normalized Cases"""

        df = self.df

        plt.figure(figsize=(12,6))
        
        plt.plot(df[self.dN],df["NormalizedCases"], color = "gray", label ="Raw Cases")
        plt.plot(df[self.dN],df["SmoothedNCases"], color="red", label ="Smoothed Cases")
        plt.ylabel("Normalized Cases")
        plt.xlabel("Time")
        plt.title("Epidemic curve "+ self.plotName)
        plt.legend()
        #plt.show()

    def plottingTheCurveNoNormalized(self):

        """It makes a plot of the No-Normalized Cases"""

        df = self.df

        plt.figure(figsize=(12,6))
        
        plt.plot(df[self.dN],df[self.cN], color = "gray", label ="Raw Cases")
        plt.plot(df[self.dN],df["SmoothedCases"], color="red", label ="Smoothed Cases")
        plt.ylabel("Cases")
        plt.xlabel("Time")
        plt.title("Epidemic curve "+ self.plotName)
        plt.legend()
        #plt.show()

    def run(self):

        """It run all the class methods in the correct order"""

        self.stansardizingDates()

        self.curveNormalization(self.cN,"NormalizedCases")
        
        self.curveSmoothing2("NormalizedCases","SmoothedNCases")
        self.curveSmoothing2(self.cN,"SmoothedCases")
    
        
        self.discreteDerivative("SmoothedNCases","FirstDerivate")
        self.curveSmoothing2("FirstDerivate","FirstDerivateSmoothed")
        
        
        self.discreteDerivative("FirstDerivateSmoothed","SecondDerivate")
        
    def run2(self):
        
        self.run()
        self.plottingTheCurveNormalized()
        self.plottingTheCurveNoNormalized()
        plt.show()

















